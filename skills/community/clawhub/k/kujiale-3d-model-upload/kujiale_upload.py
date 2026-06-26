"""
kujiale_upload.py
--------------------------
Validates the complete 1->5 chain of the Kujiale OpenAPI 3D model upload flow.

Steps tested:
  Step 1 GET /v2/commodity/upload/sts -> STS credentials + uploadTaskId + filePath
  Step 2 OSS PUT (oss2.StsAuth) -> upload ZIP bytes to Alibaba OSS
  Step 3 POST /v2/commodity/upload/create -> trigger model parse (requestParam: upload_task_id)
  Step 4 GET /v2/commodity/upload/status -> poll parse status until status==3 (ready to submit)
  Step 5 POST /v2/commodity/upload/submit -> submit model -> returns brandGoodId

Authentication: md5(appSecret + appKey + timestamp_ms)

Credentials (required — no built-in defaults):
  Set environment variables before running:
    export KUJIALE_APP_KEY=your_app_key
    export KUJIALE_APP_SECRET=your_app_secret

  Or pass via CLI flags:
    python kujiale_upload.py --app-key YOUR_KEY --app-secret YOUR_SECRET

  Or pass programmatically:
    run_skill({"app_key": "...", "app_secret": "..."})

  Priority: explicit CLI/dict value > environment variable.
  There are no built-in defaults — credentials must be provided.

Requirements:
  pip install requests oss2

Programmatic entrypoint:
  from kujiale_upload import run_skill
  summary = run_skill({"app_key": "...", "app_secret": "...", "zip_path": "..."})
  # Pass dry_run=True to skip all network calls and return mock data.
"""

from __future__ import print_function

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import zipfile

# ---------------------------------------------------------------------------
# Optional imports
# ---------------------------------------------------------------------------
try:
  import requests  # type: ignore[import-untyped]
  _HAS_REQUESTS = True
except ImportError:
  _HAS_REQUESTS = False

try:
  import oss2  # type: ignore[import-untyped]
  _HAS_OSS2 = True
except ImportError:
  _HAS_OSS2 = False

# ---------------------------------------------------------------------------
# Credentials helpers
# ---------------------------------------------------------------------------
# No hard-coded credentials. Read from environment variables at runtime.
# Override by passing app_key / app_secret explicitly in run_skill(params) or CLI.

_ENV_APP_KEY = "KUJIALE_APP_KEY"
_ENV_APP_SECRET = "KUJIALE_APP_SECRET"


def _require(condition, message):
  """Raise RuntimeError with a stable user-facing message when condition is false."""
  if not condition:
    raise RuntimeError(message)


def _resolve_credentials(app_key=None, app_secret=None):
  """
  Resolve app_key and app_secret from (in priority order):
    1. Explicit argument value
    2. Environment variable KUJIALE_APP_KEY / KUJIALE_APP_SECRET
  Raises ValueError if either is still missing.
  """
  app_key = app_key or os.environ.get(_ENV_APP_KEY, "").strip() or None
  app_secret = app_secret or os.environ.get(_ENV_APP_SECRET, "").strip() or None

  missing = []
  if not app_key:
    missing.append("app_key (env: {})".format(_ENV_APP_KEY))
  if not app_secret:
    missing.append("app_secret (env: {})".format(_ENV_APP_SECRET))
  if missing:
    raise ValueError(
      "Missing required credentials: {}.\n"
      "Set environment variables or pass via --app-key / --app-secret.\n"
      "See .env.example for reference.".format(", ".join(missing))
    )
  return app_key, app_secret


# ---------------------------------------------------------------------------
# Endpoint constants (from doc app_id=1)
STS_URL = "https://openapi.kujiale.com/v2/commodity/upload/sts"
TRIGGER_URL = "https://openapi.kujiale.com/v2/commodity/upload/create"
STATUS_URL = "https://openapi.kujiale.com/v2/commodity/upload/status"
SUBMIT_URL = "https://openapi.kujiale.com/v2/commodity/upload/submit"

