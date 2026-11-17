#!/usr/bin/env python3
"""Send a text to ChatGPT via CDP (Brave Browser) and extract the response.

Usage:
    python3 gpt_review.py --prompt "review this article..." --output /tmp/gpt_response.md
    python3 gpt_review.py --prompt-file /tmp/prompt.txt --output /tmp/gpt_response.md
    python3 gpt_review.py --prompt-file /tmp/prompt.txt --output /tmp/gpt_response.md --timeout 120

Environment:
    CDP_PORT  - CDP debugging port (default: 9222)

Requires: websockets, Brave Browser with --remote-debugging-port=9222,
          ChatGPT logged in at chatgpt.com.
"""

import argparse
import asyncio
import json
import subprocess
import sys
import time
import urllib.request
import urllib.parse

try:
    import websockets
except ImportError:
    print("Error: websockets not installed. Run: pip3 install websockets", file=sys.stderr)
    sys.exit(1)

CDP_SCRIPT = None  # Will be set from args or auto-detected


def get_cdp_script():
    """Find the cdp_exec.py script."""
    import os
    # Check common locations
    candidates = [
        os.path.expanduser(
            "skills/brave-browser-agent/"
            "skills/brave-browser-agent/scripts/cdp_exec.py"
        ),
        os.path.expanduser("~/.agents/skills/brave-browser-agent/scripts/cdp_exec.py"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def cdp_exec(tab_id, js_code, timeout_ms=15000, port=9222):
    """Execute JS in a tab via cdp_exec.py subprocess."""
    script = CDP_SCRIPT
    if not script:
        print("Error: cdp_exec.py not found", file=sys.stderr)
        return None
    result = subprocess.run(
        ["python3", script, "--port", str(port), "eval", tab_id, js_code,
         "--timeout-ms", str(timeout_ms)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0 and result.stderr:
        print(f"CDP eval error: {result.stderr.strip()}", file=sys.stderr)
    output = result.stdout.strip()
    # Filter out stderr noise, keep only the last non-empty stdout line
    if output:
        return output
    return None


def list_tabs(port=9222):
    """List open browser tabs."""
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/json/list", timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error listing tabs: {e}", file=sys.stderr)
        return None


def find_or_create_chatgpt_tab(port=9222):
    """Find an existing ChatGPT tab or create a new one."""
    tabs = list_tabs(port)
    if not tabs:
        print("No tabs found. Is Brave running?", file=sys.stderr)
        return None

    # Look for an existing chatgpt.com tab (not a conversation)
    for t in tabs:
        url = t.get("url", "")
        if "chatgpt.com" in url and ("/c/" not in url) and t.get("type") == "page":
            return t["id"]

    # Open a new tab via system command
    print("Opening new ChatGPT tab...", file=sys.stderr)
    subprocess.run(["open", "-a", "Brave Browser", "https://chatgpt.com"],
                   capture_output=True, timeout=5)
    time.sleep(8)

    # Find the new tab
    tabs = list_tabs(port)
    if not tabs:
        return None
    for t in tabs:
        url = t.get("url", "")
        if "chatgpt.com" in url and t.get("type") == "page":
            return t["id"]

    return None


def wait_for_editor(tab_id, port=9222, max_wait=15):
    """Wait for the ChatGPT prompt textarea to be ready."""
    for i in range(max_wait):
        result = cdp_exec(tab_id,
            "document.querySelector('#prompt-textarea') !== null",
            port=port)
        if result and "true" in result.lower():
            return True
        time.sleep(1)
    return False


def inject_text(tab_id, text, port=9222, chunk_size=1500):
    """Inject text into the ChatGPT ProseMirror editor, in chunks for long text.

    ProseMirror's insertText truncates very long strings. We split the text
    into chunks of `chunk_size` characters and inject each one separately.
    """
    # Clear existing content
    cdp_exec(tab_id,
        "(function(){const e=document.querySelector('#prompt-textarea');"
        "if(!e)return'no';e.focus();"
        "document.execCommand('selectAll',false,null);"
        "document.execCommand('delete',false,null);return'ok';})()",
        port=port)

    time.sleep(0.3)

    if len(text) <= chunk_size:
        # Short text: inject in one go
        escaped = json.dumps(text)
        js = (f"(function(){{"
              f"const e=document.querySelector('#prompt-textarea');"
              f"if(!e)return'no editor';"
              f"e.focus();"
              f"document.execCommand('insertText',false,{escaped});"
              f"return'injected '+e.textContent.length;"
              f"}})()")
        result = cdp_exec(tab_id, js, timeout_ms=10000, port=port)
        return result

    # Long text: inject in chunks
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    print(f"Injecting text in {len(chunks)} chunks ({len(text)} total chars)...", file=sys.stderr)
    total_injected = 0

    for idx, chunk in enumerate(chunks):
        escaped = json.dumps(chunk)
        js = (f"(function(){{"
              f"const e=document.querySelector('#prompt-textarea');"
              f"if(!e)return'no editor';"
              f"e.focus();"
              f"document.execCommand('insertText',false,{escaped});"
              f"return e.textContent.length;"
              f"}})()")
        result = cdp_exec(tab_id, js, timeout_ms=10000, port=port)
        try:
            total_injected = int(result) if result else 0
        except ValueError:
            total_injected = 0
        print(f"  Chunk {idx + 1}/{len(chunks)}: +{len(chunk)} chars → editor now {total_injected}", file=sys.stderr)
        time.sleep(0.3)  # Small pause between chunks to let ProseMirror settle

    return f"injected {total_injected} chars in {len(chunks)} chunks"


def click_send(tab_id, port=9222):
    """Click the send button in ChatGPT."""
    js = ("(function(){"
          "const btn=document.querySelector('button[data-testid=\"send-button\"]')"
          "||document.querySelector('button[aria-label=\"Send prompt\"]');"
          "if(btn){btn.click();return'clicked'};"
          "const btns=document.querySelectorAll('button');"
          "for(const b of btns){"
          "const svg=b.querySelector('svg');"
          "if(svg && b.closest('form')){b.click();return'clicked svg'}"
          "};"
          "return'not found'"
          "})()")
    return cdp_exec(tab_id, js, port=port)


def wait_for_response(tab_id, port=9222, timeout=120, check_interval=5, min_wait=30):
    """Wait for ChatGPT to finish generating a response.
    
    Args:
        min_wait: Minimum seconds to wait before stability detection kicks in.
                  This prevents false "stable" detection during ChatGPT's
                  thinking mode, where it outputs a short preview then pauses.
    """
    print(f"Waiting for response (timeout: {timeout}s, min_wait: {min_wait}s)...", file=sys.stderr)
    start = time.time()
    last_length = 0
    stable_count = 0

    while time.time() - start < timeout:
        time.sleep(check_interval)

        elapsed = int(time.time() - start)

        # Check if there's a response and if it's still growing
        js = ("(function(){"
              "const msgs=document.querySelectorAll('[data-message-author-role=\"assistant\"]');"
              "if(msgs.length===0)return'no_response';"
              "const last=msgs[msgs.length-1];"
              "const text=last.textContent;"
              "return text.length.toString();"
              "})()")
        result = cdp_exec(tab_id, js, port=port)

        if result and result != "no_response":
            try:
                current_length = int(result)
                
                # During min_wait phase: just log, don't check stability
                if elapsed < min_wait:
                    print(f"  ... min_wait phase ({elapsed}s): {current_length} chars", file=sys.stderr)
                    last_length = current_length
                    continue
                
                # After min_wait: require content > 500 chars to be considered valid
                # (thinking mode often outputs 50-200 chars then pauses)
                if current_length > 500 and current_length == last_length:
                    stable_count += 1
                    if stable_count >= 3:
                        print(f"Response stable at {current_length} chars after {elapsed}s",
                              file=sys.stderr)
                        return True
                else:
                    stable_count = 0
                last_length = current_length
                print(f"  ... response growing: {current_length} chars", file=sys.stderr)
            except ValueError:
                pass
        elif result == "no_response":
            print("  ... no response yet", file=sys.stderr)

    print(f"Timeout after {timeout}s", file=sys.stderr)
    return False


def extract_response(tab_id, port=9222, chunk_size=4000):
    """Extract the full ChatGPT response in chunks."""
    # First get total length
    js = ("(function(){"
          "const msgs=document.querySelectorAll('[data-message-author-role=\"assistant\"]');"
          "if(msgs.length===0)return'no_response';"
          "const last=msgs[msgs.length-1];"
          "return 'total:'+last.textContent.length;"
          "})()")
    result = cdp_exec(tab_id, js, port=port)

    if not result or "no_response" in result:
        return None

    total = int(result.split(":")[1])
    print(f"Extracting response ({total} chars)...", file=sys.stderr)

    # Extract in chunks
    full_text = ""
    offset = 0
    while offset < total:
        end = min(offset + chunk_size, total)
        js = (f"(function(){{"
              f"const msgs=document.querySelectorAll('[data-message-author-role=\"assistant\"]');"
              f"const last=msgs[msgs.length-1];"
              f"return last.textContent.substring({offset},{end});"
              f"}})()")
        chunk = cdp_exec(tab_id, js, timeout_ms=10000, port=port)
        if chunk:
            full_text += chunk
        offset = end

    return full_text


def close_tab(tab_id, port=9222):
    """Close a browser tab."""
    try:
        with urllib.request.urlopen(
            f"http://localhost:{port}/json/close/{tab_id}", timeout=5
        ) as resp:
            result = resp.read().decode("utf-8")
        print(f"Closed tab: {tab_id}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to close tab: {e}", file=sys.stderr)


def main():
    global CDP_SCRIPT

    parser = argparse.ArgumentParser(
        description="Send text to ChatGPT via CDP and extract the response")
    parser.add_argument("--prompt", help="Prompt text to send")
    parser.add_argument("--prompt-file", help="File containing the prompt")
    parser.add_argument("--output", required=True, help="Output file for the response")
    parser.add_argument("--timeout", type=int, default=120,
                        help="Max wait time for response in seconds (default: 120)")
    parser.add_argument("--port", type=int, default=9222, help="CDP port (default: 9222)")
    parser.add_argument("--cdp-script", help="Path to cdp_exec.py (auto-detected if omitted)")
    parser.add_argument("--keep-tab", action="store_true",
                        help="Don't close the ChatGPT tab after extraction")
    parser.add_argument("--min-wait", type=int, default=30,
                        help="Minimum seconds before stability detection (default: 30)")
    args = parser.parse_args()

    # Get prompt text
    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            prompt_text = f.read()
    elif args.prompt:
        prompt_text = args.prompt
    else:
        print("Error: provide --prompt or --prompt-file", file=sys.stderr)
        sys.exit(1)

    # Find cdp_exec.py
    CDP_SCRIPT = args.cdp_script or get_cdp_script()
    if not CDP_SCRIPT:
        print("Error: cdp_exec.py not found. Specify --cdp-script", file=sys.stderr)
        sys.exit(1)

    print(f"Prompt length: {len(prompt_text)} chars", file=sys.stderr)

    # Step 1: Find or create ChatGPT tab
    tab_id = find_or_create_chatgpt_tab(args.port)
    if not tab_id:
        print("Error: Could not find or create ChatGPT tab", file=sys.stderr)
        sys.exit(1)
    print(f"Using tab: {tab_id}", file=sys.stderr)

    # Step 2: Wait for editor
    if not wait_for_editor(tab_id, args.port):
        print("Error: ChatGPT editor not ready", file=sys.stderr)
        sys.exit(1)

    # Step 3: Inject text
    result = inject_text(tab_id, prompt_text, args.port)
    print(f"Inject result: {result}", file=sys.stderr)

    # Verify injection
    time.sleep(1)
    check = cdp_exec(tab_id,
        "document.querySelector('#prompt-textarea').textContent.length",
        port=args.port)
    print(f"Editor content length: {check}", file=sys.stderr)

    # Step 4: Click send
    result = click_send(tab_id, args.port)
    print(f"Send result: {result}", file=sys.stderr)

    if "not found" in (result or ""):
        print("Error: Could not find send button", file=sys.stderr)
        sys.exit(1)

    # Step 5: Wait for response
    if not wait_for_response(tab_id, args.port, args.timeout, min_wait=args.min_wait):
        print("Warning: Response may be incomplete", file=sys.stderr)

    # Step 6: Extract response
    response = extract_response(tab_id, args.port)
    if not response:
        print("Error: Could not extract response", file=sys.stderr)
        sys.exit(1)

    # Step 7: Save to file
    with open(args.output, "w") as f:
        f.write(response)
    print(f"Response saved to {args.output} ({len(response)} chars)", file=sys.stderr)

    # Step 8: Close tab (unless --keep-tab)
    if not args.keep_tab:
        close_tab(tab_id, args.port)

    print(f"DONE", file=sys.stderr)


if __name__ == "__main__":
    main()
