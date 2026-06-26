"""
JEPCodec — Strict Protocol Layer
JEP-04 (draft-wang-jep-judgment-event-protocol-04) + JAC-01 (draft-wang-jac-01)
"""
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .types import JEP04Event, Verb


class JEPCodec:
    PROTOCOL_VERSION = "1"
    HASH_PREFIX = "sha256:"
    CLOCK_SKEW_TOLERANCE = 300

    @staticmethod
    def encode(event: JEP04Event) -> str:
        payload = {
            "jep": event.jep,
            "verb": event.verb.value,
            "who": event.who,
            "when": event.when,
            "what": event.what,
            "nonce": event.nonce,
            "aud": event.aud,
            "ref": event.ref,
            "sig": event.sig,
        }
        if event.task_based_on is not None:
            payload["task_based_on"] = event.task_based_on
        if event.extensions is not None:
            payload["extensions"] = event.extensions
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)

    @staticmethod
    def decode(raw: str) -> JEP04Event:
        payload = json.loads(raw)
        return JEP04Event(
            jep=payload.get("jep", "1"),
            verb=Verb(payload.get("verb", "J")),
            who=payload["who"],
            when=payload["when"],
            what=payload.get("what"),
            nonce=payload["nonce"],
            aud=payload.get("aud"),
            ref=payload.get("ref"),
            sig=payload.get("sig", ""),
            task_based_on=payload.get("task_based_on"),
            extensions=payload.get("extensions"),
        )

    @staticmethod
    def compute_what(data: Dict[str, Any]) -> str:
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return f"{JEPCodec.HASH_PREFIX}{digest}"

    @staticmethod
    def generate_nonce() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def iso_to_unix(iso_timestamp: str) -> int:
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp())

    @staticmethod
    def unix_to_iso(unix_ts: int) -> str:
        dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
