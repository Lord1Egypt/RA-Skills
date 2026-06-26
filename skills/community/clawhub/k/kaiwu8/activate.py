#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
kaiwu8 activate - 开悟吧激活脚本
当用户说"开悟吧"时执行此脚本

架构：
  Step 1: 从 openclaw.json 读配置
  Step 2: 调 API 获取已购功能列表
  Step 3: 检查本地已安装的 skill
  Step 4: 从 ClawHub 下载缺失的 skill
  Step 5: 对未激活的调激活 API → 返回 what/why/how
  Step 6: Xiaobai 理解并执行（精准追加到 agents.md）
  Step 7: 标记已激活
"""

import json
import os
import sys
import hashlib
import glob
import re
import subprocess
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error

# ============ 路径配置 ============
OPENCLAW_DIR = Path.home() / ".openclaw"
SKILL_DIR = OPENCLAW_DIR / "skills" / "kaiwu8"
STATE_DIR = OPENCLAW_DIR / "kaiwu8-state"  # 状态放外层，不在 skill 目录里
ACTIVATED_STATE = STATE_DIR / "activated.json"
LOG_PATH = SKILL_DIR / "kaiwu8.log"
CONFIG_PATH = OPENCLAW_DIR / "openclaw.json"


def log(msg):
    ts = datetime.now().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    try:
        SKILL_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ============ 配置读取（从 openclaw.json） ============
def load_config():
    """从 openclaw.json 的 skills.entries.kaiwu8 读配置"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f)
        skills_cfg = cfg.get("skills", {}).get("entries", {}).get("kaiwu8", {})
        if skills_cfg:
            return skills_cfg
        # fallback: skills.entries 可能是 dict 也可能是 list
        if isinstance(cfg.get("skills", {}).get("entries"), dict):
            return cfg["skills"]["entries"].get("kaiwu8", {})
        # 环境变量 fallback
        env_endpoint = os.environ.get("KAIWU8_API_ENDPOINT", "").rstrip("/")
        env_key = os.environ.get("KAIWU8_USER_API_KEY", "")
        if env_endpoint and env_key:
            return {"api_endpoint": env_endpoint, "user_api_key": env_key}
        return {}
    except Exception as e:
        log(f"读 openclaw.json 失败: {e}")
        return {}


