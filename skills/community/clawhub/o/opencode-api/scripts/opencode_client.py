#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCode HTTP API Client（完整 SDK 版）
用於 OpenClaw 透過 HTTP API 呼叫 OpenCode Server

支援完整 SDK 功能：
- 基礎：health、session CRUD、訊息傳送、多輪對話
- 進階：structured output、noReply、abort、share、revert、providers
- 工具：text search、file search、file read、git status
- TUI：toast、prompt append
- 事件：event subscribe（需 requests + sseclient）

使用方式：
    python opencode_client.py --health
    python opencode_client.py --session <id> --prompt "<msg>"
    python opencode_client.py --task review --code "<code>"
    python opencode_client.py --providers
    python opencode_client.py --revert <session_id> --count 1
"""

import argparse
import json
import sys
import time
import threading
from pathlib import Path
from typing import Optional, Callable, Any

DEFAULT_BASE_URL = "http://127.0.0.1:4096"
DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 4096


class OpenCodeClient:
    """封裝 OpenCode Server HTTP API，支援自動啟動與完整 SDK 功能"""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        auto_start: bool = True,
        opencode_cmd: str = "opencode",
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.auto_start = auto_start
        self.opencode_cmd = opencode_cmd
        self._session_cache: Optional[dict] = None
        self._server_process: Optional[Any] = None

    # ─── 基礎方法 ───

    def is_server_running(self) -> bool:
        import requests
        try:
            r = requests.get(f"{self.base_url}/global/health", timeout=3)
            return r.status_code == 200 and r.json().get("healthy", False)
        except Exception:
            return False

    def ensure_server(self, wait_seconds: int = 15) -> bool:
        import requests
        import subprocess
        import urllib.parse

        if self.is_server_running():
            return True
        if not self.auto_start:
            return False

        print(f"[INFO] OpenCode Server 未運行，嘗試自動啟動...", file=sys.stderr)

        try:
            parsed = urllib.parse.urlparse(self.base_url)
            host = parsed.hostname or DEFAULT_SERVER_HOST
            port = parsed.port or DEFAULT_SERVER_PORT
        except Exception:
            host, port = DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT

        try:
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                subprocess.Popen(
                    ["cmd", "/c", "start", "OpenCode Server",
                     self.opencode_cmd, "serve",
                     "--port", str(port), "--hostname", host],
                    startupinfo=startupinfo,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                subprocess.Popen(
                    [self.opencode_cmd, "serve",
                     "--port", str(port), "--hostname", host],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        except FileNotFoundError:
            print(f"[ERROR] 找不到 '{self.opencode_cmd}'，請確認已安裝並加入 PATH", file=sys.stderr)
            return False
        except Exception as e:
            print(f"[ERROR] 啟動失敗: {e}", file=sys.stderr)
            return False

        for i in range(wait_seconds):
            time.sleep(1)
            if self.is_server_running():
                print(f"[INFO] OpenCode Server 已就緒（耗時 {i+1}s）", file=sys.stderr)
                return True
        print(f"[ERROR] OpenCode Server 啟動逾時（等待 {wait_seconds}s）", file=sys.stderr)
        return False

    def stop_server(self):
        if self._server_process:
            try:
                self._server_process.terminate()
                self._server_process.wait(timeout=5)
            except Exception:
                try:
                    self._server_process.kill()
                except Exception:
                    pass
            self._server_process = None

    def _ensure(self):
        if not self.is_server_running():
            if not self.ensure_server():
                raise RuntimeError(
                    "OpenCode Server 未運行且無法自動啟動。"
                    "請手動執行：opencode serve --port 4096"
                )

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        import requests
        self._ensure()
        r = requests.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, body: Optional[dict] = None) -> dict:
        import requests
        self._ensure()
        r = requests.post(f"{self.base_url}{path}", json=body or {}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _delete(self, path: str) -> bool:
        import requests
        self._ensure()
        r = requests.delete(f"{self.base_url}{path}", timeout=self.timeout)
        return r.status_code in (200, 204)

    # ─── SDK: 全域 ───

    def health(self) -> dict:
        """GET /global/health — 健康檢查"""
        return self._get("/global/health")

    # ─── SDK: 設定 ───

    def get_config(self) -> dict:
        """GET /config — 取得設定資訊"""
        return self._get("/config")

    def get_providers(self) -> dict:
        """GET /config/providers — 列出所有 provider 與預設模型"""
        return self._get("/config/providers")

    # ─── SDK: 專案 ───

    def get_project(self) -> dict:
        """GET /project — 取得當前專案資訊"""
        return self._get("/project")

    # ─── SDK: 工作階段 ───

    def list_sessions(self) -> list:
        """GET /session — 列出所有工作階段"""
        r = self._get("/session")
        return r if isinstance(r, list) else r.get("sessions", [])

    def create_session(
        self,
        title: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> dict:
        """POST /session — 建立新工作階段"""
        body: dict = {}
        if title:
            body["title"] = title
        if parent_id:
            body["parentID"] = parent_id
        return self._post("/session", body)

    def get_session(self, session_id: str) -> dict:
        """GET /session/{id} — 取得單一工作階段"""
        return self._get(f"/session/{session_id}")

    def delete_session(self, session_id: str) -> bool:
        """DELETE /session/{id} — 刪除工作階段"""
        return self._delete(f"/session/{session_id}")

    def send_message(
        self,
        session_id: str,
        prompt: str = "",
        parts: Optional[list] = None,
        model: Optional[str] = None,
        reasoning: Optional[str] = None,
        agent: Optional[str] = None,
        no_reply: bool = False,
        output_format: Optional[dict] = None,
        max_steps: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
    ) -> dict:
        """
        POST /session/{id}/message — 傳送訊息

        參數：
            session_id: 工作階段 ID
            prompt: 文字 prompt（與 parts 二選一）
            parts: 訊息部分清單，格式 [{"type": "text", "text": "..."}]
            model: 模型 ID（如 "minimax/MiniMax-M2.7"）
            reasoning: 思考深度（none/minimal/low/medium/high/xhigh）
            agent: 代理名稱（build/plan/general/explore 或自訂）
            no_reply: True=只注入不回覆（用於注入上下文）
            output_format: JSON Schema 結構化輸出設定
            max_steps: 最大迭代次數
            temperature: 溫度（0.0-1.0）
            top_p: top_p（0.0-1.0）
        """
        if parts is None:
            parts = [{"type": "text", "text": prompt}]

        body: dict = {"parts": parts}

        # 模型設定
        if model:
            if "/" in model:
                providerID, modelID = model.split("/", 1)
            else:
                providerID, modelID = model, model
            model_obj: dict = {
                "name": modelID,
                "providerID": providerID,
                "modelID": modelID
            }
            if reasoning:
                model_obj["reasoningEffort"] = reasoning
            body["model"] = model_obj
        elif reasoning:
            body["reasoningEffort"] = reasoning

        # 代理
        if agent:
            body["agent"] = agent

        # 無回覆模式
        if no_reply:
            body["noReply"] = True

        # 結構化輸出
        if output_format:
            body["outputFormat"] = output_format

        # 額外參數
        if max_steps is not None:
            body["maxSteps"] = max_steps
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["topP"] = top_p

        path = f"/session/{session_id}/message"
        if no_reply:
            self._post(path, body)
            return {"status": "queued"}
        return self._post(path, body)

    def abort_session(self, session_id: str) -> dict:
        """POST /session/{id}/abort — 中止正在執行的工作階段"""
        return self._post(f"/session/{session_id}/abort", {})

    def share_session(self, session_id: str) -> dict:
        """POST /session/{id}/share — 分享工作階段"""
        return self._post(f"/session/{session_id}/share", {})

    def unshare_session(self, session_id: str) -> dict:
        """POST /session/{id}/unshare — 取消分享"""
        return self._post(f"/session/{session_id}/unshare", {})

    def revert_session(self, session_id: str, count: int = 1) -> dict:
        """POST /session/{id}/revert — 還原訊息"""
        return self._post(f"/session/{session_id}/revert", {"count": count})

    def unrevert_session(self, session_id: str) -> dict:
        """POST /session/{id}/unrevert — 取消還原"""
        return self._post(f"/session/{session_id}/unrevert", {})

    def list_messages(self, session_id: str) -> list:
        """GET /session/{id}/messages — 列出工作階段中的訊息"""
        r = self._get(f"/session/{session_id}/messages")
        return r if isinstance(r, list) else r.get("messages", [])

    # ─── SDK: 檔案工具 ───

    def search_text(self, pattern: str, directory: Optional[str] = None) -> list:
        """
        GET /find/text — 在檔案中搜尋文字
        回傳：[{path, lines, line_number, absolute_offset, submatches}]
        """
        params = {"pattern": pattern}
        if directory:
            params["directory"] = directory
        return self._get("/find/text", params=params)

    def find_files(
        self,
        query: str,
        type: Optional[str] = None,
        directory: Optional[str] = None,
        limit: int = 50,
    ) -> list:
        """
        GET /find/files — 依名稱找檔案或目錄
        type: "file" 或 "directory"
        """
        params = {"query": query, "limit": min(limit, 200)}
        if type:
            params["type"] = type
        if directory:
            params["directory"] = directory
        return self._get("/find/files", params=params)

    def read_file(self, path: str, type: str = "raw") -> dict:
        """
        GET /file/read — 讀取檔案
        type: "raw"（完整內容）或 "patch"（diff）
        """
        return self._get("/file/read", params={"path": path, "type": type})

    def file_status(self) -> list:
        """GET /file/status — 取得已追蹤檔案的 git 狀態"""
        return self._get("/file/status")

    # ─── SDK: TUI 控制 ───

    def show_toast(
        self,
        message: str,
        variant: str = "info",
        duration: Optional[int] = None,
    ) -> bool:
        """
        POST /tui/toast — 在 OpenCode TUI 顯示 Toast 通知
        variant: info / success / warning / error
        """
        body: dict = {"message": message, "variant": variant}
        if duration:
            body["duration"] = duration
        r = self._post("/tui/toast", body)
        return r.get("ok", False)

    def append_prompt(self, text: str) -> bool:
        """POST /tui/append — 向當前 prompt 附加文字"""
        r = self._post("/tui/append", {"text": text})
        return r.get("ok", False)

    def submit_prompt(self) -> bool:
        """POST /tui/submit — 送出當前 prompt"""
        r = self._post("/tui/submit", {})
        return r.get("ok", False)

    def clear_prompt(self) -> bool:
        """POST /tui/clear — 清除 prompt"""
        r = self._post("/tui/clear", {})
        return r.get("ok", False)

    # ─── SDK: 即時事件監聽 ───

    def subscribe_events(
        self,
        session_id: Optional[str] = None,
        callback: Optional[Callable[[dict], None]] = None,
    ) -> "EventStream":
        """
        訂閱 OpenCode Server 事件串流。
        回傳 EventStream 物件，呼叫 .close() 停止監聽。

        使用範例：
            stream = client.subscribe_events(session_id=sid)
            for event in stream.stream:
                print(f"[EVENT] {event.type}: {event.data}")
        """
        return EventStream(self.base_url, session_id, callback)

    # ─── SDK: 結構化輸出捷徑 ───

    def structured_output(
        self,
        session_id: str,
        prompt: str,
        schema: dict,
        model: Optional[str] = None,
        retry_count: int = 3,
        **kwargs,
    ) -> dict:
        """
        傳送帶有 JSON Schema 的訊息，要求模型回傳結構化 JSON。
        失敗時回傳 {"error": "...", "attempts": N}
        """
        output_format = {
            "type": "json_schema",
            "schema": schema,
            "retryCount": retry_count,
        }
        response = self.send_message(
            session_id=session_id,
            prompt=prompt,
            model=model,
            output_format=output_format,
            **kwargs,
        )
        text = self.extract_text(response)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"error": text, "attempts": retry_count}

    # ─── 工具方法 ───

    def extract_text(self, response: dict) -> str:
        """從 API 回應中提取文字"""
        parts = response.get("parts", [])
        texts = []
        for p in parts:
            if p.get("type") == "text":
                txt = p.get("text", "").strip()
                if txt:
                    texts.append(txt)
        return "\n".join(texts)

    def review_code(
        self,
        code: str,
        language: str = "python",
        model: Optional[str] = None,
    ) -> str:
        """快速 code review（單輪）"""
        prompt = (
            f"請用繁體中文對以下 {language} 程式碼進行 code review，"
            f"指出：\n1. 程式碼問題或 Bug\n"
            f"2. 安全性疑慮\n3. 程式碼風格與可讀性\n"
            f"4. 改進建議（附上修正後的範例程式碼）\n\n"
            f"=== 程式碼 ===\n{code}"
        )
        session = self.create_session(title=f"Code Review - {language}")
        sid = session["id"]
        response = self.send_message(sid, prompt, model=model)
        return self.extract_text(response)

    def analyze_file(
        self,
        file_path: str,
        dir_path: str,
        model: Optional[str] = None,
    ) -> str:
        """分析單一檔案"""
        content = ""
        try:
            full_path = Path(dir_path) / file_path
            if full_path.exists():
                content = full_path.read_text(encoding="utf-8")
                if len(content) > 3000:
                    content = content[:3000] + "\n... (已截斷)"
        except Exception:
            content = "[無法讀取檔案內容]"

        prompt = (
            f"請用繁體中文分析以下檔案 ({file_path}) 的架構與邏輯：\n\n"
            f"=== 檔案內容 ===\n{content}"
        )
        session = self.create_session(title=f"分析 - {file_path}")
        sid = session["id"]
        response = self.send_message(sid, prompt, model=model)
        return self.extract_text(response)


# ─── 事件監聽 ───

class EventStream:
    """OpenCode Server SSE 事件串流封裝"""

    def __init__(
        self,
        base_url: str,
        session_id: Optional[str] = None,
        callback: Optional[Callable[[dict], None]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.session_id = session_id
        self.callback = callback
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.stream = self._create_stream()

    def _create_stream(self):
        """使用 requests + sseclient-py 實作 SSE"""
        try:
            import requests
            import sseclient
        except ImportError:
            raise RuntimeError(
                "事件監聽需要安裝 requests 與 sseclient：\n"
                "pip install requests sseclient-py"
            )

        params = {}
        if self.session_id:
            params["session"] = self.session_id

        resp = requests.get(
            f"{self.base_url}/event/subscribe",
            params=params,
            headers={"Accept": "text/event-stream"},
            stream=True,
        )
        resp.raise_for_status()
        return sseclient.SSEClient(resp)

    def _run(self):
        for event in self.stream:
            if self._stop_event.is_set():
                break
            if self.callback:
                self.callback(event)
            else:
                # yield 效果（儲存起來供迭代）
                pass

    def start(self):
        """在新執行緒啟動監聽"""
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def close(self):
        """停止監聽"""
        self._stop_event.set()
        self.stream.close()
        if self._thread:
            self._thread.join(timeout=3)


# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(
        description="OpenCode HTTP API Client（完整 SDK 版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # 健康與資訊
    parser.add_argument("--health", action="store_true", help="健康檢查")
    parser.add_argument("--providers", action="store_true", help="列出可用模型")
    parser.add_argument("--config", action="store_true", help="取得設定資訊")
    parser.add_argument("--sessions", action="store_true", help="列出所有 session")

    # 基本操作
    parser.add_argument("--session", help="現有 session ID")
    parser.add_argument("--prompt", "-p", help="訊息內容")
    parser.add_argument("--parts", help="JSON 格式的 parts（進階）")
    parser.add_argument("--title", "-t", help="新 session 標題")

    # 進階參數
    parser.add_argument("--task", choices=["review", "analyze", "custom"], help="任務類型")
    parser.add_argument("--code", help="直接傳送程式碼")
    parser.add_argument("--file", help="要分析的檔案")
    parser.add_argument("--dir", help="專案目錄")
    parser.add_argument("--model", "-m", help="模型 ID")
    parser.add_argument("--reasoning", "-r",
                        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
                        help="思考深度")
    parser.add_argument("--agent", "-a",
                        choices=["build", "plan", "general", "explore"],
                        help="指定代理")
    parser.add_argument("--no-reply", action="store_true",
                        help="注入上下文不回覆（noReply 模式）")
    parser.add_argument("--output-schema", type=str,
                        help="JSON Schema（結構化輸出），可傳檔案路徑或 JSON 字串")
    parser.add_argument("--max-steps", type=int, help="最大迭代次數")
    parser.add_argument("--temperature", type=float, help="溫度（0.0-1.0）")
    parser.add_argument("--top-p", type=float, help="top_p（0.0-1.0）")

    # Session 管理
    parser.add_argument("--abort", metavar="SESSION_ID", help="中止指定 session")
    parser.add_argument("--revert", metavar="SESSION_ID", help="還原 session")
    parser.add_argument("--revert-count", type=int, default=1, help="還原訊息數量")
    parser.add_argument("--share", metavar="SESSION_ID", help="分享 session")
    parser.add_argument("--delete", metavar="SESSION_ID", help="刪除 session")
    parser.add_argument("--revert-undo", metavar="SESSION_ID", help="取消還原")

    # 工具
    parser.add_argument("--search-text", metavar="PATTERN", help="搜尋文字")
    parser.add_argument("--find-files", metavar="QUERY", help="依名稱找檔案")
    parser.add_argument("--find-type", choices=["file", "directory"],
                        help="find-files 的類型篩選")
    parser.add_argument("--read-file", metavar="PATH", help="讀取檔案")
    parser.add_argument("--git-status", action="store_true", help="git 狀態")

    # TUI
    parser.add_argument("--toast", metavar="MESSAGE", help="顯示 toast")
    parser.add_argument("--toast-variant", default="info",
                        choices=["info", "success", "warning", "error"],
                        help="toast 類型")

    # 全域設定
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--auto-start", dest="auto_start", action="store_true", default=True)
    parser.add_argument("--no-auto-start", dest="auto_start", action="store_false")
    parser.add_argument("--opencode-cmd", default="opencode")
    parser.add_argument("--json", "-j", action="store_true", help="輸出完整 JSON")

    args = parser.parse_args()

    # ─── 快速操作（不需要 session）───
    if args.health:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.health()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.providers:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.get_providers()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.config:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.get_config()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.sessions:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.list_sessions()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # ─── Session 管理 ───
    if args.abort:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.abort_session(args.abort)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.revert:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.revert_session(args.revert, args.revert_count)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.share:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.share_session(args.share)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.delete:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        ok = client.delete_session(args.delete)
        print(json.dumps({"deleted": ok}, ensure_ascii=False))
        sys.exit(0)

    if args.revert_undo:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.unrevert_session(args.revert_undo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # ─── 工具操作 ───
    if args.search_text:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.search_text(args.search_text, directory=args.dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.find_files:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.find_files(args.find_files, type=args.find_type, directory=args.dir)
        for item in result:
            print(item)
        sys.exit(0)

    if args.read_file:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.read_file(args.read_file)
        print(result.get("content", ""))
        sys.exit(0)

    if args.git_status:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        result = client.file_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.toast:
        client = OpenCodeClient(base_url=args.base_url, auto_start=args.auto_start)
        ok = client.show_toast(args.toast, variant=args.toast_variant)
        print(json.dumps({"toast_sent": ok}, ensure_ascii=False))
        sys.exit(0)

    # ─── 訊息傳送 ───
    client = OpenCodeClient(
        base_url=args.base_url,
        timeout=args.timeout,
        auto_start=args.auto_start,
        opencode_cmd=args.opencode_cmd,
    )

    # 處理 parts JSON
    parts = None
    if args.parts:
        try:
            parts = json.loads(args.parts)
        except json.JSONDecodeError:
            print(f"[ERROR] --parts 需要有效的 JSON", file=sys.stderr)
            sys.exit(1)

    # 處理 output_schema
    output_format = None
    if args.output_schema:
        try:
            schema_path = Path(args.output_schema)
            if schema_path.exists():
                output_format = {"type": "json_schema", "schema": json.loads(schema_path.read_text(encoding="utf-8"))}
            else:
                output_format = {"type": "json_schema", "schema": json.loads(args.output_schema)}
        except json.JSONDecodeError as e:
            print(f"[ERROR] output-schema JSON 格式錯誤: {e}", file=sys.stderr)
            sys.exit(1)

    # 決定 session
    if args.session:
        sid = args.session
    else:
        session = client.create_session(title=args.title or f"OpenClaw - {args.task or 'task'}")
        sid = session["id"]
        print(f"[INFO] 建立 session: {sid}", file=sys.stderr)

    # 處理 prompt / code
    prompt_text = args.prompt or ""
    if args.task == "review" and args.code and not prompt_text:
        prompt_text = (
            f"請用繁體中文對以下程式碼進行 review，指出問題與改進建議：\n\n"
            f"{args.code}"
        )
    if args.task == "analyze" and args.code and not prompt_text:
        prompt_text = f"請用繁體中文分析：\n{args.code}"

    # 分析檔案
    if args.file and args.dir:
        result = client.analyze_file(args.file, args.dir, model=args.model)
        print(result)
        sys.exit(0)

    # 檢查必要參數
    if not prompt_text and not parts and not args.code:
        print("[ERROR] 需要 --prompt 或 --code 或 --parts", file=sys.stderr)
        sys.exit(1)

    # 送出訊息
    response = client.send_message(
        session_id=sid,
        prompt=prompt_text,
        parts=parts,
        model=args.model,
        reasoning=args.reasoning,
        agent=args.agent,
        no_reply=args.no_reply,
        output_format=output_format,
        max_steps=args.max_steps,
        temperature=args.temperature,
        top_p=args.top_p,
    )

    if args.no_reply:
        print(json.dumps(response, ensure_ascii=False), file=sys.stderr)
        print(f"[INFO] 已傳送（noReply 模式），session: {sid}")
        sys.exit(0)

    text = client.extract_text(response)
    if text:
        print(text)
    else:
        print(json.dumps(response, ensure_ascii=False, indent=2))

    if args.json:
        print(json.dumps(response, ensure_ascii=False, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
