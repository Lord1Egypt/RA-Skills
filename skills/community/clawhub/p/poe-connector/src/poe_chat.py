#!/usr/bin/env python3
"""Poe Connector — Text chat completions (streaming and non-streaming) with file input support."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from poe_utils import (
    get_client,
    retry_on_rate_limit,
    handle_api_error,
    parse_extra_body,
    build_file_messages,
    get_default_model,
    get_chat_options,
)
import openai


def build_messages(
    message: str | None,
    messages_json: str | None,
    system: str | None,
    files: list[str] | None,
) -> list[dict]:
    """Assemble the messages list from CLI arguments."""
    msgs: list[dict] = []

    if system:
        msgs.append({"role": "system", "content": system})

    if messages_json:
        try:
            cleaned = messages_json.lstrip("\ufeff").strip()
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON for --messages: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(parsed, list):
            print("Error: --messages must be a JSON array.", file=sys.stderr)
            sys.exit(1)
        msgs.extend(parsed)
    elif message:
        if files:
            msgs.extend(build_file_messages(message, files))
        else:
            msgs.append({"role": "user", "content": message})
    else:
        print("Error: provide either --message or --messages.", file=sys.stderr)
        sys.exit(1)

    return msgs


def chat(
    model: str,
    messages: list[dict],
    stream: bool = False,
    extra_body: dict | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> None:
    """Send a chat completion request to Poe and print the response."""
    client = get_client()

    kwargs: dict = {"model": model, "messages": messages}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    if temperature is not None:
        kwargs["temperature"] = temperature
    if extra_body:
        kwargs["extra_body"] = extra_body

    if stream:
        kwargs["stream"] = True

        def do_stream():
            return client.chat.completions.create(**kwargs)

        response = retry_on_rate_limit(do_stream)
        try:
            for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    print(delta, end="", flush=True)
            print()
        except openai.APIError as e:
            handle_api_error(e)
            sys.exit(1)
    else:
        def do_chat():
            return client.chat.completions.create(**kwargs)

        try:
            response = retry_on_rate_limit(do_chat)
        except openai.APIError as e:
            handle_api_error(e)
            sys.exit(1)

        content = response.choices[0].message.content
        print(content)

        usage = response.usage
        if usage:
            print(
                f"\n--- Usage: {usage.prompt_tokens} prompt + "
                f"{usage.completion_tokens} completion = "
                f"{usage.total_tokens} total tokens ---",
                file=sys.stderr,
            )


def main():
    parser = argparse.ArgumentParser(
        description="Chat with AI models via the Poe API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  %(prog)s --model Claude-Sonnet-4 --message "Hello"\n'
            '  %(prog)s --model GPT-5.2 --system "You are a pirate." --message "Ahoy" --stream\n'
            "  %(prog)s --model Claude-Sonnet-4 --message \"Describe this\" --files photo.jpg\n"
        ),
    )
    parser.add_argument("--model", "-m", help="Poe model name (default from poe_config.json)")
    parser.add_argument("--message", "-M", help="User message text")
    parser.add_argument("--messages", help="Full conversation as a JSON array of {role, content} objects")
    parser.add_argument("--system", "-s", help="System prompt")
    parser.add_argument("--stream", action="store_true", default=None, help="Stream the response token by token")
    parser.add_argument("--no-stream", dest="stream", action="store_false", help="Disable streaming")
    parser.add_argument("--files", "-f", nargs="+", help="File paths to attach (images, PDFs, audio, video)")
    parser.add_argument("--max-tokens", type=int, help="Maximum tokens in the response")
    parser.add_argument("--temperature", type=float, help="Sampling temperature (0-2)")
    parser.add_argument("--extra", help='Extra body params as JSON (e.g. \'{"thinking_budget": 10000}\')')

    args = parser.parse_args()

    model = args.model or get_default_model("chat")
    if not model:
        print("Error: no --model given and no default in poe_config.json", file=sys.stderr)
        sys.exit(1)

    opts = get_chat_options()
    stream = args.stream if args.stream is not None else opts.get("stream", False)
    max_tokens = args.max_tokens if args.max_tokens is not None else opts.get("max_tokens")
    temperature = args.temperature if args.temperature is not None else opts.get("temperature")

    messages = build_messages(args.message, args.messages, args.system, args.files)
    extra = parse_extra_body(args.extra)

    chat(
        model=model,
        messages=messages,
        stream=stream,
        extra_body=extra,
        max_tokens=max_tokens,
        temperature=temperature,
    )


if __name__ == "__main__":
    main()
