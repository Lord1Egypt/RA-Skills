"""
腾讯混元生图 3.0 - 文生图脚本
使用腾讯云 AI Art API（SubmitTextToImageJob + QueryTextToImageJob）
异步提交任务，轮询等待完成，输出图片 URL。
"""

import os
import sys
import time
import json
import argparse
import hmac
import hashlib
import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode

from dotenv import load_dotenv

load_dotenv()

SECRET_ID  = os.getenv("TENCENTCLOUD_SECRET_ID")
SECRET_KEY = os.getenv("TENCENTCLOUD_SECRET_KEY")
REGION     = os.getenv("TENCENTCLOUD_REGION", "ap-guangzhou")

HOST    = "aiart.tencentcloudapi.com"
SERVICE = "aiart"
VERSION = "2022-12-29"


# ── TC3-HMAC-SHA256 签名 ──────────────────────────────────────────────────────

def _sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _build_auth_header(action: str, payload: dict) -> dict:
    """返回携带 TC3-HMAC-SHA256 签名的完整请求头。"""
    body        = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    body_bytes  = body.encode("utf-8")
    timestamp   = int(time.time())
    date        = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    # ── CanonicalRequest
    canonical_headers  = f"content-type:application/json\nhost:{HOST}\n"
    signed_headers     = "content-type;host"
    hashed_payload     = hashlib.sha256(body_bytes).hexdigest()
    canonical_request  = "\n".join([
        "POST", "/", "",
        canonical_headers, signed_headers, hashed_payload
    ])

    # ── StringToSign
    credential_scope = f"{date}/{SERVICE}/tc3_request"
    string_to_sign   = "\n".join([
        "TC3-HMAC-SHA256",
        str(timestamp),
        credential_scope,
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    ])

    # ── Signature
    secret_date    = _sign(("TC3" + SECRET_KEY).encode("utf-8"), date)
    secret_service = _sign(secret_date, SERVICE)
    secret_signing = _sign(secret_service, "tc3_request")
    signature      = hmac.new(secret_signing,
                              string_to_sign.encode("utf-8"),
                              hashlib.sha256).hexdigest()

    authorization = (
        f"TC3-HMAC-SHA256 Credential={SECRET_ID}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    return {
        "Content-Type":    "application/json",
        "Host":            HOST,
        "X-TC-Action":     action,
        "X-TC-Version":    VERSION,
        "X-TC-Timestamp":  str(timestamp),
        "X-TC-Region":     REGION,
        "Authorization":   authorization,
    }, body_bytes


def _call(action: str, payload: dict) -> dict:
    headers, body_bytes = _build_auth_header(action, payload)
    req = Request(
        url    = f"https://{HOST}",
        data   = body_bytes,
        headers= headers,
        method = "POST"
    )
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        raise RuntimeError(f"HTTP 请求失败: {e}") from e


# ── API 封装 ──────────────────────────────────────────────────────────────────

def submit_job(prompt: str,
               resolution: str = "1024:1024",
               seed: int = None,
               logo_add: int = 0,
               revise: int = 1,
               images: list = None) -> str:
    """提交生图任务，返回 JobId。"""
    payload = {
        "Prompt":     prompt,
        "Resolution": resolution,
        "LogoAdd":    logo_add,
        "Revise":     revise,
    }
    if seed is not None:
        payload["Seed"] = seed
    if images:
        payload["Images"] = images

    print(f"[提交任务] prompt={prompt[:60]}{'...' if len(prompt)>60 else ''}")
    print(f"[参数] resolution={resolution}, revise={revise}, logo_add={logo_add}")
    if images:
        print(f"[参数] 参考图数量={len(images)}")

    resp = _call("SubmitTextToImageJob", payload)
    if "Error" in resp.get("Response", {}):
        err = resp["Response"]["Error"]
        raise RuntimeError(f"提交失败: {err['Code']} - {err['Message']}")

    job_id = resp["Response"]["JobId"]
    print(f"[任务已提交] JobId={job_id}")
    return job_id


def query_job(job_id: str) -> dict:
    """查询任务状态，返回完整 Response 字段。"""
    resp = _call("QueryTextToImageJob", {"JobId": job_id})
    if "Error" in resp.get("Response", {}):
        err = resp["Response"]["Error"]
        raise RuntimeError(f"查询失败: {err['Code']} - {err['Message']}")
    return resp["Response"]


