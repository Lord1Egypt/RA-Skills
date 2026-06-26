#!/usr/bin/env python3
"""Generate images or edit existing images using LitMedia Common Task APIs.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- When using `query`, keep polling (default timeout=600s) until
  status is 'completed' or 'failed'. Do NOT stop after a single check.
- Never hand a pending taskId back to the user and say "check it later".
  Always poll to completion within the timeout window.

Supported task types:
    text2image   Text-to-Image  — generate images from a text prompt
    image_edit   Image Edit     — edit images with prompt + reference images

Subcommands:
    run           Submit task AND poll until done — DEFAULT, use this first
    submit        Submit only, print taskId, exit — use for parallel batch jobs
    query         Poll an existing taskId until done (or timeout) — use for recovery
    list-models   Show supported models and parameter constraints
    estimate-cost Estimate credit cost before running

Usage:
    python ai_image.py run  --type text2image --model "Nano Banana" --prompt "..." [options]
    python ai_image.py run  --type image_edit --model "Nano Banana" --prompt "..." --input-images <image url|local paths> [options]
    python ai_image.py submit --type <text2image|image_edit> [task-specific options]
    python ai_image.py query  --type <text2image|image_edit> --task-id <taskId> [options]
"""

import argparse
import json as json_mod
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))

from shared.client import LitMediaClient, LitMediaError, TaskStatus
from shared.upload import resolve_local_file

TASK_TYPES = ("text2image", "image_edit")

ENDPOINTS = {
    "text2image": {
        "submit": "/lit-video/do-image",
        "query": "/lit-video/get-image-process",
    },
    "image_edit": {
        "submit": "/lit-video/do-image",
        "query": "/lit-video/get-image-process",
    },
}

DEFAULT_TIMEOUT = 600
DEFAULT_INTERVAL = 30

# ---------------------------------------------------------------------------
# Model constraints
# Each entry: { "aspectRatio": list, "resolution": list|None, "maxImages": int }
#   resolution=None means the model does NOT support resolution (do not send).
#   resolution=[...] means the parameter is required.
# ---------------------------------------------------------------------------

