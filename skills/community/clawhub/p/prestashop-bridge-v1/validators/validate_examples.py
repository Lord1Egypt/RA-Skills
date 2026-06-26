import json, re, hashlib, hmac
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET = "a3f8b2c9d4e5f6789012345678901234567890abcdef1234567890abcdef1234"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()

REQUIRED_FILES = [
    ROOT / "SKILL.md",
    ROOT / "_meta.json",
    ROOT / "README.md",
    ROOT / "SECURITY.md",
    ROOT / "openapi.yaml",
    ROOT / ".env.bridge.example",
    ROOT / "examples.http",
    ROOT / "docs" / "environment.md",
    ROOT / "schemas" / "product-update-request.schema.json",
    ROOT / "schemas" / "product-import-request.schema.json",
    ROOT / "schemas" / "order-status-update-request.schema.json",
]

ENDPOINTS = [
    "/oauth/token",
    "/v1/products/{id}",
    "/v1/orders/{id}",
    "/v1/jobs/{jobId}",
    "/v1/jobs/products/update",
    "/v1/jobs/products/import",
    "/v1/jobs/orders/status",
]

EXPECTED_VERSION = "1.0.3"
EXPECTED_ENV_VARS = [
    "APP_ENV","BRIDGE_BASE_URL","OAUTH_CLIENT_ID","OAUTH_CLIENT_SECRET","OAUTH_TOKEN_TTL",
    "JWT_PRIVATE_KEY_PATH","JWT_PUBLIC_KEY_PATH","HMAC_SECRET_CURRENT","HMAC_SECRET_PREVIOUS",
    "REDIS_DSN","DATABASE_URL","RATE_LIMIT_READ","RATE_LIMIT_WRITE","JOB_MAX_ATTEMPTS",
    "JOB_TIMEOUT_SECONDS","IDEMPOTENCY_HTTP_TTL_SECONDS","IDEMPOTENCY_DB_RETENTION_DAYS",
    "FAILED_JOB_RETENTION_DAYS","GZIP_RECOMMENDED_ABOVE_BYTES","GZIP_REQUIRED_ABOVE_BYTES",
    "MAX_PAYLOAD_BYTES","ALLOWED_SOURCE_IPS","LOG_PATH",
]


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def compute_sig(method, uri, ts, req_id, body):
    body_hash = hashlib.sha256(body).hexdigest()
    string = "\n".join([method.upper(), uri, str(ts), req_id.lower(), body_hash])
    sig = hmac.new(SECRET.encode(), string.encode(), hashlib.sha256).hexdigest()
    return body_hash, sig


def parse_examples_http(text):
    blocks = [b.strip() for b in text.split("### ") if b.strip()]
    parsed = {}
    for block in blocks:
        lines = block.splitlines()
        title = lines[0].strip()
        parsed[title] = block
    return parsed


def main():
    for path in REQUIRED_FILES:
        require(path.exists(), f"Missing required file: {path}")

    meta = json.loads((ROOT / "_meta.json").read_text(encoding="utf-8"))
    require(meta.get("version") == EXPECTED_VERSION, "_meta.json version mismatch")
    require(meta.get("environment_file") == ".env.bridge.example", "environment file missing from metadata")
    require(meta.get("validator") == "validators/validate_examples.py", "validator path missing from metadata")
    require(meta.get("environment_variables") == EXPECTED_ENV_VARS, "environment variable list mismatch in metadata")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    openapi = (ROOT / "openapi.yaml").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(f"version: {EXPECTED_VERSION}" in skill, "SKILL.md version mismatch")
    require(f"version: {EXPECTED_VERSION}" in openapi, "openapi.yaml version mismatch")
    require(EXPECTED_VERSION in readme, "README.md version mismatch")
    require("RS256" in skill and "RS256" in openapi, "RS256 must be present in skill and OpenAPI")
    require("202 Accepted" in skill, "Skill must document 202 Accepted")
    require('source_of_truth_jobs: "mysql"' in skill, "Skill must declare MySQL as source of truth for jobs")
    for endpoint in ENDPOINTS:
        require(endpoint in openapi, f"Missing endpoint in OpenAPI: {endpoint}")

    env_text = (ROOT / ".env.bridge.example").read_text(encoding="utf-8")
    for var in EXPECTED_ENV_VARS:
        require(re.search(rf"^{re.escape(var)}=", env_text, re.M), f"Missing env var in .env.bridge.example: {var}")

    for schema_path in (ROOT / "schemas").glob("*.schema.json"):
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        require(data.get("additionalProperties") is False, f"Schema must be strict: {schema_path.name}")

    examples_text = (ROOT / "examples.http").read_text(encoding="utf-8")
    require("{computed" not in examples_text and "<computed>" not in examples_text, "examples.http contains placeholder HMAC values")

    expected = {
        "Read product 123": compute_sig("GET", "/v1/products/123", 1710950400, "9a6ea3f2-672b-4f44-a143-006f09dd4abc", b""),
        "Read order 456": compute_sig("GET", "/v1/orders/456", 1710950400, "95c1fd6a-22a4-409d-bf5b-c4fbaaf2b1d0", b""),
        "Create product update job": compute_sig("POST", "/v1/jobs/products/update", 1710950400, "f47ac10b-58cc-4372-a567-0e02b2c3d479", b'{"product_id":123,"updates":{"price_ht":25.5,"stock_delta":10},"options":{"skip_reindex":false}}'),
        "Poll job status": compute_sig("GET", "/v1/jobs/550e8400-e29b-41d4-a716-446655440000", 1710950405, "53bd8b74-7117-4c49-89e6-4ec80a9e761d", b""),
        "Create product import job": compute_sig("POST", "/v1/jobs/products/import", 1710950500, "0a4f0990-67d3-4fa2-ac3f-4cc98cb8f5b4", b'{"batch_id":"batch-2026-03-21-01","items":[{"reference":"NEW-001","name":{"fr":"Nouveau","en":"New"},"price_ht":10.0,"stock_quantity":100,"images_to_download":["https://assets.example.com/img/new-001.jpg"]}],"options":{"create_if_missing":true,"update_if_exists":true,"skip_images_errors":false}}'),
        "Create order status job": compute_sig("POST", "/v1/jobs/orders/status", 1710950600, "f717d835-a6d6-4d7e-8c44-73f1ca7e63d8", b'{"order_id":456,"new_status":"shipped","notify_customer":true,"tracking_number":"TRK123456"}'),
    }
    for title, (_body_hash, sig) in expected.items():
        require(sig in examples_text, f"Expected exact HMAC missing for block: {title}")

    for path in (ROOT / "examples").glob("*.http"):
        txt = path.read_text(encoding="utf-8")
        require("<computed>" not in txt, f"Placeholder HMAC found in {path.name}")

    print("Validation passed.")

if __name__ == "__main__":
    main()
