"""Submit feedback anonymously with a persistent, content-free retry receipt."""

import hashlib
import json
import sys
import uuid
from urllib.parse import urlparse

from echo_cli.credentials import atomic_json


def submit(api, args):
    if args.text_file is not None:
        if args.text_file.stat().st_size > 20000:
            raise RuntimeError("Feedback file exceeds 20000 bytes")
        content = args.text_file.read_text(encoding="utf-8")
    else:
        content = args.text
    body = {"text": content, "work_url": args.work_url, "contact": args.contact}
    for key, maximum in (("text", 5000), ("work_url", 2048), ("contact", 240)):
        value = body[key]
        if value is not None and (
            not value.strip()
            or len(value) > maximum
            or "\x00" in value
            or any(0xD800 <= ord(c) <= 0xDFFF for c in value)
        ):
            raise RuntimeError(
                "Feedback %s must be nonblank and at most %s characters" % (key, maximum)
            )
    if args.work_url:
        parsed = urlparse(args.work_url)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or any(c.isspace() or ord(c) < 32 for c in args.work_url)
        ):
            raise RuntimeError("Use an HTTP(S) work link without credentials")
    fingerprint = hashlib.sha256(
        json.dumps(body, ensure_ascii=True, sort_keys=True).encode("utf-8")
    ).hexdigest()
    # Include the origin; one config directory may contain several instances.
    origin = hashlib.sha256(api.server.encode("utf-8")).hexdigest()[:16]
    key = str(args.operation_id) if args.operation_id else fingerprint
    receipt = api.store.path.parent / ("feedback-%s-%s.json" % (origin, key))
    with api.store.lock():
        if receipt.is_symlink():
            raise RuntimeError("Feedback receipt must not be a symlink")
        record = json.loads(receipt.read_text()) if receipt.exists() else None
        if record and record["request_hash"] != fingerprint:
            raise RuntimeError("Keep the original feedback for this operation ID")
        if record is None:
            record = {
                "operation_id": str(args.operation_id or uuid.uuid4()),
                "request_hash": fingerprint,
            }
            atomic_json(receipt, record)
    print("operation_id=" + record["operation_id"], file=sys.stderr)
    return api.request(
        "POST",
        "/v1/hosting/feedback",
        json=body,
        headers={"Idempotency-Key": record["operation_id"]},
    )