def wait_for_job(job_id: str, poll_interval: int = 5, timeout: int = 300) -> dict:
    """轮询等待任务完成，返回最终 Response。"""
    start = time.time()
    dots  = 0
    print(f"[等待完成] 轮询间隔={poll_interval}s，超时={timeout}s")
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(f"任务超时（{timeout}s）: JobId={job_id}")

        result = query_job(job_id)
        status_code = result.get("JobStatusCode", "")
        status_msg  = result.get("JobStatusMsg", "")

        if status_code == "5":          # 处理完成
            print(f"\n[完成] {status_msg}")
            return result
        elif status_code == "4":        # 处理失败
            raise RuntimeError(
                f"任务失败: {result.get('JobErrorCode')} - {result.get('JobErrorMsg')}"
            )
        else:
            dots += 1
            print(f"\r[{status_msg}] 已等待 {int(elapsed)}s {'.' * (dots % 4 + 1)}   ", end="", flush=True)
            time.sleep(poll_interval)


# ── 分辨率辅助 ─────────────────────────────────────────────────────────────────

RATIO_MAP = {
    "1:1":  "1024:1024",
    "3:4":  "768:1024",
    "4:3":  "1024:768",
    "9:16": "720:1280",
    "16:9": "1280:720",
}


def parse_resolution(value: str) -> str:
    """支持比例字符串（如 '16:9'）或像素字符串（如 '1024:1024'）。"""
    if value in RATIO_MAP:
        return RATIO_MAP[value]
    # 验证格式 W:H
    parts = value.replace("*", ":").split(":")
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        return f"{parts[0]}:{parts[1]}"
    raise ValueError(f"无法识别的分辨率格式: {value}，请使用 '宽:高' 或比例（1:1, 16:9 等）")


# ── 主程序 ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    DEFAULT_PROMPT = "一间有着精致窗户的花店，漂亮的木质门，摆放着鲜花"
    DEFAULT_RES    = "1024:1024"

    parser = argparse.ArgumentParser(
        description="腾讯混元生图 3.0 - 文生图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python hunyuan3-text-to-image.py -p "山间云雾，水墨风格"
  python hunyuan3-text-to-image.py -p "夕阳下的城市天际线" -r 16:9
  python hunyuan3-text-to-image.py -p "可爱的猫咪" -r 768:1024 --no-revise
  python hunyuan3-text-to-image.py -p "古风美女" --images http://ref1.jpg http://ref2.jpg
        """
    )
    parser.add_argument("-p", "--prompt",     default=DEFAULT_PROMPT, help="文本描述提示词")
    parser.add_argument("-r", "--resolution", default=DEFAULT_RES,
                        help="分辨率，支持 '宽:高' 像素或比例（1:1 3:4 4:3 9:16 16:9），默认 1024:1024")
    parser.add_argument("--seed",             type=int, default=None,  help="随机种子（正整数），默认随机")
    parser.add_argument("--logo",             type=int, default=0,     help="是否添加水印：0=否 1=是，默认 0")
    parser.add_argument("--no-revise",        action="store_true",     help="关闭 prompt 改写（默认开启）")
    parser.add_argument("--images",           nargs="+", default=None, help="参考图 URL 列表（最多3张），用于图生图")
    parser.add_argument("--poll-interval",    type=int, default=5,     help="轮询间隔秒数，默认 5")
    parser.add_argument("--timeout",          type=int, default=300,   help="最长等待秒数，默认 300")

    args = parser.parse_args()

    if not SECRET_ID or not SECRET_KEY:
        print("❌ 错误：请在 .env 文件中配置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY")
        sys.exit(1)

    try:
        resolution = parse_resolution(args.resolution)
        revise     = 0 if args.no_revise else 1

        job_id = submit_job(
            prompt     = args.prompt,
            resolution = resolution,
            seed       = args.seed,
            logo_add   = args.logo,
            revise     = revise,
            images     = args.images,
        )

        result = wait_for_job(job_id, args.poll_interval, args.timeout)

        print("\n" + "=" * 60)
        print("✅ 生图完成")
        print(f"原始 Prompt  : {args.prompt}")
        revised = result.get("RevisedPrompt", [])
        if revised:
            print(f"扩写后 Prompt : {revised[0]}")
        print(f"分辨率       : {resolution}")
        print(f"JobId        : {job_id}")
        print("\n📸 图片 URL（有效期 1 小时，请及时保存）：")
        for url in result.get("ResultImage", []):
            print(f"  {url}")
        print("=" * 60)

    except (RuntimeError, TimeoutError, ValueError) as e:
        print(f"\n❌ 出错: {e}")
        sys.exit(1)