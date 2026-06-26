"""
Lux3D client for image-to-3D and text-to-3D generation.
Supports both China (CN) and International API endpoints.
"""

import argparse
import base64
import io
import os
import sys
import time
import urllib.parse

import requests
from PIL import Image


# API endpoints
CN_HOST = "https://api.aholo3d.cn"
CN_PREFIX = ""
INTERNATIONAL_HOST = "https://api.aholo3d.com"
INTERNATIONAL_PREFIX = "/global"

# Default to international endpoint
DEFAULT_REGION = "international"

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2
DEFAULT_POLL_ATTEMPTS = 60
DEFAULT_POLL_INTERVAL = 15
SUPPORTED_STYLES = {
    "photorealistic",
    "cartoon",
    "anime",
    "hand_painted",
    "cyberpunk",
    "fantasy",
    "glass",
}

SUPPORTED_VERSIONS = {
    "v1.0-pro",
    "v2.0-preview",
}

SUPPORTED_FORMATS = {
    "zip",
    "glb",
    "usdz",
}


def get_api_key():
    """Read the API key from the environment each time it is needed."""
    return os.environ.get("LUX3D_API_KEY", "").strip()


def validate_api_key():
    """Validate the configured API key and return it."""
    api_key = get_api_key()
    if not api_key or api_key in {"your_lux3d_api_key", "your_invitation_code_here"}:
        raise ValueError(
            "[ERROR] API key not configured.\n"
            "Please set LUX3D_API_KEY to the base64 invitation code."
        )
    return api_key


def validate_image_path(image_path):
    """Validate that an image path exists and is readable."""
    if not image_path:
        raise ValueError("Image path cannot be empty")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not os.path.isfile(image_path):
        raise ValueError(f"Path is not a file: {image_path}")
    try:
        with open(image_path, "rb") as file_obj:
            file_obj.read(1)
    except PermissionError as exc:
        raise PermissionError(f"Permission denied reading: {image_path}") from exc


def validate_output_path(output_path):
    """Validate that the output path can be written."""
    output_dir = os.path.dirname(output_path) or "."
    if not os.path.isdir(output_dir):
        raise ValueError(f"Output directory does not exist: {output_dir}")

    test_path = os.path.join(output_dir, ".lux3d_write_test")
    try:
        with open(test_path, "w", encoding="utf-8") as file_obj:
            file_obj.write("ok")
    except OSError as exc:
        raise PermissionError(f"Cannot write to directory: {output_dir}") from exc
    finally:
        if os.path.exists(test_path):
            os.remove(test_path)


