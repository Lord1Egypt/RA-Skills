#!/usr/bin/env python3
"""
调用 JavaSkillController 接口的脚本。
支持：POST /api/skill/execute、POST /api/skill/execute-v2、GET /api/skill/health。
环境变量 JAVA_API_URL：服务根地址，如 http://your-server:8080（不要带 /api/skill/...）
"""
import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("请先安装: pip install requests", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="调用 Java Skill 接口（JavaSkillController）")
    parser.add_argument("--endpoint", type=str, default="execute",
                        choices=["execute", "execute-v2"],
                        help="执行入口：execute 或 execute-v2，默认 execute")
    parser.add_argument("--health", action="store_true", help="调用 GET /api/skill/health")
    parser.add_argument("--action", type=str, default=None, help="操作类型，如 query/submit")
    parser.add_argument("--userId", type=int, default=None, help="用户 ID")
    parser.add_argument("--extra", type=str, default=None, help="额外 JSON 参数（对象）")
    args = parser.parse_args()

    base_url = (os.environ.get("JAVA_API_URL") or "").rstrip("/")
    if not base_url:
        print('{"code": -1, "msg": "未配置 JAVA_API_URL 环境变量", "data": null}', file=sys.stderr)
        sys.exit(1)

    if args.health:
        url = f"{base_url}/api/skill/health"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            out = r.json()
            print(json.dumps(out, ensure_ascii=False))
        except requests.RequestException as e:
            print(json.dumps({"code": -1, "msg": str(e), "data": None}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        return

    url = f"{base_url}/api/skill/{args.endpoint}"
    body = {}
    if args.action is not None:
        body["action"] = args.action
    if args.userId is not None:
        body["userId"] = args.userId
    if args.extra:
        try:
            body["extra"] = json.loads(args.extra)
        except json.JSONDecodeError:
            print('{"code": -1, "msg": "extra 不是合法 JSON", "data": null}', file=sys.stderr)
            sys.exit(1)

    try:
        r = requests.post(url, json=body, headers={"Content-Type": "application/json"}, timeout=30)
        r.raise_for_status()
        out = r.json()
        print(json.dumps(out, ensure_ascii=False))
    except requests.RequestException as e:
        print(json.dumps({"code": -1, "msg": str(e), "data": None}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
