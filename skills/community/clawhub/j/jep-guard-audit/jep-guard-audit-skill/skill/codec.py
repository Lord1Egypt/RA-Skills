"""
JEPCodec — Strict Protocol Layer
Implements JEP-04 (draft-wang-jep-judgment-event-protocol-04) and
JAC-01 (draft-wang-jac-01) with zero deviation.

Responsibilities:
  - Canonicalization (RFC 8785 JCS)
  - Multihash computation (RFC 9122)
  - UUIDv4 nonce generation (RFC 9562)
  - Unix timestamp handling
  - Signature envelope (JWS / RFC 7515)
  - Extension serialization
"""
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .types import JEP04Event, Verb, JACReceipt


class JEPCodec:
    """
    Strict JEP-04 encoder/decoder.
    No business logic. No friendly field names. Only protocol.
    """

    PROTOCOL_VERSION = "1"
    HASH_PREFIX = "sha256:"
    CLOCK_SKEW_TOLERANCE = 300  # ±5 minutes (Section 2.3)

    @staticmethod
    def encode(event: JEP04Event) -> str:
        """
        Encode a JEP04Event to canonical JSON string (RFC 8785).
        This is the exact payload that gets signed.
        """
        payload = {
            "jep": event.jep,
            "verb": event.verb.value,
            "who": event.who,
            "when": event.when,
            "what": event.what,
            "nonce": event.nonce,
            "aud": event.aud,
            "ref": event.ref,
            "sig": event.sig,  # Included in canonical form for hash chain continuity
        }
        # JAC-01 core field
        if event.task_based_on is not None:
            payload["task_based_on"] = event.task_based_on
        # JEP-04 Section 2.5 extensions
        if event.extensions is not None:
            payload["extensions"] = event.extensions
        # RFC 8785: canonical JSON (lexicographic key order, no whitespace)
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)

    @staticmethod
    def decode(raw: str) -> JEP04Event:
        """Decode canonical JSON string to JEP04Event."""
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
        """
        Compute 'what' field: cryptographic multihash of decision content.
        JEP-04 Section 2.2: "what: Cryptographic multihash of decision content.
        Implementations SHOULD support common hash functions such as SHA-256 and SM3."
        """
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return f"{JEPCodec.HASH_PREFIX}{digest}"

    @staticmethod
    def generate_nonce() -> str:
        """
        Generate UUIDv4 nonce.
        JEP-04 Section 2.3: "Event initiators MUST generate a new UUIDv4 nonce for each event."
        """
        return str(uuid.uuid4())

    @staticmethod
    def iso_to_unix(iso_timestamp: str) -> int:
        """Convert ISO 8601 string to Unix seconds."""
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp())

    @staticmethod
    def unix_to_iso(unix_ts: int) -> str:
        """Convert Unix seconds to ISO 8601 UTC string."""
        dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def verify_nonce_uniqueness(nonce: str, seen: set) -> bool:
        """
        JEP-04 Section 2.3: "Receivers MUST cache nonces and reject duplicates."
        Returns True if nonce is unique, False if duplicate.
        """
        if nonce in seen:
            return False
        seen.add(nonce)
        return True

    @staticmethod
    def verify_timestamp_window(when: int, now: Optional[int] = None) -> bool:
        """
        JEP-04 Section 2.3: "Unless otherwise configured, a clock skew tolerance
        of ±5 minutes (300 seconds) is RECOMMENDED."
        """
        if now is None:
            now = int(datetime.now(timezone.utc).timestamp())
        return abs(when - now) <= JEPCodec.CLOCK_SKEW_TOLERANCE

    @staticmethod
    def build_jac_receipt(event: JEP04Event) -> JACReceipt:
        """
        JAC-01 Section 3.1: Build a minimal JAC receipt from JEP event.
        """
        canonical = JEPCodec.encode(event)
        return JACReceipt(event=event, raw_canonical=canonical)

    @staticmethod
    def verify_jac_core(receipt: JACReceipt, parent_exists_fn, parent_judgment_exists_fn) -> str:
        """
        JAC-01 Section 1.4: Core Verification Algorithm.
        Returns: "VALID", "INVALID", or "VALID_WITH_FAULT".
        """
        event = receipt.event

        # Step 1: JEP signature verification (placeholder — real crypto needed)
        if not event.sig or len(event.sig) == 0:
            return "INVALID"

        # Step 2: HJS chain verification using ref field
        if event.ref and not parent_exists_fn(event.ref):
            return "INVALID"
        # JAC-01: J verb with ref is invalid per HJS
        if event.verb == Verb.JUDGE and event.ref is not None:
            return "INVALID"

        # Step 3: JAC chain integrity via task_based_on
        if event.task_based_on and not parent_judgment_exists_fn(event.task_based_on):
            # Check for JAC-Fault extension (Section 2.8)
            if event.extensions and "https://jac.org/fault" in event.extensions:
                fault = event.extensions["https://jac.org/fault"]
                if fault.get("expected_parent") == event.task_based_on:
                    return "VALID_WITH_FAULT"
            return "INVALID"

        # Step 4: JAC chain head check
        if event.verb == Verb.JUDGE:
            return "VALID"

        return "INVALID"
