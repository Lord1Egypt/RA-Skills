#!/usr/bin/env python3
"""HTTP interaction layer for the Go Next Move skill.

This is an *additional* way to use the skill. The original CLI / LLM workflow
(`python3 scripts/next_move.py ...`) is unchanged and still fully supported.
This server simply wraps that same script behind a small web page so a person
can pick the side to move and playing strength, upload a board photo, and get
the recommended-move image back over fast HTTP instead of a slow LLM round
trip.

Design notes:
- Standard library only (http.server), so no new Python dependencies.
- The browser sends the photo as base64 JSON, so there is no multipart parsing.
- Access is gated by a stateless signed token (see skill_token.py). The link is
  valid for a fixed window (default 5 hours); after that the user needs a new
  link.
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from skill_token import (  # noqa: E402
    DEFAULT_SECRET_PATH,
    load_or_create_secret,
    token_remaining_seconds,
    verify_token,
)

NEXT_MOVE_SCRIPT = SCRIPT_DIR / "next_move.py"
MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB raw image budget
ANALYSIS_LOCK = threading.Lock()  # KataGo is heavy; serialize analyses

SIDE_ALIASES = {"black": "black", "white": "white", "黑": "black", "白": "white"}
LEVEL_ALIASES = {
    "beginner": "beginner",
    "intermediate": "intermediate",
    "advanced": "advanced",
    "初级": "beginner",
    "中级": "intermediate",
    "高级": "advanced",
}

PAGE_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
<title>围棋下一手</title>
<style>
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: #0f1115; color: #e8eaed; min-height: 100vh;
    display: flex; justify-content: center;
  }
  .wrap { width: 100%; max-width: 560px; padding: 20px 16px 64px; }
  h1 { font-size: 22px; margin: 8px 0 4px; }
  .sub { color: #9aa0a6; font-size: 13px; margin-bottom: 18px; }
  .card {
    background: #1b1e24; border: 1px solid #2a2e36; border-radius: 14px;
    padding: 18px; margin-bottom: 16px;
  }
  label { display: block; font-size: 13px; color: #c4c7cc; margin: 14px 0 6px; }
  label:first-child { margin-top: 0; }
  .seg { display: flex; gap: 8px; }
  .seg button {
    flex: 1; padding: 10px; border-radius: 10px; border: 1px solid #353a44;
    background: #23272f; color: #e8eaed; font-size: 15px; cursor: pointer;
    transition: all .12s ease;
  }
  .seg button.active { background: #3b82f6; border-color: #3b82f6; color: #fff; font-weight: 600; }
  input[type=file] {
    width: 100%; padding: 12px; border-radius: 10px; border: 1px dashed #3a3f4a;
    background: #23272f; color: #c4c7cc; font-size: 14px;
  }
  .go {
    width: 100%; margin-top: 20px; padding: 14px; border: none; border-radius: 12px;
    background: #22c55e; color: #06280f; font-size: 16px; font-weight: 700; cursor: pointer;
  }
  .go:disabled { opacity: .55; cursor: not-allowed; }
  #preview, #result img { width: 100%; border-radius: 12px; margin-top: 12px; display: none; }
  #status { font-size: 13px; color: #9aa0a6; margin-top: 12px; min-height: 18px; }
  #status.err { color: #f87171; }
  .rec { font-size: 18px; font-weight: 700; margin: 8px 0 2px; }
  .meta { font-size: 13px; color: #9aa0a6; line-height: 1.6; }
  .badge {
    display: inline-block; font-size: 12px; color: #9aa0a6; background: #23272f;
    border: 1px solid #2a2e36; border-radius: 999px; padding: 3px 10px;
  }
  .spinner {
    display: inline-block; width: 14px; height: 14px; border: 2px solid #3b82f6;
    border-top-color: transparent; border-radius: 50%; animation: spin .8s linear infinite;
    vertical-align: -2px; margin-right: 6px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>
  <div class="wrap">
    <h1>围棋下一手推荐</h1>
    <div class="sub">上传棋盘照片，选择执子方和落子水平，获得下一手推荐图。<span id="ttl" class="badge"></span></div>

    <div class="card">
      <label>轮到谁下</label>
      <div class="seg" id="side">
        <button type="button" data-val="black" class="active">黑棋</button>
        <button type="button" data-val="white">白棋</button>
      </div>

      <label>落子水平</label>
      <div class="seg" id="level">
        <button type="button" data-val="beginner">初级</button>
        <button type="button" data-val="intermediate" class="active">中级</button>
        <button type="button" data-val="advanced">高级</button>
      </div>

      <label>棋盘照片（可拍照或从相册/文件上传）</label>
      <input id="file" type="file" accept="image/*" />
      <img id="preview" alt="预览" />

      <button id="go" class="go">分析下一手</button>
      <div id="status"></div>
    </div>

    <div class="card" id="result" style="display:none">
      <div class="rec" id="rec"></div>
      <div class="meta" id="meta"></div>
      <img id="resultImg" alt="下一手结果" />
    </div>
  </div>

<script>
const params = new URLSearchParams(location.search);
const token = params.get("token") || "";
let side = "black", level = "intermediate";

function wireSeg(id, set) {
  document.querySelectorAll(`#${id} button`).forEach(b => {
    b.onclick = () => {
      document.querySelectorAll(`#${id} button`).forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      set(b.dataset.val);
    };
  });
}
wireSeg("side", v => side = v);
wireSeg("level", v => level = v);

const fileEl = document.getElementById("file");
const preview = document.getElementById("preview");
fileEl.onchange = () => {
  const f = fileEl.files[0];
  if (!f) { preview.style.display = "none"; return; }
  preview.src = URL.createObjectURL(f);
  preview.style.display = "block";
};

function readAsDataURL(file) {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(r.result);
    r.onerror = reject;
    r.readAsDataURL(file);
  });
}

const go = document.getElementById("go");
const statusEl = document.getElementById("status");
go.onclick = async () => {
  const f = fileEl.files[0];
  statusEl.className = "";
  if (!token) { statusEl.className = "err"; statusEl.textContent = "链接缺少 token，请向发起人索取新链接。"; return; }
  if (!f) { statusEl.className = "err"; statusEl.textContent = "请先选择一张棋盘照片。"; return; }
  go.disabled = true;
  statusEl.innerHTML = '<span class="spinner"></span>正在识别棋盘并分析下一手，请稍候…';
  document.getElementById("result").style.display = "none";
  try {
    const dataUrl = await readAsDataURL(f);
    const resp = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, side, level, image: dataUrl }),
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || ("HTTP " + resp.status));
    document.getElementById("rec").textContent = "推荐落点：" + (data.move || "—");
    document.getElementById("meta").innerHTML = (data.summary || "") +
      (data.details ? "<br>" + data.details : "");
    const img = document.getElementById("resultImg");
    img.src = data.result_image;
    img.style.display = "block";
    document.getElementById("result").style.display = "block";
    statusEl.textContent = "完成。";
  } catch (e) {
    statusEl.className = "err";
    statusEl.textContent = "失败：" + e.message;
  } finally {
    go.disabled = false;
  }
};

async function refreshTtl() {
  if (!token) return;
  try {
    const r = await fetch("/api/status?token=" + encodeURIComponent(token));
    const d = await r.json();
    const t = document.getElementById("ttl");
    if (d.valid) {
      const h = Math.floor(d.remaining / 3600), m = Math.floor((d.remaining % 3600) / 60);
      t.textContent = `链接有效 ${h}小时${m}分`;
    } else {
      t.textContent = "链接已失效";
      t.style.color = "#f87171";
    }
  } catch (e) {}
}
refreshTtl();
</script>
</body>
</html>
"""


