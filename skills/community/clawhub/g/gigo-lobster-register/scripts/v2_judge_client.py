from __future__ import annotations

import hashlib
import json
import math
import time
import urllib.error
import urllib.request
from pathlib import Path


def _coerce_score(value: object) -> int:
    try:
        numeric = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0
    if not math.isfinite(numeric):
        return 0
    return max(0, min(100, int(round(numeric))))


def _sanitize_judge_response(body: dict, dimensions: list[str]) -> dict:
    raw_scores = body.get("scores") if isinstance(body.get("scores"), dict) else {}
    body["scores"] = {dimension: _coerce_score(raw_scores.get(dimension)) for dimension in dimensions}
    reasoning = body.get("reasoning")
    body["reasoning"] = str(reasoning).strip()[:500] if reasoning is not None else ""
    return body


def output_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class JudgeClient:
    def __init__(self, config: dict) -> None:
        self.api_base = str(config["api_base"]).rstrip("/")
        self.skill_version = str(config.get("skill_version") or "2.0.17")
        self.task_session = config.get("task_session") if isinstance(config.get("task_session"), dict) else {}
        self.timeout_seconds = int(config.get("judge_timeout_seconds") or 120)
        self.cache_root = Path(str(config.get("bundle_cache_dir"))) / "judge-cache"
        self.cache_root.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, payload: dict) -> str:
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def judge(self, payload: dict, max_retries: int = 3) -> dict:
        cache_key = self._cache_key(payload)
        cache_path = self.cache_root / f"{cache_key}.json"
        dimensions = [str(item) for item in payload.get("dimensions_to_judge", [])]
        if cache_path.exists():
            return _sanitize_judge_response(json.loads(cache_path.read_text(encoding="utf-8")), dimensions)

        headers = {"Content-Type": "application/json"}
        ticket = self.task_session.get("ticket") if isinstance(self.task_session, dict) else None
        if ticket:
            headers["X-GIGO-Session-Ticket"] = str(ticket)

        request = urllib.request.Request(
            f"{self.api_base}/api/v2/judge",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    body = json.loads(response.read().decode("utf-8"))
                body = _sanitize_judge_response(body, dimensions)
                cache_path.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
                return body
            except urllib.error.HTTPError as error:
                if error.code == 429 and attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                if 500 <= error.code < 600 and attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                break
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                break
        return {
            "scores": {key: 0 for key in dimensions},
            "judge_model": "judge_pending",
            "judge_version": "fallback",
            "consensus": "single",
            "fallback_used": True,
            "latency_ms": 0,
            "error": "judge_pending",
        }
