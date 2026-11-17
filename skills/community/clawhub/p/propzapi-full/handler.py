"""
propzapi-full skill handler — generate images from HTML/CSS templates and capture
webpage screenshots over the propzapi REST API:
generate_image, screenshot, list_templates, create_template, embed_url.

Pure standard library. API key in PROPZAPI_KEY, sent as the X-API-Key header.
The base URL is hardcoded, so the key never reaches any other host.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.propzapi.com"  # hardcoded: the API key is never sent to any other host
USER_AGENT = "propzapi-skills/0.2.0 (+https://github.com/paperandbeyond23-gif/propzapi-skills)"
TIMEOUT_SECONDS = 60

SIGNUP_URL = "https://propzapi.com/app"
KEYS_URL = "https://propzapi.com/app"
PRICING_URL = "https://propzapi.com/pricing"

FORMATS = ("png", "jpeg", "webp", "pdf")
SHOT_FORMATS = ("png", "jpeg", "webp", "pdf")


def _key():
    k = os.environ.get("PROPZAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "PROPZAPI_KEY environment variable is not set. "
            "Get a free key (50-image trial, no card) at " + SIGNUP_URL + ", "
            "then export PROPZAPI_KEY=your_key"
        )
    return k


def _http_error(e):
    try:
        detail = e.read().decode("utf-8")[:1000]
    except Exception:
        detail = ""
    if e.code == 401:
        return {
            "error": "auth_invalid",
            "detail": "PROPZAPI_KEY was rejected. Mint a new key at " + KEYS_URL + ".",
            "keys_url": KEYS_URL,
            "http_status": 401,
        }
    if e.code == 402:
        return {
            "error": "out_of_credits",
            "detail": "Out of propzapi image credits. Top up a pack or subscribe at " + PRICING_URL + ".",
            "upgrade_url": PRICING_URL,
            "http_status": 402,
        }
    if e.code == 403:
        return {
            "error": "forbidden",
            "detail": "This propzapi origin rejected the request. Use a direct key against the public host.",
            "http_status": 403,
        }
    if e.code == 404:
        return {
            "error": "not_found",
            "detail": "No match for that request. Check the template id (e.g. tpl_... or a built-in name).",
            "http_status": 404,
        }
    if e.code == 429:
        return {
            "error": "rate_limit_exceeded",
            "detail": "Request limit hit (or too many free keys from this IP). Back off, or upgrade at " + PRICING_URL + ".",
            "upgrade_url": PRICING_URL,
            "http_status": 429,
        }
    if e.code in (502, 503):
        return {
            "error": "upstream_unavailable",
            "detail": "The render backend was briefly unreachable. Retry shortly.",
            "http_status": e.code,
        }
    return {"error": "HTTP " + str(e.code), "detail": detail}


def _request(method, path, params=None, body=None):
    try:
        qs = ""
        if params:
            clean = {k: v for k, v in params.items() if v is not None and v != ""}
            if clean:
                qs = "?" + urllib.parse.urlencode(clean)
        headers = {
            "X-API-Key": _key(),
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            API_BASE + path + qs,
            data=data,
            method=method,
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return _http_error(e)
    except urllib.error.URLError as e:
        return {"error": "network", "detail": str(e.reason)}
    except RuntimeError as e:
        return {"error": "auth_required", "detail": str(e), "signup_url": SIGNUP_URL}
    except Exception as e:
        return {"error": "unexpected", "detail": str(e)}


def _get(path, params=None):
    return _request("GET", path, params=params)


def _post(path, body):
    return _request("POST", path, body=body)


def generate_image(template, modifications=None, format="png", scale=None, quality=None):
    """
    Render an image from a template + variable modifications.

    template:      template id (e.g. "tpl_..." ) or a built-in template name (required).
    modifications: dict of {{variable}} -> value fills for the template (optional).
    format:        "png" | "jpeg" | "webp" | "pdf" (default "png").
    scale:         output scale multiplier, e.g. 1, 2 (optional).
    quality:       compression quality 1-100 for jpeg/webp (optional).
    Costs 1 credit per image, billed on delivery.
    Returns {"url", "width", "height", "format", "bytes"}, or an {"error": ...} dict.
    """
    if not template:
        return {"error": "invalid_argument", "detail": "template is required."}
    if format is not None and format not in FORMATS:
        return {"error": "invalid_argument", "detail": "format must be one of " + ", ".join(FORMATS) + "."}
    body = {"template": template, "modifications": modifications or {}, "format": format}
    if scale is not None:
        body["scale"] = scale
    if quality is not None:
        body["quality"] = quality
    return _post("/v1/images", body)


def screenshot(url, full_page=None, width=None, height=None, format="png"):
    """
    Capture a screenshot of a live webpage.

    url:       the page to capture (required).
    full_page: True to capture the entire scrollable page (optional).
    width:     viewport width in px (optional).
    height:    viewport height in px (optional).
    format:    "png" | "jpeg" | "webp" | "pdf" (default "png").
    Costs 1 credit. Returns {"url", ...}, or an {"error": ...} dict.
    """
    if not url:
        return {"error": "invalid_argument", "detail": "url is required."}
    if format is not None and format not in SHOT_FORMATS:
        return {"error": "invalid_argument", "detail": "format must be one of " + ", ".join(SHOT_FORMATS) + "."}
    body = {"url": url, "format": format}
    if full_page is not None:
        body["full_page"] = full_page
    if width is not None:
        body["width"] = width
    if height is not None:
        body["height"] = height
    return _post("/v1/screenshot", body)


def list_templates():
    """
    List available templates (built-ins and your own).

    Free — no credits charged.
    Returns {"count", "data": [{"template", "name", "width", "height", "variables"}, ...]},
    or an {"error": ...} dict.
    """
    return _get("/v1/templates")


def create_template(name, html, width, height, variables=None):
    """
    Create a reusable HTML/CSS template with {{variables}} and Jinja logic.

    name:      human-readable template name (required).
    html:      the HTML/CSS template body (required).
    width:     canvas width in px (required).
    height:    canvas height in px (required).
    variables: list of variable names the template exposes (optional).
    Free — no credits charged. Returns the created template with its "tpl_..." id,
    or an {"error": ...} dict.
    """
    if not name or not html:
        return {"error": "invalid_argument", "detail": "name and html are required."}
    body = {"name": name, "html": html, "width": width, "height": height}
    if variables is not None:
        body["variables"] = variables
    return _post("/v1/templates", body)


def embed_url(template, modifications=None, format="png"):
    """
    Sign a GET render URL suitable for a <meta property="og:image"> tag.

    template:      template id or built-in name (required).
    modifications: dict of {{variable}} -> value fills (optional).
    format:        "png" | "jpeg" | "webp" | "pdf" (default "png").
    Free — no credits charged for signing. Returns {"url", ...}, or an {"error": ...} dict.
    """
    if not template:
        return {"error": "invalid_argument", "detail": "template is required."}
    if format is not None and format not in FORMATS:
        return {"error": "invalid_argument", "detail": "format must be one of " + ", ".join(FORMATS) + "."}
    body = {"template": template, "modifications": modifications or {}, "format": format}
    return _post("/v1/embed-url", body)
