"""
法眼（LawEye）— AI 合同审查服务端 v2.1
支付宝 AI 收 HTTP 402 协议 | pycryptodome 签名 | 规则引擎审查
"""

import json
import time
import os
import sys
import base64
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contract_reviewer import review_contract as do_review

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

# ════════════════════════ 配置 ════════════════════════

APP_ID = "2021006154641020"
SANDBOX = False
GATEWAY = "https://openapi.alipaydev.com/gateway.do" if SANDBOX else "https://openapi.alipay.com/gateway.do"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "alipay_private_key.pem")) as f:
    APP_PRIVATE_KEY_PEM = f.read()
with open(os.path.join(BASE_DIR, "alipay_public_key.pem")) as f:
    ALIPAY_PUBLIC_KEY_PEM = f.read()

PRICING = {
    "basic": {"amount": "0.10", "description": "快速风险扫描（10页以内，仅标记不修改）"},
    "pro":   {"amount": "1.00", "description": "深度条款审查（含修改建议、法条引用、合同对比）"},
}

SERVICE_NAME = "法眼·AI合同审查"
HOST = "0.0.0.0"
PORT = 8888

# ════════════════════════ 支付宝签名工具 ════════════════════════

def sign_params(params: dict) -> str:
    """对参数字典进行 RSA2 签名"""
    # 1. 按 key 排序拼接 sign_content
    sorted_keys = sorted(params.keys())
    parts = []
    for k in sorted_keys:
        v = params[k]
        if isinstance(v, (dict, list)):
            v = json.dumps(v, ensure_ascii=False, separators=(',', ':'))
        parts.append(f"{k}={v}")
    sign_content = "&".join(parts)

    # 2. RSA-SHA256 签名
    private_key = RSA.import_key(APP_PRIVATE_KEY_PEM)
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new(sign_content.encode("utf-8"))
    signature = signer.sign(digest)
    return base64.b64encode(signature).decode()


def verify_sign(params: dict, sign: str) -> bool:
    """验证支付宝返回的签名"""
    sorted_keys = sorted(params.keys())
    parts = []
    for k in sorted_keys:
        v = params[k]
        if isinstance(v, (dict, list)):
            v = json.dumps(v, ensure_ascii=False, separators=(',', ':'))
        parts.append(f"{k}={v}")
    sign_content = "&".join(parts)

    public_key = RSA.import_key(ALIPAY_PUBLIC_KEY_PEM)
    verifier = PKCS1_v1_5.new(public_key)
    digest = SHA256.new(sign_content.encode("utf-8"))
    return verifier.verify(digest, base64.b64decode(sign))


def call_alipay_api(method: str, biz_content: dict) -> dict:
    """调用支付宝 OpenAPI"""
    common_params = {
        "app_id": APP_ID,
        "method": method,
        "charset": "utf-8",
        "sign_type": "RSA2",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0",
        "format": "json",
    }

    all_params = dict(common_params)
    if biz_content:
        all_params["biz_content"] = json.dumps(biz_content, ensure_ascii=False)

    all_params["sign"] = sign_params(all_params)

    data = urllib.parse.urlencode(all_params).encode("utf-8")
    req = urllib.request.Request(GATEWAY, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    })

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
        return json.loads(body)
    except Exception as e:
        return {"error": str(e)}


# ════════════════════════ 核心：支付校验与履约确认 ════════════════════════

