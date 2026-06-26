"""调云端 /judge 接口的样板。生产代码应加密 + 重试 + 缓存。"""
from __future__ import annotations

import hashlib
import json
import time

import requests


class JudgeClient:
    def __init__(self, gateway_base: str, encrypt_fn, decrypt_fn):
        self.gateway_base = gateway_base.rstrip("/")
        self.encrypt = encrypt_fn
        self.decrypt = decrypt_fn
        self.cache: dict[str, dict] = {}

    def _cache_key(self, payload: dict) -> str:
        canon = json.dumps(
            {k: payload[k] for k in ("rubric_id", "agent_output_excerpt", "context",
                                     "dimensions_to_judge")},
            sort_keys=True, ensure_ascii=False,
        )
        return hashlib.sha256(canon.encode()).hexdigest()

    def judge(self, payload: dict, max_retries: int = 3) -> dict:
        key = self._cache_key(payload)
        if key in self.cache:
            return self.cache[key]
        body = self.encrypt(payload)
        for attempt in range(max_retries):
            try:
                resp = requests.post(f"{self.gateway_base}/judge", json=body, timeout=30)
                if resp.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                resp.raise_for_status()
                result = self.decrypt(resp.json())
                self.cache[key] = result
                return result
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    return {"scores": {d: 0 for d in payload["dimensions_to_judge"]},
                            "fallback_used": True, "error": str(e)}
                time.sleep(2 ** attempt)
        return {"scores": {}, "fallback_used": True}
