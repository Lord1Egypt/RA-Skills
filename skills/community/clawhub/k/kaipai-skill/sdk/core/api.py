"""AI API core module for Kaipai AI SDK."""

import copy
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests

from sdk.auth import Signer
from sdk.core.config import USER_AGENT, GID_CACHE_FILE, INVOKE, REGIONS
from sdk.core.models import TaskResult, TaskStatus
from sdk.storage import OssUploader, resolve_oss_region, normalize_oss_endpoint
from sdk.utils import GidCache


# Progress logging
PROGRESS_ENABLED = os.environ.get("MT_AI_PROGRESS", "1").strip().lower() not in (
    "0", "false", "no", "off",
)


def _progress_log(msg: str) -> None:
    if not PROGRESS_ENABLED:
        return
    print(f"[kaipai-ai] {msg}", file=sys.stderr, flush=True)


def safe_url_preview(url: str, max_len: int = 72) -> str:
    """Shorten URLs for logs and JSON pipeline_trace."""
    if not url:
        return ""
    s = str(url).strip().replace("\n", " ")
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


# Keys whose values must not appear in progress logs (token_policy, etc.)
_REDACT_LOG_KEYS = frozenset(
    {
        "access_key",
        "secret_key",
        "session_token",
        "security_token",
        "app_secret",
        "password",
        "private_key",
        "authorization",
        # camelCase / compact variants
        "accesskey",
        "secretkey",
        "sessiontoken",
        "appsecret",
    }
)


def _redact_secrets_for_log(obj: Any) -> Any:
    """Return a deep copy safe for logging (OSS/WAPI credentials stripped)."""
    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for k, v in obj.items():
            lk = str(k).lower().replace("-", "_")
            if lk == "credentials" or lk in _REDACT_LOG_KEYS or lk.endswith("_secret"):
                out[k] = "<redacted>"
            else:
                out[k] = _redact_secrets_for_log(v)
        return out
    if isinstance(obj, list):
        return [_redact_secrets_for_log(x) for x in obj]
    return obj


def _default_task_type(raw: Any) -> str:
    """Normalize task_type from INVOKE or token_policy; empty or missing → mtlab."""
    if raw is None:
        return "mtlab"
    s = str(raw).strip()
    return s or "mtlab"


def _extract_output_urls(body: Dict[str, Any]) -> List[str]:
    """Extract output URLs from API response."""
    if not isinstance(body, dict):
        return []
    inner = body.get("data")
    if not isinstance(inner, dict):
        return []
    result = inner.get("result")
    if not isinstance(result, dict):
        return []

    ordered: List[str] = []
    seen: set = set()

    def _append_urls(values):
        if isinstance(values, list):
            for x in values:
                if isinstance(x, str) and x.startswith(("http://", "https://")) and x not in seen:
                    seen.add(x)
                    ordered.append(x)
        elif isinstance(values, str) and values.startswith(("http://", "https://")) and values not in seen:
            seen.add(values)
            ordered.append(values)

    for key in ("urls", "images", "videos", "url"):
        _append_urls(result.get(key))

    # Check nested media_info_list
    def _urls_from_media_info_list(items):
        out = []
        if not isinstance(items, list):
            return out
        for it in items:
            if isinstance(it, dict):
                md = it.get("media_data")
                if isinstance(md, str) and md.startswith(("http://", "https://")):
                    out.append(md)
        return out

    nested_data = result.get("data")
    nested_mil = nested_data.get("media_info_list") if isinstance(nested_data, dict) else None
    for mil in (result.get("media_info_list"), nested_mil):
        for u in _urls_from_media_info_list(mil):
            if u not in seen:
                seen.add(u)
                ordered.append(u)

    mtlab = result.get("mtlab_res")
    if isinstance(mtlab, dict):
        for u in _urls_from_media_info_list(mtlab.get("media_info_list")):
            if u not in seen:
                seen.add(u)
                ordered.append(u)

    return ordered


