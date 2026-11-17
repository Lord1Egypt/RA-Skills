import json
import os
import tempfile
from copy import deepcopy
import requests
from pathlib import Path
from urllib.parse import urlencode
from ai import api
from sign_sdk import sign
import config as app_config
from agent_info import resolve_agent_info, agent_headers
from input_media import InputMediaValidationError, normalize_input_media, primary_media_index, uploaded_init_images
from params_schema import ParameterValidationError, OptionsSourceError, options_field, validate_parameters, validate_dynamic_options


_UPGRADE_NOTICE_CODE = "skill_upgrade_available"


def _load_env_file():
    """
    Load environment variables from a .env file.
    Search order: 1) directory containing client.py  2) current working directory
    """
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        env_path = Path.cwd() / '.env'

    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    if key and key not in os.environ:
                        os.environ[key] = value


_load_env_file()


def _wapi_meta_code_value(meta_code):
    """
    Normalize meta.code for comparisons (int). Unparseable non-zero codes become -1.
    Treat missing / 0 / "0" as success (0).
    """
    if meta_code is None:
        return 0
    if meta_code == 0 or meta_code == "0":
        return 0
    try:
        return int(meta_code)
    except (TypeError, ValueError):
        return -1


def _normalize_notices(payload):
    """Return valid user-facing notices from a WAPI response or response envelope."""
    if not isinstance(payload, dict):
        return []
    response = payload.get("response")
    if isinstance(response, dict):
        payload = response
    raw_notices = payload.get("notices")
    if not isinstance(raw_notices, list):
        return []

    notices = []
    for item in raw_notices:
        if not isinstance(item, dict):
            continue
        message = str(item.get("message") or "").strip()
        if not message:
            continue
        notice = deepcopy(item)
        notice["message"] = message
        if notice.get("code") is not None:
            notice["code"] = str(notice["code"]).strip()
        notices.append(notice)
    return notices


class WapiApiError(RuntimeError):
    """HTTP 200 but WAPI meta.code != 0.

    The raw payload remains available for internal diagnostics, while the public
    exception text intentionally omits request identifiers and response bodies.
    """

    def __init__(self, code: int, msg: str, raw: dict, *, original_code=None):
        self.code = code
        self.original_code = original_code if original_code is not None else code
        self.msg = msg or "Request failed"
        self.raw = raw if isinstance(raw, dict) else {}
        self.notices = _normalize_notices(self.raw)
        super().__init__(f"[{self.original_code}] {self.msg}")


class ConsumeDeniedError(WapiApiError):
    """Non-zero meta from POST /skill/consume.json (quota / permission)."""


class ConfigFetchError(WapiApiError):
    """Non-zero meta from POST /skill/config.json."""


def _catalog_items(value):
    """Yield catalog keys and records from supported dict/list response shapes."""
    if isinstance(value, dict):
        nested = value.get("items")
        if isinstance(nested, list):
            value = nested
        else:
            for key, item in value.items():
                if isinstance(item, dict):
                    yield str(key), item
            return

    if isinstance(value, list):
        for item in value:
            if not isinstance(item, dict):
                continue
            key = item.get("material_id") or item.get("id")
            if key is not None and str(key).strip():
                yield str(key).strip(), item


