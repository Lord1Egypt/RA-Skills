"""High-level client for Kaipai AI SDK."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

import requests

from sdk.auth import Signer
from sdk.core.api import AiApi
from sdk.core.config import (
    GID_CACHE_FILE,
    USER_AGENT,
    WAPI_ENDPOINT,
    url_download_max_bytes,
    url_download_connect_timeout,
    url_download_read_timeout,
)


def _wapi_meta_code_value(meta_code: Any) -> int:
    """Normalize meta.code for comparisons (int)."""
    if meta_code is None:
        return 0
    if meta_code == 0 or meta_code == "0":
        return 0
    try:
        return int(meta_code)
    except (TypeError, ValueError):
        return -1


class WapiApiError(RuntimeError):
    """HTTP 200 but WAPI meta.code != 0.

    Full server payload is in ``raw``; ``str(exception)`` is intentionally short
    so errors copied to logs or JSON stdout do not leak response bodies.
    """

    def __init__(self, code: int, msg: str, raw: Dict, *, original_code=None):
        self.code = code
        self.original_code = original_code if original_code is not None else code
        self.msg = msg or "Request failed"
        self.raw = raw if isinstance(raw, dict) else {}
        super().__init__(f"[{self.original_code}] {self.msg}")


class ConsumeDeniedError(WapiApiError):
    """Non-zero meta from POST /skill/consume.json (quota / permission)."""


class WapiClient:
    """Signed HTTP client for the skill WAPI gateway."""

    def __init__(self, ak: str, sk: str, endpoint: str = WAPI_ENDPOINT):
        self.ak = ak
        self.sk = sk
        self.endpoint = endpoint

    def request(self, path: str, method: str = "GET", body: Optional[Dict] = None) -> Dict:
        """Send a signed request to WAPI."""
        import urllib.parse
        uri = f"https://{self.endpoint}{path}"
        signer = Signer(self.ak, self.sk)
        headers = {"User-Agent": USER_AGENT}
        body_str = json.dumps(body) if body else ""
        if body:
            headers["Content-Type"] = "application/json"

        signed_request = signer.sign(uri, method, headers, body_str)
        resp = requests.Session().send(signed_request, timeout=10)

        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code} from WAPI {path}")

        data = resp.json()
        meta = data.get("meta") or {}
        if _wapi_meta_code_value(meta.get("code", 0)) != 0:
            raise WapiApiError(
                _wapi_meta_code_value(meta.get("code")),
                meta.get("msg", "Request failed"),
                data,
                original_code=meta.get("code")
            )
        return data.get("response", {})


class SkillClient:
    """
    High-level client for AI task execution.

    Example::
        client = SkillClient(ak="xxx", sk="yyy")
        result = client.execute("eraser_watermark", "/path/to/image.jpg")
    """

    def __init__(
        self,
        ak: Optional[str] = None,
        sk: Optional[str] = None,
        region: str = "cn-north-4",
        auto_fetch_config: bool = True,
    ):
        self.ak = ak or os.environ.get("MT_AK")
        self.sk = sk or os.environ.get("MT_SK")
        if not self.ak or not self.sk:
            raise ValueError("AK and SK required (args or MT_AK/MT_SK env)")

        self.wapi = WapiClient(self.ak, self.sk)
        self.api = AiApi(self.ak, self.sk, region)

        if auto_fetch_config:
            self._fetch_config()

    def _fetch_config(self) -> Dict:
        """Fetch remote config and update local settings."""
        from sdk.core.config import VERSION

        try:
            gid = self._get_cached_gid()
            response = self.wapi.request(
                "/skill/config.json",
                method="POST",
                body={"gid": gid or "", "version": VERSION}
            )
        except RuntimeError as e:
            raise RuntimeError(f"Failed to fetch config: {e}") from e

        if response.get("gid"):
            self._cache_gid(response["gid"])

        # Update config
        if "algorithm" in response:
            algo = response["algorithm"]
            if "regions" in algo:
                self.api._config["regions"].update(algo["regions"])
                if self.api.region in algo["regions"]:
                    self.api.EndPoint = algo["regions"][self.api.region]
            if "invoke" in algo:
                import sdk.core.config as sdk_config
                sdk_config.INVOKE.update(algo["invoke"])

        return response

    def _get_cached_gid(self) -> Optional[str]:
        """Load gid from cache."""
        cache_file = os.path.expanduser(GID_CACHE_FILE)
        if os.path.exists(cache_file):
            try:
                with open(cache_file) as f:
                    return json.load(f).get("gid")
            except (json.JSONDecodeError, IOError):
                pass
        return None

    def _cache_gid(self, gid: str) -> None:
        """Save gid to cache."""
        cache_file = os.path.expanduser(GID_CACHE_FILE)
        try:
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, "w") as f:
                json.dump({"gid": gid}, f)
        except IOError:
            pass

    def _download_to_temp(self, url: str) -> Tuple[str, int]:
        """Download URL to temp file. Returns (path, size)."""
        max_b = url_download_max_bytes()
        conn_t = url_download_connect_timeout()
        read_t = url_download_read_timeout()

        resp = requests.get(url, stream=True, timeout=(conn_t, read_t), headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()

        fd, path = tempfile.mkstemp(prefix="kaipai_in_", suffix=".bin")
        total = 0
        try:
            with os.fdopen(fd, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        total += len(chunk)
                        if total > max_b:
                            raise RuntimeError(f"File too large (max {max_b} bytes)")
                        f.write(chunk)
        except Exception:
            os.unlink(path)
            raise
        return path, total

    def prepare_and_consume(self, source: str, task_name: str) -> Tuple[str, str]:
        """
        上传文件并消费权益，返回 (media_url, context)。

        这是核心封装方法，包含：
        1. 下载（如果是URL）
        2. 上传到OSS
        3. 消费权益

        :param source: 本地文件路径或HTTP(S) URL
        :param task_name: 任务名称
        :return: (media_url, context)
        """
        from sdk.core.api import _progress_log

        # 1. 处理输入（下载或直接使用）
        if source.startswith(("http://", "https://")):
            _progress_log(f"Downloading from URL: {source[:64]}...")
            tmp_path, size = self._download_to_temp(source)
            try:
                _progress_log(f"Downloaded {size} bytes, uploading to OSS...")
                url_data = self.api.upload_file(tmp_path)
            finally:
                os.unlink(tmp_path)
        else:
            if not os.path.isfile(source):
                raise FileNotFoundError(f"File not found: {source}")
            _progress_log(f"Uploading file to OSS: {source}")
            url_data = self.api.upload_file(source)

        if not url_data:
            raise RuntimeError("Upload failed")

        media_url = url_data.get("url") if isinstance(url_data, dict) else url_data

        # 2. 消费权益
        _progress_log(f"Consuming quota for task: {task_name}")
        gid = self._get_cached_gid()
        consume_result = self.wapi.request(
            "/skill/consume.json",
            method="POST",
            body={"url": media_url, "task": task_name, "gid": gid or ""}
        )
        context = consume_result.get("context", "") if consume_result else ""
        _progress_log("Quota consumed, submitting task...")

        return media_url, context

    def execute(
        self,
        task_name: str,
        source: str,
        params: Optional[Dict] = None,
        on_async_submitted: Optional[Callable[[str], None]] = None,
    ) -> Dict:
        """
        执行AI任务（一站式接口）。

        自动完成：下载→上传→消费权益→提交任务→轮询结果

        :param task_name: 任务名称
        :param source: 文件路径或URL
        :param params: 可选任务参数
        :param on_async_submitted: 异步任务提交回调
        :return: 任务结果
        """
        # 1. 准备资源并消费权益
        media_url, context = self.prepare_and_consume(source, task_name)

        # 2. 提交任务
        result = self.api.invoke_task(
            task_name,
            media_url,
            params,
            context,
            on_async_submitted=on_async_submitted
        )

        return result

    def query(self, task_id: str) -> Dict:
        """
        查询任务状态。

        :param task_id: 任务ID
        :return: 任务状态
        """
        policy = self.api.getAiStrategy()
        if not policy:
            raise RuntimeError("Failed to get AI strategy")
        return self.api.poll_status(task_id, policy)