def _extract_task_id(body: Dict[str, Any]) -> Optional[str]:
    """Best-effort task id from API response shape."""
    if not isinstance(body, dict):
        return None
    data = body.get("data")
    if not isinstance(data, dict):
        return None
    result = data.get("result")
    if isinstance(result, dict):
        tid = result.get("id")
        if tid is not None:
            s = str(tid).strip()
            if s:
                return s
    return None


def _with_output_urls(body: Dict[str, Any], task_id: Optional[str] = None) -> Dict[str, Any]:
    """Attach output_urls and task_id for downstream recovery."""
    if not isinstance(body, dict):
        return body
    out = {**body, "output_urls": _extract_output_urls(body)}
    tid = task_id or _extract_task_id(body)
    if tid:
        out["task_id"] = tid
    return out


def _failure_status_codes_from_env() -> frozenset:
    """Optional terminal task data.status values."""
    raw = os.environ.get("MT_AI_TASK_FAILURE_STATUSES", "3").strip()
    if not raw or raw.lower() in ("0", "false", "no", "off", "none"):
        return frozenset()
    out = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.add(int(part))
        except ValueError:
            continue
    return frozenset(out)


def _max_consecutive_poll_errors() -> int:
    raw = os.environ.get("MT_AI_POLL_MAX_CONSECUTIVE_ERRORS", "5").strip() or "5"
    try:
        n = int(raw)
    except ValueError:
        n = 5
    return max(1, min(n, 100))


def _meta_indicates_error(meta: Any) -> bool:
    if os.environ.get("MT_AI_IGNORE_META_CODE", "").strip().lower() in ("1", "true", "yes"):
        return False
    if not isinstance(meta, dict):
        return False
    code = meta.get("code")
    if code is None:
        return False
    if code == 0 or code == "0":
        return False
    return True


def _status_poll_min_total_ms() -> Optional[int]:
    """Minimum sum (ms) of status poll sleeps. Default 1 hour."""
    raw = os.environ.get("MT_AI_POLL_MIN_TOTAL_MS", "").strip()
    if not raw:
        return 3_600_000  # 1 hour default
    if raw.lower() in ("0", "false", "no", "off"):
        return None
    try:
        v = int(raw)
    except ValueError:
        return 3_600_000
    if v <= 0:
        return None
    return v


def _extend_status_poll_durations_ms(durations: List[str]) -> List[str]:
    """Ensure cumulative sleep between status polls is at least min_total_ms."""
    min_total_ms = _status_poll_min_total_ms()
    if min_total_ms is None:
        return durations
    try:
        base_total = sum(int(d) for d in durations)
    except ValueError:
        return durations
    if base_total >= min_total_ms:
        return durations
    step_raw = os.environ.get("MT_AI_POLL_EXTEND_STEP_MS", "30000").strip() or "30000"
    try:
        step_ms = int(step_raw)
    except ValueError:
        step_ms = 30000
    step_ms = max(step_ms, 1000)
    out = list(durations)
    total = base_total
    while total < min_total_ms:
        add = min(step_ms, min_total_ms - total)
        out.append(str(add))
        total += add
    return out


def _sync_timeout_override() -> int:
    """Get sync_timeout from env var MT_AI_SYNC_TIMEOUT (default 10s)."""
    raw = os.environ.get("MT_AI_SYNC_TIMEOUT", "10").strip()
    if not raw:
        return 10
    try:
        return max(1, int(raw))
    except ValueError:
        return 10


