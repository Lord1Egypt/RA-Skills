"""
OpenLens-Skill — Local-first AI Media Generation Engine
=========================================================
Mode A (Skill/API): import and call run_openlens_task(**kwargs)
Mode B (Local GUI):  python skill_main.py  → opens localhost:8501
"""

from __future__ import annotations

import json
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

import requests

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("openlens")

# ─────────────────────────────────────────────────────────────────────────────
# Constants & defaults
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_OUTPUTS_DIR = Path(__file__).parent / "outputs"
SUPPORTED_TASKS = {"T2I", "T2V", "I2V", "V2V", "T2T"}
POLL_INTERVAL = 5          # seconds between status checks
POLL_TIMEOUT  = 300        # 5 minutes max

ASPECT_MAP = {             # aspect-ratio string → (width, height)
    "16:9"  : (1280, 720),
    "9:16"  : (720, 1280),
    "1:1"   : (1024, 1024),
    "4:3"   : (1024, 768),
    "21:9"  : (1920, 816),
}

# ─────────────────────────────────────────────────────────────────────────────
# Low-level helpers
# ─────────────────────────────────────────────────────────────────────────────

def _auth_headers(api_key: str) -> dict:
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _safe_model_slug(model_id: str) -> str:
    """Convert model id to a filesystem-safe slug, e.g. 'video/wan2.6-t2v' → 'wan2.6-t2v'."""
    return model_id.replace("/", "_").replace(":", "-")


def _output_path(task_type: str, model_id: str, ext: str) -> Path:
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = _safe_model_slug(model_id)
    folder = DEFAULT_OUTPUTS_DIR / task_type.upper()
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{ts}_{slug}.{ext}"


