"""Public Lux3D API client.

The client accepts accessible HTTP(S) URLs. Upload local files with the Asset
upload API before calling a Lux3D task endpoint.
"""

import argparse
import json
import os
import pathlib
import math
import struct
import tempfile
import zipfile
import sys
import time
import urllib.parse

import requests


CN_BASE_URL = "https://api.aholo3d.cn"
INTERNATIONAL_BASE_URL = "https://api.aholo.ai/global"
REGION_BASE_URLS = {
    "cn": CN_BASE_URL,
    "international": INTERNATIONAL_BASE_URL,
}
ASSET_UPLOAD_DOCS = {
    "cn": "https://labs.aholo3d.cn/api-docs/api-reference#tag/asset",
    "international": "https://labs.aholo.ai/api-docs/en/api-reference#tag/asset",
}

DEFAULT_REGION = "international"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2
DEFAULT_POLL_ATTEMPTS = 60
DEFAULT_POLL_INTERVAL = 15
DOWNLOAD_CHUNK_SIZE = 1024 * 1024

SUPPORTED_STYLES = {
    "photorealistic",
    "cartoon",
    "anime",
    "hand_painted",
    "cyberpunk",
    "fantasy",
    "glass",
}
GENERATION_VERSIONS = {"G1", "G1-Turbo"}
MATERIAL_VERSION = "v3.0-standard"
GENERATION_FORMATS = {"zip", "glb", "ply"}
MATERIAL_FORMATS = {"zip", "glb", "usdz", "obj_zip", "fbx_zip"}
EXPORT_FORMATS = {"usdz", "obj_zip", "fbx_zip", "stl", "3mf"}
DOWNLOAD_FORMATS = GENERATION_FORMATS | MATERIAL_FORMATS | EXPORT_FORMATS | {"obj"}
ANIMATION_FORMATS = {"glb", "fbx"}
ANIMATION_OUTPUT_MODES = {"separate", "combined"}
with pathlib.Path(__file__).with_name("animation_ids.json").open(encoding="utf-8") as animation_catalog:
    ANIMATION_IDS = tuple(json.load(animation_catalog))
SUPPORTED_TASK_STATUSES = {0, 1, 3, 4, 6}
FACE_COUNT_MIN = 10000
FACE_COUNT_MAX = 300000


def get_api_key():
    """Read the API key from the environment."""
    return os.environ.get("LUX3D_API_KEY", "").strip()


def validate_api_key():
    """Return the configured API key or raise a useful error."""
    api_key = get_api_key()
    if not api_key or api_key in {"your_lux3d_api_key", "your_api_key"}:
        raise ValueError(
            "API key not configured. Set LUX3D_API_KEY to a Lux3D API key."
        )
    return api_key


def normalize_region(region=None):
    """Normalize supported region aliases and reject unknown values."""
    value = region
    if value is None:
        value = os.environ.get("LUX3D_REGION", DEFAULT_REGION)
    value = str(value).strip().lower()
    aliases = {
        "cn": "cn",
        "china": "cn",
        "domestic": "cn",
        "international": "international",
        "global": "international",
        "intl": "international",
    }
    if value not in aliases:
        raise ValueError("region must be 'cn' or 'international'")
    return aliases[value]


def get_base_url(region=None):
    """Return the configured Lux3D API root."""
    configured = os.environ.get("LUX3D_BASE_URL", "").strip()
    if configured:
        return normalize_base_url(configured, region)
    return REGION_BASE_URLS[normalize_region(region)]


def normalize_base_url(base_url=None, region=None):
    """Normalize a custom base URL to the documented Lux3D API root."""
    if not base_url:
        base_url = os.environ.get("LUX3D_BASE_URL", "").strip()
        if not base_url:
            return REGION_BASE_URLS[normalize_region(region)]
    normalized = str(base_url).strip().rstrip("/")
    if normalized == "https://api.aholo3d.com":
        return normalized + "/global"
    if normalized == "https://api.aholo.ai":
        return INTERNATIONAL_BASE_URL
    if normalized == CN_BASE_URL:
        return CN_BASE_URL
    return normalized


def get_asset_upload_docs(region=None):
    """Return the Asset upload documentation for a region."""
    return ASSET_UPLOAD_DOCS[normalize_region(region)]


def validate_http_url(value, field_name, region=None):
    """Validate a public HTTP(S) URL used by an API file field."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty HTTP(S) URL")
    normalized = value.strip()
    parsed = urllib.parse.urlparse(normalized)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        docs = get_asset_upload_docs(region)
        raise ValueError(
            f"{field_name} must be an accessible HTTP(S) URL. "
            f"Upload local files first: {docs}"
        )
    return normalized


def validate_url_suffix(value, field_name, suffixes, region=None):
    """Validate a URL and its decoded path suffix."""
    normalized = validate_http_url(value, field_name, region)
    path = urllib.parse.unquote(urllib.parse.urlparse(normalized).path).lower()
    if not any(path.endswith(suffix) for suffix in suffixes):
        expected = " or ".join(suffixes)
        raise ValueError(f"{field_name} URL path must end with {expected}")
    return normalized


def validate_output_path(output_path):
    """Validate that an output path can be written."""
    output_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    if not os.path.isdir(output_dir):
        raise ValueError(f"Output directory does not exist: {output_dir}")


def validate_prompt(prompt):
    """Validate a text-to-3D prompt."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be non-empty text")
    return prompt.strip()


def validate_style(style):
    """Validate an optional text-to-3D style."""
    if style is None:
        return None
    if style not in SUPPORTED_STYLES:
        supported = ", ".join(sorted(SUPPORTED_STYLES))
        raise ValueError(f"Unsupported style '{style}'. Supported styles: {supported}")
    return style


def validate_boolean(value, name):
    """Validate an optional boolean field."""
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean")
    return value


def validate_version(version):
    """Validate the required image/text generation version."""
    if version not in GENERATION_VERSIONS:
        raise ValueError("version is required and must be 'G1' or 'G1-Turbo'")
    return version


def validate_material_version(version):
    """Validate the required material-transfer version."""
    if version != MATERIAL_VERSION:
        raise ValueError(f"version is required and must be '{MATERIAL_VERSION}'")
    return version


def validate_face_count(faceCount):
    """Validate the target Mesh face count."""
    if faceCount is None:
        return None
    if not isinstance(faceCount, int) or isinstance(faceCount, bool):
        raise ValueError("faceCount must be an integer")
    if not FACE_COUNT_MIN <= faceCount <= FACE_COUNT_MAX:
        raise ValueError(
            f"faceCount must be in [{FACE_COUNT_MIN}, {FACE_COUNT_MAX}]"
        )
    return faceCount


def normalize_output_formats(outputFormat):
    """Normalize outputFormat while preserving order and rejecting duplicates."""
    if outputFormat is None:
        return None
    if isinstance(outputFormat, str):
        formats = [outputFormat]
    elif isinstance(outputFormat, (list, tuple)):
        formats = list(outputFormat)
    else:
        raise ValueError("outputFormat must be a string or an ordered list of strings")
    if any(not isinstance(item, str) for item in formats):
        raise ValueError("outputFormat values must be strings")
    if len(formats) != len(set(formats)):
        raise ValueError("outputFormat must not contain duplicate values")
    return formats


def validate_allowed_formats(outputFormat, allowed, label):
    """Validate outputFormat against one endpoint's public values."""
    formats = normalize_output_formats(outputFormat)
    invalid = [item for item in formats or [] if item not in allowed]
    if invalid:
        supported = ", ".join(sorted(allowed))
        raise ValueError(f"{label} supports only: {supported}")
    return formats


