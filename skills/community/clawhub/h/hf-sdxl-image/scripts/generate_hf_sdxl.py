#!/usr/bin/env python3
import argparse
import os
import sys
import time
import json
import urllib.request
import urllib.error

DEFAULT_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"


def get_model_id() -> str:
    model = os.getenv("HF_IMAGE_MODEL", DEFAULT_MODEL).strip()
    return model or DEFAULT_MODEL


def fail(message: str, code: int = 1):
    print(message, file=sys.stderr)
    sys.exit(code)


def infer_extension(content_type: str) -> str:
    if not content_type:
        return ".bin"
    content_type = content_type.split(";")[0].strip().lower()
    mapping = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "application/json": ".json",
    }
    return mapping.get(content_type, ".bin")


def request_image(prompt: str, token: str, timeout: int, extra_options: dict | None = None) -> tuple[bytes, str]:
    payload = {"inputs": prompt}
    if extra_options:
        payload["options"] = extra_options

    model_id = get_model_id()
    api_url = f"https://router.huggingface.co/hf-inference/models/{model_id}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "image/png",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            return body, content_type
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        fail(f"HTTP {e.code} from Hugging Face API for model {model_id}:\n{body}")
    except urllib.error.URLError as e:
        fail(f"Network error calling Hugging Face API: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate an image with the Hugging Face Inference API.")
    parser = argparse.ArgumentParser(description="Generate an image with the Hugging Face Inference API.")
    parser.add_argument("prompt", help="Prompt text used to generate the image")
    parser.add_argument("--output", required=True, help="Temporary or final output file path or directory. The script prints the saved file path to stdout.")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds (default: 180)")
    parser.add_argument("--wait-for-model", action="store_true", help="Ask the API to wait for model cold start instead of failing fast")
    args = parser.parse_args()

    token = os.getenv("HUGGINGFACE_TOKEN")
    if not token:
        fail("Missing HUGGINGFACE_TOKEN environment variable.")

    options = {"wait_for_model": True} if args.wait_for_model else None
    body, content_type = request_image(args.prompt, token, args.timeout, options)

    if content_type.startswith("application/json"):
        text = body.decode("utf-8", errors="replace")
        fail(f"API returned JSON instead of an image:\n{text}")

    output = args.output
    if output.endswith("/") or os.path.isdir(output) or os.path.splitext(output)[1] == "":
        os.makedirs(output, exist_ok=True)
        filename = f"hf-sdxl-{time.strftime('%Y%m%d-%H%M%S')}{infer_extension(content_type)}"
        output = os.path.join(output, filename)
    else:
        os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)

    with open(output, "wb") as f:
        f.write(body)

    print(output)


if __name__ == "__main__":
    main()