# Step 5 model params - master account, node 215 path
# location=1 (floor furniture), brandCats=["3FO4K6E984C7"] (default brand cat)
DEFAULT_LOCATION = 1
DEFAULT_BRAND_CAT = "3FO4K6E984C7"

POLL_INTERVAL = 5.0  # seconds between status polls
POLL_TIMEOUT = 300.0  # max seconds to wait for parse (5 min)


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def _sign(app_key, app_secret):
  """Return (timestamp_ms_str, md5_sign)."""
  ts = str(int(time.time() * 1000))
  raw = app_secret + app_key + ts
  sign = hashlib.md5(raw.encode("utf-8")).hexdigest()
  return ts, sign


def _auth_params(app_key, app_secret):
  ts, sign = _sign(app_key, app_secret)
  return {"appkey": app_key, "timestamp": ts, "sign": sign}


def _signed_url(base, app_key, app_secret, extra=None):
  params = _auth_params(app_key, app_secret)
  if extra:
    params.update(extra)
  return base + "?" + urllib.parse.urlencode(params)


# ---------------------------------------------------------------------------
# Test ZIP creation
# ---------------------------------------------------------------------------

def _create_test_zip(path="test_model_for_api_test.zip"):
  """
  Create a minimal ZIP containing a dummy file.
  Returns the local path.
  """
  if not os.path.exists(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
      zf.writestr("model.txt", "test model placeholder\n")
    print("[INFO] Created test zip: {}".format(path))
  return path


def _validate_zip_path(zip_path):
  """Validate the ZIP path before upload and return the normalized path."""
  _require(bool(zip_path), "zip_path is required")
  _require(os.path.exists(zip_path), "ZIP file not found: {}".format(zip_path))
  _require(os.path.isfile(zip_path), "ZIP path is not a file: {}".format(zip_path))
  _require(zip_path.lower().endswith(".zip"), "ZIP file must end with .zip: {}".format(zip_path))
  return zip_path


def _parse_json_response(resp, step_name):
  """Parse JSON and raise a stable error if the payload is invalid."""
  try:
    return resp.json()
  except Exception as exc:
    raise RuntimeError(
      "{} returned non-JSON response: {}".format(step_name, resp.text[:300])
    ) from exc


def _new_requests_session():
  """
  Create a requests Session that ignores proxy / certificate env overrides.
  In some Windows environments, trust_env=True causes TLS handshake failures
  for Kujiale and OSS endpoints even though direct SSL connections succeed.
  """
  session = requests.Session()  # type: ignore[union-attr]
  session.trust_env = False
  return session


def _new_oss_session():
  """Create an oss2 session backed by a requests Session with trust_env disabled."""
  session = oss2.Session()  # type: ignore[union-attr]
  session.session.trust_env = False
  return session


def _looks_like_network_sandbox_error(message):
  """
  Return True when an exception message looks like outbound network access
  was blocked by the current runtime, which is common in agent sandboxes.
  """
  text = (message or "").lower()
  patterns = (
    r"winerror 10013",
    r"permission denied",
    r"access.*socket",
    r"operation not permitted",
    r"failed to establish a new connection",
  )
  return any(re.search(pattern, text) for pattern in patterns)


def _format_request_failure(step_name, exc):
  """Normalize network failures into an actionable user-facing message."""
  message = str(exc)
  if _looks_like_network_sandbox_error(message):
    return (
      "{} request failed: outbound network access appears to be blocked by the current "
      "runtime or sandbox (original error: {}). Re-run the same command with unrestricted "
      "network access, or allow the agent/tool to escalate network permissions."
    ).format(step_name, message)
  return "{} request failed: {}".format(step_name, message)


def _raise_request_failure(step_name, exc):
  raise RuntimeError(_format_request_failure(step_name, exc)) from exc


# ---------------------------------------------------------------------------
# Step 1: STS
# ---------------------------------------------------------------------------

def step1_get_sts(filename, app_key, app_secret):
  """
  GET /v2/commodity/upload/sts (query param: file_name=<filename>)
  Returns the 'd' dict: accessKeyId, accessKeySecret, securityToken,
  bucket, filePath, region, uploadTaskId, expiration
  """
  url = _signed_url(STS_URL, app_key, app_secret, extra={"file_name": filename})

  print("[Step 1] GET {} file_name={}".format(STS_URL, filename))
  session = _new_requests_session()
  try:
    resp = session.get(url, timeout=15)
  except Exception as exc:
    _raise_request_failure("Step 1", exc)
  _require(resp.status_code == 200, "Step 1 HTTP {}: {}".format(resp.status_code, resp.text[:300]))

  payload = _parse_json_response(resp, "Step 1")
  _require(
    str(payload.get("c")) == "0",
    "Step 1 error: c={} m={} d={}".format(payload.get("c"), payload.get("m"), payload.get("d")),
  )

  data = payload["d"]
  for field in ("accessKeyId", "accessKeySecret", "securityToken",
                "bucket", "filePath", "region", "uploadTaskId"):
    _require(data.get(field), "Step 1 missing field: {}".format(field))

  print("[Step 1] OK uploadTaskId={} filePath={}".format(data["uploadTaskId"], data["filePath"]))
  return data


# ---------------------------------------------------------------------------
# Step 2: OSS PUT
# ---------------------------------------------------------------------------

def step2_oss_put(local_path, sts_data):
  """
  PUT file bytes to Alibaba OSS via STS credentials.
  """
  file_size = os.path.getsize(local_path)
  endpoint = "https://oss-{}.aliyuncs.com".format(sts_data["region"])
  print("[Step 2] OSS PUT endpoint={} bucket={} key={} size={}".format(
    endpoint, sts_data["bucket"], sts_data["filePath"], file_size))

  auth = oss2.StsAuth(sts_data["accessKeyId"],  # type: ignore[union-attr]
                      sts_data["accessKeySecret"],
                      sts_data["securityToken"])
  bucket = oss2.Bucket(  # type: ignore[union-attr]
    auth,
    endpoint,
    sts_data["bucket"],
    session=_new_oss_session(),
  )

  try:
    with open(local_path, "rb") as f:
      result = bucket.put_object(sts_data["filePath"], f)
  except Exception as exc:
    _raise_request_failure("Step 2 OSS PUT", exc)

  _require(result.status == 200, "Step 2 OSS PUT status={}".format(result.status))
  print("[Step 2] OK status={} etag={}".format(result.status, result.etag))


# ---------------------------------------------------------------------------
# Step 3: Trigger parse
# ---------------------------------------------------------------------------

def step3_trigger(upload_task_id, app_key, app_secret):
  """
  POST /v2/commodity/upload/create (requestParam: upload_task_id)
  Note: params go as query parameters, NOT request body.
  Expected response: {"c":"0","m":""}
  """
  url = _signed_url(TRIGGER_URL, app_key, app_secret,
                    extra={"upload_task_id": upload_task_id})

  print("[Step 3] POST {} upload_task_id={}".format(TRIGGER_URL, upload_task_id))
  session = _new_requests_session()
  try:
    resp = session.post(url, timeout=15)
  except Exception as exc:
    _raise_request_failure("Step 3", exc)
  _require(resp.status_code == 200, "Step 3 HTTP {}: {}".format(resp.status_code, resp.text[:300]))

  payload = _parse_json_response(resp, "Step 3")
  _require(
    str(payload.get("c")) == "0",
    "Step 3 error: c={} m={} d={}".format(payload.get("c"), payload.get("m"), payload.get("d")),
  )

  print("[Step 3] OK m={}".format(payload.get("m")))


# ---------------------------------------------------------------------------
# Step 4: Poll parse status
# ---------------------------------------------------------------------------

def step4_poll_status(upload_task_id, app_key, app_secret,
                      poll_interval=POLL_INTERVAL, poll_timeout=POLL_TIMEOUT):
  """
  GET /v2/commodity/upload/status polling until status == 3 (zip parse success).

  Status codes:
    0 = Generating
    1 = Parsing ZIP
    2 = ZIP parse failed
    3 = ZIP parse success (ready to submit) <- SUCCESS: ready for Step 5
    4 = Submit success
    5 = Submit task exception

  Returns the 'd' dict from the last successful response.
  """
  deadline = time.time() + poll_timeout
  attempt = 0

  print("[Step 4] Polling status for uploadTaskId={} (timeout={}s)".format(
    upload_task_id, poll_timeout))

  while True:
    attempt += 1
    if time.time() > deadline:
      raise RuntimeError(
        "Step 4 poll timeout after {}s (last attempt #{})".format(poll_timeout, attempt))

    url = _signed_url(STATUS_URL, app_key, app_secret, extra={
      "upload_task_id": upload_task_id,
      "show_image": "true",
    })

    session = _new_requests_session()
    try:
      resp = session.get(url, timeout=15)
    except Exception as exc:
      if _looks_like_network_sandbox_error(str(exc)):
        _raise_request_failure("Step 4", exc)
      print("[Step 4] Request error (retry in {}s): {}".format(poll_interval, exc))
      time.sleep(poll_interval)
      continue

    if resp.status_code != 200:
      print("[Step 4] HTTP {} (retry)".format(resp.status_code))
      time.sleep(poll_interval)
      continue

    try:
      payload = _parse_json_response(resp, "Step 4")
    except RuntimeError as exc:
      print("[Step 4] {} (retry)".format(exc))
      time.sleep(poll_interval)
      continue

    if str(payload.get("c")) != "0":
      raise RuntimeError(
        "Step 4 API error: c={} m={}".format(payload.get("c"), payload.get("m")))

    data = payload.get("d") or {}
    status = data.get("status")

    print("[Step 4] Attempt {} status={}".format(attempt, status))

    if status == 3:
      # ZIP parse success, ready to submit
      print("[Step 4] OK status=3 (zip parse success, ready to submit) "
            "previewImg={}".format(data.get("previewImg")))
      return data
    elif status == 2:
      raise RuntimeError("Step 4 FAILED: status=2 (zip parse failed)")
    elif status == 5:
      raise RuntimeError("Step 4 FAILED: status=5 (submit task exception)")
    else:
      # 0=Generating, 1=Parsing — keep waiting
      time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Step 5: Submit model (master account)
# ---------------------------------------------------------------------------

def step5_submit(upload_task_id, model_name, app_key, app_secret,
                 location=DEFAULT_LOCATION, brand_cat=DEFAULT_BRAND_CAT,
                 prod_cat=None):
  """
  POST /v2/commodity/upload/submit (application/json body)
  Returns brandGoodId (the Kujiale model asset ID).

  Response: {"c":"0","d":{"uploadResult":[{"brandGoodId":"xxx","successFlag":true,...}]}}
  """
  body_list = [{
    "uploadTaskId": upload_task_id,
    "name": model_name,
    "location": location,
    "brandCats": [brand_cat],
  }]
  if prod_cat is not None:
    body_list[0]["prodCat"] = prod_cat

  url = _signed_url(SUBMIT_URL, app_key, app_secret)
  headers = {"Content-Type": "application/json;charset=utf-8"}
  body_bytes = json.dumps(body_list, ensure_ascii=False).encode("utf-8")

  print("[Step 5] POST {} name={} uploadTaskId={}".format(SUBMIT_URL, model_name, upload_task_id))
  session = _new_requests_session()
  try:
    resp = session.post(url, data=body_bytes, headers=headers, timeout=30)
  except Exception as exc:
    _raise_request_failure("Step 5", exc)
  _require(resp.status_code == 200, "Step 5 HTTP {}: {}".format(resp.status_code, resp.text[:300]))

  payload = _parse_json_response(resp, "Step 5")
  _require(
    str(payload.get("c")) == "0",
    "Step 5 error: c={} m={} d={}".format(payload.get("c"), payload.get("m"), payload.get("d")),
  )

  result_data = payload.get("d") or {}
  upload_result = result_data.get("uploadResult") or []
  _require(upload_result, "Step 5: uploadResult list is empty: d={}".format(result_data))

  item = upload_result[0]
  success_flag = item.get("successFlag")
  brand_good_id = item.get("brandGoodId")

  _require(
    success_flag,
    "Step 5: successFlag=False for uploadTaskId={}. item={}".format(upload_task_id, item),
  )
  _require(brand_good_id, "Step 5: brandGoodId missing. item={}".format(item))

  print("[Step 5] OK brandGoodId={} successFlag={}".format(brand_good_id, success_flag))
  return brand_good_id


# ---------------------------------------------------------------------------
# Full flow
# ---------------------------------------------------------------------------

def run_full_flow(app_key, app_secret, zip_path,
                  poll_interval=POLL_INTERVAL, poll_timeout=POLL_TIMEOUT):
  """
  Executes all 5 steps and returns a summary dict with:
    uploadTaskId, filePath, previewImg, brandGoodId
  Raises AssertionError or RuntimeError on any failure.
  """
  print("=" * 60)
  print("Kujiale OpenAPI Full Flow")
  print("appKey={} zip={}".format(app_key, zip_path))
  print("=" * 60)

  filename = os.path.basename(zip_path)
  model_name = os.path.splitext(filename)[0]

  # Step 1
  sts_data = step1_get_sts(filename, app_key, app_secret)

  # Step 2
  step2_oss_put(zip_path, sts_data)

  upload_task_id = sts_data["uploadTaskId"]

  # Step 3
  step3_trigger(upload_task_id, app_key, app_secret)

  # Step 4
  status_data = step4_poll_status(
    upload_task_id, app_key, app_secret,
    poll_interval=poll_interval, poll_timeout=poll_timeout,
  )
  preview_img = status_data.get("previewImg") or ""

  # Step 5
  brand_good_id = step5_submit(
    upload_task_id=upload_task_id,
    model_name=model_name,
    app_key=app_key,
    app_secret=app_secret,
  )

  summary = {
    "uploadTaskId": upload_task_id,
    "filePath": sts_data["filePath"],
    "previewImg": preview_img,
    "brandGoodId": brand_good_id,
  }

  print()
  print("=" * 60)
  print("ALL STEPS PASSED")
  print(json.dumps(summary, ensure_ascii=False, indent=2))
  print("=" * 60)
  return summary


# ---------------------------------------------------------------------------
# Dry-run mock (no network calls)
# ---------------------------------------------------------------------------

def _run_dry(params):
  """
  Simulate the full flow without any network calls.
  Returns a mock summary dict with dry_run=True.
  Used when params['dry_run'] is True.
  """
  app_key = params.get("app_key") or os.environ.get(_ENV_APP_KEY, "").strip() or "DRY_RUN_KEY"
  zip_path = params.get("zip_path") or "test_model_for_api_test.zip"
  filename = os.path.basename(zip_path)

  print("[DRY RUN] Simulating full flow (no network calls)")
  print("[DRY RUN] app_key={} zip={}".format(app_key, zip_path))

  # Simulate test ZIP creation
  if not os.path.exists(zip_path):
    print("[DRY RUN] Would create test zip: {}".format(zip_path))
  else:
    print("[DRY RUN] Zip exists: {}".format(zip_path))

  print("[DRY RUN] Step 1 — would GET STS credentials")
  print("[DRY RUN] Step 2 — would PUT to Alibaba OSS")
  print("[DRY RUN] Step 3 — would POST trigger parse")
  print("[DRY RUN] Step 4 — would poll status until status==3")
  print("[DRY RUN] Step 5 — would POST submit model")

  summary = {
    "uploadTaskId": "DRY_RUN_TASK_ID",
    "filePath": "dry_run/path/{}".format(filename),
    "previewImg": "",
    "brandGoodId": "DRY_RUN_BRAND_GOOD_ID",
    "dry_run": True,
  }
  print()
  print("[DRY RUN] Mock summary:")
  print(json.dumps(summary, ensure_ascii=False, indent=2))
  return summary


# ---------------------------------------------------------------------------
# run_skill — programmatic entrypoint
# ---------------------------------------------------------------------------

def run_skill(params):
  """
  Programmatic entrypoint for the kujiale-openapi-flow skill.

  Accepts a configuration dict with any of the following keys
  (app_key and app_secret are required unless dry_run=True):

    app_key (str)       Kujiale OpenAPI appKey
    app_secret (str)    Kujiale OpenAPI appSecret
    zip_path (str)      Local path to ZIP file (auto-created if omitted)
    poll_interval (float) Seconds between status polls [default: 5.0]
    poll_timeout (float)  Max seconds to wait for parse [default: 300.0]
    dry_run (bool)      If True, skip network and return mock summary

  Returns a dict:
    {
      "uploadTaskId": str,
      "filePath": str,
      "previewImg": str,
      "brandGoodId": str,
      "dry_run": bool  # only present when dry_run=True
    }

  Raises:
    ImportError if requests or oss2 is not installed (real run only)
    ValueError on missing credentials
    RuntimeError on parse failure, poll timeout, or network/TLS issues
  """
  if params.get("dry_run"):
    return _run_dry(params)

  # Validate dependencies for real run
  if not _HAS_REQUESTS:
    raise ImportError("'requests' not installed. Run: pip install requests")
  if not _HAS_OSS2:
    raise ImportError("'oss2' not installed. Run: pip install oss2")

  app_key, app_secret = _resolve_credentials(
    params.get("app_key"), params.get("app_secret")
  )
  poll_interval = float(params.get("poll_interval", POLL_INTERVAL))
  poll_timeout = float(params.get("poll_timeout", POLL_TIMEOUT))
  zip_path = params.get("zip_path") or _create_test_zip()
  zip_path = _validate_zip_path(zip_path)
  _require(poll_interval > 0, "poll_interval must be > 0")
  _require(poll_timeout > 0, "poll_timeout must be > 0")

  return run_full_flow(
    app_key=app_key,
    app_secret=app_secret,
    zip_path=zip_path,
    poll_interval=poll_interval,
    poll_timeout=poll_timeout,
  )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
  parser = argparse.ArgumentParser(
    description="Validate the complete 1->5 Kujiale OpenAPI model upload chain.",
  )
  parser.add_argument("--app-key", default=None,
                      help="Kujiale OpenAPI appKey. Falls back to env var {}.".format(_ENV_APP_KEY))
  parser.add_argument("--app-secret", default=None,
                      help="Kujiale OpenAPI appSecret. Falls back to env var {}.".format(_ENV_APP_SECRET))
  parser.add_argument("--zip", default=None,
                      help="Path to a ZIP file to upload (a minimal test ZIP is created if omitted)")
  parser.add_argument("--poll-interval", type=float, default=POLL_INTERVAL,
                      help="Seconds between status polls (default: {})".format(POLL_INTERVAL))
  parser.add_argument("--poll-timeout", type=float, default=POLL_TIMEOUT,
                      help="Max seconds to wait for parse (default: {})".format(POLL_TIMEOUT))
  parser.add_argument("--dry-run", action="store_true", default=False,
                      help="Simulate all steps without making any network calls")
  args = parser.parse_args()

  if not args.dry_run:
    if not _HAS_REQUESTS:
      print("ERROR: 'requests' not installed. Run: pip install requests", file=sys.stderr)
      return 1
    if not _HAS_OSS2:
      print("ERROR: 'oss2' not installed. Run: pip install oss2", file=sys.stderr)
      return 1

  params = {
    "app_key": args.app_key,
    "app_secret": args.app_secret,
    "zip_path": args.zip,
    "poll_interval": args.poll_interval,
    "poll_timeout": args.poll_timeout,
    "dry_run": args.dry_run,
  }

  try:
    run_skill(params)
    return 0
  except (ValueError, RuntimeError, ImportError) as exc:
    print("\nFAILED: {}".format(exc), file=sys.stderr)
    return 1


if __name__ == "__main__":
  raise SystemExit(main())