"""IdleClaw Consume — Use community inference when your API credits run out."""

import argparse
import json
import sys

import httpx

from config import get_server_url, validate_model_name


def stream_chat(server_url: str, model: str, prompt: str) -> None:
    """Send a chat request and stream the response."""
    url = f"{server_url}/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        with httpx.stream("POST", url, json=payload, timeout=120) as response:
            if response.status_code == 503:
                print(f"Error: No nodes available with model '{model}'.", file=sys.stderr)
                print("Try a different model, or wait for nodes to come online.", file=sys.stderr)
                print("Run 'python scripts/status.py' to see available models.", file=sys.stderr)
                sys.exit(1)

            response.raise_for_status()

            for line in response.iter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    token = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if token:
                        print(token, end="", flush=True)
                except json.JSONDecodeError:
                    continue

            print()  # Final newline

    except httpx.ConnectError:
        print(f"Error: Cannot connect to server at {server_url}", file=sys.stderr)
        print("Check that the IdleClaw server is running, or set IDLECLAW_SERVER.", file=sys.stderr)
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"Error: Server returned {e.response.status_code}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Send a chat request to the IdleClaw network")
    parser.add_argument("--model", required=True, help="Model name (e.g., llama3.2:3b)")
    parser.add_argument("--prompt", required=True, help="Chat message to send")
    args = parser.parse_args()

    model = validate_model_name(args.model)
    server_url = get_server_url()

    stream_chat(server_url, model, args.prompt)


if __name__ == "__main__":
    main()
