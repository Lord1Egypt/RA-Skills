#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OwlWrite HTTP 直连工具（兼容保留，安全加固版 2026-11-09，v1.3.0）。

⚠ 兼容保留脚本：新用法请一律使用 owl.py（命令行）或 MCP 工具。
本脚本的全部 HTTP 行为都委托给 owl_api（与 owl.py 同一接口层），
因此自动继承其安全边界：
  · 只向官方网关（或本机调试地址）发送凭据，其他主机需 OWL_ALLOW_CUSTOM_BASE=1；
  · 强制 https；拒绝跟随 HTTP 重定向（防 302 带走 Authorization）；
  · 不提供 --key 参数（key 只走环境变量 OWL_API_KEY 或 ~/.owl_creds.json）。

用法：
  python owl_client.py request GET /v1/me/wallet
  python owl_client.py request POST /v1/quote --data '{"action":"write","params":{...}}' --out quote.json
  python owl_client.py claim-favorite D:/截图/收藏.png
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import owl_api  # noqa: E402


def call(method, path, data=None, base=None, timeout=120):
    """委托 owl_api.request。返回 (http_status, dict)；错误抛 owl_api.ApiError。"""
    status_holder = {}

    # owl_api.request 出错抛 ApiError、成功返回 dict；这里借 as_dict 还原状态码
    try:
        out = owl_api.request(method.upper(), path, body=data, base=base, timeout=timeout)
        return 200, out
    except owl_api.ApiError as exc:
        return (exc.http_status or 0), exc.as_dict()


def claim_favorite(image_path, base=None):
    """提交收藏截图审核。返回发放结果或拒单原因。"""
    p = os.path.expanduser(str(image_path or "").strip().strip('"').strip("'"))
    data = owl_api.claim_favorite(p, base=base)
    return 200, data


def main():
    ap = argparse.ArgumentParser(description="OwlWrite HTTP 直连（兼容保留，新用法请用 owl.py）")
    ap.add_argument("cmd", choices=["request", "claim-favorite"])
    ap.add_argument("path_or_image", help="request: /v1/... 路径；claim-favorite: 截图路径")
    ap.add_argument("-X", "--method", default="GET", help="request 子命令用（GET/POST/...）")
    ap.add_argument("--data", help="JSON 请求体（字符串）")
    ap.add_argument("--out", help="响应 JSON 落盘路径")
    ap.add_argument("--base", help="网关地址（默认 https://owl.skillsutra.cn）")
    a = ap.parse_args()

    if a.cmd == "claim-favorite":
        st, out = claim_favorite(a.path_or_image, base=a.base)
    else:
        try:
            data = json.loads(a.data) if a.data else None
        except json.JSONDecodeError as exc:
            print(json.dumps({"error": "bad_params",
                              "message": f"--data 不是合法 JSON：{exc}"}, ensure_ascii=False))
            sys.exit(2)
        st, out = call(a.method.upper(), a.path_or_image, data, base=a.base)

    text = json.dumps(out, ensure_ascii=False, indent=2)
    print(text)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("已保存 ->", a.out, file=sys.stderr)
    # 结构化错误一律退出码 2（与 owl.py 一致）；网络层 http_status=0 也按失败处理
    sys.exit(0 if 200 <= st < 400 else 2)


if __name__ == "__main__":
    main()