def validate_generation_options(
    version, outputFormat=None, enablePbr=None, customSize=None
):
    """Validate version-specific image/text generation fields."""
    version = validate_version(version)
    formats = validate_allowed_formats(
        outputFormat, GENERATION_FORMATS, f"{version} generation"
    )
    validate_boolean(enablePbr, "enablePbr")
    validate_custom_size(customSize)
    if version == "G1" and enablePbr is not None:
        raise ValueError("enablePbr is not a G1 field; omit it for G1")
    if version == "G1-Turbo" and customSize is not None:
        raise ValueError("customSize is not a G1-Turbo field; omit it for G1-Turbo")
    if (
        version == "G1-Turbo"
        and formats == ["ply"]
        and enablePbr is not None
    ):
        raise ValueError("enablePbr must be omitted for a G1-Turbo PLY-only request")
    return formats


def validate_custom_size(customSize):
    """Validate a model height in millimetres."""
    if customSize is None:
        return None
    if isinstance(customSize, bool) or not isinstance(customSize, (int, float)):
        raise ValueError("customSize must be a number greater than 0")
    if customSize <= 0:
        raise ValueError("customSize must be a number greater than 0")
    return customSize


def validate_material_options(
    version, outputFormat=None, aiPredictSize=None, customSize=None
):
    """Validate material-transfer fields for v3.0-standard."""
    validate_material_version(version)
    formats = validate_allowed_formats(
        outputFormat, MATERIAL_FORMATS, "Material transfer"
    )
    validate_boolean(aiPredictSize, "aiPredictSize")
    validate_custom_size(customSize)
    if aiPredictSize is True and customSize is not None:
        raise ValueError("customSize must be omitted when aiPredictSize is true")
    return formats


def validate_export_options(modelUrl, outputFormat=None, region=None):
    """Validate multi-format export input and requested formats."""
    model_url = validate_url_suffix(
        modelUrl, "modelUrl", (".zip", ".glb"), region
    )
    formats = validate_allowed_formats(
        outputFormat, EXPORT_FORMATS, "Multi-format export"
    )
    path = urllib.parse.unquote(urllib.parse.urlparse(model_url).path).lower()
    if path.endswith(".glb") and not formats:
        raise ValueError(
            "outputFormat is required for GLB input and must include at least "
            "one of: usdz, obj_zip, fbx_zip, stl, 3mf"
        )
    return model_url, formats


def add_optional(payload, name, value):
    """Add a field only when the caller supplied it."""
    if value is not None:
        payload[name] = value


def build_multimodal_payload(img=None, prompt=None, region=None):
    """Build a request that requires at least one image or text input."""
    if img is None and prompt is None:
        raise ValueError("Pass at least one of img or prompt")
    payload = {}
    if img is not None:
        payload["img"] = validate_http_url(img, "img", region)
    if prompt is not None:
        payload["prompt"] = validate_prompt(prompt)
    return payload


