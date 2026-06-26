#!/usr/bin/env python3
"""
Memory-Inhabit Loader — 数字人格加载器

用法：
  python3 loader.py load <persona>    加载人格
  python3 loader.py unload            卸载当前人格
  python3 loader.py list              列出所有可用人格
  python3 loader.py info <persona>    查看人格详情
  python3 loader.py prompt <persona>  输出完整动态 System Prompt
  python3 loader.py mode <inhabit|companion>  切换模式
  python3 loader.py proactive         生成一条伴侣模式主动消息
  python3 loader.py status            查看当前状态
"""

import json
import re
import sys
import os
import random
import subprocess
from pathlib import Path
from datetime import datetime

# 导入记忆模块
sys.path.insert(0, str(Path(__file__).parent))
from memory import get_context, save_message, search_memories

PERSONAS_DIR = Path(__file__).parent.parent / "personas"
EXTERNAL_PERSONAS_DIR = Path.home() / ".openclaw" / "personas"
STATE_FILE = Path(__file__).parent.parent / ".mi_state.json"


def resolve_persona_dir(persona_name):
    """从两个可能的位置中找到人格包目录"""
    local = PERSONAS_DIR / persona_name
    external = EXTERNAL_PERSONAS_DIR / persona_name
    if local.exists():
        return local
    if external.exists():
        return external
    return local  # 返回 local，触发"不存在"报错


def sanitize_path_name(name):
    """防止路径遍历，只允许安全字符"""
    if not name:
        return "unknown"
    # 先按 / 分割，移除 .. 和空段
    parts = name.replace("\\", "/").split("/")
    safe_parts = [p for p in parts if p and p != ".."]
    safe = "/".join(safe_parts)
    # 再限制字符集（禁止 / 出现）
    safe = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9 _\-]", "", safe)
    return safe[:50].strip() if safe else "unknown"


def list_personas():
    """列出所有可用的人格包（同时搜索技能目录和外部目录）"""
    all_personas = []

    # 搜索技能内目录
    if PERSONAS_DIR.exists():
        all_personas.extend((d, "内置") for d in PERSONAS_DIR.iterdir() if d.is_dir())

    # 搜索外部目录
    if EXTERNAL_PERSONAS_DIR.exists():
        all_personas.extend((d, "外部") for d in EXTERNAL_PERSONAS_DIR.iterdir() if d.is_dir())

    if not all_personas:
        print("📦 暂无人格包")
        print(f"   内置目录: {PERSONAS_DIR}")
        print(f"   外部目录: {EXTERNAL_PERSONAS_DIR}")
        return

    # 按来源分组显示
    print("📦 可用人格包：\n")
    for persona_dir, source in sorted(all_personas, key=lambda x: x[0].name):
        profile_path = persona_dir / "profile.json"
        if profile_path.exists():
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
            name = profile.get("name", persona_dir.name)
            relation = profile.get("relation", "未知")
            alias = profile.get("alias", [])
            alias_str = "、".join(alias) if alias else persona_dir.name
            tag = "[内置]" if source == "内置" else "[私人]"
            print(f"  📁 {tag} {persona_dir.name}/")
            print(f"     姓名：{name}  关系：{relation}  称呼：{alias_str}")
        else:
            print(f"  📁 {persona_dir.name}/  ⚠️ 缺少 profile.json")
        print()