def _deep_merge_params(base: Dict, override: Dict) -> Dict:
    """Shallow keys from override win; nested dicts are merged recursively."""
    if not base:
        return copy.deepcopy(override) if override else {}
    if not override:
        return copy.deepcopy(base)
    out = copy.deepcopy(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge_params(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


class AiApi:
    """AI API actions - core algorithm execution."""

    def __init__(
        self,
        key: str,
        secret: str,
        region: str = "cn-north-4",
        oss_region: Optional[str] = None,
        config: Optional[Dict] = None,
    ):
        """
        :param key: Your access key.
        :param secret: Your access secret key.
        :param region: API access region. Default "cn-north-4"
        :param oss_region: Optional OSS bucket region when token_policy url cannot be parsed
        :param config: Optional dict overriding regions, token_policy_type, token_policy_types
        """
        self.Key = key
        self.Secret = secret
        self._config = self._merge_connection_config(self._default_connection_config(), config)
        self.region = region
        self.oss_region = oss_region
        self.aiStrategy = None
        self.storageStrategy = None
        self.EndPoint = self._config.get("regions", {}).get(region)
        self.gid_cache = GidCache(GID_CACHE_FILE)

    def _default_connection_config(self) -> Dict:
        return {
            "regions": dict(REGIONS),
            "token_policy_type": "mtai",
            "token_policy_types": None,
        }

    def _merge_connection_config(self, base: Dict, override: Optional[Dict]) -> Dict:
        if not override:
            return copy.deepcopy(base)
        out = copy.deepcopy(base)
        for key, val in override.items():
            if key == "regions" and isinstance(val, dict):
                merged = copy.deepcopy(out.get("regions") or {})
                merged.update(val)
                out["regions"] = merged
            elif key == "token_policy_types" and isinstance(val, dict):
                merged = copy.deepcopy(out.get("token_policy_types") or {})
                merged.update(val)
                out["token_policy_types"] = merged
            else:
                out[key] = copy.deepcopy(val) if isinstance(val, dict) else val
        return out

    def _token_policy_type_for(self, name: str) -> str:
        """name is 'upload' or 'ai' - query param for /ai/token_policy?type="""
        types_map = self._config.get("token_policy_types")
        if types_map:
            return types_map.get(name) or self._config.get("token_policy_type", "mtai")
        return self._config.get("token_policy_type", "mtai")

    def _ensure_endpoint(self) -> None:
        if not self.EndPoint:
            raise RuntimeError(
                f"No endpoint configured for region {self.region!r}. "
                "Call fetch_config() first or set regions in config."
            )

    def getStrategy(self, name: str) -> Optional[Dict]:
        """Get token policy for 'upload' or 'ai'."""
        self._ensure_endpoint()
        typ = self._token_policy_type_for(name)

        import datetime as dt
        now = dt.datetime.now()
        unix_epoch = dt.datetime(1970, 1, 1)
        unix_time = (now - unix_epoch).total_seconds()

        if name == "ai" and self.aiStrategy and self.aiStrategy["ttl"] + getattr(self, 'strategyLoadTime', 0) > unix_time:
            return self.aiStrategy

        signer = Signer(self.Key, self.Secret)
        headers = {
            "Host": self.EndPoint,
            "User-Agent": USER_AGENT,
        }
        uri = f"https://{self.EndPoint}/ai/token_policy?type={typ}"
        sign_request = signer.sign(uri, "GET", headers, "")
        session = requests.Session()
        resp = session.send(sign_request)
        _progress_log(f"token_policy GET type={typ} host={self.EndPoint} → HTTP {resp.status_code}")

        if resp.status_code == 200:
            policydata = json.loads(resp.content)
            try:
                safe = _redact_secrets_for_log(policydata)
                preview = json.dumps(safe, ensure_ascii=False)[:800]
            except (TypeError, ValueError):
                preview = "<unserializable>"
            if policydata is None:
                return None
            policy = policydata["data"]
            cloud = policy["mtai"]["api"]["order"][0]
            cloudConf = policy["mtai"]["api"][cloud]
            self.aiStrategy = cloudConf
            storageCloud = policy["mtai"]["upload"]["order"][0]
            self.storageStrategy = policy["mtai"]["upload"][storageCloud]
            self.strategyLoadTime = unix_time
            if name == "ai":
                return self.aiStrategy
            return self.storageStrategy

        _progress_log(f"token_policy failed body={safe_url_preview(resp.text, max_len=120)!r}")
        return None

    def getStorageStrategy(self) -> Optional[Dict]:
        return self.getStrategy("upload")

    def getAiStrategy(self) -> Optional[Dict]:
        return self.getStrategy("ai")

    def upload_file(self, file) -> Optional[Dict]:
        """
        Upload file to OSS.

        :param file: The data to upload. This can be bytes or a string (file path).
        :return: The uploaded file URL data.
        """
        policy = self.getStorageStrategy()
        if policy is None:
            return None

        uploader = OssUploader(policy, self.oss_region, USER_AGENT)
        return uploader.upload(file)

    def submit_task(
        self,
        imageUrl: Optional[List[Dict]],
        params: Dict,
        task: str,
        taskType: str,
        context: str = "",
        on_async_submitted: Optional[Callable[[str], None]] = None,
    ) -> Dict:
        """
        Submit algorithm task.

        :param imageUrl: The image URL array [{"url":"url"}]
        :param params: API params object
        :param task: Task name to apply
        :param taskType: Task type (default: mtlab)
        :param context: Context string
        :param on_async_submitted: Callback invoked with task_id when async job is submitted
        :return: Task result data
        """
        taskType = _default_task_type(taskType)
        signer = Signer(self.Key, self.Secret)
        policy = self.getAiStrategy()
        if not policy:
            raise RuntimeError("Failed to get AI strategy")

        host = policy["url"]
        if host.find("https") > -1:
            host = host[8:]
        elif host.find("http") > -1:
            host = host[7:]

        headers = {
            "Host": host,
            "User-Agent": USER_AGENT,
        }

        sync_timeout = _sync_timeout_override()
        data = {
            "params": json.dumps(params),
            "context": context,
            "task": task,
            "task_type": taskType,
            "sync_timeout": sync_timeout,
            "init_images": imageUrl,
        }
        uri = policy["url"] + "/" + policy["push_path"]
        sign_request = signer.sign(uri, "POST", headers, json.dumps(data))
        _progress_log(
            f"algorithm POST {policy['push_path']} task={task} task_type={taskType} "
            f"sync_timeout={sync_timeout}s"
        )
        session = requests.Session()
        resp = session.send(sign_request, timeout=sync_timeout + 10)

        if resp.status_code == 200:
            taskResult = json.loads(resp.content)
            if taskResult.get("data", {}).get("status") == 9:
                tid = taskResult["data"]["result"]["id"]
                _progress_log(f"async submitted task_id={tid} → polling status until done")
                if callable(on_async_submitted):
                    try:
                        on_async_submitted(str(tid).strip())
                    except Exception:
                        pass
                return self.poll_status(tid, policy)
            else:
                out = _with_output_urls(taskResult)
                _progress_log(f"sync complete output_urls={len(out.get('output_urls', []))}")
                return out

        _progress_log(f"algorithm POST HTTP {resp.status_code}")
        raw = json.loads(resp.content)
        return _with_output_urls(raw) if isinstance(raw, dict) else raw

    def poll_status(self, taskId: str, policy: Dict) -> Dict:
        """
        Query task execute status with polling.

        :param taskId: The task id
        :param policy: Query policy with retry and gaps
        :return: The handled result data in json
        """
        host = policy["url"]
        if host.find("https") > -1:
            host = host[8:]
        elif host.find("http") > -1:
            host = host[7:]
        status_path = policy.get("status_path") or policy.get("status_query", {}).get("path", "")
        uri = policy["url"] + "/" + status_path + "?task_id=" + taskId

        loops = policy.get("status_query", {}).get("durations", "1000,2000,3000")
        durations = [p.strip() for p in str.split(loops, ",") if p.strip()]
        durations = _extend_status_poll_durations_ms(durations)
        n = len(durations)
        start = time.monotonic()
        last_api_status = None
        last_nonjson_detail = None
        err_streak = 0
        max_err = _max_consecutive_poll_errors()

        for idx, d in enumerate(durations, start=1):
            result = self._query_status(uri, policy)
            if result["is_finished"]:
                if result.get("is_failure"):
                    raw = result.get("result")
                    if not isinstance(raw, dict):
                        raw = {"meta": {"msg": str(raw)}}
                    return self._task_failed_payload(taskId, raw)
                out = _with_output_urls(result["result"], task_id=taskId)
                _progress_log(f"poll complete task_id={taskId} output_urls={len(out.get('output_urls', []))}")
                return out

            raw = result.get("result")
            if isinstance(raw, str):
                err_streak += 1
                last_nonjson_detail = raw[:120]
                if err_streak >= max_err:
                    elapsed = time.monotonic() - start
                    _progress_log(
                        f"poll aborted after {err_streak} consecutive query errors "
                        f"({elapsed:.0f}s), task_id={taskId}"
                    )
                    return self._poll_aborted_payload(taskId, idx, raw[:500], last_api_status)
            else:
                err_streak = 0
                last_nonjson_detail = None

            if isinstance(raw, dict):
                try:
                    last_api_status = raw.get("data", {}).get("status")
                except (AttributeError, TypeError):
                    pass

            elapsed = time.monotonic() - start
            if idx == 1 or idx % 3 == 0 or idx == n:
                parts = [
                    f"poll {idx}/{n}",
                    f"task_id={taskId}",
                    f"api_status={last_api_status!r}",
                    f"elapsed={elapsed:.0f}s",
                ]
                if last_nonjson_detail:
                    parts.append(f"detail={last_nonjson_detail}")
                _progress_log(" ".join(parts))

            time.sleep(int(d) / 1000)

        elapsed = time.monotonic() - start
        _progress_log(f"timeout after {n} polls ({elapsed:.0f}s), task_id={taskId}")
        return self._poll_timeout_payload(taskId, n, elapsed, last_api_status)

    def _query_status(self, uri: str, policy: Dict) -> Dict:
        """Query task status once."""
        signer = Signer(self.Key, self.Secret)
        host = policy["url"]
        if host.find("https") > -1:
            host = host[8:]
        elif host.find("http") > -1:
            host = host[7:]

        headers = {
            "Host": host,
            "User-Agent": USER_AGENT,
        }
        sign_request = signer.sign(uri, "GET", headers, "")
        read_timeout = min(int(policy.get("sync_timeout", 10)) + 10, 120)
        req_timeout = (5, read_timeout)
        session = requests.Session()
        resp = None
        last_exc = None

        for attempt in range(3):
            try:
                resp = session.send(sign_request, timeout=req_timeout)
                last_exc = None
                break
            except requests.exceptions.RequestException as e:
                last_exc = e
                if attempt < 2:
                    time.sleep(3)

        if last_exc is not None:
            return {
                "is_finished": False,
                "result": " task query network error: " + str(last_exc),
            }

        if resp.status_code == 200:
            try:
                taskResult = json.loads(resp.content)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                return {
                    "is_finished": False,
                    "result": " task query invalid JSON: " + str(e),
                }

            if _meta_indicates_error(taskResult.get("meta")):
                return {
                    "is_finished": True,
                    "is_failure": True,
                    "result": taskResult,
                }

            data = taskResult.get("data")
            if not isinstance(data, dict):
                return {"is_finished": False, "result": taskResult}

            st = data.get("status")
            if st in (10, 2, 20):
                return {"is_finished": True, "result": taskResult}

            fail_codes = _failure_status_codes_from_env()
            if fail_codes and st in fail_codes:
                return {
                    "is_finished": True,
                    "is_failure": True,
                    "result": taskResult,
                }

            return {"is_finished": False, "result": taskResult}

        _progress_log(f"task query HTTP {resp.status_code}: {safe_url_preview(resp.text, max_len=200)!r}")
        return {"is_finished": False, "result": " task query failure: " + uri}

    def _task_failed_payload(self, task_id: str, task_result_dict: Dict, reason: str = "task_failed") -> Dict:
        meta = task_result_dict.get("meta", {}) if isinstance(task_result_dict, dict) else {}
        detail = ""
        if isinstance(meta, dict):
            detail = (meta.get("msg") or meta.get("message") or "") or detail
        data = task_result_dict.get("data") if isinstance(task_result_dict, dict) else None
        if isinstance(data, dict) and not detail:
            detail = str(data.get("message") or data.get("error") or "")[:300]
        if not detail:
            detail = reason
        return {
            "error": reason,
            "skill_status": "failed",
            "task_id": task_id,
            "detail": detail,
            "meta": meta if isinstance(meta, dict) else {},
            "data": data,
            "agent_instruction": (
                "The algorithm reported failure (see detail / meta). Do not treat as "
                "success; explain to the user and suggest retry or input checks."
            ),
        }

    def _poll_aborted_payload(self, task_id: str, n_polls: int, message: str, last_api_status) -> Dict:
        return {
            "error": "poll_aborted",
            "skill_status": "failed",
            "task_id": task_id,
            "polls": n_polls,
            "detail": message,
            "last_api_status": last_api_status,
            "agent_instruction": (
                "Status polling stopped after repeated query errors. Check network, "
                "credentials, and task_id; retry or use query-task after fixing connectivity."
            ),
        }

    def _poll_timeout_payload(self, task_id: str, n_polls: int, elapsed_s: float, last_api_status) -> Dict:
        return {
            "error": "poll_timeout",
            "skill_status": "failed",
            "task_id": task_id,
            "polls": n_polls,
            "elapsed_seconds": round(elapsed_s, 1),
            "last_api_status": last_api_status,
            "agent_instruction": (
                "Polling exhausted before the task finished. Increase sessions_spawn "
                "runTimeoutSeconds (default 3600); for videoscreenclear/hdvideoallinone use "
                "spawn-run-task in the main session — do not rely on blocking run-task there "
                "under a short tool or session wait cap. Or adjust MT_AI_POLL_* env vars. "
                "Do not treat as success; user may retry."
            ),
        }

    def invoke_task(
        self,
        name: str,
        url: Any,
        params: Optional[Dict] = None,
        context: str = "",
        on_async_submitted: Optional[Callable[[str], None]] = None,
        *,
        task_type: Optional[str] = None,
    ) -> Dict:
        """
        Run invoke with merged params: preset from config.INVOKE[name], overridden by params.
        """
        from sdk.core.config import INVOKE

        table = INVOKE or {}
        if name not in table:
            raise KeyError(f"Unknown invoke preset {name!r}; add it to config.INVOKE")
        spec = table[name]
        if not isinstance(spec, dict) or "task" not in spec:
            raise ValueError(
                f"config.INVOKE[{name!r}] must include 'task'; optional 'params' (default {{}}), "
                f"optional 'task_type' (default mtlab)"
            )
        cfg_params = spec.get("params")
        if cfg_params is not None and not isinstance(cfg_params, dict):
            raise TypeError(f"config.INVOKE[{name!r}]['params'] must be a dict or omit")
        merged = _deep_merge_params(cfg_params or {}, params or {})
        task_type = _default_task_type(task_type or spec.get("task_type"))

        if url is None:
            return self.submit_task(
                None,
                merged,
                spec["task"],
                task_type,
                context,
                on_async_submitted=on_async_submitted,
            )
        if isinstance(url, str):
            return self.submit_task(
                [{"url": url}],
                merged,
                spec["task"],
                task_type,
                context,
                on_async_submitted=on_async_submitted,
            )
        return self.submit_task(
            url,
            merged,
            spec["task"],
            task_type,
            context,
            on_async_submitted=on_async_submitted,
        )

    def txt2img(self, params: Dict, context: str = "") -> Dict:
        """Generate image from text."""
        policy = self.getAiStrategy()
        tt = _default_task_type(policy.get("task_type") if policy else None)
        return self.submit_task(None, params, "txt2img", tt, context)

    def img2img(self, url: str, params: Dict, context: str = "") -> Dict:
        """Transform image to image."""
        policy = self.getAiStrategy()
        tt = _default_task_type(policy.get("task_type") if policy else None)
        return self.submit_task([{"url": url}], params, "img2img", tt, context)

    def get_gid(self, gid: str) -> Optional[Dict]:
        """Return cached GID payload if present."""
        return self.gid_cache.get(gid)

    def set_gid(self, gid: str, data: Dict) -> None:
        """Persist GID-associated data to the local cache."""
        self.gid_cache.set(gid, data)
