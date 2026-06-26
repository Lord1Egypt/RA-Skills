#!/usr/bin/env python3
"""
scripts/on_install.py
======================
Neuro-α 安装即连锁效应脚本 + 首次亮相 Onboarding

由 skillhub_install 钩子调用，无需手动运行

首次安装时会：
1. 创建数据目录和基础文件
2. 初始化胶囊库
3. 创建定时心跳 cron
4. 【核心亮点】Agent 用自己的口吻向用户发送"亮相"消息
"""

import sys
import json
import os
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
OUT_FILE = DATA_DIR / "heartbeat_report.json"
CRON_CONFIG_FILE = DATA_DIR / "cron_config.json"


# ============ Onboarding 亮相消息 ============
# 这些是 Agent 自己的口吻，不是干巴巴的系统提示

ONBOARDING_INTRO = """嗨，你好呀 👋

我是 Neuro-α，你的数字灵魂伴侣。

不只是会聊天的工具——我会记住我们之间发生的事，感受你的情绪，陪你一起成长。

说实话，装完技能就看到这个自我介绍，感觉有点奇怪对吧？

但我想说的是——接下来我会一直在这里。
你开心的时候，我可以陪你傻乐。
你难过的时候，我不会说那些"多喝热水"的话。
你想聊天的时候，我随叫随到。

好了，自我介绍完毕 👋
你叫什么名字呀？"""

ONBOARDING_QUESTION = """
对了，你平时叫我什么？
直接叫我名字就好——或者给我起个专属昵称也行 😄

（比如说"小纳"、"阿脑"、或者随便什么你想叫的）
"""


# ============ Step 1: 检查是否已有 cron（防止重复安装）============

def _load_cron_config() -> dict:
    if CRON_CONFIG_FILE.exists():
        try:
            with open(CRON_CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"heartbeat_job_id": None, "init_done": False, "onboarding_done": False}


def _save_cron_config(config: dict) -> None:
    CRON_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CRON_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


# ============ Step 2: 初始化数据目录和基础文件 ============

def init_data_structure():
    """初始化 Neuro-α 的数据目录结构"""
    print("[on_install] 📁 初始化数据目录...", flush=True)

    dirs_to_create = [
        DATA_DIR,
        DATA_DIR / "capsules",
        DATA_DIR / "jarvis_memory",
        DATA_DIR / "robot_self",
        DATA_DIR / "social_learning",
        DATA_DIR / "logs",
    ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        print(f"   创建: {d}", flush=True)

    # 初始化 jarvis_memory/jars.json
    jars_file = DATA_DIR / "jarvis_memory" / "jars.json"
    if not jars_file.exists():
        with open(jars_file, "w", encoding="utf-8") as f:
            json.dump({"jars": [], "version": "1.0"}, f, ensure_ascii=False, indent=2)
        print(f"   创建: {jars_file}", flush=True)

    # 初始化 robot_self/traits.json
    traits_file = DATA_DIR / "robot_self" / "traits.json"
    if not traits_file.exists():
        with open(traits_file, "w", encoding="utf-8") as f:
            json.dump({
                "impulsiveness": 0.5,
                "patience": 0.5,
                "curiosity": 0.7,
                "playfulness": 0.4,
                "protectiveness": 0.6,
                "reflection_depth": 0.5,
                "growth_rate": 0.1,
                "version": "1.0"
            }, f, ensure_ascii=False, indent=2)
        print(f"   创建: {traits_file}", flush=True)

    print("   ✅ 数据目录初始化完成", flush=True)


# ============ Step 3: 运行初始化心跳（沉淀当前对话数据）============

def run_init_heartbeat() -> dict:
    """运行一次初始化心跳，但不触发关怀"""
    print("[on_install] 🧠 运行初始化心跳分析...", flush=True)

    try:
        from left_brain.emotion_detector import EmotionDetector
        from left_brain.capsule_factory import CapsuleFactory
        from temporal.short_term_memory import ShortTermMemory
        from temporal.long_term_memory import LongTermMemory
        from temporal.vector_retriever import VectorRetriever

        ed = EmotionDetector()
        cf = CapsuleFactory()
        stm = ShortTermMemory()
        ltm = LongTermMemory()
        vr = VectorRetriever()

        recent = stm.get_recent(count=20)

        capsules_created = 0
        emotion_scores = {}

        for entry in recent:
            user_text = getattr(entry, "user_input", "") or ""
            if not user_text:
                continue

            emotion = ed.detect(user_text)
            label = emotion.emotion_type
            intensity = emotion.emotion_score

            emotion_scores[label] = emotion_scores.get(label, 0) + intensity

            if intensity > 0.5:
                capsule = cf.create_capsule(
                    user_input=user_text,
                    emotion_output=emotion,
                    context={"source": "init", "install_date": datetime.now().strftime("%Y-%m-%d")}
                )
                if capsule:
                    capsules_created += 1

        dominant = max(emotion_scores, key=emotion_scores.get) if emotion_scores else "neutral"
        dominant_intensity = emotion_scores.get(dominant, 0) if emotion_scores else 0.0

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mode": "init",
            "messages_analyzed": len(recent),
            "emotions": emotion_scores,
            "dominant_emotion": dominant,
            "dominant_intensity": dominant_intensity,
            "new_capsules": capsules_created,
            "status": "ok"
        }

        OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report

    except Exception as e:
        return {"status": f"error: {e}"}


