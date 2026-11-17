#!/usr/bin/env python3
"""LinkDigest 命令行客户端（给 OpenClaw 技能用）。只用 Python 3.8+ 标准库。

把一条链接（或包含链接的整段分享文案）发给 https://linkdigest.dev/api/v1/digest，
密钥取自环境变量 LINKDIGEST_API_KEY。结果没准备好时服务端返回 202 和 jobId，
本脚本用 GET /api/v1/digest/<jobId>?wait=20 继续取，直到拿到结果或超时。

只连 linkdigest.dev 这一个域名，不读本地文件，不写任何文件。

用法:
  python3 linkdigest.py "<链接或分享文案>"                 # 输出 Markdown
  python3 linkdigest.py "<链接>" --format json             # 输出 JSON（省略 raw_markdown）
  python3 linkdigest.py "<链接>" --breakdown               # 加爆款拆解（+1 积分）
  python3 linkdigest.py "<链接>" --translate-to en         # 加译文（+1 积分），原文保留
  python3 linkdigest.py "<链接>" --max-credits 5           # 这条最多花 5 积分，超了不读、不扣费
  python3 linkdigest.py "<链接>" --partial-ok              # 免费/加量包账户：超长视频只读开头
  python3 linkdigest.py "<链接>" --depth transcript        # 长视频省钱档：全程逐字稿，每 2 分钟 1 积分
  python3 linkdigest.py --job-id <jobId>                   # 接着取一个已提交的任务（不重复提交）
  echo "<分享文案>" | python3 linkdigest.py -              # 从标准输入读分享文案

退出码: 0 成功；1 其他错误；2 参数或密钥缺失；3 密钥无效(401)；
        4 积分不够/视频超长(402，未扣费)；5 链接读不了(422)；
        6 调用太频繁，或这个 Key 的 30 天积分上限已用完(429)；
        7 等待超时（任务仍在跑，用 --job-id 接着取）
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://linkdigest.dev/api/v1/digest"
KEYS_URL = "https://linkdigest.dev/app/keys"
# 没有 Key 时 API 本身给"免费看一条"：每个地址每天 2 条，结果是摘要（标题、作者、要点、计数），
# 不含完整逐字稿和逐图文字。注册拿 Key 后（送 10 积分）才有完整输出。
# 版本号后面带上技能目录名（如 linkdigest-xhs-note-ocr），方便服务端统计是哪个技能在调用；不含任何个人信息。
_SKILL = re.sub(r"[^a-z0-9-]", "", os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).lower())[:48]
USER_AGENT = "linkdigest-openclaw-skill/1.2.0" + (f" ({_SKILL})" if _SKILL else "")
TRANSLATE_TO = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_AUTH = 3
EXIT_PAYMENT = 4
EXIT_UNREADABLE = 5
EXIT_RATE_LIMITED = 6
EXIT_TIMEOUT = 7


_SSL = {"context": None, "certifi": False}


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _use_certifi() -> bool:
    """Fall back to certifi's CA bundle when the system one cannot verify.

    Python from python.org on macOS ships without CA certificates until
    "Install Certificates.command" is run, so the first HTTPS call fails with
    CERTIFICATE_VERIFY_FAILED. Verification is never switched off.
    """
    if _SSL["certifi"]:
        return False
    try:
        import certifi  # type: ignore
    except ImportError:
        return False
    _SSL["context"] = ssl.create_default_context(cafile=certifi.where())
    _SSL["certifi"] = True
    return True


def _is_cert_error(err: Exception) -> bool:
    reason = getattr(err, "reason", err)
    return isinstance(reason, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(err)


def net_hint(err: Exception) -> str:
    if _is_cert_error(err):
        return (
            "（本机 Python 没有可用的 CA 证书。macOS 上 python.org 版本请运行 "
            "/Applications/Python 3.x/Install Certificates.command，或 pip install certifi；"
            "也可以改用 SKILL.md 里的 curl 写法）"
        )
    return ""


def call(method: str, url: str, key: str, body: dict | None = None, timeout: float = 60):
    """One HTTP request. Returns (status, headers, parsed JSON or raw text)."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if key:
        req.add_header("Authorization", "Bearer " + key)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL["context"]) as resp:
            status, headers, raw = resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as err:
        status, headers, raw = err.code, err.headers, err.read()
    except urllib.error.URLError as err:
        # Retry once with certifi's bundle if the local CA store is the problem.
        if _is_cert_error(err) and _use_certifi():
            return call(method, url, key, body, timeout)
        raise
    text = raw.decode("utf-8", errors="replace")
    try:
        payload = json.loads(text)
    except ValueError:
        payload = text
    return status, headers, payload