def normalize_task_catalog(response):
    """Normalize the server-selected config schema into a task catalog.

    A recognized ``schema`` is authoritative. Responses from older servers that
    omit it keep the existing catalog-metadata inference for compatibility. An
    unknown explicit schema fails closed instead of guessing its structure.
    """
    if not isinstance(response, dict):
        return {"mode": "unavailable", "source": None, "entries": []}

    algorithm = response.get("algorithm")
    if not isinstance(algorithm, dict):
        algorithm = {}
    invoke = algorithm.get("invoke")
    if not isinstance(invoke, dict):
        invoke = {}

    schema = str(response.get("schema") or "").strip().lower()
    if schema and schema not in {"v1", "v2"}:
        return {"mode": "unavailable", "source": "schema", "entries": []}

    source = None
    raw_catalog = None
    for owner_name, owner in (("response", response), ("algorithm", algorithm)):
        for field in ("catalog", "materials"):
            candidate = owner.get(field)
            if isinstance(candidate, (dict, list)) and candidate:
                source = f"{owner_name}.{field}"
                raw_catalog = candidate
                break
        if raw_catalog is not None:
            break

    if schema == "v1":
        source = "algorithm.invoke" if invoke else None
        items = list(_catalog_items(invoke))
        mode = "legacy"
    elif schema == "v2":
        if raw_catalog is not None:
            items = list(_catalog_items(raw_catalog))
        else:
            source = "algorithm.invoke" if invoke else None
            items = list(_catalog_items(invoke))
        mode = "v2"
    elif raw_catalog is not None:
        mode = "v2"
        items = list(_catalog_items(raw_catalog))
    else:
        source = "algorithm.invoke" if invoke else None
        items = list(_catalog_items(invoke))
        metadata_fields = {"material_id", "name", "description", "media_type"}
        mode = (
            "v2"
            if any(metadata_fields.intersection(item.keys()) for _, item in items)
            else "legacy"
            if items
            else "unavailable"
        )

    entries = []
    for key, catalog_spec in items:
        runtime_spec = invoke.get(key)
        if not isinstance(runtime_spec, dict):
            runtime_spec = {}
        spec = {**runtime_spec, **catalog_spec}
        material_id = key.strip()
        if not material_id:
            continue
        name = str(spec.get("name") or "").strip()
        description = str(spec.get("description") or "").strip()
        params = spec.get("params")
        if params is None:
            params = {}
        entry = {
            "material_id": material_id,
            "name": name,
            "description": description,
            "media_type": str(spec.get("media_type") or "").strip().lower(),
            "task": str(spec.get("task") or "").strip(),
            "task_type": str(spec.get("task_type") or "").strip(),
            "params": deepcopy(params),
        }
        if spec.get("profile") is not None:
            entry["profile"] = deepcopy(spec["profile"])
        if spec.get("input_media") is not None:
            entry["input_media"] = deepcopy(spec["input_media"])
        if mode == "v2" and spec.get("params_schema") is not None:
            entry["params_schema"] = deepcopy(spec["params_schema"])
        entries.append(entry)

    return {"mode": mode, "source": source, "entries": entries}


class WapiClient:
    """Signed HTTP client for the configured Vmake WAPI gateway."""

    def __init__(self, ak, sk, *, agent_name=None, agent_version=None, agent_model=None):
        """
        :param ak: Access Key
        :param sk: Secret Key
        """
        self.ak = ak
        self.sk = sk
        self.endpoint = app_config.WAPI_ENDPOINT
        self.agent_info = resolve_agent_info(agent_name, agent_version, agent_model)

    def request(self, path, method="GET", params=None, body=None):
        """
        Send a signed request to the configured Vmake WAPI gateway.

        :return: Parsed JSON under the top-level ``response`` field
        :raises WapiApiError: on HTTP 200 with meta.code != 0
        :raises RuntimeError: on HTTP errors and transport failures
        """
        query_string = urlencode(params) if params else ""
        uri = f"https://{self.endpoint}{path}"
        if query_string:
            uri = f"{uri}?{query_string}"

        try:
            import config as app_config
            signer = sign.Signer(self.ak, self.sk)
            headers = {
                # sign.HeaderHost: self.endpoint,
                "User-Agent": app_config.USER_AGENT,
            }

            headers.update(agent_headers(self.agent_info, app_config.VERSION))

            body_str = ""
            if body:
                headers["Content-Type"] = "application/json"
                body_str = json.dumps(body)

            signed_request = signer.sign(uri, method, headers, body_str)

            session = requests.Session()
            timeout = 30 if path == "/skill/consume.json" else 10
            resp = session.send(signed_request, timeout=timeout)

            if resp.status_code == 200:
                data = json.loads(resp.content)

                meta = data.get("meta") or {}
                raw_code = meta.get("code", 0)
                norm = _wapi_meta_code_value(raw_code)

                if norm != 0:
                    msg = meta.get("msg", "Request failed")
                    raise WapiApiError(
                        norm, msg, data, original_code=raw_code
                    )

                return data.get("response", {})
            else:
                raise RuntimeError(
                    f"Request failed: HTTP {resp.status_code} | body: {resp.text}"
                )
        except (RuntimeError, WapiApiError):
            raise
        except Exception as e:
            raise RuntimeError(f"Request error: {e}")


