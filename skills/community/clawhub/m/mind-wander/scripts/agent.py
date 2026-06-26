"""
mind-wander agent loop.

Drives the Qwen3.5 model through a tool-calling loop with the mind-wander
system prompt. Handles XML-style tool calls (Qwen3.5 format), enforces
the tool call limit, and logs the session.
"""
import json
import re
import sys
import time
import logging
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent / "memory-upgrade"))
sys.path.insert(0, str(Path(__file__).parent))

from mind_wander_config import (
    WANDER_MODEL, WANDER_OLLAMA, WANDER_CTX, WANDER_TIMEOUT,
    MAX_TOOL_CALLS, WANDER_LOG_FILE,
)
from tools import TOOL_REGISTRY, mark_run
from prompt import assemble_context
from collector import save_session
from wander_graph import record_session, init_wander_graph
try:
    init_wander_graph()
except Exception:
    pass

import httpx

# ── Logging ───────────────────────────────────────────────────────────────────

WANDER_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(WANDER_LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("mind-wander")


# ── Tool schema list ──────────────────────────────────────────────────────────

TOOL_SCHEMAS = [v["schema"] for v in TOOL_REGISTRY.values()]


# ── LLM call ─────────────────────────────────────────────────────────────────

def llm_call(messages: list, system: str, model: str = None) -> dict:
    """Call Qwen3.5 via Ollama OpenAI-compatible endpoint."""
    payload = {
        "model": model or WANDER_MODEL,
        "messages": [{"role": "system", "content": system}] + messages,
        "tools": TOOL_SCHEMAS,
        "stream": False,
        "options": {
            "num_ctx": WANDER_CTX,
            "temperature": 0.7,
            "top_p": 0.9,
        },
    }
    try:
        with httpx.Client(timeout=WANDER_TIMEOUT) as client:
            resp = client.post(
                f"{WANDER_OLLAMA}/v1/chat/completions",
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        log.error(f"LLM call failed: {e}")
        raise


def parse_tool_calls(message: dict) -> list:
    """
    Extract tool calls from model response.
    Handles both OpenAI-style tool_calls array and Qwen3.5 XML-style
    <tool_call>{"name": ..., "arguments": ...}</tool_call>.
    """
    calls = []

    # OpenAI format
    if message.get("tool_calls"):
        for tc in message["tool_calls"]:
            fn = tc.get("function", {})
            name = fn.get("name", "")
            args_raw = fn.get("arguments", "{}")
            try:
                args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
            except Exception:
                args = {}
            calls.append({"name": name, "arguments": args, "id": tc.get("id", "")})
        return calls

    # Qwen3.5 XML format: <tool_call>{"name": ..., "arguments": ...}</tool_call>
    content = message.get("content", "") or ""
    xml_calls = re.findall(r"<tool_call>(.*?)</tool_call>", content, re.DOTALL)
    for raw in xml_calls:
        raw = raw.strip()
        # Fix unquoted name values: {"name": sandbox_run → {"name": "sandbox_run"
        raw_fixed = re.sub(
            r'"name":\s*([a-zA-Z_][a-zA-Z0-9_]*)',
            lambda m: f'"name": "{m.group(1)}"',
            raw
        )
        try:
            parsed = json.loads(raw_fixed)
            calls.append({
                "name": parsed.get("name", ""),
                "arguments": parsed.get("arguments", {}),
                "id": f"xml_{len(calls)}",
            })
        except Exception:
            # Last resort: regex extract name and treat rest as code argument
            name_match = re.search(r'"name":\\s*([a-zA-Z_][a-zA-Z0-9_]*)', raw)
            if name_match:
                tool_name = name_match.group(1)
                # Try to extract arguments object
                args_match = re.search(r'"arguments":\s*(\{.*)', raw, re.DOTALL)
                if args_match:
                    try:
                        args = json.loads(args_match.group(1).rstrip('}') + '}' * (args_match.group(1).count('{') - args_match.group(1).count('}')))
                    except Exception:
                        args = {}
                else:
                    args = {}
                calls.append({"name": tool_name, "arguments": args, "id": f"xml_{len(calls)}"})

    return calls


def dispatch_tool(name: str, arguments: dict) -> str:
    """Call a tool and return its result as a string."""
    if name not in TOOL_REGISTRY:
        return f"Unknown tool: {name}"
    try:
        fn = TOOL_REGISTRY[name]["fn"]
        result = fn(**arguments)
        if result.get("ok"):
            return result["result"]
        else:
            return f"Tool error: {result.get('error', 'unknown error')}"
    except Exception as e:
        return f"Tool dispatch error: {e}"


# ── Main agent loop ───────────────────────────────────────────────────────────

def run(anchor_item: str = None, dry_run: bool = False, verbose: bool = False, model_override: str = None) -> dict:
    """
    Run one mind-wander session.
    Returns {"elevated": bool, "title": str|None, "tool_calls": int, "duration": float}
    """
    t_start = time.time()
    session_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    active_model = model_override or WANDER_MODEL
    log.info(f"=== Mind-wander session {session_id} started | anchor={anchor_item} | model={active_model} ===")
    # Expose session context to tools (for dead end recording provenance)
    import tools as _tools_module
    _tools_module._CURRENT_SESSION_UUID   = session_id
    _tools_module._CURRENT_SESSION_ANCHOR = anchor_item or "auto"

    if verbose:
        print(f"\n\U0001f9e0 Mind-wander session {session_id}")
        print(f"   Model: {active_model} @ {WANDER_OLLAMA}")
        print(f"   Anchor: {anchor_item or 'auto-select'}\n")

    system, user_message = assemble_context(anchor_item)
    messages = [{"role": "user", "content": user_message}]
    _all_messages = list(messages)

    tool_call_count = 0
    elevated = False
    elevated_title = None

    if dry_run:
        print("[dry-run] Would send to model:")
        print(f"  System: {system[:200]}...")
        print(f"  User: {user_message[:300]}...")
        return {"elevated": False, "title": None, "tool_calls": 0, "duration": 0}

    try:
        while tool_call_count < MAX_TOOL_CALLS:
            # LLM turn
            response = llm_call(messages, system, model=active_model)
            msg = response["choices"][0]["message"]
            content = msg.get("content") or ""
            finish_reason = response["choices"][0].get("finish_reason", "")

            if verbose and content:
                # Strip think tags for cleaner display
                display = re.sub(r"<think>.*?</think>", "[thinking...]", content, flags=re.DOTALL)
                print(f"  Agent: {display[:500]}{'...' if len(display)>500 else ''}")

            log.info(f"Agent turn: finish={finish_reason}, content_len={len(content)}")

            # Parse tool calls
            tool_calls = parse_tool_calls(msg)

            if not tool_calls:
                # No tool calls — agent is done
                messages.append({"role": "assistant", "content": content})
                _all_messages.append({"role": "assistant", "content": content})
                log.info("Agent finished without tool calls")
                if verbose:
                    print(f"\n  → Session complete (no more tool calls)")
                break

            # Execute tool calls
            messages.append({"role": "assistant", "content": content,
                             "tool_calls": [{"id": tc["id"], "type": "function",
                                            "function": {"name": tc["name"],
                                                        "arguments": json.dumps(tc["arguments"])}}
                                           for tc in tool_calls]})
            # Capture for collector: preserve think content + tool calls
            _all_messages.append({
                "role": "assistant",
                "content": content or "",  # includes <think> blocks
                "tool_calls": [{"name": tc["name"], "arguments": tc["arguments"]}
                               for tc in tool_calls],
            })

            for tc in tool_calls:
                name = tc["name"]
                args = tc["arguments"]
                tool_call_count += 1

                if verbose:
                    print(f"  🔧 {name}({', '.join(f'{k}={repr(v)[:40]}' for k,v in args.items())})")

                log.info(f"Tool call [{tool_call_count}/{MAX_TOOL_CALLS}]: {name}({list(args.keys())})")

                result_str = dispatch_tool(name, args)

                if verbose:
                    print(f"     → {result_str[:200]}{'...' if len(result_str)>200 else ''}")

                # Track elevations
                if name == "elevate" and "elevated to" in result_str:
                    elevated = True
                    elevated_title = args.get("title", "unknown")
                    if anchor_item:
                        mark_run(anchor_item)
                    log.info(f"ELEVATED: {elevated_title}")
                    if verbose:
                        print(f"\n  ✨ ELEVATED: {elevated_title}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result_str,
                })
                _all_messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result_str,
                })

                if tool_call_count >= MAX_TOOL_CALLS:
                    log.warning("Tool call limit reached")
                    if verbose:
                        print(f"\n  ⚠️  Tool call limit reached ({MAX_TOOL_CALLS})")
                    break

            if finish_reason == "stop" and not tool_calls:
                break

    except Exception as e:
        log.error(f"Session error: {e}", exc_info=True)
        if verbose:
            print(f"\n  ❌ Session error: {e}")

    duration = time.time() - t_start
    log.info(f"Session complete: elevated={elevated}, tool_calls={tool_call_count}, duration={duration:.1f}s")

    result = {
        "elevated": elevated,
        "title": elevated_title,
        "tool_calls": tool_call_count,
        "duration": duration,
        "session_id": session_id,
    }

    # Save to wander completions + wander graph
    if not dry_run:
        try:
            save_session(
                session_id=session_id,
                model=active_model,
                anchor=anchor_item,
                system_prompt=system,
                messages=_all_messages,
                result=result,
                on_your_mind_snapshot=user_message[:500],
            )
        except Exception as e:
            log.warning(f"Collector save failed: {e}")

        try:
            record_session(
                session_uuid=session_id,
                anchor=anchor_item or "auto",
                model=active_model,
                outcome="elevated" if elevated else "discarded",
                tool_calls=tool_call_count,
                elevated_title=elevated_title,
            )
        except Exception as e:
            log.warning(f"Wander graph session record failed: {e}")

    return result
