#!/usr/bin/env python3
"""
IMA Video Creation Script — ima_video_create.py
Version: 1.0.0 (Modularized)

Video generation via IMA Open API.
Flow: product list → virtual param resolution → task create → poll status.

- Task types: text_to_video | image_to_video | first_last_frame_to_video | reference_image_to_video
- --input-images: accepts HTTPS URLs or local file paths (local files auto-uploaded to IMA CDN).

Usage:
  python3 ima_video_create.py --api-key ima_xxx --task-type text_to_video \\
    --model-id ima-pro --prompt "a cute puppy"

Logs: ~/.openclaw/logs/ima_skills/ima_create_YYYYMMDD.log
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Force unbuffered output for real-time streaming (critical for OpenClaw)
# This ensures all print() statements are immediately visible
import io
sys.stdout = io.TextIOWrapper(
    open(sys.stdout.fileno(), 'wb', 0),  # 0 = unbuffered
    encoding='utf-8',
    write_through=True
)

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

# ─── Import Modules ───────────────────────────────────────────────────────────

# Import logger module
try:
    from ima_logger import setup_logger, cleanup_old_logs
    logger = setup_logger("ima_skills")
    cleanup_old_logs(days=7)
except ImportError:
    # Fallback: create basic logger if ima_logger not available
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-5s | %(funcName)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("ima_skills")

# Import event stream module for Agent integration
try:
    from ima_events import (
        emit_task_preview, emit_progress, emit_info, emit_warning, emit_error,
        emit_result, emit_prompt, emit_stage_start, emit_stage_complete,
        emit_file_upload, emit_compliance_check, human_print
    )
    EVENT_STREAM_ENABLED = True
except ImportError:
    # Fallback: no-op implementations if ima_events not available
    EVENT_STREAM_ENABLED = False
    def emit_task_preview(*args, **kwargs): pass
    def emit_progress(*args, **kwargs): pass
    def emit_info(*args, **kwargs): pass
    def emit_warning(*args, **kwargs): pass
    def emit_error(*args, **kwargs): pass
    def emit_result(*args, **kwargs): pass
    def emit_prompt(message, options, default=None, timeout=None): return default or options[0]
    def emit_stage_start(*args, **kwargs): pass
    def emit_stage_complete(*args, **kwargs): pass
    def emit_file_upload(*args, **kwargs): pass
    def emit_compliance_check(*args, **kwargs): pass
    def human_print(*args, **kwargs): print(*args, **kwargs)

# Import compliance verification functions (with fallback)
try:
    from ima_compliance import verify_compliance_flow, requires_compliance_verification
except ImportError:
    logger.warning("ima_compliance module not found - compliance verification disabled")
    # Fallback: no-op implementations
    def requires_compliance_verification(task_type: str) -> bool:
        """Fallback when ima_compliance is unavailable."""
        return False
    
    def verify_compliance_flow(base_url: str, api_key: str, task_type: str, input_media: list):
        """Fallback when ima_compliance is unavailable."""
        logger.warning("Compliance verification skipped (module not available)")

# Import core API client functions
try:
    from ima_api_client import (
        get_product_list,
        find_model_version,
        list_all_models,
        filter_allowed_models,
        create_task,
        poll_task
    )
except ImportError as e:
    logger.error(f"Failed to import ima_api_client: {e}")
    sys.exit(1)

# Import media upload functions
try:
    from ima_media_upload import (
        normalize_input_media,
        prepare_media_url,
        is_remote_url
    )
except ImportError as e:
    logger.error(f"Failed to import ima_media_upload: {e}")
    sys.exit(1)

# Import media type detection
try:
    from ima_media_utils import (
        detect_media_type,
        extract_media_metadata,
        classify_media_inputs,
        extract_video_cover_frame,
        download_remote_media_to_temp,
    )
except ImportError as e:
    logger.error(f"Failed to import ima_media_utils: {e}")
    sys.exit(1)

# Import reflection and error handling functions
try:
    from ima_reflection import (
        extract_error_info,
        create_task_with_reflection
    )
except ImportError as e:
    logger.error(f"Failed to import ima_reflection: {e}")
    sys.exit(1)

# Import diagnostic functions
try:
    from ima_diagnostics import build_contextual_diagnosis, format_user_failure_message
except ImportError as e:
    logger.error(f"Failed to import ima_diagnostics: {e}")
    sys.exit(1)

try:
    from ima_reference_validation import (
        ReferenceInputValidationError,
        inspect_reference_source,
        validate_reference_image_to_video_inputs,
    )
except ImportError as e:
    logger.error(f"Failed to import ima_reference_validation: {e}")
    sys.exit(1)

# Import parameter resolution functions
try:
    from ima_param_resolver import extract_model_params
except ImportError as e:
    logger.error(f"Failed to import ima_param_resolver: {e}")
    sys.exit(1)

# Import constants
try:
    from ima_constants import (
        ALLOWED_MODEL_IDS,
        normalize_model_id,
        to_user_facing_model_name,
        MAX_POLL_WAIT_SECONDS,
        POLL_CONFIG,
        VIDEO_RECORDS_URL
    )
except ImportError as e:
    logger.error(f"Failed to import ima_constants: {e}")
    sys.exit(1)

# Import preference management functions
try:
    from ima_prefs import get_preferred_model_id
except ImportError as e:
    logger.error(f"Failed to import ima_prefs: {e}")
    sys.exit(1)

# ─── Local Constants ──────────────────────────────────────────────────────────

# Primary API endpoint (owned by IMA Studio)
DEFAULT_BASE_URL = "https://api.imastudio.com"

# Media upload endpoint (owned by IMA Studio)
DEFAULT_IM_BASE_URL = "https://imapi.liveme.com"

# User preference storage
PREFS_PATH = os.path.expanduser("~/.openclaw/memory/ima_prefs.json")

# ─── Preference Management ────────────────────────────────────────────────────

def flatten_and_split_args(arg_list: list) -> list[str]:
    """
    Flatten nested list arguments and split comma-separated values.
    Handles both formats:
    - --reference-image img1.jpg img2.jpg (nargs="*")
    - --reference-image img1.jpg,img2.jpg (comma-separated)
    
    Args:
        arg_list: Nested list from argparse with action="append"
                  e.g., [['img1.jpg', 'img2.jpg'], ['img3.jpg']]
                  
    Returns:
        Flattened list of individual paths
        e.g., ['img1.jpg', 'img2.jpg', 'img3.jpg']
    """
    result = []
    for item in arg_list:
        if isinstance(item, list):
            for sub_item in item:
                # Split by comma to handle comma-separated format
                result.extend([s.strip() for s in str(sub_item).split(',') if s.strip()])
        elif item:
            # Split by comma to handle comma-separated format
            result.extend([s.strip() for s in str(item).split(',') if s.strip()])
    return result


def infer_task_type(model_id: str | None,
                    user_provided: str | None,
                    input_images: list[str] | None,
                    first_last_frame: bool = False,
                    reference_image: bool = False) -> str:
    """Infer task_type from explicit input and media shape."""
    del model_id  # Reserved for future model-specific inference rules.

    if user_provided:
        return user_provided

    normalized_inputs = normalize_input_media(input_images or [])

    if reference_image:
        if not normalized_inputs:
            raise ValueError("reference_image_to_video requires at least 1 input image")
        return "reference_image_to_video"

    if first_last_frame:
        if len(normalized_inputs) < 2:
            raise ValueError("first_last_frame_to_video requires at least 2 input images")
        return "first_last_frame_to_video"

    if not normalized_inputs:
        return "text_to_video"

    media_types = {detect_media_type(source) for source in normalized_inputs}
    if "video" in media_types or "audio" in media_types:
        return "reference_image_to_video"

    if len(normalized_inputs) == 1:
        return "image_to_video"

    # Without explicit first-last-frame intent, multiple images are references.
    return "reference_image_to_video"


def prepare_media_inputs(sources: list[str | bytes],
                         api_key: str,
                         im_base_url: str) -> dict:
    """
    Upload/normalize media inputs and split them into src_image/src_video/src_audio payloads.
    """
    urls_with_metadata: list[dict] = []
    input_urls: list[str] = []
    original_inputs: list[str] = []

    def _normalize_payload_metadata(metadata: dict, media_type: str) -> dict:
        normalized = dict(metadata)
        if media_type in {"video", "audio"} and "duration" in normalized:
            try:
                normalized["duration"] = int(float(normalized["duration"]))
            except (TypeError, ValueError):
                normalized["duration"] = 0
        return normalized

    for source in sources:
        media_type = detect_media_type(source) if isinstance(source, str) else "image"
        url = prepare_media_url(source, api_key, im_base_url, media_type=media_type)
        input_urls.append(url)
        original_inputs.append(source if isinstance(source, str) else "<bytes>")

        if isinstance(source, str) and not is_remote_url(source):
            metadata = extract_media_metadata(source, media_type, url)
        else:
            metadata = {"url": url}
            if media_type == "image":
                metadata.setdefault("width", 0)
                metadata.setdefault("height", 0)
            elif media_type == "video":
                metadata.setdefault("duration", 0.0)
                metadata.setdefault("width", 0)
                metadata.setdefault("height", 0)
                metadata.setdefault("cover", "")
            elif media_type == "audio":
                metadata.setdefault("duration", 0.0)

        if media_type == "video":
            metadata["cover"] = build_video_cover_url(source, api_key, im_base_url)

        metadata = _normalize_payload_metadata(metadata, media_type)
        metadata["type"] = media_type
        urls_with_metadata.append(metadata)

    src_image, src_video, src_audio = classify_media_inputs(urls_with_metadata)
    return {
        "input_urls": input_urls,
        "src_image": src_image,
        "src_video": src_video,
        "src_audio": src_audio,
        "original_inputs": original_inputs,
    }


def build_video_cover_url(source: str | bytes,
                          api_key: str,
                          im_base_url: str) -> str:
    """Extract first frame from a video, upload it as an image, and return its URL."""
    temp_video_path = None
    temp_cover_path = None
    try:
        if isinstance(source, str) and is_remote_url(source):
            suffix = Path(source).suffix or ".mp4"
            temp_video_path = download_remote_media_to_temp(source, suffix=suffix)
            video_path = temp_video_path
        elif isinstance(source, str):
            video_path = source
        else:
            raise RuntimeError("Video cover extraction requires file-path media input")

        temp_cover_path = extract_video_cover_frame(video_path)
        return prepare_media_url(temp_cover_path, api_key, im_base_url, media_type="image")
    finally:
        for temp_path in (temp_cover_path, temp_video_path):
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    p = argparse.ArgumentParser(
        description="IMA AI Creation Script — reliable task creation via Open API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to video (ima-pro — default quality)
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_video \\
    --model-id ima-pro --prompt "a cute puppy running on grass"

  # Text to video with faster model
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_video \\
    --model-id ima-pro-fast --prompt "cinematic city skyline at sunset"

  # Image to video (ima-pro)
  python3 ima_video_create.py \\
    --api-key ima_xxx \\
    --model-id ima-pro --prompt "camera slowly zooms in" \\
    --input-images https://example.com/photo.jpg

  # Multiple images default to reference_image_to_video unless first-last-frame is explicit
  python3 ima_video_create.py \\
    --api-key ima_xxx --input-images image1.jpg image2.jpg \\
    --model-id ima-pro --prompt "character animation"

  # Reference video to video
  python3 ima_video_create.py \\
    --api-key ima_xxx --reference-video clip.mp4 \\
    --model-id ima-pro-fast --prompt "add cinematic motion"

  # Reference audio to video
  python3 ima_video_create.py \\
    --api-key ima_xxx --reference-audio narration.mp3 \\
    --model-id ima-pro-fast --prompt "generate visuals matching the narration mood"

  # First-last-frame transition (explicit task_type required)
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type first_last_frame_to_video \\
    --input-images first.jpg last.jpg \\
    --model-id ima-pro --prompt "smooth transition"

  # Text to video WITHOUT AUDIO (disable default audio generation)
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_video \\
    --model-id ima-pro --prompt "cinematic scene" \\
    --extra-params '{"audio": false}'

  # List all models for a category
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_video --list-models
""",
    )

    p.add_argument("--api-key",  required=False,
                   help="IMA Open API key (starts with ima_). Can also use IMA_API_KEY env var")
    p.add_argument("--task-type", required=False,
                   choices=list(POLL_CONFIG.keys()),
                   help="Task type to create. Auto-inferred from media when omitted.")
    p.add_argument("--model-id",
                   help="Model ID (allowed: ima-pro, ima-pro-fast; Seedance aliases are auto-mapped)")
    p.add_argument("--version-id",
                   help="Specific version ID — overrides auto-select of latest")
    p.add_argument("--prompt",
                   help="Generation prompt (required unless --list-models)")
    p.add_argument("--input-images", nargs="*", action="append", default=[],
                   help="Input image links/paths. For local files, upload to OSS first; "
                        "for remote http(s) links, use directly. Can be repeated multiple times; "
                        "values are merged and normalized as string array.")
    p.add_argument("--reference-image", nargs="*", action="append", default=[],
                   help="Reference image(s) for reference_image_to_video task type. "
                        "Automatically infers task_type=reference_image_to_video if provided. "
                        "Can specify multiple images. Merged with --input-images.")
    p.add_argument("--reference-video", nargs="*", action="append", default=[],
                   help="Reference video(s) for reference_image_to_video task type. "
                        "Automatically infers task_type=reference_image_to_video if provided. "
                        "Merged with --input-images.")
    p.add_argument("--reference-audio", nargs="*", action="append", default=[],
                   help="Reference audio file(s) for reference_image_to_video task type. "
                        "Automatically infers task_type=reference_image_to_video if provided. "
                        "Merged with --input-images.")
    p.add_argument("--size",
                   help="Override size parameter (e.g. 4k, 2k, 1024x1024)")
    p.add_argument("--extra-params",
                   help='JSON string of extra inner parameters, e.g. \'{"n":2}\'')
    p.add_argument("--language", default="en",
                   help="Language for product labels (en/zh)")
    p.add_argument("--list-models", action="store_true",
                   help="List all available models for --task-type and exit")
    p.add_argument("--output-json", action="store_true",
                   help="Output final result as JSON (for agent parsing)")

    return p