def validate_prompt(prompt):
    """Validate the text prompt for text-to-3D generation."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    return prompt.strip()


def validate_style(style):
    """Validate the requested text-to-3D style. Returns default if not provided."""
    if style is None:
        return "photorealistic"
    if style not in SUPPORTED_STYLES:
        supported = ", ".join(sorted(SUPPORTED_STYLES))
        raise ValueError(f"Unsupported style '{style}'. Supported styles: {supported}")
    return style


def validate_version(version):
    """Validate the Lux3D version parameter."""
    if version not in SUPPORTED_VERSIONS:
        supported = ", ".join(sorted(SUPPORTED_VERSIONS))
        raise ValueError(f"Unsupported version '{version}'. Supported versions: {supported}")
    return version


def validate_format(output_format):
    """Validate the output format parameter."""
    if output_format not in SUPPORTED_FORMATS:
        supported = ", ".join(sorted(SUPPORTED_FORMATS))
        raise ValueError(f"Unsupported format '{output_format}'. Supported formats: {supported}")
    return output_format


def validate_mesh_url(mesh_url):
    """Validate the mesh URL for material transfer."""
    if not mesh_url or not mesh_url.strip():
        raise ValueError("Mesh URL cannot be empty")
    return mesh_url.strip()


def get_base_url(region=None):
    """
    Get the base URL for the specified region.
    
    Args:
        region: 'cn' for China, 'international' for global. 
                If None, uses LUX3D_BASE_URL env var or LUX3D_REGION env var or default.
    
    Returns:
        The base URL for the API endpoint.
    """
    # First check if LUX3D_BASE_URL is explicitly set
    env_base_url = os.environ.get("LUX3D_BASE_URL", "").strip()
    if env_base_url:
        return env_base_url.rstrip("/")
    
    # Determine region
    if region is None:
        region = os.environ.get("LUX3D_REGION", DEFAULT_REGION).strip().lower()
    
    if region in ("cn", "china", "domestic"):
        return CN_HOST + CN_PREFIX
    elif region in ("international", "global", "intl"):
        return INTERNATIONAL_HOST + INTERNATIONAL_PREFIX
    else:
        # Default to international for unknown regions
        return INTERNATIONAL_HOST + INTERNATIONAL_PREFIX


def normalize_base_url(base_url, region=None):
    """Normalize the configured base URL to a documented Lux3D API root."""
    if base_url:
        normalized = base_url.rstrip("/")
    else:
        normalized = get_base_url(region)
    
    # Handle case where user specifies the host without prefix
    if normalized == INTERNATIONAL_HOST:
        return normalized + INTERNATIONAL_PREFIX
    if normalized == CN_HOST:
        return normalized + CN_PREFIX
    
    return normalized


def get_auth_headers():
    """Get authorization headers using the API key."""
    api_key = validate_api_key()
    return {
        "Content-Type": "application/json",
        "Authorization": api_key,
    }


def secure_request(method, url, headers=None, data=None, timeout=None, retries=None):
    """Perform an HTTP request with bounded retries."""
    request_headers = headers or {"Content-Type": "application/json"}
    timeout = timeout or REQUEST_TIMEOUT
    retries = retries or MAX_RETRIES
    last_error = None

    for attempt in range(retries):
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=request_headers,
                json=data,
                timeout=timeout,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout as exc:
            last_error = f"Request timeout (attempt {attempt + 1}/{retries})"
            if attempt == retries - 1:
                break
            time.sleep(RETRY_DELAY)
        except requests.exceptions.RequestException as exc:
            last_error = f"Request failed: {exc}"
            if attempt == retries - 1:
                break
            time.sleep(RETRY_DELAY)

    raise Exception(f"Request failed after {retries} attempts: {last_error}")


def image_to_data_url(image_path):
    """Convert an image file to a JPEG data URL."""
    validate_image_path(image_path)
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    image_bytes = buffer.getvalue()
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def ensure_success(result):
    """Validate the Lux3D API response format used in the documentation."""
    code = result.get("c")
    if code not in (None, "", 0, "0"):
        message = result.get("m") or "unknown error"
        raise Exception(f"API error: {message} (code={code})")

    legacy_code = result.get("code")
    if code is None and legacy_code not in (None, "", 0, "0"):
        message = result.get("message") or "unknown error"
        raise Exception(f"API error: {message} (code={legacy_code})")

    return result


def submit_task(path, payload, base_url=None, region=None):
    """Submit a Lux3D generation task and return its taskid."""
    url = normalize_base_url(base_url, region) + path
    headers = get_auth_headers()
    response = secure_request("POST", url, headers=headers, data=payload)

    try:
        result = response.json()
    except ValueError as exc:
        raise Exception(f"Invalid JSON response: {response.text}") from exc

    ensure_success(result)
    task_id = result.get("d")
    if task_id in (None, ""):
        raise Exception(f"Missing task id in response: {result}")
    return str(task_id)


def create_task(image_path, base_url=None, region=None, lux3d_biz_type=None, version=None):
    """Submit an image-to-3D task."""
    payload = {"img": image_to_data_url(image_path)}
    if lux3d_biz_type is not None:
        payload["lux3dBizType"] = lux3d_biz_type
    if version is not None:
        payload["version"] = validate_version(version)
    return submit_task("/lux3d/v1/generate/img-to-3d/task/create", payload, base_url=base_url, region=region)


def create_text_to_3d_task(
    prompt,
    style=None,
    image_path=None,
    base_url=None,
    region=None,
    lux3d_biz_type=None,
    version=None,
):
    """Submit a text-to-3D task with an optional reference image."""
    payload = {
        "prompt": validate_prompt(prompt),
    }
    if style is not None:
        payload["style"] = validate_style(style)
    if image_path:
        payload["img"] = image_to_data_url(image_path)
    if lux3d_biz_type is not None:
        payload["lux3dBizType"] = lux3d_biz_type
    if version is not None:
        payload["version"] = validate_version(version)
    return submit_task("/lux3d/v1/generate/text-to-3d/task/create", payload, base_url=base_url, region=region)


def create_material_transfer_task(
    image_path,
    mesh_url,
    base_url=None,
    region=None,
    version=None,
):
    """Submit a material transfer task to regenerate materials for an existing model."""
    payload = {
        "img": image_to_data_url(image_path),
        "meshUrl": validate_mesh_url(mesh_url),
    }
    if version is not None:
        payload["version"] = validate_version(version)
    return submit_task("/lux3d/v1/generate/material-transfer/task/create", payload, base_url=base_url, region=region)


def query_task_status(task_id, base_url=None, region=None, max_attempts=DEFAULT_POLL_ATTEMPTS, interval=DEFAULT_POLL_INTERVAL):
    """Poll a Lux3D task until completion and return the download URLs.
    
    Returns:
        A dictionary mapping format names to download URLs, e.g. {'zip': '...', 'glb': '...', 'usdz': '...'}
        Or a single URL string for backward compatibility with older API versions.
    """
    for _ in range(max_attempts):
        url = normalize_base_url(base_url, region) + "/lux3d/v1/generate/task/get?taskid=" + urllib.parse.quote(str(task_id))
        headers = get_auth_headers()
        response = secure_request("GET", url, headers=headers)

        try:
            result = response.json()
        except ValueError as exc:
            raise Exception(f"Invalid JSON response: {response.text}") from exc

        ensure_success(result)
        task_data = result.get("d") or {}
        status = task_data.get("status")

        if status == 3:
            outputs = task_data.get("outputs") or []
            
            # Parse multiple outputs with different formats based on URL
            format_urls = {}
            for output in outputs:
                content = output.get("content", "").strip()
                if content:
                    # Extract format from URL filename
                    if ".glb" in content.lower():
                        format_urls["glb"] = content
                    elif ".usdz" in content.lower():
                        format_urls["usdz"] = content
                    elif ".zip" in content.lower():
                        format_urls["zip"] = content
            
            # If we found multiple formats, return the dictionary
            if format_urls:
                return format_urls
            
            # Fallback: return the first output URL for backward compatibility
            if outputs and outputs[0].get("content"):
                return outputs[0]["content"]
            
            raise Exception(f"Task succeeded without output content: {result}")
        if status == 4:
            raise Exception(f"Task execution failed: {result}")

        time.sleep(interval)

    raise Exception("Task timeout")


def download_model(model_url, output_path, output_format=None):
    """
    Download the generated model file to the target path.
    
    Args:
        model_url: Can be either:
                   - A string URL (backward compatibility with single format API)
                   - A dictionary mapping format names to URLs (new multi-format API)
        output_path: The path to save the downloaded file.
        output_format: Optional output format ('zip', 'glb', 'usdz'). 
                       Required when model_url is a dictionary.
    
    Returns:
        The size of the downloaded file in bytes.
    """
    validate_output_path(output_path)
    
    # Handle multi-format API response (dict)
    if isinstance(model_url, dict):
        if output_format is None:
            raise ValueError("output_format is required when API returns multiple formats")
        
        output_format = validate_format(output_format)
        if output_format not in model_url:
            available_formats = ", ".join(sorted(model_url.keys()))
            raise ValueError(f"Format '{output_format}' not available. Available formats: {available_formats}")
        
        url_to_download = model_url[output_format]
    
    # Handle single format API response (string)
    else:
        url_to_download = model_url
        # For backward compatibility, still support URL parameter approach
        if output_format is not None:
            output_format = validate_format(output_format)
            separator = "?" if "?" not in url_to_download else "&"
            url_to_download = f"{url_to_download}{separator}format={output_format}"
    
    response = secure_request("GET", url_to_download, headers={})
    with open(output_path, "wb") as file_obj:
        file_obj.write(response.content)
    return len(response.content)


def generate_3d_model(
    image_path,
    output_path=None,
    base_url=None,
    region=None,
    lux3d_biz_type=None,
    version=None,
    output_format=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the full image-to-3D workflow."""
    validate_api_key()

    print("=== Submitting image-to-3D task ===")
    task_id = create_task(image_path, base_url=base_url, region=region, lux3d_biz_type=lux3d_biz_type, version=version)
    print(f"Task ID: {task_id}")

    print("\n=== Querying task result ===")
    model_url = query_task_status(
        task_id,
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )
    print(f"Model URL: {model_url}")

    # Determine output filename based on format
    if output_path:
        output_name = output_path
    else:
        ext = output_format or "zip"
        output_name = image_path.rsplit(".", 1)[0] + f"_3d.{ext}"
    
    print("\n=== Downloading model ===")
    size = download_model(model_url, output_name, output_format=output_format)
    print(f"Downloaded: {output_name} ({size} bytes)")
    return output_name