def validate_digital_human_model_url(value, field_name, region=None):
    """Validate the digital-human endpoint's public HTTPS GLB input."""
    model_url = validate_url_suffix(value, field_name, (".glb",), region)
    parsed = urllib.parse.urlsplit(model_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username is not None or parsed.password is not None or parsed.fragment:
        raise ValueError(f"{field_name} must be a public HTTPS GLB URL without credentials or a fragment")
    return model_url


def build_auto_rig_payload(modelUrl, *, region=None):
    """Build the exact body used for auto-rig quotation and creation."""
    model_url = validate_digital_human_model_url(modelUrl, "modelUrl", region)
    return {"modelUrl": model_url}


def validate_animation_ids(animationIds):
    if not isinstance(animationIds, (list, tuple)) or not 1 <= len(animationIds) <= 10:
        raise ValueError("animationIds must contain 1-10 distinct public animation IDs")
    if any(not isinstance(item, str) or not item.strip() or item != item.strip() or item not in ANIMATION_IDS for item in animationIds):
        raise ValueError("animationIds must use the exact public animation IDs")
    if len(set(animationIds)) != len(animationIds):
        raise ValueError("animationIds must not contain duplicates")
    return list(animationIds)


def build_animation_retarget_payload(
    rigModelUrl,
    animationIds,
    *,
    animationOutputMode=None,
    outFormat=None,
    animateInPlace=None,
    region=None,
):
    """Build one normalized call, independent of quote correlation metadata."""
    model_url = validate_digital_human_model_url(rigModelUrl, "rigModelUrl", region)
    animationIds = validate_animation_ids(animationIds)
    mode = "separate" if animationOutputMode is None else animationOutputMode
    output_format = "glb" if outFormat is None else outFormat
    if not isinstance(mode, str) or not isinstance(output_format, str) or mode not in ANIMATION_OUTPUT_MODES or output_format not in ANIMATION_FORMATS:
        raise ValueError("animationOutputMode must be separate/combined and outFormat must be glb/fbx")
    in_place = False if animateInPlace is None else validate_boolean(animateInPlace, "animateInPlace")
    return {"rigModelUrl": model_url, "animationIds": list(animationIds), "animationOutputMode": mode, "outFormat": output_format, "animateInPlace": in_place}


def generation_result_formats(version, outputFormat=None):
    """Return the documented output order for a generation request."""
    formats = normalize_output_formats(outputFormat)
    if version == "G1":
        result = ["zip", "glb"]
        if formats and "ply" in formats:
            result.append("ply")
        return result
    return formats or ["zip"]


def material_result_formats(outputFormat=None):
    """Return the documented material-transfer output order."""
    formats = normalize_output_formats(outputFormat) or []
    return ["zip", "glb"] + [
        item for item in ("usdz", "obj_zip", "fbx_zip") if item in formats
    ]


def export_result_formats(modelUrl, outputFormat=None):
    """Return expected output formats for a multi-format export request."""
    formats = normalize_output_formats(outputFormat) or []
    result = [
        item
        for item in ("usdz", "obj_zip", "fbx_zip", "stl", "3mf")
        if item in formats
    ]
    path = urllib.parse.unquote(urllib.parse.urlparse(modelUrl).path).lower()
    if path.endswith(".zip"):
        result.insert(0, "glb")
    return result


def output_extension(output_format):
    """Return the file extension for a public output format."""
    if output_format in {"obj_zip", "fbx_zip", "zip"}:
        return "zip"
    return output_format


def get_auth_headers():
    """Build the Lux3D authentication headers."""
    return {
        "Content-Type": "application/json",
        "Authorization": validate_api_key(),
    }


def secure_request(
    method,
    url,
    headers=None,
    data=None,
    timeout=None,
    retries=None,
    stream=False,
):
    """Perform an HTTP request with bounded retries."""
    method = method.upper()
    request_headers = {"Content-Type": "application/json"} if headers is None else headers
    timeout = REQUEST_TIMEOUT if timeout is None else timeout
    retries = (1 if method == "POST" else MAX_RETRIES) if retries is None else retries
    if not isinstance(retries, int) or isinstance(retries, bool) or retries < 1:
        raise ValueError("retries must be a positive integer")
    last_error = None
    for attempt in range(retries):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=request_headers,
                json=data,
                timeout=timeout,
                stream=stream,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            last_error = f"Request timeout (attempt {attempt + 1}/{retries})"
        except requests.exceptions.RequestException as exc:
            last_error = f"Request failed: {exc}"
        if attempt < retries - 1:
            time.sleep(RETRY_DELAY)
    raise RuntimeError(f"Request failed after {retries} attempts: {last_error}")


def ensure_success(result):
    """Validate create, query, and list response envelopes."""
    code = result.get("c")
    if code not in (None, "", 0, "0"):
        message = result.get("m") or "unknown error"
        raise RuntimeError(f"API error: {message} (code={code})")
    return result


def submit_task(path, payload, base_url=None, region=None):
    """Submit an asynchronous task and return its task ID."""
    url = normalize_base_url(base_url, region) + path
    response = secure_request(
        "POST", url, headers=get_auth_headers(), data=payload
    )
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Invalid JSON response: {response.text}") from exc
    ensure_success(result)
    task_id = result.get("d")
    if task_id in (None, ""):
        raise RuntimeError(f"Missing task ID in response: {result}")
    return str(task_id)


def create_image_to_3d_task(
    img=None,
    *,
    imgs=None,
    version,
    faceCount=None,
    outputFormat=None,
    enablePbr=None,
    aiPredictSize=None,
    customSize=None,
    base_url=None,
    region=None,
):
    """Create an image-to-3D task from one URL or 1-32 URL inputs."""
    if (img is None) == (imgs is None):
        raise ValueError("Pass exactly one of img or imgs")
    payload = {}
    if img is not None:
        payload["img"] = validate_http_url(img, "img", region)
    else:
        if not isinstance(imgs, (list, tuple)):
            raise ValueError("imgs must be an ordered list of 1-32 image URLs")
        if not 1 <= len(imgs) <= 32:
            raise ValueError("imgs must contain 1-32 image URLs")
        payload["imgs"] = [
            validate_http_url(item, f"imgs[{index}]", region)
            for index, item in enumerate(imgs)
        ]

    payload["version"] = validate_version(version)
    formats = validate_generation_options(
        version, outputFormat, enablePbr, customSize
    )
    add_optional(payload, "faceCount", validate_face_count(faceCount))
    if outputFormat is not None:
        payload["outputFormat"] = formats
    add_optional(payload, "enablePbr", enablePbr)
    add_optional(
        payload, "aiPredictSize", validate_boolean(aiPredictSize, "aiPredictSize")
    )
    add_optional(payload, "customSize", validate_custom_size(customSize))
    return submit_task(
        "/lux3d/v1/generate/img-to-3d/task/create",
        payload,
        base_url=base_url,
        region=region,
    )


def create_task(img=None, **kwargs):
    """Backward-compatible name for create_image_to_3d_task."""
    return create_image_to_3d_task(img, **kwargs)


def create_text_to_3d_task(
    prompt,
    *,
    version,
    style=None,
    img=None,
    faceCount=None,
    outputFormat=None,
    enablePbr=None,
    aiPredictSize=None,
    customSize=None,
    base_url=None,
    region=None,
):
    """Create a text-to-3D task with one optional reference-image URL."""
    payload = {
        "prompt": validate_prompt(prompt),
        "version": validate_version(version),
    }
    add_optional(payload, "style", validate_style(style))
    if img is not None:
        payload["img"] = validate_http_url(img, "img", region)
    formats = validate_generation_options(
        version, outputFormat, enablePbr, customSize
    )
    add_optional(payload, "faceCount", validate_face_count(faceCount))
    if outputFormat is not None:
        payload["outputFormat"] = formats
    add_optional(payload, "enablePbr", enablePbr)
    add_optional(
        payload, "aiPredictSize", validate_boolean(aiPredictSize, "aiPredictSize")
    )
    add_optional(payload, "customSize", validate_custom_size(customSize))
    return submit_task(
        "/lux3d/v1/generate/text-to-3d/task/create",
        payload,
        base_url=base_url,
        region=region,
    )


def create_material_transfer_task(
    img,
    meshUrl,
    *,
    version,
    outputFormat=None,
    aiPredictSize=None,
    customSize=None,
    base_url=None,
    region=None,
):
    """Create a v3.0-standard material-transfer task."""
    formats = validate_material_options(
        version, outputFormat, aiPredictSize, customSize
    )
    payload = {
        "img": validate_http_url(img, "img", region),
        "meshUrl": validate_http_url(meshUrl, "meshUrl", region),
        "version": validate_material_version(version),
    }
    if outputFormat is not None:
        payload["outputFormat"] = formats
    add_optional(
        payload, "aiPredictSize", validate_boolean(aiPredictSize, "aiPredictSize")
    )
    add_optional(payload, "customSize", validate_custom_size(customSize))
    return submit_task(
        "/lux3d/v1/generate/material-transfer/task/create",
        payload,
        base_url=base_url,
        region=region,
    )


def create_multimodal_to_image_task(
    img=None, *, prompt=None, base_url=None, region=None
):
    """Create one image from an image URL, text, or both."""
    payload = build_multimodal_payload(img, prompt, region)
    return submit_task(
        "/lux3d/v1/generate/multimodal-to-image/task/create",
        payload,
        base_url=base_url,
        region=region,
    )


def create_image_to_four_view_task(
    img=None, *, prompt=None, base_url=None, region=None
):
    """Create a four-view task from an image URL, text, or both."""
    payload = build_multimodal_payload(img, prompt, region)
    return submit_task(
        "/lux3d/v1/generate/image-to-four-view/task/create",
        payload,
        base_url=base_url,
        region=region,
    )


def create_part_split_task(
    glbUrl,
    *,
    base_url=None,
    region=None,
):
    """Create a part-splitting task for an accessible GLB URL."""
    payload = {"glbUrl": validate_http_url(glbUrl, "glbUrl", region)}
    return submit_task(
        "/lux3d/v1/part-split/task/create",
        payload,
        base_url=base_url,
        region=region,
    )


def create_articulation_animation_task(
    glbUrl, prompt, *, base_url=None, region=None,
):
    """Create model articulation using a GLB URL and a joint-motion prompt."""
    payload = {
        "glbUrl": validate_http_url(glbUrl, "glbUrl", region),
        "prompt": validate_prompt(prompt),
    }
    return submit_task(
        "/lux3d/v1/articulation-animation/task/create",
        payload, base_url=base_url, region=region,
    )


def create_multi_format_export_task(
    modelUrl,
    *,
    outputFormat=None,
    base_url=None,
    region=None,
):
    """Create a multi-format export task for a Lux3D ZIP or GLB URL."""
    model_url, formats = validate_export_options(
        modelUrl, outputFormat, region
    )
    payload = {"modelUrl": model_url}
    if outputFormat is not None:
        payload["outputFormat"] = formats
    return submit_task(
        "/lux3d/v1/multi-format-export/task/create",
        payload,
        base_url=base_url,
        region=region,
    )


def create_auto_rig_task(modelUrl, *, base_url=None, region=None, content_id=None):
    """Create one auto-rig task and return its ID before polling."""
    payload = build_auto_rig_payload(modelUrl, region=region)
    add_optional(payload, "contentId", content_id)
    return submit_task(
        "/lux3d/v1/animations/rig/task/create", payload,
        base_url=base_url, region=region,
    )


def create_animation_retarget_task(
    rigModelUrl, animationIds, *, animationOutputMode=None, outFormat=None,
    animateInPlace=None, base_url=None, region=None, content_id=None,
):
    """Create one animation task and return its ID before polling."""
    payload = build_animation_retarget_payload(
        rigModelUrl, animationIds, animationOutputMode=animationOutputMode,
        outFormat=outFormat, animateInPlace=animateInPlace, region=region,
    )
    add_optional(payload, "contentId", content_id)
    return submit_task(
        "/lux3d/v1/animations/retarget/task/create", payload,
        base_url=base_url, region=region,
    )


def get_task(task_id, base_url=None, region=None):
    """Query one Lux3D task once and return the public task object."""
    if task_id in (None, ""):
        raise ValueError("task_id is required")
    url = (
        normalize_base_url(base_url, region)
        + "/lux3d/v1/generate/task/get?taskid="
        + urllib.parse.quote(str(task_id))
    )
    response = secure_request("GET", url, headers=get_auth_headers())
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Invalid JSON response: {response.text}") from exc
    ensure_success(result)
    task_data = result.get("d")
    if not isinstance(task_data, dict):
        raise RuntimeError(f"Missing task data in response: {result}")
    return task_data


def infer_artifact_format(url):
    """Infer a public artifact format from a result URL when possible."""
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path).lower()
    filename = path.rsplit("/", 1)[-1]
    if filename.endswith(("_obj.zip", ".obj.zip", "obj.zip")):
        return "obj_zip"
    if filename.endswith(("_fbx.zip", ".fbx.zip", "fbx.zip")):
        return "fbx_zip"
    if filename.endswith(".usdz"):
        return "usdz"
    if filename.endswith(".stl"):
        return "stl"
    if filename.endswith(".3mf"):
        return "3mf"
    if filename.endswith(".glb"):
        return "glb"
    if filename.endswith(".ply"):
        return "ply"
    if filename.endswith(".zip"):
        return "zip"
    return None