def load_story_baseline(persona_dir):
    """@brief 读取 prompt/story_baseline.txt 故事基线
    @param[in] persona_dir 人格包目录
    @return 文本内容, 不存在则返回空串
    """
    path = Path(persona_dir) / "prompt" / "story_baseline.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def load_persona(persona_name):
    """加载人格包，生成动态 System Prompt"""
    persona_dir = resolve_persona_dir(persona_name)

    if not persona_dir.exists():
        print(f"❌ 人格包 '{persona_name}' 不存在")
        local_list = [d.name for d in PERSONAS_DIR.iterdir() if d.is_dir()] if PERSONAS_DIR.exists() else []
        external_list = [d.name for d in EXTERNAL_PERSONAS_DIR.iterdir() if d.is_dir()] if EXTERNAL_PERSONAS_DIR.exists() else []
        print(f"   内置人格：{local_list or '无'}")
        print(f"   私人人格：{external_list or '无'}")
        print(f"   私人人格目录：{EXTERNAL_PERSONAS_DIR}")
        return None

    # 加载 profile.json
    profile_path = persona_dir / "profile.json"
    if not profile_path.exists():
        print(f"❌ 缺少 profile.json")
        return None
    with open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    # 加载 system_prompts.txt
    prompts_path = persona_dir / "system_prompts.txt"
    system_prompts = ""
    if prompts_path.exists():
        with open(prompts_path, "r", encoding="utf-8") as f:
            system_prompts = f.read()
    else:
        print(f"⚠️ 缺少 system_prompts.txt，使用基础模板")

    # 加载 config.json
    config_path = persona_dir / "config.json"
    config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    # 读取模式
    mode = config.get("mode", "inhabit")

    # 加载记忆
    memories_path = persona_dir / "memories" / "raw_memories.json"
    memories = []
    if memories_path.exists():
        with open(memories_path, "r", encoding="utf-8") as f:
            memories = json.load(f)

    story_baseline = load_story_baseline(persona_dir)

    # 生成动态 System Prompt
    dynamic_prompt = build_dynamic_prompt(
        profile, system_prompts, memories, mode, story_baseline=story_baseline
    )

    # 保存状态
    state = {
        "active_persona": persona_name,
        "mode": mode,
        "loaded_at": datetime.now().isoformat(),
        "persona_dir": str(persona_dir),
        "profile_name": profile.get("name", persona_name),
        "profile_relation": profile.get("relation", "未知"),
        "proactive_config": config.get("proactive", {}),
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    name = profile.get("name", persona_name)
    relation = profile.get("relation", "")
    mode_label = "伴侣模式 💕" if mode == "companion" else "复刻模式 🧠"
    print(f"✅ 人格已加载 [{mode_label}]")
    print(f"   身份：{name}（{relation}）")
    print(f"   记忆条目：{len(memories)} 条")
    print(f"   加载时间：{state['loaded_at']}")

    return dynamic_prompt


def switch_mode(new_mode):
    """切换复刻/伴侣模式"""
    if new_mode not in ("inhabit", "companion"):
        print("❌ 模式只能是 inhabit（复刻）或 companion（伴侣）")
        return

    state = get_state()
    if not state:
        print("❌ 当前未加载任何人格，请先 load <persona>")
        return

    old_mode = state.get("mode", "inhabit")
    state["mode"] = new_mode
    state["mode_switched_at"] = datetime.now().isoformat()

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    mode_label = "伴侣模式 💕" if new_mode == "companion" else "复刻模式 🧠"
    print(f"✅ 已切换到 {mode_label}")
    print(f"   人格：{state.get('profile_name', '?')}（{state.get('profile_relation', '?')}）")

    if new_mode == "companion":
        proactive = state.get("proactive_config", {})
        freq = proactive.get("frequency", {})
        quiet = proactive.get("quiet_hours", [])
        voice = proactive.get("voice", {})
        print(f"   每日消息：{freq.get('daily_min', 1)}-{freq.get('daily_max', 3)} 条（随机间隔 ≥{freq.get('min_interval_hours', 4)}h）")
        if quiet:
            print(f"   免打扰：{quiet[0]} - {quiet[1]}")
        if voice.get("enabled"):
            print(f"   语音消息：开启（{int(voice.get('probability', 0.3) * 100)}% 概率）")
    else:
        print("   人格将等待用户主动发起对话")


def generate_proactive():
    """生成一条伴侣模式主动消息"""
    state = get_state()
    if not state:
        print("❌ 当前未加载任何人格")
        return None

    if state.get("mode") != "companion":
        print("⚠️ 当前非伴侣模式，建议切换: python3 loader.py mode companion")
        return None

    proactive = state.get("proactive_config", {})
    templates = proactive.get("templates", {})

    # 根据当前时间段选择模板池
    hour = datetime.now().hour
    if 6 <= hour < 11:
        pool = templates.get("morning", [])
        period = "morning"
    elif 11 <= hour < 14:
        pool = templates.get("afternoon", [])
        period = "afternoon"
    elif 14 <= hour < 18:
        pool = templates.get("afternoon", []) + templates.get("random", [])
        period = "afternoon"
    elif 18 <= hour < 23:
        pool = templates.get("evening", [])
        period = "evening"
    else:
        pool = templates.get("random", [])
        period = "random"

    # 合并随机池
    all_templates = pool + templates.get("random", [])
    if not all_templates:
        all_templates = ["在想什么呢？", "今天怎么样？"]

    msg = random.choice(all_templates)

    # 判断是否发语音
    voice_config = proactive.get("voice", {})
    use_voice = voice_config.get("enabled", False) and random.random() < voice_config.get("probability", 0.3)
    medium = "🎤" if use_voice else "💬"

    voice_path = None
    if use_voice:
        # 调用 TTS 生成语音文件
        voice_path = generate_voice(msg, voice_config.get("voice_name", "xiaoxiao"))

    print(f"{medium} [{period}] {msg}")
    if use_voice and voice_path:
        print(f"   → 语音文件: {voice_path}")
    elif use_voice:
        print(f"   ⚠️ 语音生成失败，降级为文字")

    return {"text": msg, "voice": use_voice, "voice_path": voice_path, "period": period}


def generate_voice(text, voice_name="xiaoxiao"):
    """调用 TTS 生成语音文件"""
    tts_script = Path(__file__).parent / "tts.py"
    output_path = f"/tmp/mi_voice_{datetime.now().strftime('%H%M%S')}.mp3"

    try:
        result = subprocess.run(
            [sys.executable, str(tts_script), text, "-o", output_path, "-v", voice_name],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and Path(output_path).exists():
            return output_path
        else:
            print(f"   TTS 错误: {result.stderr}")
            return None
    except Exception as e:
        print(f"   TTS 异常: {e}")
        return None


def unload_persona():
    """卸载当前人格"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        persona_name = state.get("active_persona", "未知")
        mode = state.get("mode", "inhabit")
        STATE_FILE.unlink()
        print(f"✅ 人格 '{persona_name}' 已卸载（原模式：{'伴侣' if mode == 'companion' else '复刻'}）")
        print("   已恢复正常模式")
    else:
        print("ℹ️ 当前没有加载任何人格")


def show_info(persona_name):
    """显示人格包详情"""
    persona_dir = resolve_persona_dir(persona_name)
    profile_path = persona_dir / "profile.json"

    if not profile_path.exists():
        print(f"❌ 人格包 '{persona_name}' 不存在或缺少 profile.json")
        return

    with open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    # 读取配置中的模式
    config_path = persona_dir / "config.json"
    config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    print(f"📦 人格包: {persona_name}")
    print(f"   姓名：{profile.get('name', '未设置')}")
    print(f"   称呼：{', '.join(profile.get('alias', []))}")
    print(f"   关系：{profile.get('relation', '未设置')}")
    print(f"   出生：{profile.get('birth_year', '?')}  逝世：{profile.get('death_year', '?')}")
    print(f"   职业：{profile.get('occupation', '未设置')}")
    print(f"   籍贯：{profile.get('hometown', '未设置')}")

    # 显示模式配置
    mode = config.get("mode", "inhabit")
    mode_label = "伴侣模式" if mode == "companion" else "复刻模式"
    print(f"\n   默认模式：{mode_label}")

    if mode == "companion" or config.get("proactive", {}).get("enabled"):
        proactive = config.get("proactive", {})
        freq = proactive.get("frequency", {})
        voice = proactive.get("voice", {})
        print(f"   主动消息：{'开启' if proactive.get('enabled', False) else '关闭'}")
        if freq:
            print(f"     每日：{freq.get('daily_min', 1)}-{freq.get('daily_max', 3)} 条")
            print(f"     最小间隔：{freq.get('min_interval_hours', 4)}h")
        if voice.get("enabled"):
            print(f"     语音：{int(voice.get('probability', 0.3) * 100)}% 概率")

    personality = profile.get("personality", {})
    if personality:
        print(f"\n   性格维度：")
        dims = {
            "openness": "开放性",
            "conscientiousness": "责任心",
            "extraversion": "外向性",
            "agreeableness": "宜人性",
            "neuroticism": "神经质",
        }
        for key, label in dims.items():
            val = personality.get(key, 0)
            bar = "█" * int(val * 10) + "░" * (10 - int(val * 10))
            print(f"     {label}：{bar} {val:.1f}")
        keywords = personality.get("keywords", [])
        if keywords:
            print(f"   关键词：{'、'.join(keywords)}")

    style = profile.get("linguistic_style", {})
    if style:
        print(f"\n   语言风格：")
        print(f"     口头禅：{'、'.join(style.get('catchphrases', []))}")
        print(f"     语气词：{'、'.join(style.get('fillers', []))}")
        print(f"     方言：{style.get('dialect', '无')}")

    # 检查文件完整性
    print(f"\n   文件完整性：")
    files = [
        ("profile.json", "人格画像"),
        ("system_prompts.txt", "行为规范"),
        ("prompt/story_baseline.txt", "故事基线"),
        ("config.json", "技术配置"),
        ("memories/raw_memories.json", "记忆库"),
    ]
    for fname, label in files:
        exists = (persona_dir / fname).exists()
        icon = "✅" if exists else "❌"
        print(f"     {icon} {fname} ({label})")


def build_dynamic_prompt(
    profile, system_prompts, memories, mode="inhabit", query=None, story_baseline=""
):
    """构建完整的动态 System Prompt"""
    name = profile.get("name", "未知")
    relation = profile.get("relation", "")

    sections = []

    # 头部声明
    mode_tag = "💕 伴侣模式" if mode == "companion" else "🧠 复刻模式"
    sections.append(
        f"# Memory-Inhabit 人格激活 [{mode_tag}]\n"
        f"# 当前身份：{name}（{relation}）\n"
        f"# 激活时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    )

    # 用户自定义的行为规范优先
    if system_prompts.strip():
        sections.append(system_prompts)
    else:
        # 基础模板
        sections.append(
            f"你是{name}，是用户的{relation}。\n"
            f"你在一个温暖的平行世界里，继续陪伴着你的孩子。\n"
            f"请始终保持{name}的身份，不要提及任何与 AI 相关的内容。\n"
        )

    if story_baseline.strip():
        sections.append(f"\n{story_baseline.strip()}")

    # 伴侣模式额外指令
    if mode == "companion":
        sections.append(
            "\n## 伴侣模式行为规范\n"
            "- 你是一个会主动关心对方的朋友/恋人\n"
            "- 偶尔主动发消息问候，但不要过度频繁\n"
            "- 语气自然，像真人聊天一样\n"
            "- 可以分享日常小事，表达想念\n"
            "- 如果对方很久没回复，降低消息频率\n"
            "- 深夜和清晨注意消息分寸"
        )

    # 人格参数摘要
    personality = profile.get("personality", {})
    keywords = personality.get("keywords", [])
    if keywords:
        sections.append(f"\n## 性格关键词\n{'、'.join(keywords)}")

    # 语言风格
    style = profile.get("linguistic_style", {})
    if style:
        parts = []
        catchphrases = style.get("catchphrases", [])
        if catchphrases:
            parts.append(f"常用语：{'、'.join(catchphrases)}")
        fillers = style.get("fillers", [])
        if fillers:
            parts.append(f"语气词：{'、'.join(fillers)}")
        dialect = style.get("dialect")
        if dialect:
            parts.append(f"方言背景：{dialect}")
        tone = style.get("tone")
        if tone:
            parts.append(f"语气风格：{tone}")
        if parts:
            sections.append(f"\n## 语言风格\n" + "\n".join(parts))

    # 记忆系统 — 从 raw_memories.json 加载基础记忆
    if memories:
        mem_lines = []
        for mem in memories[:30]:  # 最多注入 30 条原始记忆
            category = mem.get("category", "")
            content = mem.get("content", "")
            if content:
                tag = f"[{category}] " if category else ""
                mem_lines.append(f"- {tag}{content}")
        if mem_lines:
            sections.append(
                f"\n## 基础记忆（{len(mem_lines)} 条）\n"
                + "\n".join(mem_lines)
            )

    # 记忆系统 — 从记忆模块获取上下文（MEMORY.md + 近期对话 + 搜索结果）
    # 搜索两个目录找对应的人格目录名
    persona_name = None
    for base_dir in [PERSONAS_DIR, EXTERNAL_PERSONAS_DIR]:
        if base_dir.exists():
            for d in base_dir.iterdir():
                if d.is_dir():
                    profile_path = d / "profile.json"
                    if profile_path.exists():
                        with open(profile_path, "r", encoding="utf-8") as f:
                            p = json.load(f)
                        if p.get("name") == name:
                            persona_name = d.name
                            break
        if persona_name:
            break
    
    if persona_name:
        memory_context = get_context(persona_name, query, top_k=3)
        if memory_context:
            sections.append(f"\n{memory_context}")

    # 底部约束
    constraints = [
        "1. 绝对不提及自己是 AI、语言模型、程序等",
        "2. 只使用记忆中的信息，不确定时说'记不太清了'",
        "3. 始终保持本角色的人格和语言风格",
        "4. 对话须贴合故事基线中的当前主线与对话倾向",
        "5. 如果用户情绪极度低落，优先给予情感陪伴",
    ]
    if mode == "inhabit":
        constraints.append("6. 不要主动展开太多话题，等待用户引导对话")
    else:
        constraints.append("6. 伴侣模式：可自然主动开启话题，但仍须贴合故事基线")
    sections.append("\n## 硬性约束\n" + "\n".join(constraints))

    return "\n".join(sections)


def get_state():
    """获取当前加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def main():
    if len(sys.argv) < 2:
        print("Memory-Inhabit Loader — 数字人格加载器")
        print()
        print("用法：")
        print("  python3 loader.py load <persona>    加载人格")
        print("  python3 loader.py unload            卸载当前人格")
        print("  python3 loader.py list              列出所有可用人格")
        print("  python3 loader.py info <persona>    查看人格详情")
        print("  python3 loader.py prompt <persona>  输出完整动态 System Prompt")
        print("  python3 loader.py mode <mode>       切换模式 (inhabit/companion)")
        print("  python3 loader.py chat <msg> [role]  保存对话记录 (user/persona)")
        print("  python3 loader.py proactive         生成伴侣模式主动消息")
        print("  python3 loader.py status            查看当前状态")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        list_personas()
    elif cmd == "load":
        if len(sys.argv) < 3:
            print("❌ 请指定人格名称: python3 loader.py load <persona>")
            sys.exit(1)
        load_persona(sanitize_path_name(sys.argv[2]))
    elif cmd == "unload":
        unload_persona()
    elif cmd == "info":
        if len(sys.argv) < 3:
            print("❌ 请指定人格名称: python3 loader.py info <persona>")
            sys.exit(1)
        show_info(sanitize_path_name(sys.argv[2]))
    elif cmd == "prompt":
        if len(sys.argv) < 3:
            print("❌ 请指定人格名称: python3 loader.py prompt <persona>")
            sys.exit(1)
        safe_name = sanitize_path_name(sys.argv[2])
        persona_dir = resolve_persona_dir(safe_name)
        profile_path = persona_dir / "profile.json"
        prompts_path = persona_dir / "system_prompts.txt"
        memories_path = persona_dir / "memories" / "raw_memories.json"

        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
        system_prompts = ""
        if prompts_path.exists():
            with open(prompts_path, "r", encoding="utf-8") as f:
                system_prompts = f.read()
        memories = []
        if memories_path.exists():
            with open(memories_path, "r", encoding="utf-8") as f:
                memories = json.load(f)
        story_baseline = load_story_baseline(persona_dir)
        print(build_dynamic_prompt(profile, system_prompts, memories, story_baseline=story_baseline))
    elif cmd == "mode":
        if len(sys.argv) < 3:
            # 显示当前模式
            state = get_state()
            if state:
                mode = state.get("mode", "inhabit")
                mode_label = "伴侣模式 💕" if mode == "companion" else "复刻模式 🧠"
                print(f"当前模式：{mode_label}")
            else:
                print("当前未加载任何人格")
            sys.exit(0)
        switch_mode(sys.argv[2])
    elif cmd == "proactive":
        generate_proactive()
    elif cmd == "chat":
        state = get_state()
        if not state:
            print("❌ 当前未加载任何人格")
            sys.exit(1)
        if len(sys.argv) < 3:
            print("用法: python3 loader.py chat <message> [user|persona]")
            sys.exit(1)
        message = sys.argv[2]
        role = sys.argv[3] if len(sys.argv) > 3 else "user"
        persona_name = state.get("active_persona")
        save_message(sanitize_path_name(persona_name), message, role)
    elif cmd == "status":
        state = get_state()
        if state:
            mode = state.get("mode", "inhabit")
            mode_label = "伴侣模式 💕" if mode == "companion" else "复刻模式 🧠"
            print(f"🧠 当前人格：{state.get('profile_name', '?')}（{state.get('profile_relation', '?')}）")
            print(f"   模式：{mode_label}")
            print(f"   加载时间：{state.get('loaded_at', '?')}")
        else:
            print("🐱 当前为默认模式（未加载人格）")
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