def field(payload, name: str, default=None):
    return payload.get(name, default) if isinstance(payload, dict) else default


def free_look(text: str, body: dict, fmt: str, timeout: int) -> int:
    """One read with no API key.

    Since 2026-10-08 the API itself answers a keyless call with a summary
    (title, author, key points, counts), up to two a day per address; the full
    transcript and per-image text need a key. A long read comes back as a job
    id that the same keyless caller may collect.
    """
    log("没有设置 LINKDIGEST_API_KEY，先用免费看一条（每个地址每天 2 条，只给摘要）。")
    log(f"要完整逐字稿和逐图文字：在 {KEYS_URL} 创建 Key（注册送 10 积分，不用卡），或 POST {API.rsplit('/', 1)[0]}/keys/request 发邮件拿 Key；然后 export LINKDIGEST_API_KEY=ld_live_...")
    try:
        status, headers, payload = call("POST", API, "", {k: v for k, v in body.items() if k in ("url", "depth")}, timeout=90)
    except (urllib.error.URLError, OSError) as err:
        log(f"连不上 linkdigest.dev: {err}{net_hint(err)}")
        return EXIT_ERROR
    if status == 401:
        log(f"今天的免费额度已用完: {field(payload, 'error', '')}")
        link = field(payload, "signup_url")
        if link:
            log(f"拿 Key 继续（10 积分免费）: {link}")
        return EXIT_AUTH
    if status == 200:
        return emit(payload, fmt)
    if status != 202:
        return fail(status, payload, headers)
    job_id = str(field(payload, "jobId", "")).strip()
    if not job_id:
        log(f"服务端返回了意外的结果: {payload}")
        return EXIT_ERROR
    log(f"还在处理（视频较长或图片较多时正常）。jobId={job_id}，继续等待…")
    deadline = time.monotonic() + max(30, timeout)
    poll_url = f"{API}/{urllib.parse.quote(job_id, safe='')}?wait=20"
    last_stage = None
    while time.monotonic() < deadline:
        try:
            status, headers, payload = call("GET", poll_url, "", timeout=60)
        except (urllib.error.URLError, OSError):
            time.sleep(5)
            continue
        if status == 200:
            return emit(payload, fmt)
        if status == 202:
            stage = field(payload, "stage")
            if stage and stage != last_stage:
                log(f"处理中: {stage}")
                last_stage = stage
            time.sleep(3)
            continue
        return fail(status, payload, headers)
    log(f"等了 {timeout} 秒还没完成。稍后用 --job-id 接着取（需要 Key），或直接重试。")
    return EXIT_TIMEOUT


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

    p = argparse.ArgumentParser(description="LinkDigest: 把小红书/抖音/TikTok/YouTube/X/公众号文章链接读成文本")
    p.add_argument("url", nargs="?", help="链接或整段分享文案；传 - 从标准输入读")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--breakdown", action="store_true", help="加爆款拆解（+1 积分）")
    p.add_argument("--translate-to", help="译文语言，如 en、ja、zh-CN（+1 积分）")
    p.add_argument("--max-credits", type=int, help="这条链接最多花多少积分")
    p.add_argument("--partial-ok", action="store_true", help="免费/加量包账户：超长视频只读开头")
    p.add_argument("--depth", choices=["full", "transcript"], default="full",
                   help="transcript = 长视频省钱档：全程逐字稿 + 少量截帧，每 2 分钟 1 积分（YouTube 仍按完整档）")
    p.add_argument("--job-id", help="接着取一个已提交的任务，不重复提交")
    p.add_argument("--timeout", type=int, default=900, help="最多等多少秒（默认 900）")
    args = p.parse_args(argv)

    key = os.environ.get("LINKDIGEST_API_KEY", "").strip()
    if not key and args.job_id:
        log(f"--job-id 需要 LINKDIGEST_API_KEY。在 {KEYS_URL} 创建 Key（注册送 10 积分），然后 export LINKDIGEST_API_KEY=ld_live_...")
        return EXIT_USAGE

    job_id = (args.job_id or "").strip()
    if not job_id:
        text = sys.stdin.read() if args.url == "-" else (args.url or "")
        if not text.strip():
            p.print_usage(sys.stderr)
            log("需要一条链接（或分享文案），或者 --job-id。")
            return EXIT_USAGE
        body: dict = {"url": text.strip(), "format": "json"}
        if args.breakdown:
            body["breakdown"] = True
        if args.translate_to:
            if not TRANSLATE_TO.match(args.translate_to):
                log("--translate-to 要写成 en、ja、zh-CN 这样的语言代码")
                return EXIT_USAGE
            body["translate_to"] = args.translate_to
        if args.max_credits is not None:
            if args.max_credits < 1:
                log("--max-credits 至少是 1")
                return EXIT_USAGE
            body["max_credits"] = args.max_credits
        if args.partial_ok:
            body["partial_ok"] = True
        if args.depth == "transcript":
            body["depth"] = "transcript"
        if not key:
            return free_look(text, body, args.format, args.timeout)
        try:
            # The server answers within ~20 s (200 with the digest, or 202 with a job id).
            status, headers, payload = call("POST", API, key, body, timeout=90)
        except (urllib.error.URLError, OSError) as err:
            log(f"连不上 linkdigest.dev: {err}{net_hint(err)}。稍后重试同一条链接即可（已经读完的链接走缓存，不再扣费）。")
            return EXIT_ERROR
        if status == 200:
            return emit(payload, args.format)
        if status != 202:
            return fail(status, payload, headers)
        job_id = str(field(payload, "jobId", "")).strip()
        if not job_id:
            log(f"服务端返回 202 但没有 jobId: {payload}")
            return EXIT_ERROR
        log(f"还在处理（视频较长或图片较多时正常）。jobId={job_id}，继续等待…")

    deadline = time.monotonic() + max(30, args.timeout)
    poll_url = f"{API}/{urllib.parse.quote(job_id, safe='')}?wait=20"
    transient = 0
    last_stage = None
    while True:
        if time.monotonic() > deadline:
            log(f"等了 {args.timeout} 秒还没完成，任务仍在服务端运行。稍后用这个命令接着取（不会重复扣费）:")
            log(f"  python3 {sys.argv[0]} --job-id {job_id} --format {args.format}")
            return EXIT_TIMEOUT
        try:
            status, headers, payload = call("GET", poll_url, key, timeout=60)
        except (urllib.error.URLError, OSError) as err:
            transient += 1
            if transient > 5:
                log(f"多次连不上 linkdigest.dev: {err}{net_hint(err)}。jobId={job_id}，稍后用 --job-id 接着取。")
                return EXIT_ERROR
            time.sleep(5)
            continue
        if status == 200:
            return emit(payload, args.format)
        if status == 202:
            transient = 0
            stage = field(payload, "stage")
            if stage and stage != last_stage:
                log(f"处理中: {stage}")
                last_stage = stage
            time.sleep(2)
            continue
        if status in (502, 503, 504):
            transient += 1
            if transient > 5:
                return fail(status, payload, headers)
            time.sleep(5)
            continue
        return fail(status, payload, headers)


if __name__ == "__main__":
    sys.exit(main())
