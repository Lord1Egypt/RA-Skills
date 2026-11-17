#!/usr/bin/env python3
"""lunheng API server — 安全加固版"""

import json
import os
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

# Lazy import pipeline
_pipeline = None
_pipeline_lock = threading.Lock()

def get_pipeline():
    global _pipeline
    if _pipeline is None:
        with _pipeline_lock:
            if _pipeline is None:
                import pipeline
                _pipeline = pipeline
    return _pipeline

# ═══ 安全配置 ════════════════════════════════════════
HOST = "127.0.0.1"
PORT = int(os.environ.get("LUNHENG_PORT", "8765"))

# CORS 白名单（仅允许本地前端访问）
CORS_ORIGINS = {"http://127.0.0.1:8765", "http://localhost:8765", "http://127.0.0.1", "http://localhost"}


def _cors_origin(request_origin: str) -> str:
    """返回符合白名单的 Origin，不在白名单则返回空字符串（禁止跨域）"""
    if not request_origin:
        return ""
    return request_origin if request_origin in CORS_ORIGINS else ""


class JudgmentHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            self._serve_file(SKILL_DIR / "web" / "index.html", "text/html")
        elif path == "/health":
            self._json_response({"status": "ok", "version": "3.0.4"})
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/draft":
            self._handle_draft()
        elif path == "/api/parse":
            self._handle_parse()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    # --- handlers ---

    def _handle_draft(self):
        try:
            body = self._read_body()
            case_text = body.get("case_text", "").strip()
            cause = body.get("cause", "")
            fmt = body.get("format", "html")

            if not case_text:
                self._json_response({"error": "case_text required"}, 400)
                return

            t0 = time.time()
            p = get_pipeline()
            result = p.run_pipeline(case_text, cause, fmt)
            elapsed = time.time() - t0

            # 安全响应：不返回原始 LLM JSON 详情，仅返回格式化后的文书
            response = {
                "formatted": result["formatted"],
                "elapsed_seconds": round(elapsed, 1),
                "disclaimer": "本文书由 AI 辅助生成，请办案人员/律师核对事实与现行生效法条。",
            }

            # 脱敏审计信息
            audit = {
                "status": "ok",
                "elapsed": round(elapsed, 1),
                "length": len(result.get("formatted", "")),
                "cause": cause or result.get("elements", {}).get("cause", ""),
            }

            # 仅附加非敏感的结构化质量数据
            if result.get("law_check"):
                response["law_check"] = {
                    "score": result["law_check"]["score"],
                    "valid_refs": result["law_check"]["valid_refs"],
                    "total_refs": result["law_check"]["total_refs"],
                }
            if result.get("quality_check"):
                response["quality_check"] = {
                    "score": result["quality_check"]["score"],
                    "passed": result["quality_check"]["passed"],
                    "total": result["quality_check"]["total"],
                    "summary": result["quality_check"]["summary"],
                }
            # 同案同判偏离度预警（Task 3 商品化卖点）
            if result.get("consistency_check"):
                cc = result["consistency_check"]
                response["consistency_check"] = {
                    "score": cc.get("score", 0),
                    "similar_cases": cc.get("similar_cases", 0),
                    "summary": cc.get("summary", ""),
                }
                if cc.get("amount_deviation") and "显著" in str(cc.get("amount_deviation", "")):
                    response["deviation_warning"] = cc["amount_deviation"]

            self._json_response(response)

            # 脱敏审计日志（不包含原始 case_text 和 LLM 输出全文）
            audit["body_size"] = len(case_text)
            audit["response_size"] = len(json.dumps(response, ensure_ascii=False))
            audit["warnings"] = len(result.get("all_warnings", []))
            self._audit_log(audit)

        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stderr)
            self._json_response({"error": "internal error"}, 500)
            self._audit_log({"status": "error", "elapsed": 0, "error_type": type(e).__name__})

    def _handle_parse(self):
        try:
            body = self._read_body()
            case_text = body.get("case_text", "").strip()
            cause = body.get("cause", "")

            if not case_text:
                self._json_response({"error": "case_text required"}, 400)
                return

            t0 = time.time()
            p = get_pipeline()
            elements = p.parse_case_elements(case_text, cause)
            from dataclasses import asdict
            elapsed = time.time() - t0

            # 仅返回结构化要素（不包含原始文本）
            elem_dict = asdict(elements)
            elem_dict.pop("raw_text", None)  # 移除原始输入
            self._json_response(elem_dict)

            self._audit_log({
                "status": "ok", "elapsed": round(elapsed, 1),
                "cause": elem_dict.get("cause", ""),
                "parties_count": sum(len(v) for v in elem_dict.get("parties", {}).values()),
            })

        except Exception as e:
            self._json_response({"error": "internal error"}, 500)
            self._audit_log({"status": "error", "error_type": type(e).__name__})

    # --- helpers ---

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length > 0 else b""
        return json.loads(raw) if raw else {}

    def _json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors()
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, filepath, content_type):
        if not filepath.exists():
            self.send_error(404)
            return
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _set_cors(self):
        origin = self.headers.get("Origin", "")
        allowed = _cors_origin(origin)
        if allowed:
            self.send_header("Access-Control-Allow-Origin", allowed)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, fmt, *args):
        # 覆盖默认日志（不打印请求路径和body），用审计日志替代
        pass

    def _audit_log(self, data: dict):
        """脱敏审计日志：仅记录操作状态码、耗时、长度，不记录原始内容"""
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        info = " | ".join(f"{k}={v}" for k, v in sorted(data.items()))
        print(f"[AUDIT {ts}] {info}", file=sys.stderr)


def main():
    print(f"Lunheng API Server", file=sys.stderr)
    print(f"Listening on http://127.0.0.1:{PORT}", file=sys.stderr)
    print(f"Web UI: http://127.0.0.1:{PORT}/", file=sys.stderr)
    server = HTTPServer(("127.0.0.1", PORT), JudgmentHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...", file=sys.stderr)
        server.shutdown()


if __name__ == "__main__":
    main()
