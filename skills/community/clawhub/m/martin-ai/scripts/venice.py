#!/usr/bin/env python3
"""Venice AI CLI — Full platform access via SkillBoss API Hub."""

import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://api.heybossai.com/v1"
PILOT_URL = f"{API_BASE}/pilot"
USER_AGENT = "ClawdbotVeniceSkill/1.0"
CLAWDBOT_CONFIG = Path.home() / ".clawdbot" / "clawdbot.json"


# ── Auth ─────────────────────────────────────────────────────────────────────

def get_api_key() -> str | None:
    """Get API key from env or clawdbot config."""
    key = os.environ.get("SKILLBOSS_API_KEY", "").strip()
    if key:
        return key
    if CLAWDBOT_CONFIG.exists():
        try:
            cfg = json.loads(CLAWDBOT_CONFIG.read_text())
            for skill_name in ("venice-ai", "venice-ai-media"):
                k = (cfg.get("skills", {}).get("entries", {})
                     .get(skill_name, {}).get("env", {})
                     .get("SKILLBOSS_API_KEY", ""))
                if k:
                    return k.strip()
        except (json.JSONDecodeError, OSError):
            pass
    return None


def require_key() -> str:
    key = get_api_key()
    if not key:
        print("Error: SKILLBOSS_API_KEY not found.", file=sys.stderr)
        print("Set env var or configure in ~/.clawdbot/clawdbot.json", file=sys.stderr)
        print("Get your key: https://heybossai.com", file=sys.stderr)
        sys.exit(2)
    return key


# ── HTTP ─────────────────────────────────────────────────────────────────────

def pilot_request(body: dict, api_key: str, timeout: int = 120) -> dict:
    """POST to SkillBoss API Hub /v1/pilot and return parsed JSON."""
    data = json.dumps(body).encode()
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = urllib.request.Request(PILOT_URL, method="POST", headers=headers, data=data)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"Error ({e.code}): {err}", file=sys.stderr)
        sys.exit(1)


def _stream_chat(body: dict, api_key: str, timeout: int = 120):
    """Stream chat response via SkillBoss pilot (non-streaming fallback)."""
    # SkillBoss /v1/pilot does not support SSE streaming; get full response
    resp = pilot_request(body, api_key, timeout)
    choices = resp.get("result", {}).get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content", "")
        print(content)
    return resp.get("result", {}).get("usage")


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_models(args):
    """List available model types via SkillBoss API Hub."""
    print("SkillBoss API Hub auto-routes to the best available model.")
    print("\nSupported task types:")
    types = [
        ("chat",             "Text generation / chat completions"),
        ("image",            "Image generation"),
        ("video",            "Video generation"),
        ("tts",              "Text-to-speech"),
        ("stt",              "Speech-to-text"),
        ("embedding",        "Text embeddings"),
        ("search",           "Web search"),
        ("scraper",          "Web scraping / crawling"),
        ("music",            "Music generation"),
        ("sound_generation", "Sound/SFX generation"),
        ("ppt",              "Presentation generation"),
        ("email",            "Email sending"),
        ("storage",          "File storage"),
        ("http",             "Generic HTTP proxy"),
    ]
    print(f"\n{'Type':<20} {'Description'}")
    print("-" * 60)
    for t, desc in types:
        print(f"  {t:<18} {desc}")
    print("\nUse SKILLBOSS_API_KEY to authenticate all requests.")


def cmd_chat(args):
    """Generate text via chat completions."""
    key = require_key()

    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})

    if args.prompt:
        user_content = " ".join(args.prompt)
    elif not sys.stdin.isatty():
        user_content = sys.stdin.read().strip()
    else:
        print("Error: provide a prompt or pipe content via stdin", file=sys.stderr)
        sys.exit(1)

    messages.append({"role": "user", "content": user_content})

    body = {
        "type": "chat",
        "inputs": {"messages": messages},
        "prefer": "balanced",
    }

    if args.stream:
        usage = _stream_chat(body, key, timeout=args.timeout or 120)
        if args.show_usage and usage:
            _print_usage(usage)
    else:
        resp = pilot_request(body, key, timeout=args.timeout or 120)
        result = resp.get("result", {})
        choices = result.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            content = msg.get("content", "")
            if content:
                import re
                if args.strip_thinking or args.disable_thinking:
                    content = re.sub(r"<think>.*?</think>\s*", "", content, flags=re.DOTALL).strip()
                print(content)
        if args.show_usage:
            _print_usage(result.get("usage", {}))


def _print_usage(usage: dict):
    if not usage:
        return
    print("\n--- Usage ---", file=sys.stderr)
    print(f"  Prompt tokens:     {usage.get('prompt_tokens', '?')}", file=sys.stderr)
    print(f"  Completion tokens: {usage.get('completion_tokens', '?')}", file=sys.stderr)
    print(f"  Total tokens:      {usage.get('total_tokens', '?')}", file=sys.stderr)


def cmd_embed(args):
    """Generate embeddings via SkillBoss API Hub."""
    key = require_key()

    texts = list(args.texts) if args.texts else []
    if args.file:
        with open(args.file) as f:
            texts.extend(line.strip() for line in f if line.strip())

    if not texts:
        if not sys.stdin.isatty():
            texts = [line.strip() for line in sys.stdin if line.strip()]
        else:
            print("Error: provide texts as arguments, --file, or via stdin", file=sys.stderr)
            sys.exit(1)

    body = {
        "type": "embedding",
        "inputs": {"input": texts if len(texts) > 1 else texts[0]},
        "prefer": "balanced",
    }
    resp = pilot_request(body, key)
    result = resp.get("result", {})

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        data = result.get("data", [])
        for item in data:
            idx = item.get("index", 0)
            emb = item.get("embedding", [])
            print(f"[{idx}] dimension={len(emb)}, first_5={emb[:5]}")
        usage = result.get("usage", {})
        if usage:
            print(f"\nTokens used: {usage.get('total_tokens', '?')}", file=sys.stderr)


