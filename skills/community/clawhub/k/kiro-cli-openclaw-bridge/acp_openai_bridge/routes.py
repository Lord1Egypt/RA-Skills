"""FastAPI route definitions for the ACP-to-OpenAI Bridge.

Implements the OpenAI-compatible HTTP API endpoints:
- POST /v1/chat/completions (streaming and non-streaming)
- GET /v1/models
- GET /health

All endpoints access ProcessManager and SessionManager via request.app.state.
No API key validation is performed on any endpoint.
"""

import asyncio
import logging
import time

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from acp_openai_bridge.request_translator import RequestTranslator
from acp_openai_bridge.response_translator import ResponseTranslator
from acp_openai_bridge.sse_emitter import SSEEmitter
from acp_openai_bridge.sse_emitter import _extract_chunk_text

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/v1/chat/completions", response_model=None)
async def chat_completions(request: Request):
    """Handle OpenAI chat completion requests.

    Translates the OpenAI request to ACP session/prompt, sends it to the
    ACP subprocess, and returns either an SSE stream or a complete JSON
    response depending on the ``stream`` parameter.
    """
    process_manager = request.app.state.process_manager
    session_manager = request.app.state.session_manager
    config = request.app.state.config

    # 1. Parse request body JSON
    try:
        body = await request.json()
    except Exception:
        error = ResponseTranslator.to_error_response(
            message="Invalid JSON in request body",
            error_type="invalid_request_error",
        )
        return JSONResponse(content=error, status_code=400)

    # 2. Ensure ACP subprocess is available
    try:
        await process_manager.ensure_available()
    except Exception as exc:
        logger.error("ACP subprocess unavailable: %s", exc)
        error = ResponseTranslator.to_error_response(
            message="Backend ACP service unavailable",
            error_type="server_error",
            code="backend_unavailable",
        )
        return JSONResponse(content=error, status_code=502)

    # 3. Detect new conversation: reset session only when messages contain
    #    a single user message (no history yet). This way, continuing a
    #    conversation keeps the ACP session so kiro remembers context.
    messages = body.get("messages") or []
    user_messages = [m for m in messages if m.get("role") == "user"]
    is_new_conversation = len(user_messages) <= 1
    if is_new_conversation:
        try:
            await session_manager.reset_session()
            logger.info("New conversation detected, created fresh session: %s", session_manager.session_id)
        except Exception as exc:
            logger.error("Failed to reset session: %s", exc)
            error = ResponseTranslator.to_error_response(
                message="Failed to create new session",
                error_type="server_error",
                code="session_error",
            )
            return JSONResponse(content=error, status_code=502)

    # 4. Translate the request
    try:
        translated = RequestTranslator.translate(body, session_manager.session_id)
    except ValueError as exc:
        error = ResponseTranslator.to_error_response(
            message=str(exc),
            error_type="invalid_request_error",
        )
        return JSONResponse(content=error, status_code=400)

    # 4. Send session/prompt via JSON-RPC
    logger.info(
        "Sending session/prompt: session=%s, stream=%s, content_length=%d, full_content=%s",
        translated.session_id, translated.is_stream,
        sum(len(c.get("text", "")) for c in translated.content),
        str(translated.content)[:2000],
    )
    try:
        rpc_id = await process_manager.writer.send_request(
            "session/prompt",
            {
                "sessionId": translated.session_id,
                "prompt": translated.content,
            },
        )
        logger.info("session/prompt sent, rpc_id=%s", rpc_id)
    except Exception as exc:
        logger.error("Failed to send session/prompt: %s", exc)
        error = ResponseTranslator.to_error_response(
            message="Failed to communicate with ACP backend",
            error_type="server_error",
            code="backend_unavailable",
        )
        return JSONResponse(content=error, status_code=502)

    # 5. Register request future and get session queue
    response_future = process_manager.reader.register_request(rpc_id)
    session_queue = process_manager.reader.get_session_queue(translated.session_id)

    if session_queue is None:
        error = ResponseTranslator.to_error_response(
            message="Session not found",
            error_type="server_error",
            code="session_not_found",
        )
        return JSONResponse(content=error, status_code=500)

    # 6/7. Streaming vs non-streaming
    if translated.is_stream:
        return await _handle_streaming(
            request=request,
            session_queue=session_queue,
            request_id=translated.request_id,
            response_future=response_future,
            process_manager=process_manager,
            session_manager=session_manager,
            session_id=translated.session_id,
            config=config,
        )
    else:
        return await _handle_non_streaming(
            request=request,
            session_queue=session_queue,
            request_id=translated.request_id,
            response_future=response_future,
            process_manager=process_manager,
            session_manager=session_manager,
            session_id=translated.session_id,
            config=config,
        )


