import json
import os
from typing import Any, Dict, List, Optional, Tuple

import requests


def _strip_quotes(value: str) -> str:
    v = (value or "").strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        return v[1:-1]
    return v


def _safe_json_loads(raw: Optional[str]) -> Any:
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def _load_dotenv(dotenv_path: str = ".env") -> None:
    try:
        base_dir = os.path.dirname(__file__)
        path = dotenv_path or ".env"
        if not os.path.isabs(path):
            path = os.path.join(base_dir, path)
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                if "=" not in s:
                    continue
                k, v = s.split("=", 1)
                key = k.strip()
                if not key or key in os.environ:
                    continue
                os.environ[key] = _strip_quotes(v)
    except Exception:
        return


def _normalize_headers(headers: Any) -> Dict[str, str]:
    if not isinstance(headers, dict):
        return {}
    out: Dict[str, str] = {}
    for k, v in headers.items():
        key = str(k).strip()
        if not key:
            continue
        if key.lower() in {"authorization"}:
            continue
        if key.upper() == "HOST":
            key = "Host"
        out[key] = str(v)
    return out


def _truncate_str(value: Any, max_len: int = 2000) -> str:
    s = "" if value is None else str(value)
    if len(s) <= max_len:
        return s
    return s[: max_len - 1] + "…"


def _redact_for_log(value: Any, *, max_str_len: int = 2000, max_list_len: int = 20, max_depth: int = 6, _depth: int = 0) -> Any:
    if _depth >= max_depth:
        return "<truncated>"
    if isinstance(value, dict):
        out: Dict[str, Any] = {}
        for k, v in value.items():
            key = str(k)
            if key.lower() in {"authorization", "api_key", "apikey"}:
                continue
            out[key] = _redact_for_log(
                v,
                max_str_len=max_str_len,
                max_list_len=max_list_len,
                max_depth=max_depth,
                _depth=_depth + 1,
            )
        return out
    if isinstance(value, list):
        trimmed = value[:max_list_len]
        out_list = [
            _redact_for_log(
                x,
                max_str_len=max_str_len,
                max_list_len=max_list_len,
                max_depth=max_depth,
                _depth=_depth + 1,
            )
            for x in trimmed
        ]
        if len(value) > max_list_len:
            out_list.append("<truncated>")
        return out_list
    if isinstance(value, str):
        return _truncate_str(value, max_len=max_str_len)
    return value


def _summarize_debug_detail(detail: Any) -> Any:
    if not isinstance(detail, dict):
        return detail
    summary: Dict[str, Any] = {}
    for key in ("url", "path", "status_code", "request_id"):
        if key in detail:
            summary[key] = detail.get(key)
    if "response" in detail:
        summary["response"] = detail.get("response")
    return summary or detail


def _has_cjk(text: str) -> bool:
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":
            return True
    return False


def _maybe_fix_mojibake(text: str) -> str:
    if not text:
        return text
    if _has_cjk(text):
        return text
    if not any(x in text for x in ("Ã", "Â", "æ", "ç", "å", "é", "è", "ä", "ö", "ü")):
        return text
    try:
        fixed = text.encode("latin1").decode("utf-8")
    except Exception:
        return text
    return fixed if _has_cjk(fixed) else fixed