TEXT2IMAGE_MODELS = {
    "Nano Banana":      {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": None, "model_id": 2},
    "Nano Banana 2":    {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["1K", "2K", "4K"], "model_id": 9},
    "Nano Banana Pro":  {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["1K", "2K", "4K"], "model_id": 4},
    "Seedream 4.0":     {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["1K", "2K"], "model_id": 5},
    "Seedream 4.5":     {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["1K", "2K"], "model_id": 6},
}

IMAGE_EDIT_MODELS = {
    "Nano Banana":      {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": None, "model_id": 2},
    "Nano Banana 2":    {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["1K", "2K", "4K"], "model_id": 9},
    "Nano Banana Pro":  {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["1K", "2K", "4K"], "model_id": 4},
    "Seedream 4.5":     {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["1K", "2K"], "model_id": 6},
    "Seedream 5.0":     {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": None, "model_id": 8},
}

MODEL_REGISTRY = {"text2image": TEXT2IMAGE_MODELS, "image_edit": IMAGE_EDIT_MODELS}

# ---------------------------------------------------------------------------
# Pricing — credits per image (generateCount=1).
# Key: resolution string or "default" for models without resolution.
# totalCost = unitCost × generateCount
# ---------------------------------------------------------------------------

_PRICING = {
    "text2image": {
        "Nano Banana 2":    {"1K": 15, "2K": 15, "4K": 20},
        "Nano Banana Pro":  {"1K": 15, "2K": 15, "4K": 30},
        "Nano Banana":      {"default": 10},
        "Seedream 4.0":     {"2K": 10, "4K": 15},
        "Seedream 4.5":     {"1K": 15, "2K": 20},
    },
    "image_edit": {
        "Nano Banana 2":    {"1K": 15, "2K": 15, "4K": 20},
        "Nano Banana Pro":  {"1K": 15, "2K": 15, "4K": 30},
        "Nano Banana":      {"default": 10},
        "Seedream 5.0":     {"default": 5},
        "Seedream 4.5":     {"1K": 15, "2K": 20},
    },
}


def estimate_cost(task_type: str, model: str, resolution: str | None,
                  count: int = 1) -> float | None:
    """Return estimated total cost in credits, or None if model/params unknown."""
    prices = _PRICING.get(task_type, {}).get(model)
    if not prices:
        return None
    if resolution and resolution in prices:
        return round(prices[resolution] * count, 2)
    if "default" in prices:
        return round(prices["default"] * count, 2)
    return None

def get_model_id(task_type: str, model: str, quiet: bool) -> int:
    """Warn on stderr if parameters are incompatible with model constraints."""
    model_id = 9
    registry = MODEL_REGISTRY.get(task_type, {})
    if model not in registry:
        if not quiet:
            known = ", ".join(sorted(registry.keys()))
            print(
                f"Warning: unknown model '{model}' for {task_type}. "
                f"Known models: {known}",
                file=sys.stderr,
            )
        return model_id

    spec = registry[model]
    return spec.get("model_id", 9)

def validate_model_params(task_type: str, model: str, aspect_ratio: str | None,
                          resolution: str | None, quiet: bool) -> None:
    """Warn on stderr if parameters are incompatible with model constraints."""
    registry = MODEL_REGISTRY.get(task_type, {})
    if model not in registry:
        if not quiet:
            known = ", ".join(sorted(registry.keys()))
            print(
                f"Warning: unknown model '{model}' for {task_type}. "
                f"Known models: {known}",
                file=sys.stderr,
            )
        return

    spec = registry[model]

    if aspect_ratio and aspect_ratio not in spec["aspectRatio"]:
        if not quiet:
            print(
                f"Warning: model '{model}' supports aspectRatio "
                f"{spec['aspectRatio']}, got '{aspect_ratio}'.",
                file=sys.stderr,
            )

    if resolution and spec["resolution"] is None:
        if not quiet:
            print(
                f"Warning: model '{model}' does not support resolution "
                f"(got '{resolution}'). Do NOT send this parameter.",
                file=sys.stderr,
            )
    elif resolution and spec["resolution"] and resolution not in spec["resolution"]:
        if not quiet:
            print(
                f"Warning: model '{model}' supports resolution "
                f"{spec['resolution']}, got '{resolution}'.",
                file=sys.stderr,
            )
    elif not resolution and spec["resolution"] is not None:
        if not quiet:
            print(
                f"Warning: model '{model}' requires resolution "
                f"(one of {spec['resolution']}). Please provide --resolution.",
                file=sys.stderr,
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resolve_file(client: LitMediaClient, file_ref: str, quiet: bool) -> str:
    """If file_ref looks like a local path, upload it and return fileId."""
    return resolve_local_file(file_ref, quiet=quiet, client=client)


def build_text2image_body(args, model_id) -> dict:
    body = {
        "image_model": model_id,
        "prompt": args.prompt,
        "ratio": args.aspect_ratio,
        "image_num": args.count,
    }

    registry = MODEL_REGISTRY.get(args.type, {})
    if args.model in registry:
        spec = registry[args.model]
        if args.resolution and spec["resolution"] is not None:
            body["quality"] = args.resolution

    return body


def build_image_edit_body(args, model_id, client: LitMediaClient) -> dict:
    body = {
        "image_model": model_id,
        "prompt": args.prompt,
        "ratio": args.aspect_ratio,
        "image_num": args.count,
    }
    if args.input_images:
        body["img_url"] = resolve_file(client, args.input_images, args.quiet)

    registry = MODEL_REGISTRY.get(args.type, {})
    if args.model in registry:
        spec = registry[args.model]
        if args.resolution and spec["resolution"] is not None:
            body["quality"] = args.resolution.lower()

    return body


def build_body(args, client: LitMediaClient) -> dict:
    """Dispatch to the type-specific body builder, with model constraint checks."""
    validate_model_params(
        args.type, args.model,
        getattr(args, "aspect_ratio", None),
        getattr(args, "resolution", None),
        args.quiet,
    )

    model_id = get_model_id(args.type, args.model, args.quiet)
    if args.type == "text2image":
        return build_text2image_body(args, model_id)
    elif args.type == "image_edit":
        return build_image_edit_body(args, model_id, client)
    raise ValueError(f"Unknown type: {args.type}")


def do_submit(client: LitMediaClient, task_type: str, body: dict, quiet: bool) -> str:
    """POST submit task, return taskId."""
    path = ENDPOINTS[task_type]["submit"]
    label = {"text2image": "text-to-image", "image_edit": "image-edit"}
    if not quiet:
        print(f"Submitting {label[task_type]} task...", file=sys.stderr)
    result = client.post(path, json=body)
    task_id = result["create_id"]
    if not quiet:
        print(f"Task submitted. taskId: {task_id}", file=sys.stderr)
    return task_id


def do_poll(client: LitMediaClient, task_type: str, task_id: str,
            timeout: float, interval: float, quiet: bool) -> dict:
    """Poll until status is terminal or timeout is exceeded."""
    path = ENDPOINTS[task_type]["query"]
    if not quiet:
        print(
            f"Polling task {task_id} (timeout={timeout}s, interval={interval}s)...",
            file=sys.stderr,
        )
    return client.poll_task(
        path,
        task_id,
        interval=interval,
        timeout=timeout,
        verbose=not quiet,
    )


def download_image(url: str, output: str, quiet: bool) -> None:
    """Download an image from URL to a local file."""
    import requests as req

    if not quiet:
        print(f"Downloading image to {output}...", file=sys.stderr)

    resp = req.get(url, stream=True)
    resp.raise_for_status()

    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    if not quiet:
        size_kb = os.path.getsize(output) / 1024
        print(f"Downloaded: {output} ({size_kb:.1f} KB)", file=sys.stderr)


def print_result(result: dict, args, client: LitMediaClient) -> None:
    """Print final result: image URLs by default, full JSON with --json."""

    status = TaskStatus(result.get("status"))

    images = result.get("image_urls", [])
    if status == TaskStatus.COMPLETED:
        if args.output_dir and images:
            os.makedirs(args.output_dir, exist_ok=True)
            for i, url in enumerate(images):
                ext = "jpg"
                time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                out_path = os.path.join(args.output_dir, f"image_{time_name}.{ext}")
                download_image(url, out_path, args.quiet)
                print(f"out_path = {out_path} url = {url}")
        elif images:
            for i, url in enumerate(images):
                print(f"Image generation successful. Image url = {url}")

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        cost = result.get("cost_credit", "N/A")
        print(f"status: {status.label}  cost: {cost} credits")

        error_msg = result.get("error", "") or result.get("real_error", "")
        if status == TaskStatus.FAILED:
            print(f"  [1] failed: {error_msg or 'Unknown error'}")



# ---------------------------------------------------------------------------
# Argument definitions
# ---------------------------------------------------------------------------

def add_common_args(p):
    """Add arguments shared by all task types."""
    p.add_argument("--type", required=True, choices=TASK_TYPES,
                   help="Task type: text2image or image_edit")
    p.add_argument("--model", required=True,
                   help='Model display name, e.g. "Nano Banana", "Seedream 5.0"')
    p.add_argument("--prompt", required=True,
                   help="Text prompt describing the image to generate or the edit to apply")
    p.add_argument("--aspect-ratio", required=True,
                   help='Aspect ratio, e.g. "16:9", "1:1"')
    p.add_argument("--resolution", default="1K",
                   help='Resolution: "1K", "2K", "4K" (model-dependent, some require it, some forbid it)')
    p.add_argument("--count", type=int, default=1,
                   help="Number of images to generate (1-4, default: 1)")

def add_image_edit_args(p):
    """Add image-edit specific arguments."""
    p.add_argument("--input-images", default=None,
                   help="Reference image url or local paths for image editing")


def add_poll_args(p):
    """Add polling control arguments."""
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Max polling time in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                   help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")


def add_output_args(p):
    """Add output/download arguments."""
    p.add_argument("--output-dir", default=None,
                   help="Download result images to this directory")
    p.add_argument("--json", action="store_true",
                   help="Output full JSON response")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="Suppress status messages on stderr")


def validate_args(args, parser):
    """Validate type-specific required arguments."""
    if args.type == "image_edit":
        if not args.input_images:
            parser.error("--input-images is required for image_edit")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_list_models(args, parser):
    """Print supported models and their parameter constraints."""
    task_type = args.type
    registry = MODEL_REGISTRY.get(task_type, {})
    if not registry:
        print(f"No models registered for type '{task_type}'.")
        return

    if args.json:
        print(json_mod.dumps(registry, indent=2, ensure_ascii=False))
        return

    type_label = {"text2image": "Text-to-Image", "image_edit": "Image Edit"}
    print(f"\n{type_label.get(task_type, task_type)} - Supported Models\n")

    if task_type == "image_edit":
        print(f"{'Model':<22} {'Aspect Ratio':<45} {'Resolution':<22} {'Max Images'}")
        print("-" * 100)
        for name, spec in registry.items():
            ar = ", ".join(spec["aspectRatio"])
            res = ", ".join(spec["resolution"]) if spec["resolution"] else "N/A (forbidden)"
            mi = str(spec.get("maxImages", "N/A"))
            print(f"{name:<22} {ar:<45} {res:<22} {mi}")
    else:
        print(f"{'Model':<22} {'Aspect Ratio':<45} {'Resolution'}")
        print("-" * 80)
        for name, spec in registry.items():
            ar = ", ".join(spec["aspectRatio"])
            res = ", ".join(spec["resolution"]) if spec["resolution"] else "N/A (forbidden)"
            print(f"{name:<22} {ar:<45} {res}")
    print()


def cmd_estimate_cost(args, parser):
    """Print estimated cost for a given model + parameters."""
    cost = estimate_cost(args.type, args.model, args.resolution, args.count or 1)
    if cost is None:
        print(f"Cannot estimate cost for model '{args.model}' with given parameters.", file=sys.stderr)
        print("Use list-models to see available models, or check references/api-docs.md.", file=sys.stderr)
        sys.exit(1)
    count = args.count or 1
    unit = round(cost / count, 2)
    if args.json:
        print(json_mod.dumps({"type": args.type, "model": args.model,
                               "resolution": args.resolution,
                               "count": count, "unitCost": unit, "totalCost": cost}))
    else:
        print(f"type: {args.type}  model: {args.model}  "
              f"resolution: {args.resolution or 'default'}  count: {count}")
        print(f"estimated unit cost: {unit} credits")
        print(f"estimated total cost: {cost} credits")


def cmd_run(args, parser):
    """Submit task then poll until done — full flow (default)."""
    validate_args(args, parser)
    client = LitMediaClient()
    body = build_body(args, client)
    task_id = do_submit(client, args.type, body, args.quiet)
    result = do_poll(client, args.type, task_id, args.timeout, args.interval, args.quiet)
    print_result(result, args, client)


def cmd_submit(args, parser):
    """Submit task only — print taskId and exit immediately."""
    validate_args(args, parser)
    client = LitMediaClient()
    body = build_body(args, client)
    task_id = do_submit(client, args.type, body, args.quiet)
    print(task_id)


def cmd_query(args, parser):
    """Poll an existing task by taskId until done or timeout."""
    client = LitMediaClient()
    try:
        result = do_poll(
            client, args.type, args.task_id,
            args.timeout, args.interval, args.quiet,
        )
        print_result(result, args, client)
    except TimeoutError as e:
        if not args.quiet:
            print(f"Timeout reached: {e}", file=sys.stderr)
            print("Fetching last known status...", file=sys.stderr)
        path = ENDPOINTS[args.type]["query"]
        last = client.get(path, json={"create_id": args.task_id})
        status = last.get("status")
        task_id = last.get("taskId", args.task_id)
        if args.json:
            print(json_mod.dumps(last, indent=2, ensure_ascii=False))
        else:
            print(f"status: {status}  taskId: {task_id}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="LitMedia AI Image — text-to-image and image editing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. `query` polls continuously (not once) until done or --timeout.
  4. NEVER hand a pending taskId back to the user — always poll to completion.

Task types:
  text2image  Text-to-Image  (model + prompt → images)
  image_edit  Image Edit     (model + prompt + reference images → edited images)

Examples:
  # List available models for a task type
  python ai_image.py list-models --type text2image

  # Text-to-image
  python ai_image.py run --type text2image --model "Nano Banana" \\
      --prompt "A futuristic city" --aspect-ratio "16:9" --count 2

  # Image editing
  python ai_image.py run --type image_edit --model "Nano Banana" \\
      --prompt "Change background to a beach" --aspect-ratio "16:9"\\
      --input-images photo.jpg

  # Estimate cost
  python ai_image.py estimate-cost --type text2image --model "Nano Banana" \\
      --resolution "2K" --count 2

  # Query a timed-out task
  python ai_image.py query --type text2image --task-id <taskId>
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # -- run (default full flow) --
    p_run = sub.add_parser("run", help="[DEFAULT] Submit task and poll until done")
    add_common_args(p_run)
    add_image_edit_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    # -- submit only --
    p_submit = sub.add_parser("submit", help="Submit task only, print taskId and exit")
    add_common_args(p_submit)
    add_image_edit_args(p_submit)
    add_output_args(p_submit)

    # -- query / poll existing task --
    p_query = sub.add_parser("query", help="Poll existing taskId until done or timeout")
    p_query.add_argument("--type", required=True, choices=TASK_TYPES,
                         help="Task type (needed to select correct query endpoint)")
    p_query.add_argument("--task-id", required=True,
                         help="taskId returned by 'submit' or a previous 'run'")
    add_poll_args(p_query)
    add_output_args(p_query)

    # -- list-models --
    p_list = sub.add_parser("list-models", help="Show supported models and parameter constraints")
    p_list.add_argument("--type", required=True, choices=TASK_TYPES,
                        help="Task type to list models for")
    p_list.add_argument("--json", action="store_true",
                        help="Output as JSON")

    # -- estimate-cost --
    p_cost = sub.add_parser("estimate-cost", help="Estimate credit cost before running a task")
    p_cost.add_argument("--type", required=True, choices=TASK_TYPES,
                        help="Task type")
    p_cost.add_argument("--model", required=True, help="Model display name")
    p_cost.add_argument("--resolution", default=None, help="Resolution (e.g. 1K, 2K, 4K)")
    p_cost.add_argument("--count", type=int, default=1, help="generateCount (1-4)")
    p_cost.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.subcommand == "run":
        cmd_run(args, p_run)
    elif args.subcommand == "submit":
        cmd_submit(args, p_submit)
    elif args.subcommand == "query":
        cmd_query(args, p_query)
    elif args.subcommand == "list-models":
        cmd_list_models(args, p_list)
    elif args.subcommand == "estimate-cost":
        cmd_estimate_cost(args, p_cost)


if __name__ == "__main__":
    main()