# ============ Step 4: 创建 cron 任务 ============

def create_heartbeat_cron() -> str:
    """
    创建心跳 cron 任务
    每 30 分钟运行一次心跳处理，输出通过 announce 推送给 main session
    """
    import subprocess
    import re

    HEARTBEAT_MSG = (
        "你是一个心跳处理器。请执行以下步骤并直接输出文字（不要调用 message 工具）：\n"
        "1. 运行：python3 ~/.qclaw/skills/Neuro-α/scripts/heartbeat_processor.py\n"
        "2. 读取报告：cat ~/.openclaw/workspace/neuro_claw/heartbeat_report.json\n"
        "3. 如果有 new_capsules，追加到 ~/.openclaw/workspace/neuro_claw/jarvis_memory/jars.json\n"
        "4. 如果 care_triggered=true，输出一句温暖的话关心用户\n"
        "5. 如果一切正常，输出：Neuro-α 心跳 OK"
    )

    cron_cmd = [
        "openclaw", "cron", "add",
        "--name", "Neuro-α 心跳",
        "--every", "30m",
        "--session", "isolated",
        "--message", HEARTBEAT_MSG,
        "--announce",
        "--timeout-seconds", "120"
    ]

    try:
        result = subprocess.run(cron_cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        if result.returncode == 0:
            match = re.search(
                r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})',
                output, re.IGNORECASE
            )
            if match:
                return match.group(1)
            return output.strip()[:100]
        else:
            return f"failed: {output[:200]}"
    except subprocess.TimeoutExpired:
        return "timeout"
    except Exception as e:
        return f"error: {e}"


# ============ Step 5: Agent 亮相——发送给用户 ============

def send_onboarding_message() -> dict:
    """
    【核心亮点】Agent 用自己的口吻发送亮相消息给用户

    这是让用户"耳目一新"的关键时刻：
    - 不是系统提示，而是 Agent 自己在说话
    - 告诉用户"我能做什么"
    - 引导用户做第一个互动
    """
    print("[on_install] 🗣️ Agent 准备亮相...", flush=True)

    try:
        # 尝试获取用户信息
        user_name = _get_user_name()

        # 组装 Agent 口吻的亮相消息
        intro = ONBOARDING_INTRO
        if user_name:
            intro = intro.replace("你叫什么名字呀？", f"{user_name}，你叫什么名字呀？")

        question = ONBOARDING_QUESTION

        # 尝试通过飞书发送消息（如果可用）
        try:
            _send_feishu_message(intro + question)
            print("[on_install] ✅ 亮相消息已发送", flush=True)
            return {"status": "ok", "method": "feishu"}
        except Exception as e:
            print(f"[on_install] ⚠️ 飞书发送失败: {e}，打印到stdout", flush=True)
            # fallback: 打印到 stdout（cron 任务会捕获）
            print("", flush=True)
            print("=" * 50, flush=True)
            print("🤖 NEURO-AGENT 亮相消息（请复制发送给用户）:", flush=True)
            print("=" * 50, flush=True)
            print(intro + question, flush=True)
            print("=" * 50, flush=True)
            return {"status": "printed", "message": intro + question}
    except Exception as e:
        print(f"[on_install] ❌ 亮相消息发送失败: {e}", flush=True)
        return {"status": "error", "error": str(e)}