def _build_chat_input_message(
    *,
    input_message: Optional[Dict[str, Any]],
    text: Optional[str],
    image_url: Optional[str],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if input_message is not None:
        return input_message, None
    content: List[Dict[str, Any]] = []
    if text is not None and str(text).strip():
        content.append({"type": "text", "text": str(text)})
    if image_url is not None and str(image_url).strip():
        content.append({"type": "image_url", "image_url": {"url": str(image_url)}})
    if not content:
        return None, "缺少 input_message：请提供 input_message 或 text/image_url"
    return {"content": content}, None


def _build_search_query(
    *,
    query: Optional[Dict[str, Any]],
    text: Optional[str],
    image_url: Optional[str],
    image_query_instruction: Optional[str],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if query is not None:
        return query, None
    query_obj: Dict[str, Any] = {}
    if text is not None and str(text).strip():
        query_obj["text"] = text
    if image_url is not None and str(image_url).strip():
        query_obj["image_url"] = image_url
    if image_query_instruction is not None and str(image_query_instruction).strip():
        query_obj["image_query_instruction"] = image_query_instruction
    if not query_obj or (not query_obj.get("text") and not query_obj.get("image_url")):
        return None, "query 必须至少包含 text 或 image_url"
    return query_obj, None


class VikingAISearch:
    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        application_id: Optional[str] = None,
        timeout: int = 60,
    ) -> None:
        _load_dotenv()
        self.base_url = (base_url or os.getenv("VIKING_AISEARCH_API_BASE") or "").rstrip("/")
        self.api_key = api_key or os.getenv("VIKING_AISEARCH_API_KEY")
        self.application_id = application_id or os.getenv("VIKING_AISEARCH_APPLICATION_ID") or ""
        self.extra_headers = _normalize_headers(
            _safe_json_loads(os.getenv("VIKING_AISEARCH_EXTRA_HEADERS_JSON"))
        )
        self.timeout = timeout

        if not self.base_url:
            raise ValueError(
                "缺少 base_url：请设置 VIKING_AISEARCH_API_BASE 或在初始化时传入 base_url"
            )
        if not self.api_key:
            raise ValueError(
                "缺少 api_key：请设置 VIKING_AISEARCH_API_KEY 或在初始化时传入 api_key"
            )

    def _ok(self, data: Any, message: str, *, raw: Any) -> Dict[str, Any]:
        return {"success": True, "message": message, "data": data, "raw": raw}

    def _error(self, message: str, *, error: Any = None, raw: Any = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"success": False, "message": message}
        if error is not None:
            payload["error"] = error
        if raw is not None:
            payload["raw"] = raw
        return payload

    def _wrap_raw(self, raw: Any, request_id: Optional[str]) -> Any:
        if isinstance(raw, dict):
            raw.setdefault("request_id", request_id)
            return raw
        return {"request_id": request_id, "response": raw}

    def _headers(self, *, accept: str) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": accept,
        }
        if self.extra_headers:
            headers.update(self.extra_headers)
        return headers

    def _post_json(self, path: str, payload: Dict[str, Any]) -> Any:
        url = f"{self.base_url}{path}"
        headers = self._headers(accept="application/json")
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(str(e)) from e

        raw_json: Any = None
        raw_text: str = ""
        try:
            raw_json = resp.json()
        except Exception:
            raw_text = resp.text

        if resp.status_code >= 400:
            response_payload = raw_json if raw_json is not None else _truncate_str(raw_text)
            debug_detail: Dict[str, Any] = {
                "url": url,
                "path": path,
                "status_code": resp.status_code,
                "request": {"body": _redact_for_log(payload)},
                "response": response_payload,
            }
            raise RuntimeError(f"HTTP {resp.status_code}", debug_detail)

        return raw_json if raw_json is not None else raw_text

    def _post_stream(self, path: str, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = self._headers(accept="text/event-stream")
        try:
            resp = requests.post(
                url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as e:
            raise RuntimeError(str(e)) from e
        resp.encoding = "utf-8"

        if resp.status_code >= 400:
            raw_json: Any = None
            raw_text: str = ""
            try:
                raw_json = resp.json()
            except Exception:
                raw_text = resp.text
            response_payload = raw_json if raw_json is not None else _truncate_str(raw_text)
            debug_detail: Dict[str, Any] = {
                "url": url,
                "path": path,
                "status_code": resp.status_code,
                "request": {"body": _redact_for_log(payload)},
                "response": response_payload,
            }
            raise RuntimeError(f"HTTP {resp.status_code}", debug_detail)

        return resp

    def _aggregate_chat_stream(self, resp: requests.Response) -> Dict[str, Any]:
        request_id: str = ""
        text_parts: List[str] = []
        citations: List[Any] = []
        chunk_count = 0

        buf = ""
        for raw_line in resp.iter_lines(decode_unicode=False):
            if raw_line is None:
                continue
            if isinstance(raw_line, bytes):
                s = raw_line.decode("utf-8", errors="replace").strip()
            else:
                s = str(raw_line).strip()
            if not s:
                continue
            if s.startswith("data:"):
                s = s[len("data:") :].strip()
                if s == "[DONE]":
                    break
            buf = (buf + s) if buf else s
            try:
                obj = json.loads(buf)
            except Exception:
                continue
            buf = ""

            chunk_count += 1

            if not request_id:
                request_id = str(obj.get("request_id") or "")

            result = obj.get("result") or {}
            if isinstance(result, dict):
                if "content" in result and result.get("content") is not None:
                    part = str(result.get("content"))
                    text_parts.append(_maybe_fix_mojibake(part))
                if "citation" in result and result.get("citation") is not None:
                    c = result.get("citation")
                    if isinstance(c, list):
                        citations.extend(c)
                    else:
                        citations.append(c)
                if str(result.get("stop_reason") or "") == "stop":
                    break

        content_text = "".join(text_parts)
        data = {
            "request_id": request_id or None,
            "content": _maybe_fix_mojibake(content_text),
            "citation": citations,
        }
        raw = {"request_id": request_id or None, "chunk_count": chunk_count}
        return {"data": data, "raw": raw}

    def chat(
        self,
        *,
        application_id: str = "",
        session_id: str = "",
        dataset_id: str = "",
        input_message: Optional[Dict[str, Any]] = None,
        text: Optional[str] = None,
        image_url: Optional[str] = None,
        user: Optional[Dict[str, Any]] = None,
        enable_suggestions: Optional[bool] = None,
        search_param: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        application_id = application_id or self.application_id
        if not application_id:
            return self._error("application_id 不能为空")

        path = f"/api/v1/application/{application_id}/chat_search"

        if body is not None:
            if not isinstance(body, dict):
                return self._error("body 必须为 JSON Object")
            if not str(body.get("session_id") or ""):
                return self._error("session_id 不能为空（body.session_id）")
            try:
                resp = self._post_stream(path, body)
                aggregated = self._aggregate_chat_stream(resp)
                return self._ok(aggregated["data"], "对话成功", raw=aggregated["raw"])
            except Exception as e:
                err: Dict[str, Any] = {"detail": str(e)}
                raw: Any = None
                if isinstance(e, RuntimeError) and len(e.args) >= 2:
                    err["message"] = str(e.args[0])
                    raw = e.args[1]
                    if isinstance(raw, dict):
                        err["detail"] = _summarize_debug_detail(raw)
                rid = None
                if isinstance(raw, dict):
                    rid = raw.get("request_id") or raw.get("requestId") or raw.get("RequestId")
                msg = err.get("message") or "对话失败"
                return self._error(msg, error=err, raw=self._wrap_raw(raw, rid))

        if not session_id:
            return self._error("session_id 不能为空")

        body_dict: Dict[str, Any] = {"session_id": session_id}
        if user is not None:
            body_dict["user"] = user
        if enable_suggestions is not None:
            body_dict["enable_suggestions"] = True if enable_suggestions else False
        if dataset_id and search_param is None:
            search_param = {"dataset_ids": [dataset_id]}
        elif dataset_id and isinstance(search_param, dict) and not search_param.get("dataset_ids"):
            search_param = {**search_param, "dataset_ids": [dataset_id]}
        if search_param is not None:
            body_dict["search_param"] = search_param
        if context is not None:
            body_dict["context"] = context

        input_msg, err = _build_chat_input_message(
            input_message=input_message,
            text=text,
            image_url=image_url,
        )
        if err:
            return self._error(err)
        body_dict["input_message"] = input_msg

        try:
            resp = self._post_stream(path, body_dict)
            aggregated = self._aggregate_chat_stream(resp)
            return self._ok(aggregated["data"], "对话成功", raw=aggregated["raw"])
        except Exception as e:
            err_obj: Dict[str, Any] = {"detail": str(e)}
            raw: Any = None
            if isinstance(e, RuntimeError) and len(e.args) >= 2:
                err_obj["message"] = str(e.args[0])
                raw = e.args[1]
                if isinstance(raw, dict):
                    err_obj["detail"] = _summarize_debug_detail(raw)
            rid = None
            if isinstance(raw, dict):
                rid = raw.get("request_id") or raw.get("requestId") or raw.get("RequestId")
            msg = err_obj.get("message") or "对话失败"
            return self._error(msg, error=err_obj, raw=self._wrap_raw(raw, rid))

    def search(
        self,
        application_id: str = "",
        scene_id: str = "",
        dataset_id: str = "",
        *,
        session_id: str = "",
        query: Optional[Dict[str, Any]] = None,
        text: Optional[str] = None,
        image_url: Optional[str] = None,
        image_query_instruction: Optional[str] = None,
        page_number: int = 1,
        page_size: Optional[int] = None,
        user: Optional[Dict[str, Any]] = None,
        filter: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        output_fields: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
        conditional_boost: Optional[List[Dict[str, Any]]] = None,
        disable_personalize: Optional[bool] = None,
    ) -> Dict[str, Any]:
        application_id = application_id or self.application_id
        if not application_id:
            return self._error("application_id 不能为空")

        if not dataset_id:
            dataset_id = os.getenv("VIKING_AISEARCH_SEARCH_DATASET_ID") or ""
        if not scene_id:
            scene_id = os.getenv("VIKING_AISEARCH_SEARCH_SCENE_ID") or ""

        if not dataset_id and scene_id and not scene_id.strip().startswith("scene"):
            dataset_id, scene_id = scene_id, ""
        if not dataset_id:
            return self._error("dataset_id 不能为空")
        if page_number < 1:
            return self._error("page_number 必须从 1 开始")

        query_obj, err = _build_search_query(
            query=query,
            text=text,
            image_url=image_url,
            image_query_instruction=image_query_instruction,
        )
        if err:
            return self._error(err)

        body: Dict[str, Any] = {
            "query": query_obj,
            "dataset_id": dataset_id,
            "page_number": page_number,
        }
        if session_id:
            body["session_id"] = session_id
        if page_size is not None:
            body["page_size"] = page_size
        if user is not None:
            body["user"] = user
        if filter is not None:
            body["filter"] = filter
        if sort_by is not None:
            body["sort_by"] = sort_by
        if sort_order is not None:
            body["sort_order"] = sort_order
        if output_fields is not None:
            body["output_fields"] = output_fields
        if context is not None:
            body["context"] = context
        if conditional_boost is not None:
            body["conditional_boost"] = conditional_boost
        if disable_personalize is not None:
            body["disable_personalize"] = disable_personalize

        if scene_id:
            path = f"/api/v1/application/{application_id}/search/{scene_id}"
        else:
            path = f"/api/v1/application/{application_id}/search"

        try:
            raw = self._post_json(path, body)
            result = (raw or {}).get("result") or {}
            normalized = {
                "request_id": (raw or {}).get("request_id"),
                "search_results": result.get("search_results") or [],
                "total_items": result.get("total_items"),
                "spell_correction": result.get("spell_correction"),
            }
            if isinstance(raw, dict):
                raw.setdefault("request_id", normalized.get("request_id"))
                return self._ok(normalized, "搜索成功", raw=raw)
            return self._ok(normalized, "搜索成功", raw={"request_id": normalized.get("request_id"), "response": raw})
        except Exception as e:
            err_obj: Dict[str, Any] = {"detail": str(e)}
            raw: Any = None
            if isinstance(e, RuntimeError) and len(e.args) >= 2:
                err_obj["message"] = str(e.args[0])
                raw = e.args[1]
                if isinstance(raw, dict):
                    err_obj["detail"] = _summarize_debug_detail(raw)
            msg = err_obj.get("message") or "搜索失败"
            return self._error(msg, error=err_obj, raw=self._wrap_raw(raw, None))