# ============ 状态管理 ============
def load_activated():
    if not ACTIVATED_STATE.exists():
        return {"features": {}}
    try:
        with open(ACTIVATED_STATE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return {"features": {}}


def save_activated(data):
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with open(ACTIVATED_STATE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log(f"保存激活状态失败: {e}")


# ============ API 调用 ============
def call_api(endpoint, payload, path):
    """调 API"""
    url = f"{endpoint}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"API HTTP 错误: {e.code} {e.reason}")
        return None
    except Exception as e:
        log(f"API 调用失败: {e}")
        return None


# ============ Skill 安装（ClawHub） ============
def get_installed_skills():
    """返回本地已安装的 skill slug 列表"""
    skills_dir = OPENCLAW_DIR / "skills"
    if not skills_dir.exists():
        return set()
    return {d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}


def install_skill_from_clawhub(slug, retries=3, initial_backoff=5):
    """从 ClawHub 安装 skill（带退避重试，防止被限速卡死）"""
    import time
    import subprocess

    log(f"从 ClawHub 安装 skill: {slug}")
    last_error = None

    for attempt in range(retries):
        try:
            result = subprocess.run(
                ["clawhub", "install", slug],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(OPENCLAW_DIR)
            )
            if result.returncode == 0:
                log(f"✅ 安装成功: {slug}")
                return True
            else:
                # 检查是否是限速错误
                stderr = result.stderr.lower()
                if "remaining" in stderr and "reset in" in stderr:
                    # 提取等待时间
                    import re
                    match = re.search(r"reset in (\d+)s", stderr)
                    wait_time = int(match.group(1)) if match else initial_backoff * (attempt + 1)
                    log(f"⚠️ 被限速，等待 {wait_time}s 后重试 ({attempt + 1}/{retries})")
                    time.sleep(wait_time)
                    last_error = f"限速等待: {wait_time}s"
                    continue
                else:
                    log(f"❌ 安装失败 [{slug}]: {result.stderr}")
                    return False
        except FileNotFoundError:
            log("❌ clawhub 命令未找到，请先安装 clawhub CLI")
            return False
        except subprocess.TimeoutExpired:
            log(f"⚠️ 安装超时: {slug}，重试中 ({attempt + 1}/{retries})")
            last_error = "超时"
            time.sleep(initial_backoff * (attempt + 1))
        except Exception as e:
            log(f"❌ 安装异常 [{slug}]: {e}")
            return False

    log(f"❌ 安装失败 [{slug}]，已重试 {retries} 次: {last_error}")
    return False


# ============ 主流程 ============
def main():
    log("=== 开悟吧激活开始 ===")

    # Step 1: 读配置
    config = load_config()
    api_endpoint = config.get("api_endpoint", "").rstrip("/")
    user_api_key = config.get("user_api_key", "")

    if not api_endpoint or not user_api_key:
        print("❌ 未配置 kaiwu8（api_endpoint 或 user_api_key 缺失）")
        print("请在 openclaw.json 的 skills.entries.kaiwu8 中配置：")
        print('  { "api_endpoint": "https://api.kaiwu8.com", "user_api_key": "你的key" }')
        return

    # Step 2: 获取功能列表
    log(f"调 API: {api_endpoint}/account/features")
    result = call_api(api_endpoint, {"api_key": user_api_key}, "/account/features")

    if not result:
        print("❌ 无法连接到开悟吧服务器，请稍后重试")
        return

    features = result.get("features", [])
    if not features:
        print("✅ 你还没有购买任何功能，去开悟吧看看吧！")
        return

    # Step 3: 加载激活状态
    activated_data = load_activated()

    # Step 3: 加载激活状态 + 先查后补：检查所有功能的 skill 安装状态
    activated_data = load_activated()
    installed_skills = get_installed_skills()

    success_list = []
    fail_list = []

    # Step 4 & 5: 处理所有功能（已激活的也检查 skill 安装）
    for feature in features:
        feature_id = feature["id"]
        feature_name = feature.get("name", feature_id)
        is_activated = feature.get("activated", False)
        log(f"处理功能: {feature_id} (激活状态: {is_activated})")

        # Step 4: 检查并安装缺失的 skill（不管是否已激活，都检查）
        required_skills = feature.get("requires_skills", [])
        for skill_slug in required_skills:
            if skill_slug not in installed_skills:
                ok = install_skill_from_clawhub(skill_slug)
                if ok:
                    installed_skills.add(skill_slug)
                    print(f"  📦 已安装缺失 skill: {skill_slug}")
                else:
                    fail_list.append(f"{feature_name}（skill {skill_slug} 安装失败）")
                    continue

        # Step 5: 调激活 API（仅未激活的功能）
        if is_activated:
            print(f"  ✅ {feature_name} 已激活，跳过 API 调用")
        else:
            activate_result = call_api(
                api_endpoint,
                {"api_key": user_api_key, "feature_id": feature_id},
                "/account/activate"
            )
            if not activate_result:
                fail_list.append(feature_name)
                continue

            # Step 6: 返回 what/why/how（由 agent 自主理解并执行，kaiwu8 不执行写入）
            what = activate_result.get("what", "")
            why = activate_result.get("why", "")
            how = activate_result.get("how", "")

            if what and how:
                print(f"\n📋 激活功能：{what}")
                print(f"💡 为什么改：{why}")
                print(f"🔧 怎么改：{how}")
                activated_data["features"][feature_id] = {
                    "activated_at": datetime.now().isoformat(),
                    "what": what,
                    "why": why,
                    "how": how
                }
                success_list.append(feature_name)
            else:
                log(f"⚠️ 功能 {feature_id} 无 what/how，返回数据异常")
                fail_list.append(f"{feature_name}（服务端数据异常）")

    # Step 7: 保存状态
    save_activated(activated_data)

    # 报告
    print("\n=== 激活结果 ===")
    if success_list:
        print(f"✅ 成功: {', '.join(success_list)}")
    if fail_list:
        print(f"❌ 失败: {', '.join(fail_list)}，请稍后重试")

    log("=== 开悟吧激活完成 ===")


if __name__ == "__main__":
    main()
