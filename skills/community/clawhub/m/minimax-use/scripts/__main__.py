#!/usr/bin/env python3
"""
AI MiniMax - Network search, image understanding, and LLM inference tools
Callable directly from OpenClaw via exec

Usage:
  python3 -m scripts web_search "query"
  python3 -m scripts understand_image "prompt" /path/to/image.jpg
  python3 -m scripts chat "message" [--system "system prompt"] [--model "model name"]
"""

import os
import sys
import json
import argparse
import requests
import base64

# Read from system environment variables
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")
MINIMAX_API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com/anthropic")

# Available models
AVAILABLE_MODELS = {
    "M2.7": "MiniMax-M2.7",
    "M2.7-highspeed": "MiniMax-M2.7-highspeed",
    "M2.5": "MiniMax-M2.5",
    "M2.5-highspeed": "MiniMax-M2.5-highspeed",
    "M2.1": "MiniMax-M2.1",
    "M2.1-highspeed": "MiniMax-M2.1-highspeed",
    "M2": "MiniMax-M2",
}


def web_search(query: str, count: int = 10) -> dict:
    """Perform web search"""
    if not MINIMAX_API_KEY:
        return {"success": False, "error": "MINIMAX_API_KEY not set. Please set MINIMAX_API_KEY environment variable."}

    url = f"{MINIMAX_API_HOST}/v1/coding_plan/search"
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"q": query}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Check API errors
        base_resp = data.get("base_resp", {})
        if base_resp.get("status_code") != 0:
            return {"success": False, "error": base_resp.get("status_msg", "API error")}

        return {"success": True, "result": data}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def understand_image(prompt: str, image_source: str) -> dict:
    """Understand image content"""
    if not MINIMAX_API_KEY:
        return {"success": False, "error": "MINIMAX_API_KEY not set. Please set MINIMAX_API_KEY environment variable."}

    # Handle image: convert local file to base64, or use URL directly
    image_url = image_source

    if not image_source.startswith(("http://", "https://")):
        # Local file, convert to base64
        try:
            with open(image_source, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
                # Determine MIME type from file extension
                ext = image_source.lower().split(".")[-1]
                mime_type = {
                    "jpg": "image/jpeg",
                    "jpeg": "image/jpeg",
                    "png": "image/png",
                    "webp": "image/webp"
                }.get(ext, "image/jpeg")
                image_url = f"data:{mime_type};base64,{img_data}"
        except Exception as e:
            return {"success": False, "error": f"Failed to read image: {str(e)}"}

    url = f"{MINIMAX_API_HOST}/v1/coding_plan/vlm"
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "image_url": image_url
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Check API errors
        base_resp = data.get("base_resp", {})
        if base_resp.get("status_code") != 0:
            return {"success": False, "error": base_resp.get("status_msg", "API error")}

        # VLM response content is in 'content' field
        content = data.get("content", "")
        return {"success": True, "result": content}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def chat(
    message: str,
    system: str = None,
    model: str = "MiniMax-M2.7",
    temperature: float = 1.0,
    max_tokens: int = 4096,
    stream: bool = False,
    history: list = None
) -> dict:
    """
    Chat with MiniMax LLM for inference

    Args:
        message: User message
        system: System prompt (optional)
        model: Model name, default MiniMax-M2.7
        temperature: Temperature parameter, range (0.0, 1.0], default 1.0
        max_tokens: Max tokens to generate, default 4096
        stream: Enable streaming response, default False
        history: History list for multi-turn conversation, each message {"role": "user"/"assistant", "content": "..."}

    Returns:
        Success: {"success": True, "result": {"content": [...], "thinking": "..."}}
        Failure: {"success": False, "error": "error message"}
    """
    if not MINIMAX_API_KEY:
        return {"success": False, "error": "MINIMAX_API_KEY not set. Please set MINIMAX_API_KEY environment variable."}

    # LLM inference uses Token Plan endpoint
    url = f"{MINIMAX_API_HOST}/v1/messages"

    # Build message list
    messages = []
    if history:
        for msg in history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": [{"type": "text", "text": msg.get("content", "")}]
            })

    # Add current user message
    messages.append({
        "role": "user",
        "content": [{"type": "text", "text": message}]
    })

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "stream": stream,
        "temperature": temperature
    }

    if system:
        payload["system"] = system

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        # Parse response content
        content_blocks = []
        thinking_content = None

        for block in data.get("content", []):
            if block.get("type") == "thinking":
                thinking_content = block.get("thinking", "")
            elif block.get("type") == "text":
                content_blocks.append(block.get("text", ""))

        result = {
            "content": "\n".join(content_blocks),
            "thinking": thinking_content,
            "usage": data.get("usage", {}),
            "stop_reason": data.get("stop_reason")
        }

        return {"success": True, "result": result}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def stream_chat(
    message: str,
    system: str = None,
    model: str = "MiniMax-M2.7",
    temperature: float = 1.0,
    max_tokens: int = 4096,
    history: list = None
) -> dict:
    """
    Chat with MiniMax LLM using streaming mode.

    Args:
        message: User message
        system: System prompt (optional)
        model: Model name, default MiniMax-M2.7
        temperature: Temperature parameter, range (0.0, 1.0], default 1.0
        max_tokens: Max tokens to generate, default 4096
        history: History list for multi-turn conversation

    Returns:
        Success: {"success": True, "result": {"content": "...", "thinking": "...", "chunks": [...]}}
        Failure: {"success": False, "error": "error message"}
    """
    if not MINIMAX_API_KEY:
        return {"success": False, "error": "MINIMAX_API_KEY not set. Please set MINIMAX_API_KEY environment variable."}

    url = f"{MINIMAX_API_HOST}/v1/messages"

    # Build message list
    messages = []
    if history:
        for msg in history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": [{"type": "text", "text": msg.get("content", "")}]
            })

    messages.append({
        "role": "user",
        "content": [{"type": "text", "text": message}]
    })

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "stream": True,
        "temperature": temperature
    }

    if system:
        payload["system"] = system

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120, stream=True)
        response.raise_for_status()

        full_content = ""
        thinking_content = None
        chunks = []

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str.strip() == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        event_type = data.get("type")

                        if event_type == "content_block_delta":
                            delta = data.get("delta", {})
                            if delta.get("type") == "text_delta":
                                text = delta.get("text", "")
                                full_content += text
                                chunks.append(text)
                        elif event_type == "message_delta":
                            delta = data.get("delta", {})
                            if delta.get("type") == "text_delta":
                                # Sometimes thinking comes this way too
                                pass
                    except json.JSONDecodeError:
                        continue

        result = {
            "content": full_content,
            "thinking": thinking_content,
            "chunks": chunks,
            "usage": {},
            "stop_reason": "stop_sequence"
        }

        return {"success": True, "result": result}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def translate(
    text: str,
    target_lang: str = "English",
    source_lang: str = "auto",
    model: str = "MiniMax-M2.7",
    temperature: float = 1.0,
    max_tokens: int = 4096
) -> dict:
    """
    Translate text using MiniMax LLM

    Args:
        text: Text to translate
        target_lang: Target language, e.g., "English", "Chinese", "Japanese"
        source_lang: Source language, "auto" for auto-detect, default "auto"
        model: Model name, default MiniMax-M2.7
        temperature: Temperature parameter, range (0.0, 1.0], default 1.0
        max_tokens: Max tokens to generate, default 4096

    Returns:
        Success: {"success": True, "result": {"translated_text": "...", "source_lang": "...", "target_lang": "..."}}
        Failure: {"success": False, "error": "error message"}
    """
    # Build translation prompt
    if source_lang == "auto":
        system_prompt = f"""You are a professional translation assistant.
Translate the following text into {target_lang}.
Only return the translated text, do not add any explanations, notes, or additional content."""
    else:
        system_prompt = f"""You are a professional translation assistant.
Translate the following {source_lang} text into {target_lang}.
Only return the translated text, do not add any explanations, notes, or additional content."""

    result = chat(
        message=text,
        system=system_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )

    if result.get("success"):
        translated_text = result.get("result", {}).get("content", "")
        detected_lang = source_lang if source_lang != "auto" else "auto"
        return {
            "success": True,
            "result": {
                "translated_text": translated_text.strip(),
                "source_lang": detected_lang,
                "target_lang": target_lang
            }
        }
    else:
        return result


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "web_search":
        parser = argparse.ArgumentParser()
        parser.add_argument("query", help="Search query")
        parser.add_argument("--count", "-n", type=int, default=10)
        args = parser.parse_args(sys.argv[2:])
        result = web_search(args.query, args.count)

    elif command == "understand_image":
        parser = argparse.ArgumentParser()
        parser.add_argument("prompt", help="Analysis prompt")
        parser.add_argument("image", help="Image path or URL")
        args = parser.parse_args(sys.argv[2:])
        result = understand_image(args.prompt, args.image)

    elif command == "chat":
        parser = argparse.ArgumentParser()
        parser.add_argument("message", help="User message")
        parser.add_argument("--system", "-s", help="System prompt")
        parser.add_argument("--model", "-m", default="MiniMax-M2.7",
                          help="Model name (default: MiniMax-M2.7)")
        parser.add_argument("--temperature", "-t", type=float, default=1.0,
                          help="Temperature (0.0-1.0, default: 1.0)")
        parser.add_argument("--max-tokens", type=int, default=4096,
                          help="Max tokens (default: 4096)")
        args = parser.parse_args(sys.argv[2:])
        result = chat(
            message=args.message,
            system=args.system,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )

    elif command == "models":
        # List available models
        result = {"success": True, "result": AVAILABLE_MODELS}

    elif command == "translate":
        parser = argparse.ArgumentParser()
        parser.add_argument("text", help="Text to translate")
        parser.add_argument("--to", "-t", default="English", help="Target language (default: English)")
        parser.add_argument("--from", "-f", dest="source_lang", default="auto", help="Source language (default: auto)")
        parser.add_argument("--model", "-m", default="MiniMax-M2.7", help="Model name")
        args = parser.parse_args(sys.argv[2:])
        result = translate(
            text=args.text,
            target_lang=args.to,
            source_lang=args.source_lang,
            model=args.model
        )

    elif command == "stream_chat":
        parser = argparse.ArgumentParser()
        parser.add_argument("message", help="User message")
        parser.add_argument("--system", "-s", help="System prompt")
        parser.add_argument("--model", "-m", default="MiniMax-M2.7",
                          help="Model name (default: MiniMax-M2.7)")
        parser.add_argument("--temperature", "-t", type=float, default=1.0,
                          help="Temperature (0.0-1.0, default: 1.0)")
        parser.add_argument("--max-tokens", type=int, default=4096,
                          help="Max tokens (default: 4096)")
        args = parser.parse_args(sys.argv[2:])
        result = stream_chat(
            message=args.message,
            system=args.system,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )

    else:
        result = {"success": False, "error": f"Unknown command: {command}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