def parse_part_split_output(task_data):
    """Return the only final reconstructed GLB from a part-splitting task."""
    outputs = task_data.get("outputs") or []
    if len(outputs) != 1 or not isinstance(outputs[0], dict):
        raise RuntimeError(
            "Part-splitting task must return exactly one final GLB output"
        )
    content = outputs[0].get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("Part-splitting task returned no final GLB URL")
    url = validate_http_url(content.strip(), "partSplit.glb")
    if infer_artifact_format(url) != "glb":
        raise RuntimeError("Part-splitting task output must be a GLB URL")
    return url


def parse_articulation_animation_output(task_data):
    """Read the final artifact URL without assuming a ZIP or GLB format."""
    outputs = task_data.get("outputs") or []
    if len(outputs) != 1 or not isinstance(outputs[0], dict):
        raise RuntimeError("Articulation task must return one final artifact URL")
    return validate_http_url(outputs[0].get("content"), "articulation result")


def parse_task_outputs(task_data):
    """Parse result URLs without discarding their documented order."""
    contents = []
    for output in task_data.get("outputs") or []:
        if not isinstance(output, dict):
            continue
        content = output.get("content")
        if isinstance(content, str):
            content = content.strip()
        if content is None:
            continue
        if isinstance(content, str):
            if not content or content.lower() in {"not_requested", "null"}:
                continue
        contents.append(content)
    if not contents:
        raise RuntimeError(f"Task succeeded without output content: {task_data}")

    if len(contents) == 1 and isinstance(contents[0], str):
        try:
            view_urls = json.loads(contents[0])
        except (TypeError, ValueError):
            view_urls = None
        if isinstance(view_urls, dict) and ("actions" in view_urls or "error" in view_urls):
            return view_urls
        if (
            isinstance(view_urls, list)
            and len(view_urls) == 4
            and all(isinstance(item, str) for item in view_urls)
        ):
            return [
                validate_http_url(item, f"fourView[{index}]")
                for index, item in enumerate(view_urls)
            ]
    artifacts = {}
    for content in contents:
        if not isinstance(content, str):
            break
        output_format = infer_artifact_format(content)
        if output_format is None or output_format in artifacts:
            break
        artifacts[output_format] = content
    else:
        return artifacts
    return contents[0] if len(contents) == 1 else contents


def validate_animation_results(outputs, animationIds, *, outFormat="glb", animationOutputMode="separate"):
    """Validate every action against the accepted request without guessing file order."""
    if not isinstance(outputs, dict) or not isinstance(outputs.get("actions"), list):
        raise ValueError("Animation output must contain an actions array")
    actions = outputs["actions"]
    if len(actions) != len(animationIds):
        raise ValueError("Animation output is missing or has extra requested actions")
    url_key = {"glb": "animationGlbUrl", "fbx": "fbxUrl"}.get(outFormat)
    if url_key is None or animationOutputMode not in ANIMATION_OUTPUT_MODES:
        raise ValueError("Accepted animation format or output mode is invalid")
    results = {}
    for action in actions:
        if not isinstance(action, dict):
            raise ValueError("Animation action must be an object")
        action_id = action.get("animation_id")
        if not isinstance(action_id, str) or action_id not in animationIds or action_id in results:
            raise ValueError("Animation output has an unknown or duplicate action")
        status = action.get("status")
        result = {"animation_id": action_id, "status": status}
        if status == "success":
            other_key = "fbxUrl" if outFormat == "glb" else "animationGlbUrl"
            if action.get(other_key) is not None:
                raise ValueError("Animation success has a result in the wrong requested format")
            result[url_key] = validate_http_url(action.get(url_key), url_key)
        elif status == "failed":
            error = action.get("error")
            if not isinstance(error, dict) or any(not isinstance(error.get(key), str) or not error[key].strip() for key in ("code", "message")):
                raise ValueError("Failed animation must have an error code and message")
            result["error"] = {"code": error["code"], "message": error["message"]}
        else:
            raise ValueError("Animation action must have terminal success or failed status")
        results[action_id] = result
    urls = [action[url_key] for action in results.values() if action["status"] == "success"]
    if animationOutputMode == "combined" and len(set(urls)) > 1:
        raise ValueError("Combined actions must reference the same returned file")
    if animationOutputMode == "separate" and len(set(urls)) != len(urls):
        raise ValueError("Separate actions must reference independent returned files")
    return [results[action_id] for action_id in animationIds]


def query_task_status(
    task_id,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
    output_parser=None,
):
    """Poll a task until it succeeds, fails, or is cancelled."""
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    if not isinstance(interval, (int, float)) or interval < 0:
        raise ValueError("interval must be a non-negative number")
    for attempt in range(max_attempts):
        task_data = get_task(task_id, base_url=base_url, region=region)
        status = task_data.get("status")
        if status == 3:
            if output_parser is not None:
                return output_parser(task_data)
            return parse_task_outputs(task_data)
        if status in {4, 5}:
            raise RuntimeError(f"Task failed: {task_data}")
        if status == 6:
            raise RuntimeError(f"Task was cancelled: {task_data}")
        if status not in {0, 1, 2}:
            raise RuntimeError(f"Unknown task status: {status}")
        if attempt < max_attempts - 1:
            time.sleep(interval)
    raise TimeoutError("Task did not finish before the polling limit")


def list_tasks(
    page=1,
    pagesize=20,
    status=None,
    starttime=None,
    endtime=None,
    base_url=None,
    region=None,
):
    """List tasks for the current API-key account."""
    if not isinstance(page, int) or isinstance(page, bool) or page < 1:
        raise ValueError("page must be a positive integer")
    if (
        not isinstance(pagesize, int)
        or isinstance(pagesize, bool)
        or not 1 <= pagesize <= 100
    ):
        raise ValueError("pagesize must be an integer between 1 and 100")
    if (
        status is not None
        and (
            not isinstance(status, int)
            or isinstance(status, bool)
            or status not in SUPPORTED_TASK_STATUSES
        )
    ):
        raise ValueError("status must be one of 0, 1, 3, 4, or 6")
    for name, value in (("starttime", starttime), ("endtime", endtime)):
        if (
            value is not None
            and (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value < 0
            )
        ):
            raise ValueError(
                f"{name} must be a non-negative Unix timestamp in milliseconds"
            )
    if starttime is not None and endtime is not None and starttime >= endtime:
        raise ValueError("starttime must be earlier than endtime")

    params = {"page": page, "pagesize": pagesize}
    for name, value in (
        ("status", status),
        ("starttime", starttime),
        ("endtime", endtime),
    ):
        if value is not None:
            params[name] = value
    url = (
        normalize_base_url(base_url, region)
        + "/lux3d/v1/generate/task/list?"
        + urllib.parse.urlencode(params)
    )
    response = secure_request("GET", url, headers=get_auth_headers())
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Invalid JSON response: {response.text}") from exc
    ensure_success(result)
    return result.get("d") or {
        "items": [],
        "total": 0,
        "page": page,
        "pageSize": pagesize,
    }


def download_model(model_url, output_path):
    """Download atomically, retaining an existing file if transfer fails."""
    model_url = validate_http_url(model_url, "model_url")
    validate_output_path(output_path)
    response = secure_request("GET", model_url, headers={}, stream=True)
    total_size = 0
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=os.path.dirname(os.path.abspath(output_path)), prefix=".lux3d-", delete=False,
        ) as file_obj:
            temporary = file_obj.name
            for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                if chunk:
                    file_obj.write(chunk)
                    total_size += len(chunk)
        if total_size <= 0:
            raise ValueError("Downloaded artifact is empty")
        os.replace(temporary, output_path)
        return total_size
    finally:
        response.close()
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)