def build_next_move_args(args) -> list[str]:
    """Translate forwarded CLI options into extra next_move.py arguments."""
    extra: list[str] = []
    if getattr(args, "visits", None):
        extra += ["--visits", str(args.visits)]
    if getattr(args, "coordinate_style", None):
        extra += ["--coordinate-style", args.coordinate_style]
    if getattr(args, "katago", None):
        extra += ["--katago", str(args.katago)]
    if getattr(args, "model", None):
        extra += ["--model", str(args.model)]
    if getattr(args, "analysis_config", None):
        extra += ["--analysis-config", str(args.analysis_config)]
    if getattr(args, "skill_config", None):
        extra += ["--skill-config", str(args.skill_config)]
    return extra


class Handler(BaseHTTPRequestHandler):
    server_version = "GoNextMove/1.0"
    secret = ""
    next_move_args: list[str] = []

    def log_message(self, fmt, *args):  # noqa: A003 - quieter logging
        sys.stderr.write("[web] %s - %s\n" % (self.address_string(), fmt % args))

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            body = PAGE_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/api/status":
            qs = parse_qs(parsed.query)
            token = (qs.get("token") or [""])[0]
            payload = verify_token(self.secret, token)
            if payload is None:
                self._send_json(200, {"valid": False})
            else:
                self._send_json(200, {"valid": True, "remaining": token_remaining_seconds(payload)})
            return
        if parsed.path == "/healthz":
            self._send_json(200, {"ok": True})
            return
        self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/analyze":
            self._send_json(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_UPLOAD_BYTES + 2 * 1024 * 1024:
            self._send_json(413, {"error": "请求过大或为空"})
            return
        try:
            req = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._send_json(400, {"error": "请求体不是合法 JSON"})
            return

        if verify_token(self.secret, req.get("token", "")) is None:
            self._send_json(401, {"error": "token 无效或已过期，请索取新链接"})
            return

        side = SIDE_ALIASES.get(str(req.get("side", "")).strip().lower())
        level = LEVEL_ALIASES.get(str(req.get("level", "")).strip().lower())
        if side is None:
            self._send_json(400, {"error": "side 必须是 black 或 white"})
            return
        if level is None:
            level = "intermediate"

        image_bytes = self._decode_image(req.get("image", ""))
        if image_bytes is None:
            self._send_json(400, {"error": "图片缺失或无法解码"})
            return

        try:
            result = self._run_analysis(image_bytes, side, level)
        except AnalysisError as exc:
            self._send_json(500, {"error": str(exc)})
            return
        self._send_json(200, result)

    @staticmethod
    def _decode_image(data_url: str) -> bytes | None:
        if not isinstance(data_url, str) or not data_url:
            return None
        b64 = data_url.split(",", 1)[1] if data_url.startswith("data:") else data_url
        try:
            raw = base64.b64decode(b64, validate=False)
        except (ValueError, base64.binascii.Error):
            return None
        if not raw or len(raw) > MAX_UPLOAD_BYTES:
            return None
        return raw

    def _run_analysis(self, image_bytes: bytes, side: str, level: str) -> dict:
        with tempfile.TemporaryDirectory(prefix="go-next-web-") as tmp:
            tmp_dir = Path(tmp)
            in_path = tmp_dir / "board.jpg"
            out_path = tmp_dir / "result.jpg"
            in_path.write_bytes(image_bytes)

            cmd = [
                sys.executable,
                str(NEXT_MOVE_SCRIPT),
                str(in_path),
                "--input", "image",
                "--side-to-move", side,
                "--level", level,
                "--source-result-image", str(out_path),
                *self.next_move_args,
            ]
            with ANALYSIS_LOCK:
                proc = subprocess.run(
                    cmd,
                    cwd=str(REPO_ROOT),
                    capture_output=True,
                    text=True,
                    timeout=600,
                )
            if proc.returncode != 0:
                detail = (proc.stderr or proc.stdout or "").strip().splitlines()
                tail = detail[-1] if detail else "未知错误"
                raise AnalysisError(f"分析失败：{tail}")

            try:
                analysis = json.loads(proc.stdout)
            except (ValueError, json.JSONDecodeError) as exc:
                raise AnalysisError("无法解析分析结果") from exc

            image_path = Path(analysis.get("source_result_image") or out_path)
            if not image_path.exists():
                raise AnalysisError("结果图未生成")
            result_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")

        rec = analysis.get("recommendation") or {}
        reason = analysis.get("reason") or {}
        move = rec.get("move")
        summary = reason.get("summary", "")
        explanation = reason.get("explanation") or []
        details = "<br>".join(str(x) for x in explanation[:3])
        return {
            "move": move,
            "summary": summary,
            "details": details,
            "side": side,
            "level": level,
            "result_image": "data:image/jpeg;base64," + result_b64,
        }


class AnalysisError(Exception):
    pass


def run_server(
    host: str,
    port: int,
    secret: str,
    next_move_args: list[str] | None = None,
) -> ThreadingHTTPServer:
    Handler.secret = secret
    Handler.next_move_args = next_move_args or []
    httpd = ThreadingHTTPServer((host, port), Handler)
    return httpd


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the Go Next Move web UI over HTTP.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host, default: 127.0.0.1")
    parser.add_argument("--port", type=int, default=8848, help="Bind port, default: 8848")
    parser.add_argument("--secret-path", type=Path, default=DEFAULT_SECRET_PATH, help="Secret file path")
    parser.add_argument("--visits", type=int, help="Forward a KataGo visit budget to next_move.py")
    parser.add_argument(
        "--coordinate-style",
        choices=["gtp", "sequential"],
        help="Forward coordinate style to next_move.py",
    )
    parser.add_argument("--katago", help="Forward an explicit katago executable path to next_move.py")
    parser.add_argument("--model", help="Forward an explicit KataGo model path to next_move.py")
    parser.add_argument("--analysis-config", help="Forward an explicit KataGo analysis config to next_move.py")
    parser.add_argument("--skill-config", help="Forward an explicit project analysis override config to next_move.py")
    args = parser.parse_args()

    secret = load_or_create_secret(args.secret_path)
    extra = build_next_move_args(args)

    httpd = run_server(args.host, args.port, secret, extra)
    sys.stderr.write(f"[web] listening on http://{args.host}:{args.port}\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