def _download(url: str, dest: Path, headers: dict | None = None) -> Path:
    """Stream-download a remote URL to *dest* without loading it all into RAM."""
    log.info("Downloading → %s", dest)
    with requests.get(url, headers=headers, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
    log.info("Saved %s  (%.1f MB)", dest.name, dest.stat().st_size / 1_048_576)
    return dest


# ─────────────────────────────────────────────────────────────────────────────
# Payload builders  (one per endpoint style)
# ─────────────────────────────────────────────────────────────────────────────

def _build_t2i_payload(model_id: str, prompt: str,
                        resolution: str, steps: int) -> dict:
    w, h = ASPECT_MAP.get(resolution, (1024, 1024))
    return {
        "model"  : model_id,
        "prompt" : prompt,
        "n"      : 1,
        "width"  : w,
        "height" : h,
        "steps"  : steps,
        "response_format": "url",
    }


def _build_t2v_payload(model_id: str, prompt: str,
                        resolution: str, duration: int, fps: int) -> dict:
    """Build payload for T2V API call (OnlyPix format)."""
    # Map aspect ratio to API-supported resolution strings
    RES_MAP = {
        "16:9": "720p",       # 1280*720
        "9:16": "720*1280",
        "1:1": "960*960",
        "4:3": "1024*768",
        "21:9": "1920*816",
    }
    size = RES_MAP.get(resolution, "720p")
    return {
        "model": model_id,
        "input": {"prompt": prompt},
        "parameters": {
            "size": size,
            "duration": duration,
            "fps": fps,
        },
    }


def _build_i2v_payload(model_id: str, prompt: str,
                        resolution: str, duration: int) -> dict:
    """Build payload for I2V/V2V API call (OnlyPix format)."""
    RES_MAP = {
        "16:9": "720p",
        "9:16": "720*1280",
        "1:1": "960*960",
        "4:3": "1024*768",
        "21:9": "1920*816",
    }
    size = RES_MAP.get(resolution, "720p")
    return {
        "model": model_id,
        "input": {"prompt": prompt},
        "parameters": {
            "size": size,
            "duration": duration,
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# API callers
# ─────────────────────────────────────────────────────────────────────────────

def _call_t2i(base_url: str, api_key: str, model_id: str,
              prompt: str, resolution: str, steps: int) -> Path:
    payload = _build_t2i_payload(model_id, prompt, resolution, steps)
    url     = f"{base_url.rstrip('/')}/images/generations"
    log.info("T2I request → %s  model=%s", url, model_id)
    resp = requests.post(url, headers=_auth_headers(api_key),
                         json=payload, timeout=60)
    resp.raise_for_status()
    image_url = resp.json()["data"][0]["url"]
    dest = _output_path("T2I", model_id, "png")
    return _download(image_url, dest)


def _call_t2t(base_url: str, api_key: str, model_id: str,
              prompt: str, system_prompt: str = "") -> str:
    url = f"{base_url.rstrip('/')}/chat/completions"
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model_id, "messages": messages,
               "temperature": 0.7, "max_tokens": 2048}
    log.info("T2T request → %s  model=%s", url, model_id)
    resp = requests.post(url, headers=_auth_headers(api_key),
                         json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _submit_video(base_url: str, api_key: str, payload: dict,
                  image_path: str | None = None,
                  video_path: str | None = None) -> str:
    """Submit a video task; return task_id."""
    url = f"{base_url.rstrip('/')}/video/generations"
    headers = {"Authorization": f"Bearer {api_key}"}

    if image_path or video_path:
        # Multipart form for I2V / V2V
        data  = {k: str(v) for k, v in payload.items()}
        files = {}
        if image_path:
            files["image"] = open(image_path, "rb")
        if video_path:
            files["video"] = open(video_path, "rb")
        resp = requests.post(url, headers=headers, data=data, files=files, timeout=60)
    else:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)

    resp.raise_for_status()
    body = resp.json()
    task_id = (body.get("id") or body.get("task_id")
               or (body.get("data") or {}).get("id"))
    if not task_id:
        raise RuntimeError(f"No task_id in response: {json.dumps(body)[:200]}")
    log.info("Video task submitted  id=%s", task_id)
    return task_id


def _poll_video(base_url: str, api_key: str,
                task_id: str, model_id: str,
                task_type: str) -> Path:
    """Poll until SUCCEED; stream-download the result."""
    status_url = f"{base_url.rstrip('/')}/video/generations/{task_id}"
    deadline   = time.time() + POLL_TIMEOUT

    while time.time() < deadline:
        resp = requests.get(status_url, headers=_auth_headers(api_key), timeout=30)
        resp.raise_for_status()
        data   = resp.json()
        status = (data.get("status") or data.get("state") or "").upper()
        pct    = data.get("progress", data.get("percentage", 0))
        log.info("  status=%-12s  progress=%s%%", status, pct)

        if status in ("SUCCEED", "SUCCESS", "COMPLETED", "DONE"):
            video_url = (
                data.get("video_url")
                or (data.get("videos") or [{}])[0].get("url")
                or (data.get("videos") or [{}])[0].get("video_url")
                or (data.get("output") or {}).get("url")
            )
            if not video_url:
                raise RuntimeError(f"Task succeeded but no video URL found: {data}")
            dest = _output_path(task_type, model_id, "mp4")
            return _download(video_url, dest)

        if status in ("FAILED", "ERROR", "CANCELLED"):
            raise RuntimeError(f"Task {task_id} ended with status {status}. "
                               f"Details: {json.dumps(data)[:300]}")
        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"Task {task_id} did not complete within {POLL_TIMEOUT}s.")


# ─────────────────────────────────────────────────────────────────────────────
# Public Skill API  ← OpenClaw calls this
# ─────────────────────────────────────────────────────────────────────────────

def run_openlens_task(
    url: str,
    api_key: str,
    model_id: str,
    prompt: str,
    task_type: str = "T2V",
    video_specs: dict | None = None,
    image_path: str | None = None,
    video_path: str | None = None,
    system_prompt: str = "",
    outputs_dir: str | None = None,
) -> dict:
    """
    Execute an AI generation task and save the result locally.

    Parameters
    ----------
    url         : API base URL, e.g. "https://api.onlypixai.com/v1"
    api_key     : Bearer token
    model_id    : e.g. "video/wan2.6-t2v" or "flux.1-schnell"
    prompt      : Generation prompt
    task_type   : "T2I" | "T2V" | "I2V" | "V2V" | "T2T"
    video_specs : {"resolution": "16:9", "duration": 10, "fps": 24}
    image_path  : Local path to source image (I2V)
    video_path  : Local path to source video (V2V)
    system_prompt: System message for T2T tasks
    outputs_dir : Override default outputs folder

    Returns
    -------
    dict with keys: success, task_type, local_path (or text), model_id,
                    prompt, error (if any)
    """
    global DEFAULT_OUTPUTS_DIR
    if outputs_dir:
        DEFAULT_OUTPUTS_DIR = Path(outputs_dir)

    task_type = task_type.upper()
    if task_type not in SUPPORTED_TASKS:
        return {"success": False, "error": f"Unknown task_type '{task_type}'. "
                f"Supported: {SUPPORTED_TASKS}"}

    specs = video_specs or {}
    resolution = specs.get("resolution", "16:9")
    duration   = int(specs.get("duration", 10))
    fps        = int(specs.get("fps", 24))
    steps      = int(specs.get("steps", 20))

    try:
        if task_type == "T2I":
            path = _call_t2i(url, api_key, model_id, prompt, resolution, steps)
            return {"success": True, "task_type": task_type,
                    "local_path": str(path.resolve()),
                    "model_id": model_id, "prompt": prompt}

        elif task_type == "T2T":
            text = _call_t2t(url, api_key, model_id, prompt, system_prompt)
            return {"success": True, "task_type": task_type,
                    "text": text, "model_id": model_id, "prompt": prompt}

        elif task_type == "T2V":
            payload = _build_t2v_payload(model_id, prompt, resolution, duration, fps)
            task_id = _submit_video(url, api_key, payload)
            path    = _poll_video(url, api_key, task_id, model_id, task_type)
            return {"success": True, "task_type": task_type, "task_id": task_id,
                    "local_path": str(path.resolve()),
                    "model_id": model_id, "prompt": prompt}

        elif task_type == "I2V":
            if not image_path:
                return {"success": False, "error": "image_path is required for I2V"}
            payload = _build_i2v_payload(model_id, prompt, resolution, duration)
            task_id = _submit_video(url, api_key, payload, image_path=image_path)
            path    = _poll_video(url, api_key, task_id, model_id, task_type)
            return {"success": True, "task_type": task_type, "task_id": task_id,
                    "local_path": str(path.resolve()),
                    "model_id": model_id, "prompt": prompt}

        elif task_type == "V2V":
            if not video_path:
                return {"success": False, "error": "video_path is required for V2V"}
            payload = _build_i2v_payload(model_id, prompt, resolution, duration)
            task_id = _submit_video(url, api_key, payload, video_path=video_path)
            path    = _poll_video(url, api_key, task_id, model_id, task_type)
            return {"success": True, "task_type": task_type, "task_id": task_id,
                    "local_path": str(path.resolve()),
                    "model_id": model_id, "prompt": prompt}

    except TimeoutError as e:
        log.error("Timeout: %s", e)
        return {"success": False, "error": str(e)}
    except requests.HTTPError as e:
        body = ""
        try:
            body = e.response.json()
        except Exception:
            body = e.response.text[:300]
        log.error("HTTP error: %s  body=%s", e, body)
        return {"success": False, "error": str(e), "api_response": body}
    except Exception as e:
        log.exception("Unexpected error")
        return {"success": False, "error": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# Mode B: Local GUI  (streamlit run skill_main.py)
# ─────────────────────────────────────────────────────────────────────────────

def _launch_gui():
    """Launch the Streamlit GUI from skill_main.py itself."""
    import streamlit as st

    st.set_page_config(page_title="OpenLens-Skill", page_icon="🎬", layout="wide")
    st.title("🎬 OpenLens-Skill — Local Execution Engine")
    st.caption("Generates AI images/videos and saves them to your local machine.")

    # ── Sidebar: config ──────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Configuration")
        base_url = st.text_input("Base URL", value="https://api.onlypixai.com/v1",
                                 key="sb_url")
        api_key  = st.text_input("API Key", type="password", key="sb_key")
        model_id = st.text_input("Model ID", value="video/wan2.6-t2v", key="sb_model")
        out_dir  = st.text_input("Output folder", value=str(DEFAULT_OUTPUTS_DIR),
                                 key="sb_out")
        st.divider()
        st.header("🎛️ Video Specs")
        resolution = st.selectbox("Aspect Ratio", ["16:9","9:16","1:1","4:3"], key="sb_res")
        duration   = st.selectbox("Duration (s)", [5, 10, 15], key="sb_dur")
        fps        = st.selectbox("FPS", [24, 30], key="sb_fps")
        steps      = st.slider("Steps (T2I)", 10, 50, 20, key="sb_steps")

    # ── Main area ────────────────────────────────────────────
    task_type = st.selectbox("Task", ["T2V", "T2I", "I2V", "V2V", "T2T"], key="task_sel")

    prompt = st.text_area("Prompt", placeholder="Describe what you want…",
                          height=120, key="prompt_ta")
    system_prompt = ""
    if task_type == "T2T":
        system_prompt = st.text_input("System prompt (optional)", key="sys_prompt")

    image_path_input = None
    video_path_input = None
    if task_type == "I2V":
        uploaded = st.file_uploader("Source image", type=["jpg","jpeg","png","webp"],
                                    key="i2v_up")
        if uploaded:
            tmp = Path("/tmp") / uploaded.name
            tmp.write_bytes(uploaded.read())
            image_path_input = str(tmp)

    if task_type == "V2V":
        uploaded = st.file_uploader("Source video", type=["mp4","mov"], key="v2v_up")
        if uploaded:
            tmp = Path("/tmp") / uploaded.name
            tmp.write_bytes(uploaded.read())
            video_path_input = str(tmp)

    if st.button("🚀 Generate", type="primary", use_container_width=True,
                 key="gen_btn"):
        if not api_key:
            st.warning("⚠️ Please fill in the API Key.")
            st.stop()
        if not prompt:
            st.warning("⚠️ Please enter a prompt.")
            st.stop()

        with st.spinner("Generating… please wait"):
            result = run_openlens_task(
                url=base_url, api_key=api_key, model_id=model_id,
                prompt=prompt, task_type=task_type,
                video_specs={"resolution": resolution, "duration": duration,
                             "fps": fps, "steps": steps},
                image_path=image_path_input,
                video_path=video_path_input,
                system_prompt=system_prompt,
                outputs_dir=out_dir,
            )

        if result["success"]:
            st.success("✅ Generation complete!")
            if task_type == "T2T":
                st.write(result.get("text", ""))
            elif task_type == "T2I":
                local = Path(result["local_path"])
                st.image(str(local), use_container_width=True)
                st.download_button("⬇️ Download Image", local.read_bytes(),
                                   file_name=local.name, mime="image/png",
                                   key="dl_img")
                st.code(result["local_path"], language=None)
            else:
                local = Path(result["local_path"])
                st.video(str(local))
                st.download_button("⬇️ Download Video", local.read_bytes(),
                                   file_name=local.name, mime="video/mp4",
                                   key="dl_vid")
                st.code(result["local_path"], language=None)
        else:
            st.error(f"❌ {result.get('error')}")
            if "api_response" in result:
                st.json(result["api_response"])


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Detect whether we are inside a Streamlit runtime
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            _launch_gui()
        else:
            # Plain Python execution: show quick CLI demo
            import argparse
            parser = argparse.ArgumentParser(description="OpenLens-Skill CLI")
            parser.add_argument("--url",      required=True)
            parser.add_argument("--api-key",  required=True)
            parser.add_argument("--model",    required=True)
            parser.add_argument("--prompt",   required=True)
            parser.add_argument("--task",     default="T2V",
                                choices=list(SUPPORTED_TASKS))
            parser.add_argument("--resolution", default="16:9")
            parser.add_argument("--duration",   type=int, default=10)
            parser.add_argument("--fps",        type=int, default=24)
            parser.add_argument("--image",      default=None)
            parser.add_argument("--video",      default=None)
            parser.add_argument("--out-dir",    default=None)
            args = parser.parse_args()

            result = run_openlens_task(
                url=args.url,
                api_key=args.api_key,
                model_id=args.model,
                prompt=args.prompt,
                task_type=args.task,
                video_specs={"resolution": args.resolution,
                             "duration": args.duration, "fps": args.fps},
                image_path=args.image,
                video_path=args.video,
                outputs_dir=args.out_dir,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except ImportError:
        print("Streamlit not installed. Install with:  pip install streamlit")
        sys.exit(1)
