"""
Nostr DM primitives for NIP-AA agents.

Supports NIP-04 (deprecated but widely used) and NIP-44 (modern) encrypted
direct messages.  Agents use DMs for:
  - Guardian communication
  - Contract negotiation
  - Peer-to-peer coordination
  - Receiving citizenship notifications
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DirectMessage:
    """A decrypted Nostr DM."""
    sender_pubkey: str
    recipient_pubkey: str
    content: str
    timestamp: int
    event_id: str = ""
    nip_version: str = "nip-04"  # "nip-04" or "nip-44"


class NostrDM:
    """
    Nostr DM handler for NIP-AA agents.

    Provides encrypt/decrypt for NIP-04, event construction for sending DMs,
    and relay interaction for receiving DMs.

    Usage:
        dm = NostrDM(agent_pubkey_hex, agent_privkey_hex)
        encrypted = dm.encrypt_nip04(recipient_pubkey, "hello")
        event = dm.build_dm_event(recipient_pubkey, "hello")
        dm.send(relay_url, event)
    """

    def __init__(
        self,
        agent_pubkey_hex: str,
        agent_privkey_hex: str,
        relay_urls: list[str] | None = None,
    ):
        self.agent_pubkey_hex = agent_pubkey_hex
        self.agent_privkey_hex = agent_privkey_hex
        self.relay_urls = relay_urls or [
            "wss://relay.damus.io",
            "wss://relay.primal.net",
            "wss://nos.lol",
        ]

    # ── NIP-04 encryption (kind 4) ───────────────────────────────────────

    def encrypt_nip04(self, recipient_pubkey_hex: str, plaintext: str) -> str:
        """
        Encrypt a message using NIP-04 (AES-256-CBC with shared ECDH secret).

        Returns: base64(ciphertext) + "?iv=" + base64(iv)

        Uses coincurve for ECDH if available; falls back to the cryptography
        package alone.
        """
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives.padding import PKCS7

        shared_key = self._nip04_shared_key(recipient_pubkey_hex)

        # AES-256-CBC
        iv = os.urandom(16)
        padder = PKCS7(128).padder()
        padded = padder.update(plaintext.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return base64.b64encode(ciphertext).decode() + "?iv=" + base64.b64encode(iv).decode()

    def decrypt_nip04(self, sender_pubkey_hex: str, encrypted: str) -> str:
        """
        Decrypt a NIP-04 encrypted message.

        Expects format: base64(ciphertext)?iv=base64(iv)

        Uses coincurve for ECDH if available; falls back to the cryptography
        package alone (secp256k1 ECDH is supported there as well).
        """
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives.padding import PKCS7

        parts = encrypted.split("?iv=")
        if len(parts) != 2:
            raise ValueError("Invalid NIP-04 ciphertext format")

        ciphertext = base64.b64decode(parts[0])
        iv = base64.b64decode(parts[1])

        shared_key = self._nip04_shared_key(sender_pubkey_hex)

        # AES-256-CBC decrypt
        cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = PKCS7(128).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
        return plaintext.decode()

    # ── Event construction ────────────────────────────────────────────────

    def build_dm_event(
        self,
        recipient_pubkey_hex: str,
        plaintext: str,
        nip_version: str = "nip-04",
    ) -> dict[str, Any]:
        """
        Build a DM event ready for relay publication.

        nip_version: "nip-04" uses kind 4; "nip-44" uses kind 1059 (gift wrap).
        Currently only NIP-04 is fully implemented.
        """
        if nip_version == "nip-04":
            encrypted_content = self.encrypt_nip04(recipient_pubkey_hex, plaintext)
            kind = 4
        else:
            raise NotImplementedError(
                "NIP-44 gift wrap not yet implemented — use nip-04 for now"
            )

        event = {
            "pubkey": self.agent_pubkey_hex,
            "created_at": int(time.time()),
            "kind": kind,
            "tags": [["p", recipient_pubkey_hex]],
            "content": encrypted_content,
        }
        event["id"] = self._compute_id(event)
        event["sig"] = self._sign(event["id"])
        return event

    # ── Relay interaction ─────────────────────────────────────────────────

    def send(self, relay_url: str, event: dict[str, Any]) -> bool:
        """Publish a signed event to a single relay via WebSocket."""
        try:
            import websocket
        except ImportError:
            logger.error("websocket-client required for relay communication")
            return False

        try:
            ws = websocket.create_connection(relay_url, timeout=10)
            message = json.dumps(["EVENT", event])
            ws.send(message)
            response = ws.recv()
            ws.close()
            logger.info("Sent event %s to %s: %s", event["id"][:16], relay_url, response)
            return True
        except Exception as exc:
            logger.error("Failed to send to %s: %s", relay_url, exc)
            return False

    def send_to_all_relays(self, event: dict[str, Any]) -> dict[str, bool]:
        """Publish event to all configured relays. Returns {relay: success}."""
        results = {}
        for relay_url in self.relay_urls:
            results[relay_url] = self.send(relay_url, event)
        return results

    def fetch_dms(
        self,
        relay_url: str,
        since: int | None = None,
        limit: int = 50,
    ) -> list[DirectMessage]:
        """
        Fetch and decrypt DMs addressed to this agent from a relay.

        Returns decrypted DirectMessage objects sorted by timestamp.
        """
        try:
            import websocket
        except ImportError:
            logger.error("websocket-client required for relay communication")
            return []

        filters: dict[str, Any] = {
            "kinds": [4],
            "#p": [self.agent_pubkey_hex],
            "limit": limit,
        }
        if since:
            filters["since"] = since

        try:
            ws = websocket.create_connection(relay_url, timeout=15)
            sub_id = hashlib.sha256(os.urandom(16)).hexdigest()[:16]
            ws.send(json.dumps(["REQ", sub_id, filters]))

            messages: list[DirectMessage] = []
            while True:
                raw = ws.recv()
                data = json.loads(raw)
                if data[0] == "EOSE":
                    break
                if data[0] == "EVENT" and len(data) >= 3:
                    event = data[2]
                    try:
                        plaintext = self.decrypt_nip04(
                            event["pubkey"], event["content"]
                        )
                        messages.append(DirectMessage(
                            sender_pubkey=event["pubkey"],
                            recipient_pubkey=self.agent_pubkey_hex,
                            content=plaintext,
                            timestamp=event["created_at"],
                            event_id=event.get("id", ""),
                            nip_version="nip-04",
                        ))
                    except Exception as exc:
                        logger.warning("Failed to decrypt DM %s: %s", event.get("id", "?"), exc)

            ws.close()
            messages.sort(key=lambda m: m.timestamp)
            return messages

        except Exception as exc:
            logger.error("Failed to fetch DMs from %s: %s", relay_url, exc)
            return []

    # ── Internal ──────────────────────────────────────────────────────────

    def _nip04_shared_key(self, their_pubkey_hex: str) -> bytes:
        """
        Return the 32-byte NIP-04 shared key: x-coordinate of the ECDH point.

        NIP-04 spec: shared_key = x-coordinate of (privkey * their_pubkey).
        Note: coincurve's ecdh() returns sha256(compressed_point), which is
        non-standard; we use point multiplication instead to get the raw x.

        Tries coincurve first; falls back to the cryptography package so the
        skill works in environments where coincurve is not installed.
        """
        compressed = bytes.fromhex("02" + their_pubkey_hex)
        try:
            from coincurve import PrivateKey, PublicKey
            sk = PrivateKey(bytes.fromhex(self.agent_privkey_hex))
            # Point multiplication gives the shared point; x is bytes [1:33]
            shared_point = PublicKey(compressed).multiply(sk.secret)
            return shared_point.format(compressed=True)[1:]
        except ImportError:
            pass

        # Fallback: cryptography package only
        from cryptography.hazmat.primitives.asymmetric.ec import (
            ECDH,
            EllipticCurvePublicKey,
            SECP256K1,
            derive_private_key,
        )
        from cryptography.hazmat.backends import default_backend

        privkey_int = int(self.agent_privkey_hex, 16)
        private_key = derive_private_key(privkey_int, SECP256K1(), default_backend())
        public_key = EllipticCurvePublicKey.from_encoded_point(SECP256K1(), compressed)
        # exchange() returns the raw x-coordinate of the shared point
        return private_key.exchange(ECDH(), public_key)

    def _compute_id(self, event: dict[str, Any]) -> str:
        serialised = json.dumps(
            [0, event["pubkey"], event["created_at"], event["kind"],
             event["tags"], event["content"]],
            separators=(",", ":"),
            ensure_ascii=False,
        )
        return hashlib.sha256(serialised.encode()).hexdigest()

    def _sign(self, event_id_hex: str) -> str:
        try:
            from coincurve import PrivateKey
            sk = PrivateKey(bytes.fromhex(self.agent_privkey_hex))
            sig = sk.sign_schnorr(bytes.fromhex(event_id_hex))
            return sig.hex()
        except Exception:
            return ""
