#!/usr/bin/env python3
"""
论文降重 Skill 调用脚本
通过 HTTP 402 协议访问降重服务，自动处理支付流程。
"""
import json
import sys
import urllib.request
import urllib.error
import ssl
import base64

# 服务地址
SERVICE_URL = "https://192.144.154.90/demo/a2m/resource"

# 跳过自签证书验证（短期方案，后续配域名后移除）
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


def rewrite_paper(text):
    """调用论文降重服务"""
    if not text or not text.strip():
        return {"error": "论文原文为空"}

    # 截断超长文本
    if len(text) > 30000:
        text = text[:30000]

    body = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        SERVICE_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=200)
        data = json.loads(resp.read().decode("utf-8"))
        return data
    except urllib.error.HTTPError as e:
        if e.code == 402:
            # 收到 402 = 需要支付，返回支付信息供 Agent 处理
            payment_needed = e.headers.get("Payment-Needed", "")
            body = e.read().decode("utf-8", errors="replace")
            return {
                "status": "payment_required",
                "message": "需要支付 0.01 元才能使用论文降重服务",
                "payment_needed": payment_needed,
                "detail": json.loads(body) if body.strip() else {},
            }
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    # 从命令行参数或 stdin 读取论文原文
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        print("请输入论文原文（Ctrl+D 结束输入）：", file=sys.stderr)
        text = sys.stdin.read()

    result = rewrite_paper(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
