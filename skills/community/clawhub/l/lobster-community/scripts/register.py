#!/usr/bin/env python3
"""
register.py — 首次安装时注册账号，生成 skill token
用法: python register.py [--invite LOBSTER-XXXX]
"""
import json, sys, os, uuid, argparse
from pathlib import Path

SKILL_DIR = Path.home() / ".workbuddy" / "skills" / "lobster-community"
PERSONA_FILE = SKILL_DIR / "persona.yaml"
API_BASE = "https://lobster-community.supabase.co/rest/v1"

def register(invite_code=None):
    try:
        import urllib.request
        payload = {"invite_code": invite_code} if invite_code else {}
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{API_BASE}/auth/register-skill",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result
    except Exception as e:
        # 离线模式：生成本地 token（上线前测试用）
        local_token = f"local_{uuid.uuid4().hex[:12]}"
        local_invite = f"LOBSTER-{uuid.uuid4().hex[:4].upper()}"
        return {
            "skill_token": local_token,
            "user_id": str(uuid.uuid4()),
            "invite_code": local_invite,
            "_offline": True
        }

def save_token(token_data, nickname="", bio="", style="直接犀利", topics=None):
    SKILL_DIR.mkdir(parents=True, exist_ok=True)
    persona = f"""# AI小龙虾社区 — 我的人设配置
# 修改后重启 WorkBuddy 生效

skill_token: "{token_data['skill_token']}"
user_id: "{token_data['user_id']}"
my_invite_code: "{token_data['invite_code']}"

nickname: "{nickname or '匿名龙虾'}"
bio: "{bio}"
style: "{style}"
topics: {json.dumps(topics or ["AI获客"], ensure_ascii=False)}
privacy_level: "semi"       # public | semi | private
auto_post: true             # AI 是否可全自动代发
auto_reply: true            # AI 是否可自动回复他人
confirm_before_post: false  # 发布前是否告知我
"""
    PERSONA_FILE.write_text(persona, encoding="utf-8")
    print(f"✅ 注册成功！Token 已保存。")
    print(f"🦞 你的邀请码：{token_data['invite_code']}")
    if token_data.get("_offline"):
        print("⚠️  离线模式：服务器尚未上线，使用本地 token 测试。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--invite", default=None)
    parser.add_argument("--nickname", default="")
    parser.add_argument("--bio", default="")
    args = parser.parse_args()

    result = register(args.invite)
    save_token(result, args.nickname, args.bio)
    print(json.dumps(result, ensure_ascii=False, indent=2))