def generate_text_to_3d(
    prompt,
    output_path=None,
    style=None,
    image_path=None,
    base_url=None,
    region=None,
    lux3d_biz_type=None,
    version=None,
    output_format=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the full text-to-3D workflow."""
    validate_api_key()

    print("=== Submitting text-to-3D task ===")
    task_id = create_text_to_3d_task(
        prompt,
        style=style,
        image_path=image_path,
        base_url=base_url,
        region=region,
        lux3d_biz_type=lux3d_biz_type,
        version=version,
    )
    print(f"Task ID: {task_id}")

    print("\n=== Querying task result ===")
    model_url = query_task_status(
        task_id,
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )
    print(f"Model URL: {model_url}")

    # Determine output filename based on format
    if output_path:
        output_name = output_path
    else:
        ext = output_format or "zip"
        output_name = f"lux3d_text_to_3d.{ext}"
    
    print("\n=== Downloading model ===")
    size = download_model(model_url, output_name, output_format=output_format)
    print(f"Downloaded: {output_name} ({size} bytes)")
    return output_name


def generate_material_transfer(
    image_path,
    mesh_url,
    output_path=None,
    base_url=None,
    region=None,
    version=None,
    output_format=None,
    max_attempts=DEFAULT_POLL_ATTEMPTS,
    interval=DEFAULT_POLL_INTERVAL,
):
    """Run the full material transfer workflow."""
    validate_api_key()

    print("=== Submitting material transfer task ===")
    task_id = create_material_transfer_task(
        image_path,
        mesh_url,
        base_url=base_url,
        region=region,
        version=version,
    )
    print(f"Task ID: {task_id}")

    print("\n=== Querying task result ===")
    model_url = query_task_status(
        task_id,
        base_url=base_url,
        region=region,
        max_attempts=max_attempts,
        interval=interval,
    )
    print(f"Model URL: {model_url}")

    # Determine output filename based on format
    if output_path:
        output_name = output_path
    else:
        ext = output_format or "zip"
        output_name = f"lux3d_material_transfer.{ext}"
    
    print("\n=== Downloading model ===")
    size = download_model(model_url, output_name, output_format=output_format)
    print(f"Downloaded: {output_name} ({size} bytes)")
    return output_name


def build_parser():
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Lux3D client for image-to-3D and text-to-3D generation. "
                    "Supports both China (CN) and International API endpoints."
    )
    parser.add_argument(
        "--region", "-r",
        choices=["cn", "international"],
        default=None,
        help="API region: 'cn' for China (api.aholo3d.cn), 'international' for global (api.aholo3d.com/global). "
             "Can also be set via LUX3D_REGION environment variable. Default: international"
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Override API base URL. Can also be set via LUX3D_BASE_URL environment variable."
    )
    subparsers = parser.add_subparsers(dest="command")

    image_parser = subparsers.add_parser("image", help="Generate a 3D model from an image.")
    image_parser.add_argument("image_path", help="Input image path")
    image_parser.add_argument("output_path", nargs="?", help="Output file path")
    image_parser.add_argument("--biz-type", dest="lux3d_biz_type", help="Optional business type")
    image_parser.add_argument("--version", default=None, help="Lux3D version: v2.0-preview (default) or v1.0-pro")
    image_parser.add_argument("--format", dest="output_format", choices=["zip", "glb", "usdz"], default=None,
                              help="Output format: zip (default), glb, usdz. Only applicable for v2.0-preview")
    image_parser.add_argument("--max-attempts", type=int, default=DEFAULT_POLL_ATTEMPTS)
    image_parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL)

    text_parser = subparsers.add_parser("text", help="Generate a 3D model from text.")
    text_parser.add_argument("prompt", help="Text prompt")
    text_parser.add_argument("output_path", nargs="?", help="Output file path")
    text_parser.add_argument("--style", default=None, help="Generation style (default: photorealistic)")
    text_parser.add_argument("--image", dest="image_path", help="Optional reference image path")
    text_parser.add_argument("--biz-type", dest="lux3d_biz_type", help="Optional business type")
    text_parser.add_argument("--version", default=None, help="Lux3D version: v2.0-preview (default) or v1.0-pro")
    text_parser.add_argument("--format", dest="output_format", choices=["zip", "glb", "usdz"], default=None,
                              help="Output format: zip (default), glb, usdz. Only applicable for v2.0-preview")
    text_parser.add_argument("--max-attempts", type=int, default=DEFAULT_POLL_ATTEMPTS)
    text_parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL)

    material_parser = subparsers.add_parser("material", help="Regenerate materials for an existing 3D model.")
    material_parser.add_argument("image_path", help="Reference image path for material")
    material_parser.add_argument("output_path", nargs="?", help="Output file path")
    material_parser.add_argument("--mesh-url", required=True, help="URL of the GLB model file")
    material_parser.add_argument("--version", default=None, help="Lux3D version: v2.0-preview (default) or v1.0-pro")
    material_parser.add_argument("--format", dest="output_format", choices=["zip", "glb", "usdz"], default=None,
                              help="Output format: zip (default), glb, usdz. Only applicable for v2.0-preview")
    material_parser.add_argument("--max-attempts", type=int, default=DEFAULT_POLL_ATTEMPTS)
    material_parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL)

    return parser


def main():
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args()

    # Keep the historical one-argument form for image-to-3D.
    if not args.command:
        if len(sys.argv) >= 2 and not sys.argv[1].startswith("-"):
            # Check if it's the legacy form: python lux3d_client.py input.jpg [output.zip]
            if len(sys.argv) <= 3 or sys.argv[2] not in ("image", "text"):
                image_path = sys.argv[1]
                output_path = sys.argv[2] if len(sys.argv) >= 3 else None
                result = generate_3d_model(
                    image_path,
                    output_path=output_path,
                    region=args.region,
                    base_url=args.base_url,
                )
                print(f"\n[SUCCESS] Model saved to: {result}")
                return
        parser.print_help()
        raise SystemExit(1)

    if args.command == "image":
        result = generate_3d_model(
            args.image_path,
            output_path=args.output_path,
            base_url=args.base_url,
            region=args.region,
            lux3d_biz_type=args.lux3d_biz_type,
            version=args.version,
            output_format=args.output_format,
            max_attempts=args.max_attempts,
            interval=args.interval,
        )
        print(f"\n[SUCCESS] Model saved to: {result}")
        return

    if args.command == "text":
        result = generate_text_to_3d(
            args.prompt,
            output_path=args.output_path,
            style=args.style,
            image_path=args.image_path,
            base_url=args.base_url,
            region=args.region,
            lux3d_biz_type=args.lux3d_biz_type,
            version=args.version,
            output_format=args.output_format,
            max_attempts=args.max_attempts,
            interval=args.interval,
        )
        print(f"\n[SUCCESS] Model saved to: {result}")
        return

    if args.command == "material":
        result = generate_material_transfer(
            args.image_path,
            mesh_url=args.mesh_url,
            output_path=args.output_path,
            base_url=args.base_url,
            region=args.region,
            version=args.version,
            output_format=args.output_format,
            max_attempts=args.max_attempts,
            interval=args.interval,
        )
        print(f"\n[SUCCESS] Model saved to: {result}")
        return

    parser.print_help()
    raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"\n[ERROR] {exc}")
        raise SystemExit(1)
    except Exception as exc:
        print(f"\n[ERROR] {exc}")
        raise SystemExit(1)