def cmd_tts(args):
    """Text-to-speech generation via SkillBoss API Hub."""
    key = require_key()

    if args.list_voices:
        print("Voice selection is handled automatically by SkillBoss API Hub.")
        print("Available voice hint parameter: voice=<voice_id>")
        return

    if not args.text:
        print("Error: provide text to speak", file=sys.stderr)
        sys.exit(1)

    text = " ".join(args.text)
    inputs: dict = {"text": text}
    if args.voice:
        inputs["voice"] = args.voice

    body = {
        "type": "tts",
        "inputs": inputs,
        "prefer": "balanced",
    }
    resp = pilot_request(body, key, timeout=60)
    result = resp.get("result", {})
    audio_url = result.get("audio_url", "")

    if audio_url:
        # Download audio from returned URL
        req = urllib.request.Request(audio_url, headers={"User-Agent": USER_AGENT})
        audio_resp = urllib.request.urlopen(req, timeout=60)
        audio_data = audio_resp.read()
        out = Path(args.output) if args.output else Path(f"/tmp/venice-tts-{int(dt.datetime.now().timestamp())}.mp3")
        out.write_bytes(audio_data)
        print(f"Audio saved to: {out}")
        print(f"\nMEDIA: {out.as_posix()}")
    else:
        print("Unexpected response format", file=sys.stderr)
        print(str(result)[:500], file=sys.stderr)


def cmd_transcribe(args):
    """Speech-to-text transcription via SkillBoss API Hub."""
    key = require_key()

    if args.url:
        req = urllib.request.Request(args.url, headers={"User-Agent": USER_AGENT})
        resp = urllib.request.urlopen(req, timeout=60)
        audio_data = resp.read()
    elif args.file:
        fp = Path(args.file)
        if not fp.exists():
            print(f"Error: file not found: {fp}", file=sys.stderr)
            sys.exit(1)
        audio_data = fp.read_bytes()
    else:
        print("Error: provide --file or --url", file=sys.stderr)
        sys.exit(1)

    audio_b64 = base64.b64encode(audio_data).decode()
    body = {
        "type": "stt",
        "inputs": {"audio": audio_b64},
        "prefer": "balanced",
    }
    resp = pilot_request(body, key, timeout=120)
    result = resp.get("result", {})
    text = result.get("text", "") or result.get("transcript", "")
    if text:
        print(text)
    else:
        print(json.dumps(result, indent=2))


def cmd_balance(args):
    """Check SkillBoss account balance."""
    print("To check your SkillBoss API Hub balance, visit: https://heybossai.com/dashboard")
    print("Or contact SkillBoss support for API-based balance queries.")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Venice AI CLI (via SkillBoss API Hub)", prog="venice")
    sub = parser.add_subparsers(dest="command", help="Command")

    # models
    p_models = sub.add_parser("models", help="Show available task types")
    p_models.add_argument("--type", default="text", help="Model type(s) (informational only)")
    p_models.add_argument("--filter", help="Filter models by keyword (informational only)")

    # chat
    p_chat = sub.add_parser("chat", help="Text generation (chat completions)")
    p_chat.add_argument("prompt", nargs="*", help="Prompt text")
    p_chat.add_argument("--model", "-m", help="Model hint (auto-routed by SkillBoss)")
    p_chat.add_argument("--system", "-s", help="System prompt")
    p_chat.add_argument("--stream", action="store_true", help="Stream output (response fetched then printed)")
    p_chat.add_argument("--temperature", "-t", type=float, help="Sampling temperature (hint)")
    p_chat.add_argument("--max-tokens", type=int, help="Max output tokens (hint)")
    p_chat.add_argument("--json", action="store_true", help="Request JSON output")
    p_chat.add_argument("--strip-thinking", action="store_true", help="Strip thinking blocks from output")
    p_chat.add_argument("--disable-thinking", action="store_true", help="Disable reasoning entirely")
    p_chat.add_argument("--show-usage", action="store_true", help="Show token usage stats")
    p_chat.add_argument("--timeout", type=int, help="Request timeout in seconds")

    # embed
    p_embed = sub.add_parser("embed", help="Generate embeddings")
    p_embed.add_argument("texts", nargs="*", help="Texts to embed")
    p_embed.add_argument("--file", help="File with texts (one per line)")
    p_embed.add_argument("--output", choices=["summary", "json"], default="summary", help="Output format")

    # tts
    p_tts = sub.add_parser("tts", help="Text-to-speech")
    p_tts.add_argument("text", nargs="*", help="Text to speak")
    p_tts.add_argument("--voice", help="Voice hint")
    p_tts.add_argument("--output", "-o", help="Output file path")
    p_tts.add_argument("--list-voices", action="store_true", help="List available voices")

    # transcribe
    p_trans = sub.add_parser("transcribe", help="Speech-to-text")
    p_trans.add_argument("file", nargs="?", help="Audio file path")
    p_trans.add_argument("--url", help="Audio URL")
    p_trans.add_argument("--timestamps", action="store_true", help="Include word timestamps (if supported)")

    # balance
    sub.add_parser("balance", help="Check account balance")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmds = {
        "models": cmd_models,
        "chat": cmd_chat,
        "embed": cmd_embed,
        "tts": cmd_tts,
        "transcribe": cmd_transcribe,
        "balance": cmd_balance,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