async def _handle_streaming(
    request: Request,
    session_queue: asyncio.Queue,
    request_id: str,
    response_future: asyncio.Future,
    process_manager,
    session_manager,
    session_id: str,
    config,
) -> StreamingResponse:
    """Handle a streaming chat completion request.

    Creates an SSEEmitter and wraps it in a StreamingResponse. Detects
    client disconnect and sends session/cancel when appropriate.
    """
    emitter = SSEEmitter(
        queue=session_queue,
        request_id=request_id,
        response_future=response_future,
    )

    async def event_generator():
        try:
            async for chunk in emitter.stream():
                # Check for client disconnect
                if await request.is_disconnected():
                    logger.info("Client disconnected during streaming, cancelling")
                    await _send_cancel(process_manager, session_id)
                    return
                yield chunk
            # After stream ends, check for context overflow
            if response_future.done():
                try:
                    result = response_future.result()
                    if isinstance(result, dict) and session_manager.is_context_overflow_error(result):
                        logger.info("Context overflow detected in streaming, resetting session")
                        await session_manager.reset_session()
                except Exception:
                    pass
        except asyncio.CancelledError:
            logger.info("Streaming cancelled, sending session/cancel")
            await _send_cancel(process_manager, session_id)
            raise
        except Exception:
            logger.exception("Error during streaming")
            await _send_cancel(process_manager, session_id)
            raise

    return StreamingResponse(
        content=event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


async def _handle_non_streaming(
    request: Request,
    session_queue: asyncio.Queue,
    request_id: str,
    response_future: asyncio.Future,
    process_manager,
    session_manager,
    session_id: str,
    config,
) -> JSONResponse:
    """Handle a non-streaming chat completion request.

    Collects all agent_message_chunk notifications while waiting for the
    response future to complete, then builds a full chat completion response.
    """
    collected_texts: list[str] = []
    timeout = config.request_timeout

    async def _collect_and_wait():
        """Collect notification texts until response_future completes."""
        # Start a task to collect queue items
        collect_task = asyncio.ensure_future(_collect_chunks(session_queue, collected_texts, response_future))

        try:
            # Wait for the response future
            await response_future
        finally:
            # Ensure collection task is done
            collect_task.cancel()
            try:
                await collect_task
            except asyncio.CancelledError:
                pass

    try:
        await asyncio.wait_for(_collect_and_wait(), timeout=timeout)
    except asyncio.TimeoutError:
        logger.warning("Request %s timed out after %s seconds", request_id, timeout)
        await _send_cancel(process_manager, session_id)
        error = ResponseTranslator.to_error_response(
            message=f"Request timed out after {timeout} seconds",
            error_type="server_error",
            code="timeout",
        )
        return JSONResponse(content=error, status_code=504)
    except ConnectionError as exc:
        logger.error("ACP connection error: %s", exc)
        error = ResponseTranslator.to_error_response(
            message="Backend ACP service unavailable",
            error_type="server_error",
            code="backend_unavailable",
        )
        return JSONResponse(content=error, status_code=502)

    # Check for JSON-RPC error in the response
    response = response_future.result()
    logger.info("session/prompt response: %s", str(response)[:500])
    if "error" in response:
        rpc_error = response["error"]
        error_msg = rpc_error.get("message", "Unknown ACP error")
        logger.error("ACP returned JSON-RPC error: %s", rpc_error)

        # Context overflow: reset session and notify user
        if session_manager.is_context_overflow_error(response):
            logger.info("Context overflow detected, resetting session")
            await session_manager.reset_session()
            error = ResponseTranslator.to_error_response(
                message="对话上下文已达到限制，已自动创建新会话。请重新发送您的问题。",
                error_type="server_error",
                code="context_overflow",
            )
            return JSONResponse(content=error, status_code=400)

        error = ResponseTranslator.to_error_response(
            message=error_msg,
            error_type="server_error",
        )
        return JSONResponse(content=error, status_code=500)

    # Extract stop reason and build response
    result = response.get("result", {})
    stop_reason = result.get("stopReason", "end_turn")
    content = "".join(collected_texts)
    logger.info(
        "Non-streaming response: stop_reason=%s, collected_chunks=%d, content_len=%d, content_preview=%.200s",
        stop_reason, len(collected_texts), len(content), content,
    )

    chat_response = ResponseTranslator.to_chat_completion(
        request_id=request_id,
        content=content,
        stop_reason=stop_reason,
    )
    return JSONResponse(content=chat_response)


async def _collect_chunks(
    queue: asyncio.Queue,
    collected_texts: list[str],
    response_future: asyncio.Future,
) -> None:
    """Collect agent_message_chunk texts from the session queue.

    Runs until the response_future completes or a None sentinel is received.
    """
    while not response_future.done():
        try:
            item = await asyncio.wait_for(queue.get(), timeout=0.5)
        except asyncio.TimeoutError:
            continue

        if item is None:
            break

        text = _extract_chunk_text(item)
        if text:
            collected_texts.append(text)

    # Drain any remaining items
    while not queue.empty():
        item = queue.get_nowait()
        if item is None:
            break
        text = _extract_chunk_text(item)
        if text:
            collected_texts.append(text)


async def _send_cancel(process_manager, session_id: str) -> None:
    """Send a session/cancel request to the ACP subprocess."""
    try:
        await process_manager.writer.send_request(
            "session/cancel",
            {"sessionId": session_id},
        )
    except Exception:
        logger.warning("Failed to send session/cancel", exc_info=True)


@router.get("/v1/models")
async def list_models() -> JSONResponse:
    """Return the fixed model list containing kiro-acp."""
    return JSONResponse(
        content={
            "object": "list",
            "data": [
                {
                    "id": "kiro-acp",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "kiro",
                }
            ],
        }
    )


@router.get("/health")
async def health_check(request: Request) -> JSONResponse:
    """Return ACP subprocess health status."""
    process_manager = request.app.state.process_manager
    is_available = process_manager.is_available

    if is_available:
        return JSONResponse(
            content={"status": "ok", "acp_available": True}
        )
    else:
        return JSONResponse(
            content={"status": "degraded", "acp_available": False}
        )


# ---------------------------------------------------------------------------
# Anthropic Messages API compatibility (/v1/messages)
# ---------------------------------------------------------------------------

@router.post("/v1/messages", response_model=None)
async def anthropic_messages(request: Request):
    """Handle Anthropic Messages API requests.

    Translates the Anthropic format into the internal OpenAI-like format
    and delegates to the same ACP backend.

    Anthropic request format:
        {"model": "...", "messages": [{"role": "user", "content": "..."}],
         "max_tokens": 4096, "stream": true}

    Anthropic response format (non-streaming):
        {"id": "msg_...", "type": "message", "role": "assistant",
         "content": [{"type": "text", "text": "..."}],
         "model": "...", "stop_reason": "end_turn",
         "usage": {"input_tokens": N, "output_tokens": N}}

    Anthropic streaming format (SSE):
        event: message_start
        data: {"type": "message_start", "message": {...}}

        event: content_block_start
        data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

        event: content_block_delta
        data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "..."}}

        event: content_block_stop
        data: {"type": "content_block_stop", "index": 0}

        event: message_delta
        data: {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": N}}

        event: message_stop
        data: {"type": "message_stop"}
    """
    import json as _json
    import uuid

    process_manager = request.app.state.process_manager
    session_manager = request.app.state.session_manager
    config = request.app.state.config

    # 1. Parse request body
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            content={"type": "error", "error": {"type": "invalid_request_error", "message": "Invalid JSON"}},
            status_code=400,
        )

    # 2. Ensure ACP subprocess is available
    try:
        await process_manager.ensure_available()
    except Exception as exc:
        logger.error("ACP subprocess unavailable: %s", exc)
        return JSONResponse(
            content={"type": "error", "error": {"type": "api_error", "message": "Backend unavailable"}},
            status_code=502,
        )

    # 3. Extract user message from Anthropic format
    messages = body.get("messages", [])
    if not messages:
        return JSONResponse(
            content={"type": "error", "error": {"type": "invalid_request_error", "message": "messages is required"}},
            status_code=400,
        )

    # Find last user message
    user_content = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, str):
                user_content = content
            elif isinstance(content, list):
                # Anthropic format: [{"type": "text", "text": "..."}]
                user_content = " ".join(
                    block.get("text", "") for block in content if block.get("type") == "text"
                )
            break

    if not user_content and not any(m.get("role") == "user" for m in messages):
        return JSONResponse(
            content={"type": "error", "error": {"type": "invalid_request_error", "message": "No user message found"}},
            status_code=400,
        )

    is_stream = body.get("stream", False)
    msg_id = f"msg_{uuid.uuid4().hex[:24]}"

    # 4. Detect new conversation: only reset session when there's a single user message
    user_messages = [m for m in messages if m.get("role") == "user"]
    is_new_conversation = len(user_messages) <= 1
    if is_new_conversation:
        try:
            await session_manager.reset_session()
            logger.info("New conversation detected, created fresh session: %s", session_manager.session_id)
        except Exception as exc:
            logger.error("Failed to reset session: %s", exc)
            return JSONResponse(
                content={"type": "error", "error": {"type": "api_error", "message": "Failed to create new session"}},
                status_code=502,
            )

    # 5. Send to ACP
    try:
        rpc_id = await process_manager.writer.send_request(
            "session/prompt",
            {
                "sessionId": session_manager.session_id,
                "prompt": [{"type": "text", "text": user_content}],
            },
        )
    except Exception as exc:
        logger.error("Failed to send session/prompt: %s", exc)
        return JSONResponse(
            content={"type": "error", "error": {"type": "api_error", "message": "Backend communication failed"}},
            status_code=502,
        )

    response_future = process_manager.reader.register_request(rpc_id)
    session_queue = process_manager.reader.get_session_queue(session_manager.session_id)

    if session_queue is None:
        return JSONResponse(
            content={"type": "error", "error": {"type": "api_error", "message": "Session not found"}},
            status_code=500,
        )

    model_name = body.get("model", "kiro-acp")

    if is_stream:
        # Anthropic streaming format
        async def anthropic_stream():
            input_tokens = ResponseTranslator.estimate_tokens(user_content)
            output_tokens = 0

            # message_start
            yield f"event: message_start\ndata: {_json.dumps({'type': 'message_start', 'message': {'id': msg_id, 'type': 'message', 'role': 'assistant', 'content': [], 'model': model_name, 'stop_reason': None, 'usage': {'input_tokens': input_tokens, 'output_tokens': 0}}})}\n\n"

            # content_block_start
            yield f"event: content_block_start\ndata: {_json.dumps({'type': 'content_block_start', 'index': 0, 'content_block': {'type': 'text', 'text': ''}})}\n\n"

            # Stream content deltas
            while True:
                queue_task = asyncio.ensure_future(session_queue.get())
                pending = {queue_task}
                if not response_future.done():
                    pending.add(response_future)

                done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

                if queue_task in done:
                    item = queue_task.result()
                    if item is None:
                        break
                    text = _extract_chunk_text(item)
                    if text:
                        output_tokens += ResponseTranslator.estimate_tokens(text)
                        yield f"event: content_block_delta\ndata: {_json.dumps({'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': text}})}\n\n"
                else:
                    queue_task.cancel()

                if response_future.done():
                    # Drain remaining
                    while not session_queue.empty():
                        item = session_queue.get_nowait()
                        if item is None:
                            break
                        text = _extract_chunk_text(item)
                        if text:
                            output_tokens += ResponseTranslator.estimate_tokens(text)
                            yield f"event: content_block_delta\ndata: {_json.dumps({'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': text}})}\n\n"
                    break

            # Get stop reason
            stop_reason = "end_turn"
            if response_future.done():
                try:
                    result = response_future.result()
                    stop_reason = result.get("result", {}).get("stopReason", "end_turn")
                except Exception:
                    pass

            # content_block_stop
            yield f"event: content_block_stop\ndata: {_json.dumps({'type': 'content_block_stop', 'index': 0})}\n\n"

            # message_delta
            yield f"event: message_delta\ndata: {_json.dumps({'type': 'message_delta', 'delta': {'stop_reason': stop_reason}, 'usage': {'output_tokens': output_tokens}})}\n\n"

            # message_stop
            yield f"event: message_stop\ndata: {_json.dumps({'type': 'message_stop'})}\n\n"

        return StreamingResponse(
            content=anthropic_stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
        )
    else:
        # Non-streaming Anthropic response
        collected_texts: list[str] = []
        timeout = config.request_timeout

        async def _collect_and_wait():
            collect_task = asyncio.ensure_future(_collect_chunks(session_queue, collected_texts, response_future))
            try:
                await response_future
            finally:
                collect_task.cancel()
                try:
                    await collect_task
                except asyncio.CancelledError:
                    pass

        try:
            await asyncio.wait_for(_collect_and_wait(), timeout=timeout)
        except asyncio.TimeoutError:
            await _send_cancel(process_manager, session_manager.session_id)
            return JSONResponse(
                content={"type": "error", "error": {"type": "api_error", "message": "Request timed out"}},
                status_code=504,
            )
        except ConnectionError:
            return JSONResponse(
                content={"type": "error", "error": {"type": "api_error", "message": "Backend unavailable"}},
                status_code=502,
            )

        response = response_future.result()
        if "error" in response:
            return JSONResponse(
                content={"type": "error", "error": {"type": "api_error", "message": response["error"].get("message", "Unknown error")}},
                status_code=500,
            )

        result = response.get("result", {})
        stop_reason = result.get("stopReason", "end_turn")
        content = "".join(collected_texts)

        return JSONResponse(content={
            "id": msg_id,
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": content}],
            "model": model_name,
            "stop_reason": stop_reason,
            "usage": {
                "input_tokens": ResponseTranslator.estimate_tokens(user_content),
                "output_tokens": ResponseTranslator.estimate_tokens(content),
            },
        })