def main():
    """Main execution function."""
    args   = build_parser().parse_args()
    base   = DEFAULT_BASE_URL
    
    # Display production environment configuration
    logger.info(f"Using PRODUCTION environment (base_url={base})")
    emit_info(f"🏭 PRODUCTION Environment: {base}")
    
    # Merge explicit reference media into the shared media input list before inference.
    reference_media: list[str] = []
    for attr_name in ("reference_image", "reference_video", "reference_audio"):
        attr_value = getattr(args, attr_name, None)
        if attr_value:
            reference_media.extend(flatten_and_split_args(attr_value))

    for item in reference_media:
        args.input_images.append([item])

    normalized_inputs = normalize_input_media(args.input_images)

    try:
        inferred_task_type = infer_task_type(
            model_id=args.model_id,
            user_provided=args.task_type,
            input_images=normalized_inputs,
            reference_image=bool(reference_media),
        )
    except ValueError as e:
        logger.error(str(e))
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not args.task_type:
        args.task_type = inferred_task_type
        logger.info(
            "Auto-inferred task_type=%s from %s input(s)",
            args.task_type,
            len(normalized_inputs),
        )
        emit_info(
            f"Auto-inferred task_type: {args.task_type} "
            f"(based on {len(normalized_inputs)} input item(s))"
        )
        human_print(
            f"ℹ️  Auto-inferred task_type: {args.task_type} "
            f"({len(normalized_inputs)} input item(s))",
            flush=True,
        )

    if args.model_id:
        normalized_model_id = normalize_model_id(args.model_id)
        if normalized_model_id not in ALLOWED_MODEL_IDS:
            print(
                f"❌ model_id='{args.model_id}' is not allowed in ima-seedance2-video-generator.\n"
                f"   Allowed model_ids: {', '.join(sorted(ALLOWED_MODEL_IDS))}",
                file=sys.stderr,
            )
            sys.exit(1)
        args.model_id = normalized_model_id

    # Get API key from args or environment variable
    apikey = args.api_key or os.getenv("IMA_API_KEY")
    if not apikey:
        logger.error("API key is required. Use --api-key or set IMA_API_KEY environment variable")
        sys.exit(1)

    start_time = time.time()
    masked_key = f"{apikey[:10]}..." if len(apikey) > 10 else "***"
    logger.info(f"Script started: task_type={args.task_type}, model_id={args.model_id or 'auto'}, "
                f"api_key={masked_key}, base_url={base}")

    # ── 1. Query product list ──────────────────────────────────────────────────
    emit_stage_start("query", "Querying product list...")
    human_print(f"🔍 Querying product list: category={args.task_type}", flush=True)
    try:
        tree = get_product_list(base, apikey, args.task_type,
                                language=args.language)
        emit_stage_complete("query", f"Product list retrieved: {len(tree)} models found")
    except Exception as e:
        logger.error(f"Product list failed: {str(e)}")
        emit_error(f"Product list failed: {e}", stage="query")
        print(f"❌ Product list failed: {e}", file=sys.stderr)
        sys.exit(1)

    # ── List models mode ───────────────────────────────────────────────────────
    if args.list_models:
        models = filter_allowed_models(list_all_models(tree))
        if not models:
            print(
                f"\n❌ No allowed models found for '{args.task_type}'. "
                f"Expected one of: {', '.join(sorted(ALLOWED_MODEL_IDS))}",
                file=sys.stderr,
            )
            sys.exit(1)
        human_print(f"\nAvailable models for '{args.task_type}':")
        human_print(f"{'Name':<28} {'model_id':<34} {'version_id':<44} {'pts':>4}  attr_id")
        human_print("─" * 120)
        for m in models:
            human_print(f"{m['name']:<28} {m['model_id']:<34} {m['version_id']:<44} "
                        f"{m['credit']:>4}  {m['attr_id']}")
        sys.exit(0)

    # ── Resolve model_id ───────────────────────────────────────────────────────
    if not args.model_id:
        # Check API key preference
        pref_model = get_preferred_model_id(apikey, args.task_type)
        if pref_model:
            args.model_id = pref_model
            human_print(f"💡 Using your preferred model: {pref_model}", flush=True)
        else:
            print("❌ --model-id is required (no saved preference found)", file=sys.stderr)
            print(
                "   Allowed model_ids: " + ", ".join(sorted(ALLOWED_MODEL_IDS)),
                file=sys.stderr,
            )
            sys.exit(1)

    if not args.prompt:
        print("❌ --prompt is required", file=sys.stderr)
        sys.exit(1)

    # ── 2. Find model version in tree ─────────────────────────────────────────
    node = find_model_version(tree, args.model_id, args.version_id)
    if not node:
        logger.error(f"Model not found: model_id={args.model_id}, task_type={args.task_type}")
        available_models = filter_allowed_models(list_all_models(tree))
        available = [f"  {m['model_id']}" for m in available_models]
        print(f"❌ model_id='{args.model_id}' not found for task_type='{args.task_type}'.",
              file=sys.stderr)
        if available:
            print("   Available allowed model_ids:\n" + "\n".join(available), file=sys.stderr)
        else:
            print(
                "   No allowed model_ids returned by product list. "
                f"Expected: {', '.join(sorted(ALLOWED_MODEL_IDS))}",
                file=sys.stderr,
            )
        sys.exit(1)

    # ── 3. Extract params (including virtual param resolution) ────────────────
    try:
        mp = extract_model_params(node)
    except RuntimeError as e:
        logger.error(f"Param extraction failed: {str(e)}")
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    display_model_name = to_user_facing_model_name(
        mp.get("model_name"),
        mp.get("model_id"),
    )
    
    # ── Emit Task Preview (SKILL.md Rule 2: inform user BEFORE execution) ──────
    emit_task_preview(
        model=display_model_name,
        task_type=args.task_type,
        duration=args.extra_params and json.loads(args.extra_params).get("duration") if args.extra_params else None,
        size=args.size,
        credit=mp['credit'],
        estimated_time="4-6 minutes",
        environment="test" if "test" in base else "production"
    )
    
    human_print(f"✅ Model found:")
    human_print(f"   name          = {display_model_name}")
    human_print(f"   model_id      = {mp['model_id']}")
    human_print(f"   model_version = {mp['model_version']}   ← version_id from product list")
    human_print(f"   attribute_id  = {mp['attribute_id']}")
    human_print(f"   credit        = {mp['credit']} pts")
    human_print(f"   form_params   = {json.dumps(mp['form_params'], ensure_ascii=False)}")

    # Apply overrides
    extra: dict = {}
    if args.size:
        extra["size"] = args.size
    if args.extra_params:
        try:
            extra.update(json.loads(args.extra_params))
        except json.JSONDecodeError as e:
            print(f"❌ Invalid --extra-params JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # ── 4. Strict preflight validation for multimodal reference tasks ─────────
    if args.task_type == "reference_image_to_video" and normalized_inputs:
        try:
            emit_stage_start("validate", "Validating reference media constraints...")
            reference_media_details = [inspect_reference_source(source) for source in normalized_inputs]
            validate_reference_image_to_video_inputs(reference_media_details)
            emit_stage_complete("validate", "Reference media constraints satisfied")
        except ReferenceInputValidationError as e:
            logger.error(f"Reference media validation failed: {e}")
            emit_error(f"Reference media validation failed: {e}", stage="validate")
            print(str(e), file=sys.stderr)
            sys.exit(1)

    # ── 5. Process input media (upload if needed) ─────────────────────────────
    prepared_media = {
        "input_urls": [],
        "src_image": [],
        "src_video": [],
        "src_audio": [],
        "original_inputs": [],
    }
    normalized_inputs = normalize_input_media(args.input_images)
    if normalized_inputs:
        im_base = DEFAULT_IM_BASE_URL
        
        emit_stage_start("upload", f"Processing {len(normalized_inputs)} input media item(s)...")
        human_print(f"\n📤 Processing {len(normalized_inputs)} input media item(s)…", flush=True)
        
        try:
            prepared_media = prepare_media_inputs(normalized_inputs, apikey, im_base)
            for i, (original_source, media_url) in enumerate(
                zip(prepared_media["original_inputs"], prepared_media["input_urls"]),
                1,
            ):
                if isinstance(original_source, str) and is_remote_url(original_source):
                    human_print(f"   [{i}] Using URL: {media_url[:60]}...")
                    emit_info(f"Using URL [{i}/{len(normalized_inputs)}]: {os.path.basename(media_url)}")
                else:
                    filename = os.path.basename(original_source) if isinstance(original_source, str) else "bytes"
                    human_print(f"   [{i}] Uploaded: {filename} → {media_url[:60]}...")
                    emit_file_upload(filename, i, len(normalized_inputs), media_url)
        except RuntimeError as e:
            logger.error(f"Failed to process media inputs: {e}")
            emit_error(f"Failed to process media inputs: {e}", stage="upload")
            print(f"❌ Failed to process media inputs: {e}", file=sys.stderr)
            sys.exit(1)
        
        emit_stage_complete("upload", f"All {len(prepared_media['input_urls'])} media item(s) ready")
        human_print(f"✅ All {len(prepared_media['input_urls'])} media item(s) ready")

    # ── 5.5. Asset Compliance Verification (V2) ────────────────────────────────
    # Verify all input media (images/videos/audio) before task creation
    if requires_compliance_verification(args.task_type) and prepared_media["input_urls"]:
        try:
            emit_stage_start("verify", "Asset compliance verification required...")
            human_print(f"\n🔒 Asset compliance verification required...", flush=True)
            
            verify_compliance_flow(
                base_url=base,
                api_key=apikey,
                task_type=args.task_type,
                media_paths=prepared_media["original_inputs"],
                uploaded_urls=prepared_media["input_urls"],
            )
            
            emit_stage_complete("verify", "All assets verified and compliant")
            human_print(f"✅ All assets verified and compliant", flush=True)
        except Exception as e:
            logger.error(f"Compliance verification failed: {e}")
            emit_error(f"Compliance verification failed: {e}", stage="verify")
            print(f"❌ Compliance verification failed: {e}", file=sys.stderr)
            print(f"   Task creation aborted for safety.", file=sys.stderr)
            sys.exit(1)

    # ── 6. Create task (with Reflection) ──────────────────────────────────────
    emit_stage_start("create", "Creating video generation task...")
    human_print(f"\n🚀 Creating task…", flush=True)
    
    try:
        task_id = create_task_with_reflection(
            base_url=base,
            api_key=apikey,
            task_type=args.task_type,
            model_params=mp,
            prompt=args.prompt,
            input_urls=prepared_media["input_urls"],
            extra_params=extra if extra else None,
            src_image=prepared_media["src_image"],
            src_video=prepared_media["src_video"],
            src_audio=prepared_media["src_audio"],
            max_attempts=3  # Up to 3 automatic retries with reflection
        )
        emit_stage_complete("create", f"Task created: {task_id}")
    except RuntimeError as e:
        logger.error(f"Task creation failed after reflection: {str(e)}")
        emit_error(f"Create task failed: {e}", stage="create")
        print(f"❌ Create task failed:\n{e}", file=sys.stderr)
        sys.exit(1)

    human_print(f"✅ Task created: {task_id}", flush=True)

    # ── 7. Poll for result ─────────────────────────────────────────────────────
    cfg        = POLL_CONFIG.get(args.task_type, {"interval": 5, "max_wait": MAX_POLL_WAIT_SECONDS})
    est_max    = cfg["max_wait"] // 2   # optimistic estimate = half of max_wait
    
    emit_stage_start("polling", f"Polling for result (max {cfg['max_wait']}s)...")
    human_print(f"\n⏳ Polling… (interval={cfg['interval']}s, max={cfg['max_wait']}s)",
                flush=True)

    # Progress callback for SKILL.md Rule 3: progress updates every 30-45s
    def progress_callback(percent, elapsed, message):
        emit_progress(percent, elapsed, message, stage="polling")
    
    try:
        media = poll_task(base, apikey, task_id,
                          estimated_max=est_max,
                          poll_interval=cfg["interval"],
                          max_wait=cfg["max_wait"],
                          on_progress=progress_callback)
        emit_stage_complete("polling", "Video generated successfully")
    except (TimeoutError, RuntimeError) as e:
        logger.error(f"Task polling failed: {str(e)}")
        poll_error = extract_error_info(e)
        diagnosis = build_contextual_diagnosis(
            error_info=poll_error,
            task_type=args.task_type,
            model_params=mp,
            current_params=extra if extra else {},
            input_images=prepared_media["input_urls"],
            credit_rules=mp.get("all_credit_rules", []),
        )
        logger.error(
            "Polling contextual diagnosis: %s",
            json.dumps(diagnosis, ensure_ascii=False),
        )
        print(
            "\n❌ "
            + format_user_failure_message(
                diagnosis=diagnosis,
                attempts_used=1,
                max_attempts=1,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # ── 8. Output result ───────────────────────────────────────────────────────
    result_url = media.get("url") or media.get("preview_url") or ""
    cover_url  = media.get("cover_url") or ""

    # Emit final result event (SKILL.md Rule 5: SEND results properly)
    emit_result(
        success=True,
        task_id=task_id,
        url=result_url,
        cover_url=cover_url,
        message=f"Video generated successfully: {display_model_name} | {mp['credit']} pts"
    )
    
    human_print(f"\n✅ Generation complete!")
    human_print(f"   URL:   {result_url}")
    if cover_url:
        human_print(f"   Cover: {cover_url}")

    if args.output_json:
        out = {
            "task_id":    task_id,
            "url":        result_url,
            "cover_url":  cover_url,
            "model_id":   mp["model_id"],
            "model_name": display_model_name,
            "credit":     mp["credit"],
        }
        print("\n" + json.dumps(out, ensure_ascii=False, indent=2))

    total_time = int(time.time() - start_time)
    logger.info(f"Script completed: total_time={total_time}s, task_id={task_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