class SkillClient:
    """
    High-level client: remote config, quota consume, upload, and task run.

    Example::
        client = SkillClient()
        client.fetch_config()
        result = client.run_task("sod", "/path/to/image.jpg")
    """

    def __init__(self, ak=None, sk=None, region="cn-north-4", oss_region=None, auto_fetch_config=True, *, agent_name=None, agent_version=None, agent_model=None):
        """
        :param ak: Access Key (default: env ``MT_AK``)
        :param sk: Secret Key (default: env ``MT_SK``)
        :param region: API region, default cn-north-4
        :param oss_region: Optional OSS region override
        :param auto_fetch_config: If True, fetch remote config on init
        :param agent_name: Optional caller host name; defaults to SKILL_AGENT_NAME
        :param agent_version: Optional host version; defaults to SKILL_AGENT_VERSION
        :param agent_model: Optional caller model; defaults to SKILL_AGENT_MODEL
        """
        self.ak = ak or os.environ.get("MT_AK")
        self.sk = sk or os.environ.get("MT_SK")

        if not self.ak or not self.sk:
            raise ValueError('请通过参数或 MT_AK / MT_SK 提供 AK 和 SK')

        self.wapi = WapiClient(self.ak, self.sk, agent_name=agent_name, agent_version=agent_version, agent_model=agent_model)

        self._pipeline_trace: list = []
        self._notices: list = []
        self._notice_keys: set = set()
        self.api = api.AiApi(
            self.ak,
            self.sk,
            region,
            oss_region,
            notice_handler=self._collect_notices,
        )
        self.config_response = None
        self.task_catalog = None

        if auto_fetch_config:
            self.fetch_config()

    def fetch_config(self, gid=None, version=None):
        """
        Fetch skill config from wapi and refresh local SDK settings.

        :param gid: Optional group id (uses cached gid if omitted)
        :param version: Client version string (default from config.VERSION)
        """
        if version is None:
            version = getattr(app_config, "VERSION", "v2.0.2")

        if not gid:
            cached_gid = self._get_cached_gid()
            if cached_gid:
                gid = cached_gid

        try:
            response = self.wapi.request(
                "/skill/config.json",
                method="POST",
                body={
                    "gid": gid or "",
                    "version": version or "",
                    "supported_schemas": list(
                        getattr(app_config, "SUPPORTED_SCHEMAS", ("v2", "v1"))
                    ),
                },
            )
        except WapiApiError as e:
            raise ConfigFetchError(
                e.code, e.msg, e.raw, original_code=e.original_code
            ) from e
        except RuntimeError as e:
            raise ConfigFetchError(
                -1,
                '获取 Skill 配置失败（请检查网络、AK/SK 和服务端）。详情：' + str(e),
                {},
            ) from e

        if response.get("gid"):
            self._cache_gid(response["gid"])

        self._collect_notices(response)
        has_upgrade_notice = any(
            notice.get("code") == _UPGRADE_NOTICE_CODE
            for notice in self._notices
        )
        if response.get("need_update") and not has_upgrade_notice:
            message = response.get("update_message", "A newer version is available; please update.")
            latest = str(response.get("latest_version") or "").strip()
            self._collect_notices(
                {
                    "notices": [
                        {
                            "code": _UPGRADE_NOTICE_CODE,
                            "level": "warning",
                            "message": message,
                            "dedupe_key": _UPGRADE_NOTICE_CODE + ":" + latest,
                        }
                    ]
                }
            )

        self._update_config_from_response(response)
        self.config_response = response
        self.task_catalog = normalize_task_catalog(response)
        if self.task_catalog["mode"] == "v2":
            for entry in self.task_catalog["entries"]:
                if not entry["task"]:
                    continue
                runtime_spec = {
                    "task": entry["task"],
                    "task_type": entry["task_type"],
                    "params": deepcopy(entry["params"]),
                }
                if "profile" in entry:
                    runtime_spec["profile"] = deepcopy(entry["profile"])
                if "input_media" in entry:
                    runtime_spec["input_media"] = deepcopy(entry["input_media"])
                if "params_schema" in entry:
                    runtime_spec["params_schema"] = deepcopy(entry["params_schema"])
                app_config.INVOKE[entry["material_id"]] = runtime_spec

        return response

    def _collect_notices(self, payload):
        """Collect server notices once per client run while preserving unknown fields."""
        added = 0
        for notice in _normalize_notices(payload):
            key = str(
                notice.get("dedupe_key")
                or (str(notice.get("code") or "") + ":" + notice["message"])
            )
            if key in self._notice_keys:
                continue
            self._notice_keys.add(key)
            self._notices.append(notice)
            added += 1
        return added

    def get_notices(self):
        """Return a defensive copy of notices collected during this client run."""
        return deepcopy(self._notices)

    def _attach_notices(self, result):
        """Attach collected notices to a result without changing its success semantics."""
        if not isinstance(result, dict):
            return result
        self._collect_notices(result)
        out = dict(result)
        if self._notices:
            out["notices"] = self.get_notices()
        return out

    def get_task_catalog(self, *, refresh=False):
        """Return the normalized remote task catalog, fetching it when needed."""
        if refresh or self.task_catalog is None:
            self.fetch_config()
        return deepcopy(self.task_catalog)

    def resolve_task(self, task_name):
        """Resolve only a task advertised by the successfully fetched config.

        V2 prefers the exact material_id returned by catalog. A unique display name
        remains accepted for backward compatibility.
        Legacy aliases are accepted only when the response is legacy and the alias
        exists in its invoke map.
        """
        requested = str(task_name or "").strip()
        catalog = self.get_task_catalog()
        mode = catalog.get("mode")
        entries = catalog.get("entries") or []
        if mode == "v2":
            for entry in entries:
                if entry.get("material_id") == requested:
                    return entry
            matches = [entry for entry in entries if entry.get("name") == requested]
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                raise KeyError(
                    f'V2 任务名称 {requested!r} 在服务端配置中不唯一；请使用 catalog 返回的准确 material_id。'
                )
            raise KeyError(
                f'未找到 V2 任务 {requested!r}；请运行 `vmake_ai.py catalog` 并使用返回的准确 material_id。'
            )
        if mode == "legacy":
            for entry in entries:
                if entry.get("material_id") == requested:
                    return entry
            raise KeyError(
                f'旧版任务 {requested!r} 未由服务端配置返回；不允许使用本地备用任务。'
            )
        raise RuntimeError(
            '服务端配置未提供可用的 V2 目录或旧版 invoke 配置。'
        )

    def _get_cached_gid(self):
        """Load gid from local disk cache."""
        cache_file = os.path.expanduser('~/.cache/kaipai/gid.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("gid")
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def _cache_gid(self, gid):
        """Persist gid to local disk cache."""
        cache_file = os.path.expanduser('~/.cache/kaipai/gid.json')
        try:
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"gid": gid}, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _update_config_from_response(self, response):
        """Apply algorithm block from config response to AiApi and INVOKE."""
        if "algorithm" not in response:
            return

        algo = response["algorithm"]

        if "regions" in algo:
            self.api._config["regions"].update(algo["regions"])
            if self.api.region in algo["regions"]:
                self.api.EndPoint = algo["regions"][self.api.region]

        if "token_policy_type" in algo:
            self.api._config["token_policy_type"] = algo["token_policy_type"]

        if "token_policy_types" in algo:
            self.api._config["token_policy_types"] = algo["token_policy_types"]

        if "invoke" in algo:
            import config as app_config
            app_config.INVOKE.update(algo["invoke"])

    def _consume_permission(self, url, task, urls=None):
        """Consume once with a primary URL and the complete ordered media list."""
        if not url and not urls:
            raise InputMediaValidationError('至少需要提供一个输入素材')
        body = {"task": task, "gid": self._get_cached_gid() or ""}
        if url is not None:
            body["url"] = url
        body["urls"] = list(urls) if urls else [url]

        try:
            response = self.wapi.request(
                "/skill/consume.json",
                method="POST",
                body=body
            )
            self._collect_notices(response)
            return response
        except WapiApiError as e:
            self._collect_notices({"notices": e.notices})
            raise ConsumeDeniedError(
                e.code, e.msg, e.raw, original_code=e.original_code
            ) from e

    @staticmethod
    def _preview_media_ref(url) -> str:
        if url is None:
            return ""
        if isinstance(url, str):
            return api.safe_url_preview(url)
        if isinstance(url, dict):
            u = url.get("url") or url.get("uri")
            if u:
                return api.safe_url_preview(str(u))
        try:
            return api.safe_url_preview(json.dumps(url, ensure_ascii=False), max_len=80)
        except (TypeError, ValueError):
            return "<non-serializable>"

    def _fetch_http_input_to_tempfile(self, url: str) -> tuple[str, int]:
        """
        Stream-download URL to a temp file (bounded size). Caller must unlink path.
        """
        preview = api.safe_url_preview(url)
        conn_t = app_config.url_download_connect_timeout()
        read_t = app_config.url_download_read_timeout()
        max_b = app_config.url_download_max_bytes()
        headers = {
            "User-Agent": app_config.USER_AGENT,
        }
        try:
            with requests.get(
                url,
                stream=True,
                timeout=(conn_t, read_t),
                headers=headers,
            ) as resp:
                try:
                    resp.raise_for_status()
                except requests.HTTPError as e:
                    code = getattr(resp, "status_code", "?")
                    raise RuntimeError(
                        f"Input URL HTTP {code} (url={preview}). "
                        "Signed URLs may be expired; shell may have broken the URL at '&' without quotes."
                    ) from e

                fd, path = tempfile.mkstemp(prefix="openclaw_in_", suffix=".bin")
                total = 0
                try:
                    with os.fdopen(fd, "wb") as out:
                        for chunk in resp.iter_content(chunk_size=65536):
                            if not chunk:
                                continue
                            total += len(chunk)
                            if total > max_b:
                                raise RuntimeError(
                                    f"Input URL download exceeds max bytes ({max_b}); url={preview}. "
                                    "Set MT_AI_URL_MAX_BYTES to raise the cap or use a smaller file."
                                )
                            out.write(chunk)
                except Exception:
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
                    raise

                if total == 0:
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
                    raise RuntimeError(
                        f"Input URL returned empty body (url={preview})."
                    )

                return path, total
        except requests.Timeout as e:
            raise RuntimeError(
                f"Input URL download timed out (url={preview}). "
                f"Try MT_AI_URL_READ_TIMEOUT (read={read_t}s, connect={conn_t}s) or "
                f"`vmake_ai.py resolve-input --url ...` then pass local --input. Detail: {e}"
            ) from e
        except requests.RequestException as e:
            raise RuntimeError(
                f"Input URL download failed (url={preview}): {e}"
            ) from e

    def validate_task_parameters(self, selection, params=None):
        """Validate a V2 selection before downloads, uploads, quota or worker launch."""
        schema = selection.get("params_schema")
        if schema is None:
            return
        if params is not None and not isinstance(params, dict):
            raise ParameterValidationError("params: expected object")
        override = (params or {}).get("parameter")
        if isinstance(override, dict) and "repost_url" in override:
            raise ParameterValidationError("parameter.repost_url: system callback is not user-editable")
        merged = api._deep_merge_params(selection.get("params") or {}, params or {})
        parameter = merged.get("parameter")
        # Remove system transport fields from a validation copy only.
        if isinstance(parameter, dict):
            merged["parameter"] = {key: value for key, value in parameter.items()
                                   if key not in ("repost_url", "rsp_media_type")}
        validate_parameters(schema, merged)
        validate_dynamic_options(
            schema, merged,
            lambda field_path: self.get_params_field_options(selection["material_id"], field_path),
        )

    def get_params_field_options(self, task_name, field_path):
        """Fetch a complete option list for an advertised params-root field; never consume."""
        selection = self.resolve_task(task_name)
        schema = selection.get("params_schema")
        if schema is None:
            raise ValueError('当前任务未配置 params_schema')
        options_field(schema, field_path)
        try:
            return self.wapi.request(
                "/skill/params_field_options.json", method="POST",
                body={"material_id": selection["material_id"], "field_path": field_path},
            )
        except Exception as error:
            raise OptionsSourceError('获取参数字段选项失败：' + str(error)) from error

    def _resolve_executable_task(self, task_name, params=None, profile=None):
        """Validate the remote task and preset before any upload or paid operation."""
        selection = self.resolve_task(task_name)
        resolved_task = selection.get("material_id")
        if not str(selection.get("task") or "").strip():
            raise ValueError(
                f'远端任务 {resolved_task!r} 缺少可执行配置；请检查服务端任务目录。'
            )
        self.validate_task_parameters(selection, params)
        api._prepare_invoke_task(resolved_task, params, profile)
        return selection

    def validate_input_media(self, selection, value):
        """Validate all inputs before uploads or quota consumption."""
        return normalize_input_media(value, selection)

    def run_task(
        self,
        task_name,
        image_path=None,
        params=None,
        on_async_submitted=None,
        profile=None,
    ):
        """
        Upload media (or use remote URL) and run the named algorithm task.

        :param task_name: Preset name from config INVOKE
        :param image_path: Local path, HTTP(S) URL, or ordered list of sources/input objects
        :param params: Optional invoke params merged over preset defaults
        :param profile: Optional first-input profile merged over preset defaults
        :param on_async_submitted: Optional callback invoked with the accepted task id
            before polling, so callers can persist a recovery checkpoint.
        """
        self._pipeline_trace = []
        selection = self._resolve_executable_task(task_name, params, profile)
        inputs = self.validate_input_media(selection, image_path)
        resolved_task = selection.get("material_id")
        display_task = selection.get("name") or str(task_name or "").strip()
        self._pipeline_trace.append(
            {
                "step": "resolve_remote_task",
                "config_mode": self.task_catalog.get("mode"),
                "task": display_task,
                "media_type": selection.get("media_type"),
            }
        )

        urls = [self._upload_input_media(item["source"]) for item in inputs]
        primary = primary_media_index(inputs)
        url = urls[primary] if urls else None
        ref = self._preview_media_ref(url)
        self._pipeline_trace.append({"step": "media_url_ready", "input_media": ref})
        self.api._validate_execution_policy(self.api.getAiStrategy())
        api._progress_log(f"quota: POST /skill/consume.json task={display_task!r}")
        consume_info = self._consume_permission(url, resolved_task, urls=urls)
        self._collect_notices(consume_info)
        context = consume_info.get("context", "") if consume_info else ""
        api._progress_log("quota: consume OK → submit algorithm job")

        self._pipeline_trace.append({"step": "consume_quota", "task": display_task})
        self._pipeline_trace.append(
            {"step": "submit_algorithm", "invoke_preset": display_task}
        )

        invoke_kwargs = {}
        if on_async_submitted is not None:
            invoke_kwargs["on_async_submitted"] = on_async_submitted
        if profile is not None:
            invoke_kwargs["profile"] = profile
        result = self.api.invoke_task(
            resolved_task, urls[0] if len(inputs) == 1 and not inputs[0]["profile"] else uploaded_init_images(inputs, urls),
            params, context, **invoke_kwargs
        )
        return self._attach_notices(result)

    def _upload_input_media(self, image_path):
        """Upload one input, cleaning remote-download files even on failure."""
        if isinstance(image_path, str) and image_path.startswith(("http://", "https://")):
            preview = api.safe_url_preview(image_path)
            api._progress_log(f"input: download from URL (GET {preview})")
            tmp_path, n = self._fetch_http_input_to_tempfile(image_path)
            try:
                api._progress_log(
                    f"input: download done ({n} bytes) → OSS upload (PutObject)"
                )
                self._pipeline_trace.append(
                    {"step": "download_input", "from_url": preview, "bytes": n}
                )
                url = self.api.getFileUrl(tmp_path)
                self._pipeline_trace.append(
                    {"step": "upload_input", "via": "oss_put_object", "bytes": n}
                )
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
        else:
            ip = image_path
            sz = None
            if isinstance(ip, str) and os.path.isfile(ip):
                sz = os.path.getsize(ip)
                api._progress_log(
                    f"input: local file → OSS upload ({os.path.basename(ip)}, {sz} bytes)"
                )
            else:
                api._progress_log("input: local path → OSS upload (PutObject)")
            url = self.api.getFileUrl(image_path)
            self._pipeline_trace.append(
                {
                    "step": "upload_input",
                    "via": "oss_put_object",
                    "path": os.path.basename(ip) if isinstance(ip, str) else str(ip),
                    "bytes": sz,
                }
            )
        if isinstance(url, dict):
            url = url.get("url")
        if not isinstance(url, str) or not url.strip():
            raise RuntimeError('上传输入媒体失败')

        return url

    def poll_task_status(self, task_id: str):
        """
        Resume status polling for an existing async task (same signing / token policy
        as run-task). Does not upload media or call consume — use the ``task_id`` from
        a previous submit or failure JSON.

        :param task_id: Full task id string from ``data.result.id`` or failure payload
        :return: Same shapes as ``run_task`` (success dict with ``output_urls``, or
            failure dicts with ``skill_status`` / ``error``).
        """
        tid = (task_id or "").strip()
        if not tid:
            raise ValueError('必须提供 task_id')
        self._pipeline_trace = [
            {
                "step": "resume_poll",
                "description": "No input download, OSS upload, or consume; algorithm status GET only",
                "task_id": tid,
            }
        ]
        api._progress_log(
            "query-task: resume polling only (no input download / OSS upload / consume)"
        )
        policy = self.api.getAiStrategy()
        if not policy:
            raise RuntimeError(
                '加载 AI token policy 失败（请检查网络、AK/SK 和 fetch_config）。'
            )
        return self._attach_notices(self.api.status(tid, policy))
