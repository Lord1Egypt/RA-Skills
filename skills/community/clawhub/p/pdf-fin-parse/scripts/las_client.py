"""LAS-AI PDF 解析算子客户端（las_pdf_parse_doubao）。

异步算子：submit → poll，没有客户端单次同步超时问题。

接口：
    submit(url, parse_mode, ...) -> task_id
    poll(task_id) -> raw_response dict
    wait_completion(task_id, ...) -> final_response dict（阻塞直到终态）

所有过程日志走 stderr。
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict, Optional

import requests


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

DEFAULT_REGION = "cn-beijing"
REGION_TO_DOMAIN = {
    "cn-beijing":  "operator.las.cn-beijing.volces.com",
    "cn-shanghai": "operator.las.cn-shanghai.volces.com",
}
OPERATOR_ID = "las_pdf_parse_doubao"
OPERATOR_VERSION = "v1"

# 业务码 2002（请求超时）/ 2003（服务端限流）可重试
_RETRYABLE_BUSINESS_CODES = {"2002", "2003"}
_RETRYABLE_HTTP_STATUSES = {408, 425, 429, 500, 502, 503, 504}


class LASError(RuntimeError):
    """LAS API 调用失败的统一异常。"""


# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def _api_key() -> str:
    k = os.environ.get("LAS_API_KEY")
    if not k:
        raise LASError("LAS_API_KEY 未配置（env.sh 或环境变量）")
    return k


def _api_base(region: str) -> str:
    env_base = os.environ.get("LAS_API_BASE")
    if env_base:
        return env_base.rstrip("/")
    domain = REGION_TO_DOMAIN.get(region)
    if not domain:
        raise LASError(f"未知 region: {region}；请用 LAS_API_BASE 显式指定")
    return f"https://{domain}/api/v1"


def _headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_api_key()}",
    }


def _extract_meta(resp: Any) -> Dict[str, Any]:
    if isinstance(resp, dict) and isinstance(resp.get("metadata"), dict):
        return resp["metadata"]
    return {}


# ---------------------------------------------------------------------------
# HTTP 调用 + 重试
# ---------------------------------------------------------------------------

def _post_with_retry(url: str, payload: Dict[str, Any], *,
                     timeout_s: int = 60, max_attempts: int = 3,
                     backoff_s: float = 1.0) -> Dict[str, Any]:
    """POST JSON，对 5xx/429/限流 业务码退避重试。"""
    last_err: Optional[Exception] = None
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.post(url, headers=_headers(), json=payload, timeout=timeout_s)
            if not r.ok:
                if r.status_code in _RETRYABLE_HTTP_STATUSES and attempt < max_attempts:
                    time.sleep(backoff_s * (2 ** (attempt - 1)))
                    continue
                # 非可重试 HTTP 错误
                try:
                    j = r.json()
                    meta = _extract_meta(j)
                    raise LASError(
                        f"HTTP {r.status_code}: business_code={meta.get('business_code')} "
                        f"error_msg={meta.get('error_msg')} request_id={meta.get('request_id')}"
                    )
                except (ValueError, KeyError):
                    raise LASError(f"HTTP {r.status_code}: {r.text[:500]}")

            j = r.json()
            if not isinstance(j, dict):
                raise LASError(f"返回不是 JSON object: {type(j).__name__}")

            # 检查业务级可重试
            meta = _extract_meta(j)
            bc = meta.get("business_code")
            if bc is not None and str(bc) in _RETRYABLE_BUSINESS_CODES and attempt < max_attempts:
                time.sleep(backoff_s * (2 ** (attempt - 1)))
                continue
            return j
        except requests.RequestException as e:
            last_err = e
            if attempt < max_attempts:
                time.sleep(backoff_s * (2 ** (attempt - 1)))
                continue
            raise LASError(f"网络错误: {e}") from e
    raise LASError(f"重试 {max_attempts} 次后仍失败: {last_err}")


# ---------------------------------------------------------------------------
# 对外接口
# ---------------------------------------------------------------------------

def submit(url: str, *,
           parse_mode: str = "normal",
           start_page: int = 1,
           num_pages: Optional[int] = None,
           region: str = DEFAULT_REGION) -> str:
    """提交 PDF 解析任务，返回 task_id。

    Args:
        url: PDF 可下载地址，支持 http(s)://、tos://bucket/key
        parse_mode: "normal"（默认，快）或 "detail"（深度，慢，更精细）
        start_page: 起始页（1-based）
        num_pages: 解析页数，None=到末尾，max 200
        region: LAS region
    """
    submit_url = f"{_api_base(region)}/submit"
    data: Dict[str, Any] = {"url": url, "start_page": start_page,
                            "parse_mode": parse_mode}
    if num_pages is not None:
        data["num_pages"] = num_pages
    payload = {
        "operator_id": OPERATOR_ID,
        "operator_version": OPERATOR_VERSION,
        "data": data,
    }
    _log(f"[las] submit url={url[:80]}... parse_mode={parse_mode} "
         f"start_page={start_page} num_pages={num_pages}")
    resp = _post_with_retry(submit_url, payload)
    task_id = _extract_meta(resp).get("task_id")
    if not task_id:
        raise LASError(f"submit 返回缺少 task_id: {json.dumps(resp)[:500]}")
    _log(f"[las] submit ok, task_id={task_id}")
    return task_id


def poll(task_id: str, *, region: str = DEFAULT_REGION) -> Dict[str, Any]:
    """单次轮询任务状态，返回完整响应 dict。"""
    poll_url = f"{_api_base(region)}/poll"
    payload = {
        "operator_id": OPERATOR_ID,
        "operator_version": OPERATOR_VERSION,
        "task_id": task_id,
    }
    return _post_with_retry(poll_url, payload)


def wait_completion(task_id: str, *,
                    region: str = DEFAULT_REGION,
                    max_attempts: int = 60,
                    poll_interval: Optional[int] = None) -> Dict[str, Any]:
    """阻塞轮询直到 COMPLETED/FAILED/TIMEOUT 终态，返回最终响应。

    退避策略：未指定 poll_interval 时，前 2 次 10s，3-5 次 20s，之后 30s。
    """
    for attempt in range(max_attempts):
        resp = poll(task_id, region=region)
        meta = _extract_meta(resp)
        status = meta.get("task_status")

        if status == "COMPLETED":
            _log(f"[las] task {task_id} COMPLETED (attempt={attempt + 1})")
            return resp
        if status in ("FAILED", "TIMEOUT"):
            raise LASError(
                f"task {task_id} {status}: "
                f"business_code={meta.get('business_code')} "
                f"error_msg={meta.get('error_msg')}"
            )

        # PENDING / RUNNING
        if poll_interval is not None:
            interval = poll_interval
        elif attempt < 2:
            interval = 10
        elif attempt < 5:
            interval = 20
        else:
            interval = 30
        _log(f"[las] task {task_id} {status} ({attempt + 1}/{max_attempts}), "
             f"{interval}s 后再查")
        time.sleep(interval)

    raise LASError(f"task {task_id} 轮询 {max_attempts} 次仍未完成")
