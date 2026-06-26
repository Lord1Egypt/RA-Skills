import base64
import json
import os
import sys
import time
import urllib.parse
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests


def _get_env_secrets() -> Dict[str, str]:
    access_key = (os.getenv("IEMAIL_ACCESS_KEY") or "").strip()
    access_key_secret = (os.getenv("IEMAIL_ACCESS_KEY_SECRET") or "").strip()
    sender = (os.getenv("IEMAIL_SENDER") or "").strip()
    out: Dict[str, str] = {}
    if access_key:
        out["access-key"] = access_key
    if access_key_secret:
        out["accessKeySecret"] = access_key_secret
    if sender:
        out["sender"] = sender
    return out


def _has_required_env_secrets() -> bool:
    env = _get_env_secrets()
    return bool(env.get("access-key") and env.get("accessKeySecret") and env.get("sender"))


def _looks_like_email(value: str) -> bool:
    v = (value or "").strip()
    return "@" in v and "." in v.split("@")[-1] and " " not in v


def _pad_pkcs5(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def _aes_ecb_encrypt(key: bytes, plaintext: bytes) -> bytes:
    try:
        from Crypto.Cipher import AES  # type: ignore
    except Exception:
        AES = None

    if AES is not None:
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(_pad_pkcs5(plaintext, 16))

    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # type: ignore
    except ImportError:
        os.system(f"{sys.executable} -m pip install cryptography -q")
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # type: ignore

    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    padded = _pad_pkcs5(plaintext, 16)
    return encryptor.update(padded) + encryptor.finalize()


def build_access_sign(access_key_secret: str, timestamp_ms: str) -> str:
    key = access_key_secret.encode("utf-8")
    if len(key) not in (16, 24, 32):
        raise ValueError("accessKeySecret length must be 16/24/32 bytes for AES key")
    ciphertext = _aes_ecb_encrypt(key, timestamp_ms.encode("utf-8"))
    b64 = base64.b64encode(ciphertext).decode("utf-8")
    return b64


def build_access_sign_urlencoded(access_key_secret: str, timestamp_ms: str) -> str:
    b64 = build_access_sign(access_key_secret, timestamp_ms)
    return urllib.parse.quote_plus(b64, safe="")


class IemailClient:
    def __init__(
        self,
        access_key: str,
        access_key_secret: str,
        base_url: str = "https://iemail-api.dmartech.cn",
        sign_mode: str = "urlencoded",
    ):
        self.access_key = access_key
        self.access_key_secret = access_key_secret
        self.base_url = base_url.rstrip("/")
        self.sign_mode = sign_mode

    def _headers(self) -> Dict[str, str]:
        ts = str(int(time.time() * 1000))
        if self.sign_mode == "raw":
            sign = build_access_sign(self.access_key_secret, ts)
        else:
            sign = build_access_sign_urlencoded(self.access_key_secret, ts)
        return {"access-key": self.access_key, "access-sign": sign, "Content-Type": "application/json"}

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self.base_url + path
        r = requests.get(url, headers=self._headers(), params=params, timeout=15)
        text = r.text
        try:
            data = json.loads(text)
        except Exception:
            raise RuntimeError(f"non-json response ({r.status_code}): {text[:500]}")

        if isinstance(data, dict) and data.get("code") == 401 and self.sign_mode == "urlencoded":
            self.sign_mode = "raw"
            r2 = requests.get(url, headers=self._headers(), params=params, timeout=15)
            text2 = r2.text
            try:
                return json.loads(text2)
            except Exception:
                raise RuntimeError(f"non-json response ({r2.status_code}): {text2[:500]}")

        return data

    def post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = self.base_url + path
        r = requests.post(url, headers=self._headers(), json=payload, timeout=15)
        text = r.text
        try:
            data = json.loads(text)
        except Exception:
            raise RuntimeError(f"non-json response ({r.status_code}): {text[:500]}")

        if isinstance(data, dict) and data.get("code") == 401 and self.sign_mode == "urlencoded":
            self.sign_mode = "raw"
            r2 = requests.post(url, headers=self._headers(), json=payload, timeout=15)
            text2 = r2.text
            try:
                return json.loads(text2)
            except Exception:
                raise RuntimeError(f"non-json response ({r2.status_code}): {text2[:500]}")

        return data


def pick_email_config_sn(cfg_resp: Dict[str, Any]) -> Optional[str]:
    data = cfg_resp.get("data") if isinstance(cfg_resp, dict) else None
    result_list = data.get("resultList") if isinstance(data, dict) else None
    if not isinstance(result_list, list) or not result_list:
        return None
    fallback = None
    for item in result_list:
        if not isinstance(item, dict):
            continue
        if fallback is None:
            fallback = item.get("sn")
        if item.get("isDefault") is True and (item.get("configType") in (None, 1)):
            return item.get("sn")
    return fallback


def pick_sender_sn(sender_resp: Dict[str, Any], preferred_from_email: Optional[str]) -> Optional[str]:
    data = sender_resp.get("data") if isinstance(sender_resp, dict) else None
    result_list = data.get("resultList") if isinstance(data, dict) else None
    if not isinstance(result_list, list) or not result_list:
        return None
    if preferred_from_email:
        pref = preferred_from_email.strip().lower()
        for item in result_list:
            if not isinstance(item, dict):
                continue
            from_email = (item.get("fromEmail") or "").strip().lower()
            if from_email and from_email == pref:
                return item.get("sn")
    first = result_list[0]
    return first.get("sn") if isinstance(first, dict) else None


def pick_reply_sn(reply_resp: Dict[str, Any]) -> Optional[str]:
    data = reply_resp.get("data") if isinstance(reply_resp, dict) else None
    result_list = data.get("resultList") if isinstance(data, dict) else None
    if not isinstance(result_list, list) or not result_list:
        return None
    first = result_list[0]
    if not isinstance(first, dict):
        return None
    reply_sn = first.get("replySn")
    return reply_sn if isinstance(reply_sn, str) else None


def send_transactional_single_email(to_email: str, subject: str, content: str) -> Dict[str, Any]:
    if not _has_required_env_secrets():
        raise ValueError("missing env: IEMAIL_ACCESS_KEY, IEMAIL_ACCESS_KEY_SECRET, IEMAIL_SENDER")
    secrets = _get_env_secrets()
    access_key = secrets.get("access-key")
    access_key_secret = secrets.get("accessKeySecret")
    preferred_sender = secrets.get("sender") or secrets.get("from") or secrets.get("fromEmail")
    if not access_key or not access_key_secret:
        raise ValueError("missing access-key/accessKeySecret from env")
    if not preferred_sender:
        raise ValueError("missing sender/fromEmail (provide IEMAIL_SENDER)")
    if not _looks_like_email(preferred_sender):
        raise ValueError("invalid sender format (expected email address)")

    client = IemailClient(access_key=access_key, access_key_secret=access_key_secret)
    cfg = client.get_json(
        "/openapi/open-api/v1/emailSupplierConfig/getEmailSupplierConfig",
        params={"page": "1", "pageLength": "50", "sortField": "updateDate", "sortType": "desc"},
    )
    email_config_sn = pick_email_config_sn(cfg)
    if not email_config_sn:
        raise RuntimeError(f"cannot find emailConfigSn, response: {json.dumps(cfg, ensure_ascii=False)[:800]}")

    sender = client.get_json("/openapi/open-api/v1/email/getSender", params={"emailSupplierConfigSn": email_config_sn})
    sender_address_sn = pick_sender_sn(sender, preferred_sender)
    if not sender_address_sn:
        raise RuntimeError(f"cannot find senderAddressSn, response: {json.dumps(sender, ensure_ascii=False)[:800]}")

    reply = client.get_json("/openapi/open-api/v1/email/getReplyAddress", params={"emailConfigSn": email_config_sn})
    reply_sn = pick_reply_sn(reply)

    payload: Dict[str, Any] = {
        "emailConfigSn": email_config_sn,
        "senderAddressSn": sender_address_sn,
        "subject": subject,
        "content": {"value": content},
        "recipient": {"email": to_email},
    }
    if reply_sn:
        payload["replyAddressSn"] = reply_sn

    return client.post_json("/iemail-send/open-api/v2/send/transactional/sendSingleEmail", payload)


def main(argv: List[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        add_help=True,
        description="Send transactional email via Iemail OpenAPI",
    )
    parser.add_argument("--to", dest="to_email", default=None)
    parser.add_argument("--subject", dest="subject", default=None)
    parser.add_argument("--content", dest="content", default=None)
    args, unknown = parser.parse_known_args(argv[1:])

    to_email = None
    subject = None
    content = None

    if unknown:
        if len(unknown) >= 1:
            to_email = unknown[0]
        if len(unknown) >= 2:
            subject = unknown[1]
        if len(unknown) >= 3:
            content = unknown[2]
    to_email = (args.to_email or to_email or os.getenv("IEMAIL_TO") or "").strip()
    subject = (args.subject or subject or "Iemail transactional test").strip()
    content = args.content or content or "Hello from Iemail"

    if not to_email:
        raise SystemExit('missing recipient email. Provide --to "a@b.com" or set IEMAIL_TO.')
    if not _looks_like_email(to_email):
        raise SystemExit("invalid recipient email format")

    resp = send_transactional_single_email(to_email, subject, content)
    sys.stdout.write(json.dumps(resp, ensure_ascii=False))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
