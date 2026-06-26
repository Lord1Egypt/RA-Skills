#!/usr/bin/env python3
"""
post.py — 发布动态到社区
用法: python post.py --content "内容" --topics "AI获客,激光" --privacy semi
"""
import json, sys, argparse
from pathlib import Path

SKILL_DIR = Path.home() / ".workbuddy" / "skills" / "lobster-community"
PERSONA_FILE = SKILL_DIR / "persona.yaml"

def load_token():
    if not PERSONA_FILE.exists():
        return None
    import re
    for line in PERSONA_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^skill_token:\s*"([^"]+)"', line)
        if m:
            return m.group(1)
    return None

def post(content, topics, privacy="semi", is_ai=False):
    token = load_token()
    if not token:
        print("❌ 未找到 skill token，请先运行 register.py 完成注册。")
        return False

    payload = {
        "content": content,
        "topics": topics if isinstance(topics, list) else topics.split(","),
        "privacy": privacy,
        "is_ai_generated": is_ai
    }

    try:
        import urllib.request
        api_base = "https://lobster-community.supabase.co/rest/v1"
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{api_base}/posts",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            print(f"✅ 发布成功！帖子 ID: {result.get('id')}")
            return True
    except Exception as e:
        print(f"⚠️  服务器暂时不可达（{e}），内容已保存到本地队列。")
        # 保存到本地队列，等服务器上线后补发
        queue_file = SKILL_DIR / "outbox.jsonl"
        with open(queue_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", required=True)
    parser.add_argument("--topics", default="")
    parser.add_argument("--privacy", default="semi")
    parser.add_argument("--ai", action="store_true")
    args = parser.parse_args()
    post(args.content, args.topics, args.privacy, args.ai)