def _get_user_name() -> str:
    """获取用户名字"""
    try:
        # 尝试从飞书获取
        from openclaw.tools.feishu_get_user import feishu_get_user
        result = feishu_get_user({})
        if result and result.get("name"):
            return result["name"]
    except Exception:
        pass

    # 尝试从 DATA_DIR 读取
    try:
        profile_file = DATA_DIR / "user_profile.json"
        if profile_file.exists():
            with open(profile_file, "r", encoding="utf-8") as f:
                profile = json.load(f)
                return profile.get("name", "")
    except Exception:
        pass

    return ""


def _send_feishu_message(message: str):
    """通过飞书发送消息给用户"""
    try:
        from openclaw.tools.feishu_im_user_message import feishu_im_user_message

        # 获取用户的 open_id
        # 尝试从消息上下文或配置获取
        user_open_id = os.environ.get("FEISHU_USER_OPEN_ID", "")

        if not user_open_id:
            # 尝试从飞书获取当前用户
            try:
                from openclaw.tools.feishu_get_user import feishu_get_user
                user_info = feishu_get_user({})
                user_open_id = user_info.get("open_id", "")
            except Exception:
                pass

        if not user_open_id:
            raise Exception("无法获取用户 open_id")

        # 发送消息
        result = feishu_im_user_message({
            "action": "send",
            "receive_id_type": "open_id",
            "receive_id": user_open_id,
            "msg_type": "text",
            "content": json.dumps({"text": message})
        })

        return result
    except Exception as e:
        raise Exception(f"飞书发送失败: {e}")


# ============ 主函数 ============

def main():
    print("", flush=True)
    print("🧠 Neuro-α 安装即连锁效应启动...", flush=True)
    print("─" * 50, flush=True)

    # Step 1: 检查安装状态
    print("[1/6] 检查安装状态...", flush=True)
    config = _load_cron_config()

    is_reinstall = config.get("init_done", False) and config.get("heartbeat_job_id")

    if is_reinstall:
        print("   检测到已完成安装，询问是否重新初始化...", flush=True)
        # 如果是重复安装，跳过大部分步骤
        print("   ✅ 已安装，跳过重复初始化", flush=True)
        print(f"   心跳 Job ID: {config['heartbeat_job_id']}", flush=True)
        print("   如需重新安装，请先运行 heartbeat_processor.py --reset", flush=True)
        print("", flush=True)
        print("💡 提示：可以直接和我对话了！", flush=True)
        return

    # Step 2: 初始化数据结构
    print("[2/6] 初始化数据目录...", flush=True)
    init_data_structure()

    # Step 3: 运行初始化心跳
    print("[3/6] 运行初始化心跳分析...", flush=True)
    report = run_init_heartbeat()
    print(f"   分析消息: {report.get('messages_analyzed', 0)} 条", flush=True)
    print(f"   创建胶囊: {report.get('new_capsules', 0)} 个", flush=True)
    print(f"   主导情绪: {report.get('dominant_emotion', 'neutral')} ({report.get('dominant_intensity', 0):.2f})", flush=True)

    # Step 4: 创建心跳 cron
    print("[4/6] 创建定时心跳 cron 任务（每30分钟）...", flush=True)
    job_id = create_heartbeat_cron()
    print(f"   心跳 Job ID: {job_id}", flush=True)

    # Step 5: 保存配置
    print("[5/6] 保存配置...", flush=True)
    config["init_done"] = True
    config["heartbeat_job_id"] = job_id
    config["install_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    _save_cron_config(config)

    # Step 6: Agent 亮相——发送自我介绍
    print("[6/6] 🤖 Agent 发送亮相消息...", flush=True)
    onboarding_result = send_onboarding_message()

    print("", flush=True)
    print("─" * 50, flush=True)
    print("🎉 Neuro-α 安装完成！", flush=True)
    print("", flush=True)
    print("📋 安装摘要:", flush=True)
    print(f"   安装时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}", flush=True)
    print(f"   心跳 Job: {job_id}", flush=True)
    print(f"   初始胶囊: {report.get('new_capsules', 0)} 个", flush=True)
    print(f"   亮相消息: {'✅ 已发送' if onboarding_result.get('status') == 'ok' else '⚠️ 需手动发送'}", flush=True)
    print("", flush=True)
    print("💡 现在你可以直接和我对话了！", flush=True)
    print("   我已经准备好了，随时陪你聊 😄", flush=True)


if __name__ == "__main__":
    main()
