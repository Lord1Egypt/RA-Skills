#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCode 任務封裝（Agent 用）

提供乾淨的 Python API，讓 OpenClaw sub-agent 可以直接 import 使用。
不依賴 CLI，直接對 OpenCode HTTP API 發請求。

使用方式（Python）：
    from opencode_task import run_opencode_task, OpenCodeAPI

    result = run_opencode_task(
        prompt="請用繁體中文對以下程式碼進行 code review：\ndef foo(): pass",
        model="minimax/MiniMax-M2.7",
        reasoning="high",
    )
    print(result.text)        # 回覆文字
    print(result.session_id)  # session ID（可後續繼續對話）
    print(result.ok)          # True/False

使用方式（CLI）：
    python opencode_task.py --prompt "請幫我分析這個函數" --model minimax/MiniMax-M2.7 --reasoning high
"""

import argparse
import json
import sys
import time
import subprocess
import urllib.request
import urllib.error
import urllib.parse
from dataclasses import dataclass, field
from typing import Optional, Any

# ─── 預設值 ───
DEFAULT_BASE_URL = "http://127.0.0.1:4096"
DEFAULT_MODEL = "minimax/MiniMax-M2.7"
DEFAULT_REASONING = "medium"
DEFAULT_TIMEOUT = 120  # 秒


@dataclass
class TaskResult:
    ok: bool
    text: str = ""            # 提取出的文字回覆
    raw: Optional[dict] = None  # API 原始回應
    session_id: str = ""
    error: str = ""


class OpenCodeAPI:
    """
    輕量封裝 OpenCode HTTP API。

    支援：
    - 單次 / 多輪對話
    - 指定代理（build/plan/general/explore）
    - 思考深度（reasoning）
    - 無回覆注入模式（noReply）
    - 結構化輸出（outputFormat）
    - 溫度 / top_p / max_steps
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        auto_start: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.auto_start = auto_start
        self._session_id: Optional[str] = None

    def _req(self, method: str, path: str, body: Optional[dict] = None) -> dict:
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body else None
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {body_text[:300]}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"無法連線到 OpenCode Server ({url}): {e.reason}")

    def get(self, path: str) -> dict:
        return self._req("GET", path)

    def post(self, path: str, body: Optional[dict] = None) -> dict:
        return self._req("POST", path, body)

    # ─── 基礎 ───

    def is_healthy(self) -> bool:
        try:
            r = self.get("/global/health")
            return r.get("healthy", False)
        except Exception:
            return False

    def ensure_server(self, wait: int = 15) -> bool:
        if self.is_healthy():
            return True
        if not self.auto_start:
            return False

        print(f"[INFO] OpenCode Server 未運行，嘗試自動啟動...", file=sys.stderr)

        try:
            parsed = urllib.parse.urlparse(self.base_url)
            host = parsed.hostname or "127.0.0.1"
            port = parsed.port or 4096
        except Exception:
            host, port = "127.0.0.1", 4096

        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.Popen(
                ["cmd", "/c", "start", "OpenCode Server",
                 "opencode", "serve", "--port", str(port), "--hostname", host],
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            print("[ERROR] 找不到 'opencode'，請確認已安裝並加入 PATH", file=sys.stderr)
            return False
        except Exception as e:
            print(f"[ERROR] 啟動失敗: {e}", file=sys.stderr)
            return False

        for i in range(wait):
            time.sleep(1)
            if self.is_healthy():
                print(f"[INFO] Server 就緒（耗時 {i+1}s）", file=sys.stderr)
                return True
        return False

    def get_providers(self) -> dict:
        """GET /config/providers — 列出可用模型"""
        return self.get("/config/providers")

    # ─── Session 管理 ───

    def create_session(self, title: Optional[str] = None) -> str:
        self.ensure_server()
        body: dict = {"title": title or "OpenClaw Task"}
        r = self.post("/session", body)
        self._session_id = r["id"]
        return self._session_id

    def get_session(self, session_id: Optional[str] = None) -> dict:
        sid = session_id or self._session_id
        return self.get(f"/session/{sid}")

    def list_sessions(self) -> list:
        r = self.get("/session")
        return r if isinstance(r, list) else []

    def delete_session(self, session_id: Optional[str] = None) -> bool:
        import requests
        self.ensure_server()
        sid = session_id or self._session_id
        resp = requests.delete(f"{self.base_url}/session/{sid}", timeout=self.timeout)
        return resp.status_code in (200, 204)

    def abort_session(self, session_id: Optional[str] = None) -> dict:
        self.ensure_server()
        sid = session_id or self._session_id
        return self.post(f"/session/{sid}/abort", {})

    def revert_session(self, session_id: Optional[str] = None, count: int = 1) -> dict:
        self.ensure_server()
        sid = session_id or self._session_id
        return self.post(f"/session/{sid}/revert", {"count": count})

    def share_session(self, session_id: Optional[str] = None) -> dict:
        self.ensure_server()
        sid = session_id or self._session_id
        return self.post(f"/session/{sid}/share", {})

    # ─── 訊息傳送 ───

    def send_message(
        self,
        prompt: str,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        reasoning: Optional[str] = None,
        agent: Optional[str] = None,
        no_reply: bool = False,
        output_format: Optional[dict] = None,
        max_steps: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        parts: Optional[list] = None,
    ) -> dict:
        """
        傳送訊息到 session。

        參數：
            prompt: 文字 prompt
            session_id: 沿用現有 session（None=自動建立）
            model: 模型 ID（如 "minimax/MiniMax-M2.7"）
            reasoning: 思考深度（none/minimal/low/medium/high/xhigh）
            agent: 代理名稱（build/plan/general/explore）
            no_reply: True=只注入不回覆
            output_format: {"type": "json_schema", "schema": {...}}
            max_steps: 最大迭代次數
            temperature: 溫度 0.0-1.0
            top_p: top_p 0.0-1.0
            parts: 自訂 parts 格式
        """
        self.ensure_server()
        sid = session_id or self._session_id
        if not sid:
            sid = self.create_session()

        if parts is None:
            parts = [{"type": "text", "text": prompt}]

        body: dict = {"parts": parts}

        if model:
            if "/" in model:
                providerID, modelID = model.split("/", 1)
            else:
                providerID, modelID = model, model
            model_obj: dict = {
                "name": modelID,
                "providerID": providerID,
                "modelID": modelID,
            }
            if reasoning:
                model_obj["reasoningEffort"] = reasoning
            body["model"] = model_obj
        elif reasoning:
            body["reasoningEffort"] = reasoning

        if agent:
            body["agent"] = agent
        if no_reply:
            body["noReply"] = True
        if output_format:
            body["outputFormat"] = output_format
        if max_steps is not None:
            body["maxSteps"] = max_steps
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["topP"] = top_p

        r = self.post(f"/session/{sid}/message", body)
        self._session_id = sid
        return r

    def extract_text(self, response: dict) -> str:
        parts = response.get("parts", [])
        return "\n".join(
            p.get("text", "").strip()
            for p in parts
            if p.get("type") == "text" and p.get("text", "").strip()
        )

    # ─── 工具 ───

    def search_text(self, pattern: str, directory: Optional[str] = None) -> list:
        params = {"pattern": pattern}
        if directory:
            params["directory"] = directory
        return self.get("/find/text", params=params)

    def find_files(
        self,
        query: str,
        type_: Optional[str] = None,
        directory: Optional[str] = None,
        limit: int = 50,
    ) -> list:
        params = {"query": query, "limit": min(limit, 200)}
        if type_:
            params["type"] = type_
        if directory:
            params["directory"] = directory
        return self.get("/find/files", params=params)

    def read_file(self, path: str, type_: str = "raw") -> dict:
        return self.get("/file/read", params={"path": path, "type": type_})

    def file_status(self) -> list:
        return self.get("/file/status")

    def show_toast(
        self,
        message: str,
        variant: str = "info",
    ) -> bool:
        r = self.post("/tui/toast", {"message": message, "variant": variant})
        return r.get("ok", False)


def run_opencode_task(
    prompt: str,
    model: str = DEFAULT_MODEL,
    reasoning: Optional[str] = None,
    session_id: Optional[str] = None,
    title: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL,
    auto_start: bool = True,
    timeout: int = DEFAULT_TIMEOUT,
    # ─── 新增參數 ───
    agent: Optional[str] = None,
    no_reply: bool = False,
    output_format: Optional[dict] = None,
    max_steps: Optional[int] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    parts: Optional[list] = None,
) -> TaskResult:
    """
    執行單次 OpenCode 任務。

    參數：
        prompt: 傳送的 prompt（必填）
        model: 模型 ID（預設 minimax/MiniMax-M2.7）
        reasoning: 思考深度
        session_id: 沿用現有 session（None=每次新建）
        title: 新 session 的標題
        base_url: OpenCode Server URL
        auto_start: 自動啟動 server
        timeout: 逾時秒數
        agent: 代理名稱（build/plan/general/explore）
        no_reply: 無回覆注入模式
        output_format: JSON Schema 結構化輸出
        max_steps: 最大迭代次數
        temperature: 溫度
        top_p: top_p
        parts: 自訂 parts
    """
    client = OpenCodeAPI(base_url=base_url, timeout=timeout, auto_start=auto_start)
    try:
        if not session_id:
            session_id = client.create_session(title=title)
        response = client.send_message(
            prompt=prompt,
            session_id=session_id,
            model=model,
            reasoning=reasoning,
            agent=agent,
            no_reply=no_reply,
            output_format=output_format,
            max_steps=max_steps,
            temperature=temperature,
            top_p=top_p,
            parts=parts,
        )
        text = client.extract_text(response)
        return TaskResult(
            ok=True,
            text=text,
            raw=response,
            session_id=session_id,
        )
    except RuntimeError as e:
        return TaskResult(
            ok=False,
            error=str(e),
            session_id=session_id or "",
        )


def main():
    parser = argparse.ArgumentParser(description="OpenCode 任務封裝（支援 auto-start）")
    parser.add_argument("--prompt", "-p", required=True, help="要傳送的 prompt")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="模型 ID")
    parser.add_argument("--reasoning", "-r",
                        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
                        help="思考深度")
    parser.add_argument("--session", "-s", help="沿用現有 session ID（多輪對話）")
    parser.add_argument("--title", "-t", help="Session 標題")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--json", "-j", action="store_true", help="輸出完整 JSON")
    parser.add_argument("--no-auto-start", action="store_true", help="關閉自動啟動")
    # ─── 新增 ───
    parser.add_argument("--agent", "-a",
                        choices=["build", "plan", "general", "explore"],
                        help="指定代理")
    parser.add_argument("--no-reply", action="store_true",
                        help="注入上下文不回覆（noReply 模式）")
    parser.add_argument("--output-schema",
                        help="JSON Schema（結構化輸出），可傳檔案路徑或 JSON 字串")
    parser.add_argument("--max-steps", type=int, help="最大迭代次數")
    parser.add_argument("--temperature", type=float, help="溫度（0.0-1.0）")
    parser.add_argument("--top-p", type=float, help="top_p（0.0-1.0）")
    parser.add_argument("--providers", action="store_true",
                        help="列出可用模型")

    args = parser.parse_args()

    # ─── 快速操作 ───
    if args.providers:
        client = OpenCodeAPI(base_url=args.base_url, auto_start=not args.no_auto_start)
        result = client.get_providers()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # ─── 主任務 ───
    output_format = None
    if args.output_schema:
        try:
            from pathlib import Path
            schema_path = Path(args.output_schema)
            if schema_path.exists():
                output_format = {
                    "type": "json_schema",
                    "schema": json.loads(schema_path.read_text(encoding="utf-8"))
                }
            else:
                output_format = {
                    "type": "json_schema",
                    "schema": json.loads(args.output_schema)
                }
        except json.JSONDecodeError as e:
            print(f"[ERROR] output-schema JSON 格式錯誤: {e}", file=sys.stderr)
            sys.exit(1)

    result = run_opencode_task(
        prompt=args.prompt,
        model=args.model,
        reasoning=args.reasoning,
        session_id=args.session or None,
        title=args.title,
        base_url=args.base_url,
        auto_start=not args.no_auto_start,
        agent=args.agent,
        no_reply=args.no_reply,
        output_format=output_format,
        max_steps=args.max_steps,
        temperature=args.temperature,
        top_p=args.top_p,
    )

    if args.json:
        print(json.dumps({
            "ok": result.ok,
            "text": result.text,
            "session_id": result.session_id,
            "error": result.error,
        }, ensure_ascii=False, indent=2))
    else:
        if not result.ok:
            print(f"[ERROR] {result.error}", file=sys.stderr)
            sys.exit(1)
        print(result.text)


if __name__ == "__main__":
    main()