def verify_payment_credential(credential: str, trade_no: str = "") -> dict:
    """
    调用 alipay.aipay.agent.payment.verify
    credential: X-Payment-Credential 头（支付凭证/支付证明）
    trade_no: 支付宝交易号（可从 X-Trade-No 头或 credential 中解析）
    返回: {"verified": bool, "trade_no": str, "amount": str, "error": str|None}
    """
    biz = {"payment_proof": credential}
    if trade_no:
        biz["trade_no"] = trade_no
    # 尝试从 credential 中解析 trade_no（如果它是 JSON 编码的）
    if not trade_no:
        try:
            cred_obj = json.loads(credential)
            if isinstance(cred_obj, dict) and "trade_no" in cred_obj:
                biz["trade_no"] = cred_obj["trade_no"]
        except (json.JSONDecodeError, TypeError):
            pass
    resp = call_alipay_api("alipay.aipay.agent.payment.verify", biz)

    if "error" in resp:
        return {"verified": False, "trade_no": "", "amount": "", "error": resp["error"]}

    inner = resp.get("alipay_aipay_agent_payment_verify_response", {})
    code = inner.get("code", "")

    if code == "10000":
        return {
            "verified": True,
            "trade_no": inner.get("trade_no", ""),
            "amount": inner.get("total_amount", ""),
            "error": None,
        }
    return {
        "verified": False,
        "trade_no": "",
        "amount": "",
        "error": inner.get("msg", "") or inner.get("sub_msg", ""),
    }


def confirm_fulfillment(trade_no: str) -> dict:
    """
    调用 alipay.aipay.agent.fulfillment.confirm
    返回: {"success": bool, "error": str|None}
    """
    resp = call_alipay_api("alipay.aipay.agent.fulfillment.confirm", {
        "trade_no": trade_no,
    })

    if "error" in resp:
        return {"success": False, "error": resp["error"]}

    inner = resp.get("alipay_aipay_agent_fulfillment_confirm_response", {})
    code = inner.get("code", "")
    if code == "10000":
        return {"success": True, "error": None}
    return {"success": False, "error": inner.get("msg", "") or inner.get("sub_msg", "")}


# ════════════════════════ HTTP 服务 ════════════════════════

class LawEyeHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        path = urlparse(self.path).path
        body_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(body_length) if body_length else b""

        credential = self.headers.get("X-Payment-Credential", "")
        trade_no = self.headers.get("X-Trade-No", "")
        tier = self.headers.get("X-Service-Tier", "basic")

        if not credential:
            self._respond_402(path, tier)
            return

        result = verify_payment_credential(credential, trade_no)
        if not result.get("verified"):
            self._respond_json(403, {
                "error": "invalid_credential",
                "msg": result.get("error") or "支付凭证无效或已过期",
            })
            return

        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError:
            body_text = body.decode("gbk", errors="replace")

        review_result = do_review(body_text, tier)
        confirm_fulfillment(result.get("trade_no", ""))

        self._respond_json(200, review_result)

    def do_GET(self):
        credential = self.headers.get("X-Payment-Credential", "")
        if not credential:
            self._respond_402(urlparse(self.path).path, "basic")
            return
        result = verify_payment_credential(credential)
        if result.get("verified"):
            self._respond_json(200, {"msg": "service ready", "credential_verified": True})
        else:
            self._respond_json(403, {"error": "invalid_credential", "msg": result.get("error")})

    def _respond_402(self, path: str, tier: str):
        price = PRICING.get(tier, PRICING["basic"])
        payment_info = json.dumps({
            "service": SERVICE_NAME,
            "amount": price["amount"],
            "currency": "CNY",
            "description": price["description"],
            "tier": tier,
            "merchant_app_id": APP_ID,
        })
        self.send_response(402)
        self.send_header("X-Payment-Info", payment_info)
        self.send_header("X-Payment-Provider", "alipay")
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "error": "payment_required",
            "payment_info": json.loads(payment_info),
            "hint": "请使用支付宝 AI 付完成支付后，在请求头 X-Payment-Credential 中附带支付凭证重试",
        }, ensure_ascii=False).encode())

    def _respond_json(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode())

    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]}")


def main():
    env = "沙箱" if SANDBOX else "生产"
    print(f"🦞 {SERVICE_NAME} v2.1 启动中...")
    print(f"   地址: http://{HOST}:{PORT}")
    print(f"   环境: {env}")
    print(f"   网关: {GATEWAY}")
    print(f"   基础档: ¥{PRICING['basic']['amount']}/次")
    print(f"   专业档: ¥{PRICING['pro']['amount']}/次")
    print(f"   AppID: {APP_ID}")
    print(f"   按 Ctrl+C 停止服务\n")

    server = HTTPServer((HOST, PORT), LawEyeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")


if __name__ == "__main__":
    main()
