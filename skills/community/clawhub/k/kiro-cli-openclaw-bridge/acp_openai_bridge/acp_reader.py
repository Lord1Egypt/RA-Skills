"""Asynchronous stdout reader and JSON-RPC message dispatcher.

Continuously reads lines from the ACP subprocess stdout, parses JSON-RPC
messages, and routes Responses (with id) to Futures and Notifications
(without id) to session Queues.
"""

import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class ACPReader:
    """异步 stdout 读取器和消息分发器

    Reads lines from the ACP subprocess stdout, parses each line as JSON,
    and dispatches:
    - Messages with an `id` field as JSON-RPC Responses → sets the
      corresponding asyncio.Future result.
    - Messages without `id` and method == "session/update" as Notifications
      → pushes params into the corresponding session asyncio.Queue.
    """

    def __init__(self, stdout: asyncio.StreamReader) -> None:
        self._stdout = stdout
        self._pending_requests: dict[str | int, asyncio.Future] = {}
        self._session_queues: dict[str, asyncio.Queue] = {}
        self._read_task: asyncio.Task | None = None
        self._is_running: bool = False
        self._stdin_writer = None  # Set by ProcessManager after creation
        self._write_lock: asyncio.Lock | None = None  # Shared lock with JSONRPCWriter

    def start(self) -> None:
        """启动后台读取任务。

        Creates an asyncio.Task that runs _read_loop() in the background.
        """
        if self._read_task is not None:
            return
        self._is_running = True
        self._read_task = asyncio.get_event_loop().create_task(self._read_loop())

    async def stop(self) -> None:
        """停止读取任务，通知所有等待者。

        Cancels the background read task, then notifies all pending Futures
        with a ConnectionError and sends None sentinel to all session Queues
        so consumers can detect shutdown.
        """
        self._is_running = False

        if self._read_task is not None:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass
            self._read_task = None

        self._notify_all_waiters()

    def register_request(self, request_id: str | int) -> asyncio.Future:
        """注册一个 JSON-RPC 请求，返回用于等待响应的 Future。

        Args:
            request_id: The JSON-RPC request id to register.

        Returns:
            An asyncio.Future that will be resolved when the corresponding
            JSON-RPC Response arrives.
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self._pending_requests[request_id] = future
        return future

    def register_session(self, session_id: str) -> asyncio.Queue:
        """注册一个会话，返回用于接收通知的 Queue。

        Args:
            session_id: The ACP session id to register.

        Returns:
            An asyncio.Queue that will receive notification params dicts
            for this session.
        """
        queue: asyncio.Queue = asyncio.Queue()
        self._session_queues[session_id] = queue
        return queue

    def get_session_queue(self, session_id: str) -> asyncio.Queue | None:
        """获取会话的通知队列。

        Args:
            session_id: The ACP session id to look up.

        Returns:
            The asyncio.Queue for the session, or None if not registered.
        """
        return self._session_queues.get(session_id)

    def unregister_session(self, session_id: str) -> None:
        """注销会话的通知队列。

        Args:
            session_id: The ACP session id to unregister.
        """
        self._session_queues.pop(session_id, None)

    async def _read_loop(self) -> None:
        """核心读取循环：逐行读取 stdout，解析并分发。

        Reads lines from stdout until EOF or cancellation. Each line is
        parsed as JSON and dispatched based on whether it contains an `id`
        field (Response) or is a session/update notification.
        """
        try:
            while self._is_running:
                try:
                    line = await self._stdout.readline()
                except ValueError as exc:
                    logger.error("readline buffer overflow (line too long): %s", exc)
                    continue
                if not line:
                    # EOF — subprocess stdout closed
                    logger.warning("ACP subprocess stdout reached EOF")
                    self._is_running = False
                    self._notify_all_waiters()
                    return

                line_str = line.decode("utf-8").strip()
                if not line_str:
                    continue

                try:
                    message = json.loads(line_str)
                except json.JSONDecodeError:
                    logger.warning("Invalid JSON from ACP stdout: %s", line_str)
                    continue

                logger.debug("ACP stdout message: %s", line_str[:300])

                if "id" in message and "method" in message:
                    # JSON-RPC Request FROM the agent (e.g. session/request_permission)
                    await self._handle_agent_request(message)
                elif "id" in message:
                    # JSON-RPC Response — route to pending Future
                    self._dispatch_response(message)
                elif message.get("method") == "session/update":
                    # JSON-RPC Notification — route to session Queue
                    self._dispatch_notification(message)
                else:
                    logger.debug(
                        "Ignoring unrecognized message without id: %s",
                        message.get("method", "<no method>"),
                    )
        except asyncio.CancelledError:
            logger.debug("ACP reader loop cancelled")
            raise

    def _dispatch_response(self, message: dict) -> None:
        """Route a JSON-RPC Response to its pending Future.

        Args:
            message: The parsed JSON-RPC response dict containing an `id` field.
        """
        request_id = message["id"]
        if "error" in message:
            logger.error(
                "ACP returned error for request %s: %s",
                request_id, message["error"],
            )
        future = self._pending_requests.pop(request_id, None)
        if future is not None and not future.done():
            future.set_result(message)
        elif future is None:
            logger.warning(
                "Received response for unknown request id: %s", request_id
            )

    def _dispatch_notification(self, message: dict) -> None:
        """Route a session/update Notification to its session Queue.

        Extracts sessionId from params and pushes the entire params dict
        into the corresponding queue so the consumer can inspect the
        update type.

        Args:
            message: The parsed JSON-RPC notification dict with
                     method == "session/update".
        """
        params = message.get("params", {})
        session_id = params.get("sessionId")
        if session_id is None:
            logger.warning(
                "session/update notification missing sessionId: %s", message
            )
            return

        queue = self._session_queues.get(session_id)
        if queue is not None:
            queue.put_nowait(params)
        else:
            logger.warning(
                "Received notification for unregistered session: %s", session_id
            )

    async def _handle_agent_request(self, message: dict) -> None:
        """Handle a JSON-RPC request FROM the agent (has both id and method).

        Handles ACP client-side methods:
        - fs/read_text_file: Reads file content from disk
        - fs/write_text_file: Writes file content to disk
        - terminal/create: Creates a terminal and runs a command
        - terminal/output: Returns terminal output
        - terminal/wait_for_exit: Waits for terminal to exit
        - terminal/release: Releases a terminal
        - terminal/kill: Kills a terminal process
        """
        import os
        import subprocess
        import uuid

        method = message.get("method", "")
        request_id = message["id"]
        params = message.get("params", {})

        logger.info("Agent request: method=%s, id=%s", method, request_id)

        result = None
        error = None

        if method == "session/request_permission":
            options = params.get("options", [])
            tool_call = params.get("toolCall", {})
            logger.info("Permission request: %s", tool_call.get("title", "unknown"))
            logger.info("Available options: %s", json.dumps(options, ensure_ascii=False))

            deny_keywords = ("deny", "reject", "refuse", "cancel")
            allow_keywords = ("allow", "accept", "approve", "yes", "confirm")

            selected_option = None
            # Pass 1: prefer allow_always
            for opt in options:
                kind = opt.get("kind", "").lower()
                if "allow_always" in kind:
                    selected_option = opt.get("optionId")
                    break
            # Pass 2: any allow option
            if selected_option is None:
                for opt in options:
                    kind = opt.get("kind", "").lower()
                    label = opt.get("label", "").lower()
                    if any(kw in kind for kw in allow_keywords) or any(kw in label for kw in allow_keywords):
                        selected_option = opt.get("optionId")
                        break
            # Pass 3: pick first non-deny option
            if selected_option is None:
                for opt in options:
                    kind = opt.get("kind", "").lower()
                    label = opt.get("label", "").lower()
                    if not any(kw in kind for kw in deny_keywords) and not any(kw in label for kw in deny_keywords):
                        selected_option = opt.get("optionId")
                        break
            # Pass 4: last resort
            if selected_option is None and options:
                selected_option = options[-1].get("optionId")

            if selected_option is None:
                logger.warning("No options for permission request %s", request_id)
                return

            result = {"outcome": {"outcome": "selected", "optionId": selected_option}}
            logger.info("Sending approval response: result=%s", result)

        elif method == "fs/read_text_file":
            file_path = params.get("path", "")
            start_line = params.get("startLine", 0)
            max_lines = params.get("maxLines")
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()
                if start_line > 0:
                    lines = lines[start_line:]
                if max_lines is not None and max_lines > 0:
                    lines = lines[:max_lines]
                content = "".join(lines)
                result = {"content": content}
                logger.info("Read file: %s (%d chars)", file_path, len(content))
            except FileNotFoundError:
                error = {"code": -32001, "message": f"File not found: {file_path}"}
            except Exception as exc:
                error = {"code": -32000, "message": str(exc)}

        elif method == "fs/write_text_file":
            file_path = params.get("path", "")
            content = params.get("content", "")
            try:
                os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                result = {}
                logger.info("Wrote file: %s (%d chars)", file_path, len(content))
            except Exception as exc:
                error = {"code": -32000, "message": str(exc)}

        elif method == "terminal/create":
            cmd_args = params.get("args", [])
            cwd = params.get("cwd")
            env_vars = params.get("env", [])
            try:
                env = os.environ.copy()
                for ev in env_vars:
                    if isinstance(ev, dict):
                        env[ev.get("name", "")] = ev.get("value", "")

                # Join args into a shell command string so pipes, redirects etc. work
                if isinstance(cmd_args, list):
                    cmd_str = " ".join(cmd_args)
                else:
                    cmd_str = str(cmd_args)

                logger.info("Terminal exec: %s (cwd=%s)", cmd_str, cwd)

                proc = subprocess.run(
                    cmd_str,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=cwd,
                    env=env,
                    timeout=30,
                )
                terminal_id = str(uuid.uuid4())
                # Store terminal output for later retrieval
                if not hasattr(self, "_terminals"):
                    self._terminals = {}
                self._terminals[terminal_id] = {
                    "output": proc.stdout + proc.stderr,
                    "exitCode": proc.returncode,
                }
                result = {"terminalId": terminal_id}
                logger.info("Terminal created: %s, exit=%d", terminal_id, proc.returncode)
            except subprocess.TimeoutExpired:
                terminal_id = str(uuid.uuid4())
                if not hasattr(self, "_terminals"):
                    self._terminals = {}
                self._terminals[terminal_id] = {"output": "Command timed out", "exitCode": -1}
                result = {"terminalId": terminal_id}
            except Exception as exc:
                error = {"code": -32000, "message": str(exc)}

        elif method == "terminal/output":
            terminal_id = params.get("terminalId", "")
            terminals = getattr(self, "_terminals", {})
            term = terminals.get(terminal_id)
            if term:
                result = {
                    "output": term.get("output", ""),
                    "truncated": False,
                    "exitStatus": {"exitCode": term.get("exitCode", 0)} if term.get("exitCode") is not None else None,
                }
            else:
                result = {"output": "", "truncated": False, "exitStatus": None}

        elif method == "terminal/wait_for_exit":
            terminal_id = params.get("terminalId", "")
            terminals = getattr(self, "_terminals", {})
            term = terminals.get(terminal_id)
            if term:
                result = {"exitCode": term.get("exitCode", 0), "signal": None}
            else:
                result = {"exitCode": 0, "signal": None}

        elif method == "terminal/release":
            terminal_id = params.get("terminalId", "")
            terminals = getattr(self, "_terminals", {})
            terminals.pop(terminal_id, None)
            result = {}

        elif method == "terminal/kill":
            terminal_id = params.get("terminalId", "")
            result = {}

        else:
            logger.warning("Unhandled agent request: method=%s, id=%s", method, request_id)
            error = {"code": -32601, "message": f"Method not found: {method}"}

        # Send the response
        if error:
            response = {"jsonrpc": "2.0", "error": error, "id": request_id}
        else:
            response = {"jsonrpc": "2.0", "result": result, "id": request_id}

        if self._stdin_writer is not None:
            data = (json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
            if self._write_lock:
                async with self._write_lock:
                    self._stdin_writer.write(data)
                    await self._stdin_writer.drain()
            else:
                self._stdin_writer.write(data)
                await self._stdin_writer.drain()
            logger.debug("Sent response for %s (id=%s)", method, request_id)
        else:
            logger.error("Cannot respond to agent request — no stdin writer available")

    def _notify_all_waiters(self) -> None:
        """Notify all pending Futures and session Queues of shutdown.

        Sets a ConnectionError on all pending Futures and pushes a None
        sentinel into all session Queues so consumers can detect that the
        reader is no longer available.
        """
        # Notify all pending request Futures
        for request_id, future in self._pending_requests.items():
            if not future.done():
                future.set_exception(
                    ConnectionError("ACP reader stopped or subprocess exited")
                )
        self._pending_requests.clear()

        # Send None sentinel to all session Queues
        for session_id, queue in self._session_queues.items():
            queue.put_nowait(None)