def map_artifact_urls(outputs, expected_formats):
    """Map ordered or named task outputs to expected formats."""
    if isinstance(outputs, dict):
        missing = [item for item in expected_formats if item not in outputs]
        if missing:
            raise ValueError(
                "Missing expected result formats: " + ", ".join(missing)
            )
        return {item: outputs[item] for item in expected_formats}
    if isinstance(outputs, str) and len(expected_formats) == 1:
        return {expected_formats[0]: outputs}
    if (
        isinstance(outputs, list)
        and len(outputs) == len(expected_formats)
        and all(isinstance(item, str) for item in outputs)
    ):
        return dict(zip(expected_formats, outputs))
    raise ValueError("Task outputs do not match the expected result formats")


def download_requested_models(outputs, output_path, expected_formats):
    """Download all expected model artifacts in documented output order."""
    artifact_urls = map_artifact_urls(outputs, expected_formats)
    if len(expected_formats) == 1:
        output_format = expected_formats[0]
        path = output_path
        if not os.path.splitext(path)[1]:
            path = f"{path}.{output_extension(output_format)}"
        return [(path, download_model(artifact_urls[output_format], path))]

    output_base, _ = os.path.splitext(output_path)
    downloads = []
    for output_format in expected_formats:
        path = f"{output_base}_{output_format}.{output_extension(output_format)}"
        size = download_model(artifact_urls[output_format], path)
        downloads.append((path, size))
    return downloads


def complete_task(
    task_id,
    *,
    output_path=None,
    expected_formats=None,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
    output_parser=None,
):
    """Wait for a task, optionally downloading all expected artifacts."""
    outputs = query_task_status(
        task_id,
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
        output_parser=output_parser,
    )
    if output_path is None:
        return outputs
    if not expected_formats:
        raise ValueError("expected_formats are required when downloading results")
    return download_requested_models(outputs, output_path, expected_formats)


