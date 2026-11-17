#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""infoseek_auth.py — Infoseek OAuth 2.0 + RBAC + Secret 加密

供 QCM V0.5.0 / V0.6.0 测试套件（tests/basic/qcm_mcp_v050/v060_test.py）使用的
服务端认证模块。设计原则：

  - 纯 stdlib 实现，无外部硬依赖（cryptography 仅 SecretCipher 可选增强，缺失时 XOR 兜底）
  - JWT 采用最小可验证签名格式：  infoseek.<base64url(payload)>.<base64url(hmac-sha256)>
  - 默认租户 default-client 为 admin（check_scope/check_tool 全放行）
  - 签名密钥默认常量；可用 env INFOSEEK_JWT_SECRET 覆盖（需 server 与导入方一致）

契约（对齐 v050 测试）：
  AuthManager()
  AuthManager.client_credentials(client_id, client_secret, scope=None)
      -> {"access_token": "infoseek.*", "token_type": "Bearer", "expires_in": 3600}
      -> 错误凭证 raise ValueError("invalid_client")
  AuthManager.verify(token) -> payload dict | None
  AuthManager.check_scope(payload, scope) -> bool
  AuthManager.check_tool(payload, tool) -> bool
  SecretCipher(master_key).encrypt(plain) / .decrypt(cipher)  # roundtrip
"""
import base64
import hashlib
import hmac
import json
import os
import time

# ── S7：dep_registry 事实层惰性 accessor（cryptography 可选点零漂移收口）──
_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        import sys as _sys
        _core = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core')
        if _core not in _sys.path:
            _sys.path.insert(0, _core)
        import dep_registry as _mod
        _dr = _mod
    return _dr

# ── 签名密钥（server 与直接导入方必须一致）──
JWT_SECRET = os.environ.get("INFOSEEK_JWT_SECRET", "infoseek-default-jwt-secret-v1")
TOKEN_PREFIX = "infoseek."

# ── 客户端凭据存储（client_id -> client_secret）──
CLIENTS = {
    "default-client": "default-secret",
}

# 默认租户（admin → RBAC 全放行）
DEFAULT_TENANT = "admin"
DEFAULT_SCOPE = ["tools/call", "tools/list", "resources/read"]


def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def _sign(body: str, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    return _b64url(digest)


class AuthManager:
    """OAuth 2.0 client_credentials 签发 / 校验 + RBAC。"""

    def __init__(self, jwt_secret: str = None, clients: dict = None):
        self.jwt_secret = jwt_secret or JWT_SECRET
        self.clients = dict(CLIENTS)
        if clients:
            self.clients.update(clients)

    # ── 签发 ──
    def client_credentials(self, client_id: str, client_secret: str, scope=None):
        """签发 access_token（client_credentials 流程）

        错误凭证 -> raise ValueError("invalid_client")（HTTP 层映射为 401）
        """
        if client_id not in self.clients or self.clients[client_id] != client_secret:
            raise ValueError("invalid_client")
        now = int(time.time())
        payload = {
            "sub": client_id,
            "client_id": client_id,
            "iat": now,
            "exp": now + 3600,
            "scope": list(scope) if scope else list(DEFAULT_SCOPE),
            "tenant": DEFAULT_TENANT,
            "admin": True,
        }
        body = _b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        sig = _sign(body, self.jwt_secret)
        return {
            "access_token": f"{TOKEN_PREFIX}{body}.{sig}",
            "token_type": "Bearer",
            "expires_in": 3600,
        }

    # ── 校验 ──
    def verify(self, token: str):
        """校验 JWT 签名 + 有效期。合法 -> payload；否则 -> None。"""
        if not token or not token.startswith(TOKEN_PREFIX):
            return None
        try:
            raw = token[len(TOKEN_PREFIX):]
            body, sig = raw.rsplit(".", 1)
            if not hmac.compare_digest(_sign(body, self.jwt_secret), sig):
                return None
            payload = json.loads(_b64url_decode(body).decode("utf-8"))
            if int(payload.get("exp", 0)) < int(time.time()):
                return None
            return payload
        except Exception:
            return None

    # ── RBAC ──
    def check_scope(self, payload, scope: str) -> bool:
        if payload is None:
            return False
        if payload.get("admin"):
            return True
        return scope in payload.get("scope", [])

    def check_tool(self, payload, tool: str) -> bool:
        if payload is None:
            return False
        if payload.get("admin"):
            return True
        return "tools/call" in payload.get("scope", [])


class SecretCipher:
    """密钥加密（Fernet 优先 · XOR+base64 兜底）。保证 roundtrip 且非 no-op。"""

    def __init__(self, master_key: str):
        self.master_key = master_key
        self._fernet = None
        try:
            if not _dep_reg().is_available("cryptography"):
                raise ImportError("cryptography unavailable")
            from cryptography.fernet import Fernet
            key = base64.urlsafe_b64encode(hashlib.sha256(master_key.encode("utf-8")).digest())
            self._fernet = Fernet(key)
        except Exception:
            self._fernet = None

    def encrypt(self, plain: str) -> str:
        if self._fernet is not None:
            return self._fernet.encrypt(plain.encode("utf-8")).decode("utf-8")
        return self._xor_cipher(plain.encode("utf-8"))

    def decrypt(self, cipher: str) -> str:
        if self._fernet is not None:
            return self._fernet.decrypt(cipher.encode("utf-8")).decode("utf-8")
        return self._xor_decrypt(cipher)

    @staticmethod
    def _xor_cipher(raw: bytes) -> str:
        key = b"infoseek-xor-key-v1"
        out = bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))
        return _b64url(out)

    @staticmethod
    def _xor_decrypt(cipher: str) -> str:
        key = b"infoseek-xor-key-v1"
        raw = _b64url_decode(cipher)
        out = bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))
        return out.decode("utf-8")


if __name__ == "__main__":
    # 自检
    am = AuthManager()
    t = am.client_credentials("default-client", "default-secret", ["tools/call"])
    assert t["access_token"].startswith("infoseek.")
    assert t["token_type"] == "Bearer" and t["expires_in"] == 3600
    p = am.verify(t["access_token"])
    assert p and p["sub"] == "default-client"
    assert am.check_scope(p, "tools/call") and am.check_tool(p, "research_v3")
    assert am.check_scope(None, "tools/call") is False
    c = SecretCipher("master-key")
    e = c.encrypt("REDACTED-SECRET")
    assert e != "REDACTED-SECRET"
    assert c.decrypt(e) == "REDACTED-SECRET"
    print("infoseek_auth self-check OK")
