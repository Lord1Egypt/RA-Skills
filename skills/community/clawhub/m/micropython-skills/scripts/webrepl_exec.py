#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebREPL client for executing MicroPython code over WiFi.

Connects to a MicroPython device's WebREPL via websocket and executes code
in raw REPL mode, capturing output for the AI Agent to parse.

Usage:
    python3 webrepl_exec.py --host 192.168.1.100 --password repl123 --code "print('hello')"
    python3 webrepl_exec.py --host 192.168.1.100 --password repl123 --file script.py

Requires: pip install websocket-client
"""

import sys
import time
import argparse


def check_dependency():
    """Check if websocket-client is installed."""
    try:
        import websocket  # noqa: F401
        return True
    except ImportError:
        print(
            "ERROR: websocket-client is not installed.\n"
            "Install with: pip install websocket-client\n"
            "This is only needed for WiFi/WebREPL mode. "
            "For USB connections, use mpremote instead.",
            file=sys.stderr,
        )
        return False


def webrepl_exec(host, password, code, port=8266, connect_timeout=5, exec_timeout=30):
    """Execute code on device via WebREPL, return output."""
    import websocket

    url = f"ws://{host}:{port}"

    try:
        ws = websocket.create_connection(url, timeout=connect_timeout)
    except Exception as e:
        return None, f"Connection failed to {url}: {e}"

    try:
        # Read initial prompt (password prompt)
        initial = ws.recv()
        if isinstance(initial, bytes):
            initial = initial.decode("utf-8", errors="replace")

        # Send password
        ws.send(password + "\r\n")
        time.sleep(0.3)

        # Read password response
        resp = ws.recv()
        if isinstance(resp, bytes):
            resp = resp.decode("utf-8", errors="replace")

        if "denied" in resp.lower() or "rejected" in resp.lower():
            return None, "WebREPL authentication failed — wrong password"

        # Enter raw REPL mode (Ctrl-A)
        ws.send(b"\x01")
        time.sleep(0.2)
        # Drain any response
        ws.settimeout(0.5)
        try:
            ws.recv()
        except:
            pass

        # Send code (Ctrl-D to execute)
        if isinstance(code, str):
            code = code.encode("utf-8")
        ws.send(code + b"\x04")

        # Read output until we see ">" (raw REPL completion) or timeout
        ws.settimeout(1.0)
        output_parts = []
        deadline = time.time() + exec_timeout

        while time.time() < deadline:
            try:
                chunk = ws.recv()
                if isinstance(chunk, bytes):
                    chunk = chunk.decode("utf-8", errors="replace")
                output_parts.append(chunk)

                # Raw REPL signals completion with ">"
                full = "".join(output_parts)
                if "\x04>" in full or full.endswith(">"):
                    break
            except websocket.WebSocketTimeoutException:
                continue
            except websocket.WebSocketConnectionClosedException:
                break

        if time.time() >= deadline:
            return "".join(output_parts), "Execution timed out"

        # Exit raw REPL (Ctrl-B)
        ws.send(b"\x02")

        # Clean up output: remove raw REPL markers
        output = "".join(output_parts)
        output = output.replace("OK", "", 1)  # Remove initial "OK" from raw REPL
        output = output.replace("\x04", "").replace(">", "").strip()

        return output, ""

    finally:
        try:
            ws.close()
        except:
            pass


def main():
    parser = argparse.ArgumentParser(
        description="Execute MicroPython code over WebREPL"
    )
    parser.add_argument("--host", required=True, help="Device IP address")
    parser.add_argument("--password", required=True, help="WebREPL password")
    parser.add_argument("--code", help="MicroPython code to execute")
    parser.add_argument("--file", help="MicroPython script file to execute")
    parser.add_argument("--port", type=int, default=8266, help="WebREPL port (default: 8266)")
    parser.add_argument("--timeout", type=int, default=30, help="Execution timeout in seconds (default: 30)")
    args = parser.parse_args()

    if not check_dependency():
        sys.exit(1)

    if not args.code and not args.file:
        print("ERROR: Provide either --code or --file", file=sys.stderr)
        sys.exit(1)

    code = args.code
    if args.file:
        try:
            with open(args.file, "r") as f:
                code = f.read()
        except OSError as e:
            print(f"ERROR: Cannot read file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

    output, error = webrepl_exec(
        args.host, args.password, code,
        port=args.port, exec_timeout=args.timeout
    )

    if output:
        print(output)
    if error:
        print(f"ERROR:{error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