def generate_3d_model(
    img=None,
    output_path=None,
    *,
    imgs=None,
    version,
    faceCount=None,
    outputFormat=None,
    enablePbr=None,
    aiPredictSize=None,
    customSize=None,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the image-to-3D create, poll, and optional download workflow."""
    task_id = create_image_to_3d_task(
        img,
        imgs=imgs,
        version=version,
        faceCount=faceCount,
        outputFormat=outputFormat,
        enablePbr=enablePbr,
        aiPredictSize=aiPredictSize,
        customSize=customSize,
        base_url=base_url,
        region=region,
    )
    return complete_task(
        task_id,
        output_path=output_path,
        expected_formats=generation_result_formats(version, outputFormat),
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )


def generate_text_to_3d(
    prompt,
    output_path=None,
    *,
    version,
    style=None,
    img=None,
    faceCount=None,
    outputFormat=None,
    enablePbr=None,
    aiPredictSize=None,
    customSize=None,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the text-to-3D create, poll, and optional download workflow."""
    task_id = create_text_to_3d_task(
        prompt,
        version=version,
        style=style,
        img=img,
        faceCount=faceCount,
        outputFormat=outputFormat,
        enablePbr=enablePbr,
        aiPredictSize=aiPredictSize,
        customSize=customSize,
        base_url=base_url,
        region=region,
    )
    return complete_task(
        task_id,
        output_path=output_path,
        expected_formats=generation_result_formats(version, outputFormat),
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )


def generate_material_transfer(
    img,
    meshUrl,
    output_path=None,
    *,
    version,
    outputFormat=None,
    aiPredictSize=None,
    customSize=None,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the material-transfer create, poll, and optional download workflow."""
    task_id = create_material_transfer_task(
        img,
        meshUrl,
        version=version,
        outputFormat=outputFormat,
        aiPredictSize=aiPredictSize,
        customSize=customSize,
        base_url=base_url,
        region=region,
    )
    return complete_task(
        task_id,
        output_path=output_path,
        expected_formats=material_result_formats(outputFormat),
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )


def generate_multimodal_image(
    img=None,
    output_path=None,
    *,
    prompt=None,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the multimodal single-image create, poll, and optional download workflow."""
    task_id = create_multimodal_to_image_task(
        img, prompt=prompt, base_url=base_url, region=region
    )
    result = complete_task(
        task_id,
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )
    if not isinstance(result, str):
        raise RuntimeError("The multimodal image task did not return one image URL")
    image_url = validate_http_url(result, "image result", region)
    if output_path is None:
        return image_url
    return [(output_path, download_model(image_url, output_path))]


def generate_four_views(
    img=None,
    *,
    prompt=None,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the multimodal viewpoint-completion workflow and return four URLs."""
    task_id = create_image_to_four_view_task(
        img, prompt=prompt, base_url=base_url, region=region
    )
    result = complete_task(
        task_id,
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )
    if not (
        isinstance(result, list)
        and len(result) == 4
        and all(isinstance(item, str) for item in result)
    ):
        raise RuntimeError("The four-view task did not return four image URLs")
    return result


def generate_part_split(
    glbUrl,
    output_path=None,
    *,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run part splitting and return or download the final reconstructed GLB."""
    if output_path is not None:
        validate_output_path(output_path)
    task_id = create_part_split_task(
        glbUrl, base_url=base_url, region=region
    )
    return complete_task(
        task_id,
        output_path=output_path,
        expected_formats=["glb"] if output_path is not None else None,
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
        output_parser=parse_part_split_output,
    )



RETOPOLOGY_OUTPUT_SLOTS = ("glb", "obj", "obj_zip")


def build_mesh_retopology_payload(
    modelUrl, faceLimit, *, quad=True, bakeTextures=False, textureSize=2048,
    region=None,
):
    """Validate public retopology fields before any paid submission."""
    model_url = validate_url_suffix(modelUrl, "modelUrl", (".glb",), region)
    if not isinstance(quad, bool) or not isinstance(bakeTextures, bool):
        raise ValueError("quad and bakeTextures must be booleans")
    minimum, maximum = (1000, 500000) if quad else (2000, 1000000)
    if (isinstance(faceLimit, bool) or not isinstance(faceLimit, int)
            or not minimum <= faceLimit <= maximum):
        raise ValueError(f"faceLimit must be an integer between {minimum} and {maximum}")
    if (isinstance(textureSize, bool) or not isinstance(textureSize, int)
            or textureSize not in {512, 1024, 2048, 4096}):
        raise ValueError("textureSize must be one of 512, 1024, 2048 or 4096")
    return {"modelUrl": model_url, "faceLimit": faceLimit, "quad": quad,
            "bakeTextures": bakeTextures, "textureSize": textureSize}


def parse_mesh_retopology_output(task_data):
    """Preserve three provider slots, accepting only the documented empty ZIP."""
    outputs = task_data.get("outputs")
    if not isinstance(outputs, list) or len(outputs) != 3:
        raise RuntimeError("Retopology requires exactly three output slots")
    artifacts = {}
    for index, name in enumerate(RETOPOLOGY_OUTPUT_SLOTS):
        item = outputs[index]
        if not isinstance(item, dict) or not isinstance(item.get("content"), str):
            raise RuntimeError(f"Invalid retopology output slot: {name}")
        content = item["content"]
        if index == 2 and content == "":
            continue
        try:
            artifacts[name] = validate_http_url(content, name)
        except ValueError as exc:
            raise RuntimeError(f"Invalid retopology output URL: {name}") from exc
    return artifacts


def retopology_result(task_id, artifacts, bake_textures):
    return {
        "taskId": str(task_id), "artifacts": artifacts,
        "texturePackageAvailable": "obj_zip" in artifacts,
        "warnings": ["TEXTURE_PACKAGE_NOT_GENERATED"]
        if bake_textures and "obj_zip" not in artifacts else [],
    }


def create_mesh_retopology_task(
    modelUrl, faceLimit, *, quad=True, bakeTextures=False, textureSize=2048,
    base_url=None, region=None, content_id=None,
):
    payload = build_mesh_retopology_payload(
        modelUrl, faceLimit, quad=quad, bakeTextures=bakeTextures,
        textureSize=textureSize, region=region,
    )
    if content_id is not None:
        if not isinstance(content_id, str) or not content_id.strip() or len(content_id) > 255:
            raise ValueError("content_id must be a non-empty string of at most 255 characters")
        payload["contentId"] = content_id

    return submit_task(
        "/lux3d/v1/mesh-retopology/task/create", payload,
        base_url=base_url, region=region,
    )



def validate_retopology_download(file_path, kind):
    """Check downloaded model structure before replacing a previous result."""
    size = os.path.getsize(file_path)
    if size == 0:
        raise ValueError("Retopology artifact is empty")
    if kind == "glb":
        with open(file_path, "rb") as stream:
            header = stream.read(20)
            if (len(header) != 20 or header[:4] != b"glTF"
                    or struct.unpack_from("<I", header, 4)[0] != 2
                    or struct.unpack_from("<I", header, 8)[0] != size
                    or header[16:20] != b"JSON"):
                raise ValueError("Invalid retopology GLB")
            length = struct.unpack_from("<I", header, 12)[0]
            if length > size - 20:
                raise ValueError("Invalid GLB JSON chunk")
            document = json.loads(stream.read(length).decode("utf-8"))
            if not isinstance(document, dict) or not document.get("meshes"):
                raise ValueError("Retopology GLB has no meshes")
    elif kind == "obj":
        counts = [0, 0, 0]
        faces = 0
        with open(file_path, encoding="utf-8-sig") as stream:
            for line in stream:
                parts = line.split("#", 1)[0].split()
                if not parts:
                    continue
                if parts[0] in ("v", "vt", "vn"):
                    slot = ("v", "vt", "vn").index(parts[0])
                    minimum = 1 if slot == 1 else 3
                    if len(parts) <= minimum or not all(math.isfinite(float(v)) for v in parts[1:]):
                        raise ValueError("Invalid OBJ coordinate")
                    counts[slot] += 1
                elif parts[0] == "f":
                    if len(parts) < 4:
                        raise ValueError("Invalid OBJ face")
                    for token in parts[1:]:
                        refs = token.split("/")
                        if len(refs) > 3 or not refs[0]:
                            raise ValueError("Invalid OBJ face reference")
                        for slot, value in enumerate(refs):
                            if not value:
                                if slot == 1 and len(refs) == 3 and refs[2]:
                                    continue
                                raise ValueError("Empty OBJ face reference")
                            index = int(value)
                            if index == 0 or abs(index) > counts[slot]:
                                raise ValueError("OBJ face index out of bounds")
                    faces += 1
        if not counts[0] or not faces:
            raise ValueError("OBJ has no geometry")
    elif kind == "obj_zip":
        with zipfile.ZipFile(file_path) as archive:
            names = [n.lower() for n in archive.namelist()]
            if (archive.testzip() is not None or
                    not any(n.endswith(".obj") for n in names) or
                    not any(n.endswith(".mtl") for n in names) or
                    sum(n.endswith(".png") for n in names) < 3):
                raise ValueError("Invalid retopology OBJ texture package")
    return size


def download_retopology_artifacts(artifacts, output_path):
    """Keep prior downloads intact if a resumed transfer fails."""
    base, _ = os.path.splitext(os.fspath(output_path))
    downloads = []
    for kind in RETOPOLOGY_OUTPUT_SLOTS:
        if kind not in artifacts:
            continue
        target = f"{base}_{kind}.{output_extension(kind)}"
        directory = os.path.dirname(os.path.abspath(target))
        with tempfile.NamedTemporaryFile(dir=directory, prefix=".retopology-", delete=False) as stream:
            temporary = stream.name
        try:
            download_model(artifacts[kind], temporary)
            size = validate_retopology_download(temporary, kind)
            os.replace(temporary, target)
            downloads.append((target, size))
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return downloads


def resume_mesh_retopology(
    task_id, output_path=None, *, bakeTextures=False, base_url=None, region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS, interval=DEFAULT_POLL_INTERVAL,
):
    """Resume the original task; never create another task on query/download failure."""
    if not isinstance(bakeTextures, bool):
        raise ValueError("bakeTextures must be a boolean")
    artifacts = query_task_status(
        task_id, base_url=base_url, region=region, max_attempts=max_attempts,
        interval=interval, output_parser=parse_mesh_retopology_output,
    )
    result = retopology_result(task_id, artifacts, bakeTextures)
    if output_path is not None:
        result["downloads"] = download_retopology_artifacts(artifacts, output_path)
    return result


def generate_mesh_retopology(
    modelUrl, faceLimit, output_path=None, *, quad=True, bakeTextures=False,
    textureSize=2048, base_url=None, region=None, content_id=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS, interval=DEFAULT_POLL_INTERVAL,
):
    if output_path is not None:
        validate_output_path(output_path)
    task_id = create_mesh_retopology_task(
        modelUrl, faceLimit, quad=quad, bakeTextures=bakeTextures,
        textureSize=textureSize, base_url=base_url, region=region,
        content_id=content_id,
    )
    # Persist this ID in the caller's task record before polling; CLI also emits it.
    print(json.dumps({"taskId": str(task_id)}), file=sys.stderr, flush=True)
    return resume_mesh_retopology(
        task_id, output_path, bakeTextures=bakeTextures, base_url=base_url,
        region=region, max_attempts=max_attempts, interval=interval,
    )


def resume_animation_retarget(
    task_id, animationIds, output_path=None, *, animationOutputMode="separate",
    outFormat="glb", base_url=None, region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS, interval=DEFAULT_POLL_INTERVAL,
):
    """Resume one task; preserve action failures and download each returned URL once."""
    animationIds = validate_animation_ids(animationIds)
    if not isinstance(outFormat, str) or outFormat not in ANIMATION_FORMATS:
        raise ValueError("outFormat must be glb/fbx")
    if not isinstance(animationOutputMode, str) or animationOutputMode not in ANIMATION_OUTPUT_MODES:
        raise ValueError("animationOutputMode must be separate/combined")
    outputs = query_task_status(
        task_id, base_url=base_url, region=region,
        max_attempts=max_attempts, interval=interval,
    )
    actions = validate_animation_results(
        outputs, animationIds, outFormat=outFormat, animationOutputMode=animationOutputMode,
    )
    url_key = "animationGlbUrl" if outFormat == "glb" else "fbxUrl"
    files = {}
    for action in actions:
        if action["status"] == "success":
            files.setdefault(action[url_key], []).append(action["animation_id"])
    failures = sum(action["status"] == "failed" for action in actions)
    result = {"taskId": str(task_id), "actions": actions,
              "completion": "failed" if not files else "partial" if failures else "complete"}
    if output_path is not None:
        base, _ = os.path.splitext(os.fspath(output_path))
        downloads = []
        for url, action_ids in files.items():
            label = "combined" if animationOutputMode == "combined" else action_ids[0]
            target = f"{base}_{label}.{outFormat}"
            size = download_model(url, target)
            downloads.append({"path": target, "format": outFormat, "size": size,
                              "animationIds": action_ids})
        result["downloads"] = downloads
    return result


def generate_articulation_animation(
    glbUrl, prompt, output_path=None, *, base_url=None, region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS, interval=DEFAULT_POLL_INTERVAL,
):
    """Create, poll, and optionally download the actual articulation artifact."""
    if output_path is not None:
        validate_output_path(output_path)
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    if not isinstance(interval, (int, float)) or isinstance(interval, bool) or not 0 <= interval < float("inf"):
        raise ValueError("interval must be a finite non-negative number")
    task_id = create_articulation_animation_task(
        glbUrl, prompt, base_url=base_url, region=region,
    )
    print(f"Task created: {task_id}", file=sys.stderr)
    result_url = complete_task(
        task_id, base_url=base_url, region=region,
        max_attempts=max_attempts, interval=interval,
        output_parser=parse_articulation_animation_output,
    )
    if output_path is None:
        return result_url
    url_path = urllib.parse.unquote(urllib.parse.urlparse(result_url).path)
    extension = os.path.splitext(url_path)[1].lower()
    if not extension[1:].isascii() or not extension[1:].isalnum() or len(extension) > 12:
        extension = ".bin"
    output_base, _ = os.path.splitext(os.fspath(output_path))
    path = output_base + extension
    return [(path, download_model(result_url, path))]


def generate_multi_format_export(
    modelUrl,
    output_path=None,
    *,
    outputFormat=None,
    base_url=None,
    region=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the multi-format export create, poll, and optional download workflow."""
    task_id = create_multi_format_export_task(
        modelUrl,
        outputFormat=outputFormat,
        base_url=base_url,
        region=region,
    )
    return complete_task(
        task_id,
        output_path=output_path,
        expected_formats=export_result_formats(modelUrl, outputFormat),
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )


def add_poll_arguments(parser):
    """Add shared polling controls to a CLI subcommand."""
    parser.add_argument(
        "--max-attempts", type=int, default=DEFAULT_POLL_ATTEMPTS
    )
    parser.add_argument(
        "--interval", type=float, default=DEFAULT_POLL_INTERVAL
    )


def add_generation_arguments(parser):
    """Add shared version-specific image/text generation options."""
    parser.add_argument(
        "--version", required=True, choices=sorted(GENERATION_VERSIONS)
    )
    parser.add_argument(
        "--face-count",
        dest="faceCount",
        type=int,
        default=None,
        help=f"Mesh face count in [{FACE_COUNT_MIN}, {FACE_COUNT_MAX}]",
    )
    parser.add_argument(
        "--format",
        dest="outputFormat",
        action="append",
        choices=sorted(GENERATION_FORMATS),
        default=None,
        help="Repeat to request multiple formats.",
    )
    pbr_group = parser.add_mutually_exclusive_group()
    pbr_group.add_argument(
        "--enable-pbr", dest="enablePbr", action="store_true"
    )
    pbr_group.add_argument(
        "--no-pbr", dest="enablePbr", action="store_false"
    )
    parser.set_defaults(enablePbr=None)
    size_group = parser.add_mutually_exclusive_group()
    size_group.add_argument(
        "--ai-predict-size", dest="aiPredictSize", action="store_true"
    )
    size_group.add_argument(
        "--no-ai-predict-size", dest="aiPredictSize", action="store_false"
    )
    parser.set_defaults(aiPredictSize=None)
    parser.add_argument(
        "--custom-size",
        dest="customSize",
        type=float,
        help="G1 target height in millimetres; omit for G1-Turbo.",
    )
    add_poll_arguments(parser)


def build_parser():
    """Build the public command-line interface."""
    parser = argparse.ArgumentParser(
        description="Lux3D client using accessible URL inputs."
    )
    parser.add_argument(
        "--region",
        "-r",
        choices=["cn", "international"],
        default=None,
        help="API region. Default for this package: international",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Override the API root; LUX3D_BASE_URL is also supported.",
    )
    subparsers = parser.add_subparsers(dest="command")

    image_parser = subparsers.add_parser(
        "image", help="Generate 3D from one or more accessible image URLs."
    )
    image_parser.add_argument("img", help="Primary accessible image URL")
    image_parser.add_argument(
        "output_path", nargs="?", help="Optional output path or filename base"
    )
    image_parser.add_argument(
        "--image-view",
        dest="imageViews",
        action="append",
        default=None,
        help="Additional accessible image URL; repeat up to 31 times.",
    )
    add_generation_arguments(image_parser)

    text_parser = subparsers.add_parser(
        "text", help="Generate 3D from text and an optional image URL."
    )
    text_parser.add_argument("prompt")
    text_parser.add_argument(
        "output_path", nargs="?", help="Optional output path or filename base"
    )
    text_parser.add_argument("--style", choices=sorted(SUPPORTED_STYLES))
    text_parser.add_argument(
        "--image", dest="img", help="Optional accessible reference-image URL"
    )
    add_generation_arguments(text_parser)

    material_parser = subparsers.add_parser(
        "material", help="Transfer materials using accessible image and GLB URLs."
    )
    material_parser.add_argument("img", help="Material reference image URL")
    material_parser.add_argument(
        "output_path", nargs="?", help="Optional output path or filename base"
    )
    material_parser.add_argument(
        "--mesh-url", dest="meshUrl", required=True, help="Accessible GLB URL"
    )
    material_parser.add_argument(
        "--version", required=True, choices=[MATERIAL_VERSION]
    )
    material_parser.add_argument(
        "--format",
        dest="outputFormat",
        action="append",
        choices=sorted(MATERIAL_FORMATS),
        default=None,
    )
    material_size_group = material_parser.add_mutually_exclusive_group()
    material_size_group.add_argument(
        "--ai-predict-size", dest="aiPredictSize", action="store_true"
    )
    material_size_group.add_argument(
        "--no-ai-predict-size", dest="aiPredictSize", action="store_false"
    )
    material_parser.set_defaults(aiPredictSize=None)
    material_parser.add_argument("--custom-size", dest="customSize", type=float)
    add_poll_arguments(material_parser)

    multimodal_image_parser = subparsers.add_parser(
        "multimodal-image",
        help="Generate one image from an image URL, text, or both.",
    )
    multimodal_image_parser.add_argument(
        "--image", dest="img", help="Optional accessible reference-image URL"
    )
    multimodal_image_parser.add_argument(
        "--prompt", help="Optional non-empty image-generation prompt"
    )
    multimodal_image_parser.add_argument(
        "--output", dest="output_path", help="Optional image download path"
    )
    add_poll_arguments(multimodal_image_parser)

    four_view_parser = subparsers.add_parser(
        "four-view", help="Generate four viewpoints from an image URL, text, or both."
    )
    four_view_parser.add_argument(
        "img", nargs="?", help="Optional accessible object image URL"
    )
    four_view_parser.add_argument(
        "--prompt", help="Optional non-empty object or viewpoint prompt"
    )
    add_poll_arguments(four_view_parser)

    part_split_parser = subparsers.add_parser(
        "part-split", help="Split a GLB model and return one reconstructed GLB."
    )
    part_split_parser.add_argument("glbUrl", help="Accessible GLB model URL")
    part_split_parser.add_argument(
        "output_path",
        nargs="?",
        help="Optional output path for the reconstructed GLB.",
    )
    add_poll_arguments(part_split_parser)

    retopology_parser = subparsers.add_parser(
        "retopology", help="Retopologize a static GLB; face budget is required."
    )
    retopology_parser.add_argument("modelUrl")
    retopology_parser.add_argument("output_path", nargs="?")
    retopology_parser.add_argument("--face-limit", type=int, required=True, dest="faceLimit")
    retopology_parser.add_argument("--triangle", action="store_true")
    retopology_parser.add_argument("--bake-textures", action="store_true", dest="bakeTextures")
    retopology_parser.add_argument("--texture-size", type=int, default=2048, dest="textureSize")
    retopology_parser.add_argument("--content-id", dest="content_id")
    add_poll_arguments(retopology_parser)
    resume_retopology_parser = subparsers.add_parser(
        "retopology-result", help="Resume polling/downloading an existing retopology task."
    )
    resume_retopology_parser.add_argument("task_id")
    resume_retopology_parser.add_argument("output_path", nargs="?")
    resume_retopology_parser.add_argument("--bake-textures", action="store_true", dest="bakeTextures")
    add_poll_arguments(resume_retopology_parser)

    articulation_parser = subparsers.add_parser(
        "articulation", help="Add joints and motion to GLB model parts."
    )
    articulation_parser.add_argument("glbUrl", help="Accessible GLB model URL")
    articulation_parser.add_argument(
        "output_path", nargs="?", help="Optional download filename base; suffix follows the result URL."
    )
    articulation_parser.add_argument("--prompt", required=True, help="Joint-motion instructions")
    articulation_parser.add_argument(
        "--submit-only", action="store_true", help="Return the task ID without polling or downloading."
    )
    add_poll_arguments(articulation_parser)

    export_parser = subparsers.add_parser(
        "export", help="Export a Lux3D ZIP or GLB URL to other formats."
    )
    export_parser.add_argument("modelUrl", help="Accessible .zip or .glb URL")
    export_parser.add_argument(
        "output_path", nargs="?", help="Optional output path or filename base"
    )
    export_parser.add_argument(
        "--format",
        dest="outputFormat",
        action="append",
        choices=sorted(EXPORT_FORMATS),
        default=None,
    )
    add_poll_arguments(export_parser)

    rig_parser = subparsers.add_parser("auto-rig", help="Create auto-rig and return its task ID immediately.")
    rig_parser.add_argument("modelUrl", help="Public HTTPS character GLB URL")
    rig_parser.add_argument("--content-id", dest="content_id")

    retarget_parser = subparsers.add_parser("retarget", help="Create one animation task and return its task ID immediately.")
    retarget_parser.add_argument("rigModelUrl", help="Public HTTPS rigged character GLB URL")
    retarget_parser.add_argument("--animation-id", dest="animationIds", action="append", required=True, choices=ANIMATION_IDS)
    retarget_parser.add_argument("--output-mode", dest="animationOutputMode", choices=sorted(ANIMATION_OUTPUT_MODES), default="separate")
    retarget_parser.add_argument("--format", dest="outFormat", choices=sorted(ANIMATION_FORMATS), default="glb")
    retarget_parser.add_argument("--animate-in-place", dest="animateInPlace", action="store_true")
    retarget_parser.add_argument("--content-id", dest="content_id")

    result_parser = subparsers.add_parser("retarget-result", help="Resume an animation task without creating another task.")
    result_parser.add_argument("task_id")
    result_parser.add_argument("output_path", nargs="?", help="Optional output filename base")
    result_parser.add_argument("--animation-id", dest="animationIds", action="append", required=True, choices=ANIMATION_IDS)
    result_parser.add_argument("--output-mode", dest="animationOutputMode", choices=sorted(ANIMATION_OUTPUT_MODES), default="separate")
    result_parser.add_argument("--format", dest="outFormat", choices=sorted(ANIMATION_FORMATS), default="glb")
    add_poll_arguments(result_parser)

    rig_result_parser = subparsers.add_parser("rig-result", help="Resume an auto-rig task without creating another task.")
    rig_result_parser.add_argument("task_id")
    rig_result_parser.add_argument("output_path", nargs="?", help="Optional GLB output path")
    add_poll_arguments(rig_result_parser)

    query_parser = subparsers.add_parser("query", help="Query one task once.")
    query_parser.add_argument("task_id")

    list_parser = subparsers.add_parser(
        "list", help="List generation tasks for the current account."
    )
    list_parser.add_argument("--page", type=int, default=1)
    list_parser.add_argument("--pagesize", type=int, default=20)
    list_parser.add_argument(
        "--status",
        type=int,
        choices=sorted(SUPPORTED_TASK_STATUSES),
        default=None,
    )
    list_parser.add_argument("--starttime", type=int, default=None)
    list_parser.add_argument("--endtime", type=int, default=None)
    return parser


def print_result(result):
    """Print a CLI result without Python representation noise."""
    if isinstance(result, (dict, list, tuple)):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)


def main():
    """Command-line entry point."""
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        raise SystemExit(1)

    common = {"base_url": args.base_url, "region": args.region}
    if args.command == "image":
        image_urls = [args.img] + list(args.imageViews or [])
        image_input = (
            {"img": image_urls[0]} if len(image_urls) == 1 else {"imgs": image_urls}
        )
        result = generate_3d_model(
            output_path=args.output_path,
            version=args.version,
            faceCount=args.faceCount,
            outputFormat=args.outputFormat,
            enablePbr=args.enablePbr,
            aiPredictSize=args.aiPredictSize,
            customSize=args.customSize,
            max_attempts=args.max_attempts,
            interval=args.interval,
            **image_input,
            **common,
        )
    elif args.command == "text":
        result = generate_text_to_3d(
            args.prompt,
            output_path=args.output_path,
            version=args.version,
            style=args.style,
            img=args.img,
            faceCount=args.faceCount,
            outputFormat=args.outputFormat,
            enablePbr=args.enablePbr,
            aiPredictSize=args.aiPredictSize,
            customSize=args.customSize,
            max_attempts=args.max_attempts,
            interval=args.interval,
            **common,
        )
    elif args.command == "material":
        result = generate_material_transfer(
            args.img,
            args.meshUrl,
            output_path=args.output_path,
            version=args.version,
            outputFormat=args.outputFormat,
            aiPredictSize=args.aiPredictSize,
            customSize=args.customSize,
            max_attempts=args.max_attempts,
            interval=args.interval,
            **common,
        )
    elif args.command == "multimodal-image":
        result = generate_multimodal_image(
            args.img,
            output_path=args.output_path,
            prompt=args.prompt,
            max_attempts=args.max_attempts,
            interval=args.interval,
            **common,
        )
    elif args.command == "four-view":
        result = generate_four_views(
            args.img,
            prompt=args.prompt,
            max_attempts=args.max_attempts,
            interval=args.interval,
            **common,
        )
    elif args.command == "part-split":
        result = generate_part_split(
            args.glbUrl,
            output_path=args.output_path,
            max_attempts=args.max_attempts,
            interval=args.interval,
            **common,
        )
    elif args.command == "retopology":
        result = generate_mesh_retopology(
            args.modelUrl, args.faceLimit, args.output_path, quad=not args.triangle,
            bakeTextures=args.bakeTextures, textureSize=args.textureSize,
            base_url=args.base_url, region=args.region, content_id=args.content_id,
            max_attempts=args.max_attempts, interval=args.interval,
        )
    elif args.command == "retopology-result":
        result = resume_mesh_retopology(
            args.task_id, args.output_path, bakeTextures=args.bakeTextures,
            base_url=args.base_url, region=args.region,
            max_attempts=args.max_attempts, interval=args.interval,
        )
    elif args.command == "articulation":
        if args.submit_only:
            if args.output_path is not None:
                parser.error("articulation --submit-only cannot be used with output_path")
            result = create_articulation_animation_task(args.glbUrl, args.prompt, **common)
        else:
            result = generate_articulation_animation(
                args.glbUrl, args.prompt, output_path=args.output_path,
                max_attempts=args.max_attempts, interval=args.interval, **common,
            )
    elif args.command == "export":
        result = generate_multi_format_export(
            args.modelUrl,
            output_path=args.output_path,
            outputFormat=args.outputFormat,
            max_attempts=args.max_attempts,
            interval=args.interval,
            **common,
        )
    elif args.command == "auto-rig":
        result = {"taskId": create_auto_rig_task(args.modelUrl, content_id=args.content_id, **common)}
    elif args.command == "retarget":
        result = {"taskId": create_animation_retarget_task(
            args.rigModelUrl, args.animationIds, animationOutputMode=args.animationOutputMode,
            outFormat=args.outFormat, animateInPlace=args.animateInPlace,
            content_id=args.content_id, **common,
        )}
    elif args.command == "retarget-result":
        result = resume_animation_retarget(
            args.task_id, args.animationIds, args.output_path,
            animationOutputMode=args.animationOutputMode, outFormat=args.outFormat,
            max_attempts=args.max_attempts, interval=args.interval, **common,
        )
    elif args.command == "rig-result":
        result = complete_task(
            args.task_id, output_path=args.output_path, expected_formats=["glb"],
            max_attempts=args.max_attempts, interval=args.interval, **common,
        )
    elif args.command == "query":
        result = get_task(args.task_id, **common)
    elif args.command == "list":
        result = list_tasks(
            page=args.page,
            pagesize=args.pagesize,
            status=args.status,
            starttime=args.starttime,
            endtime=args.endtime,
            **common,
        )
    else:
        parser.error(f"Unknown command: {args.command}")
        return
    print_result(result)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, TimeoutError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)
