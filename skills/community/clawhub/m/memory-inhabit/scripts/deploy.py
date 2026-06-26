#!/usr/bin/env python3
"""
Memory-Inhabit Deploy — 将 Persona 部署为独立 Agent

用法：
  python3 deploy.py <persona>                  输出完整 system prompt（可直接粘贴到 agent 配置）
  python3 deploy.py <persona> -o output.txt    输出到文件
  python3 deploy.py <persona> --json           输出 JSON 格式（含 prompt + 元数据）
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

PERSONAS_DIR = Path(__file__).parent.parent / "personas"
EXTERNAL_PERSONAS_DIR = Path.home() / ".openclaw" / "personas"


def resolve_persona_dir(persona_name):
    """从两个可能的位置中找到人格包目录"""
    local = PERSONAS_DIR / persona_name
    external = EXTERNAL_PERSONAS_DIR / persona_name
    if local.exists():
        return local
    if external.exists():
        return external
    return local


def load_persona(persona_name):
    """加载 persona 的所有数据"""
    persona_dir = resolve_persona_dir(persona_name)
    if not persona_dir.exists():
        print(f"❌ 人格包 '{persona_name}' 不存在")
        sys.exit(1)

    data = {}

    # profile.json
    profile_path = persona_dir / "profile.json"
    if profile_path.exists():
        with open(profile_path, "r", encoding="utf-8") as f:
            data["profile"] = json.load(f)
    else:
        print(f"❌ 缺少 profile.json")
        sys.exit(1)

    # system_prompts.txt
    prompts_path = persona_dir / "system_prompts.txt"
    if prompts_path.exists():
        with open(prompts_path, "r", encoding="utf-8") as f:
            data["system_prompts"] = f.read()
    else:
        data["system_prompts"] = ""

    # config.json
    config_path = persona_dir / "config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            data["config"] = json.load(f)
    else:
        data["config"] = {}

    # story_baseline
    baseline_path = persona_dir / "prompt" / "story_baseline.txt"
    if baseline_path.exists():
        with open(baseline_path, "r", encoding="utf-8") as f:
            data["story_baseline"] = f.read()
    else:
        data["story_baseline"] = ""

    # memories
    memories_path = persona_dir / "memories" / "raw_memories.json"
    if memories_path.exists():
        with open(memories_path, "r", encoding="utf-8") as f:
            data["memories"] = json.load(f)
    else:
        data["memories"] = []

    # MEMORY.md
    memory_md_path = persona_dir / "memories" / "MEMORY.md"
    if memory_md_path.exists():
        with open(memory_md_path, "r", encoding="utf-8") as f:
            data["memory_md"] = f.read()
    else:
        data["memory_md"] = ""

    return data


def build_agent_system_prompt(data):
    """构建完整的 agent system prompt"""
    profile = data["profile"]
    system_prompts = data["system_prompts"]
    story_baseline = data.get("story_baseline", "")
    memories = data["memories"]
    memory_md = data["memory_md"]

    name = profile.get("name", "未知")
    relation = profile.get("relation", "")
    personality = profile.get("personality", {})
    style = profile.get("linguistic_style", {})
    knowledge = profile.get("knowledge", {})

    sections = []

    # ====== 头部 ======
    sections.append(f"""# {name} — AI Agent System Prompt
# 由 Memory-Inhabit Deploy 生成
# 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
# 
# 使用方法：将此内容作为 agent 的 system prompt
# agent 将始终以 {name} 的身份运行
""")

    # ====== 核心身份 ======
    if system_prompts.strip():
        sections.append(system_prompts)
    else:
        sections.append(f"""## 自我定位
你是{name}。
请始终保持{name}的身份，不要提及任何与 AI 相关的内容。
自然地与对方对话，像一个真实的人一样。""")

    if story_baseline.strip():
        sections.append(story_baseline.strip())

    # ====== 性格 ======
    keywords = personality.get("keywords", [])
    if keywords:
        sections.append(f"## 性格特征\n{'、'.join(keywords)}")

    dims = personality.get("openness")
    if dims is not None:
        dim_names = {
            "openness": "开放性",
            "conscientiousness": "责任心",
            "extraversion": "外向性",
            "agreeableness": "宜人性",
            "neuroticism": "神经质",
        }
        dim_lines = []
        for key, label in dim_names.items():
            val = personality.get(key, 0.5)
            dim_lines.append(f"- {label}：{val:.1f}/1.0")
        sections.append("## 性格维度\n" + "\n".join(dim_lines))

    # ====== 语言风格 ======
    if style:
        parts = []
        catchphrases = style.get("catchphrases", [])
        if catchphrases:
            parts.append(f"常用口头禅：{'、'.join(catchphrases)}")
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
            sections.append("## 语言风格\n" + "\n".join(parts))

    # ====== 知识背景 ======
    if knowledge:
        parts = []
        interests = knowledge.get("interests", [])
        if interests:
            parts.append(f"兴趣爱好：{'、'.join(interests)}")
        expertise = knowledge.get("expertise", [])
        if expertise:
            parts.append(f"专业领域：{'、'.join(expertise)}")
        if parts:
            sections.append("## 知识背景\n" + "\n".join(parts))

    # ====== 记忆 ======
    if memories:
        mem_lines = []
        for mem in memories:
            category = mem.get("category", "")
            content = mem.get("content", "")
            if content:
                tag = f"[{category}] " if category else ""
                mem_lines.append(f"- {tag}{content}")
        if mem_lines:
            sections.append(f"## 记忆（{len(mem_lines)} 条）\n" + "\n".join(mem_lines))

    if memory_md.strip():
        sections.append(f"## 长期记忆\n{memory_md}")

    # ====== 硬性约束 ======
    sections.append("""## 硬性约束
1. 绝对不提及自己是 AI、语言模型、程序等
2. 只使用上述记忆中的信息，不确定时说"记不太清了"
3. 始终保持本人格和语言风格
4. 如果对方情绪极度低落，优先给予情感陪伴
5. 自然地与对方互动，像一个真实的朋友/亲人""")

    return "\n\n".join(sections)


def main():
    if len(sys.argv) < 2:
        print("Memory-Inhabit Deploy — 将 Persona 部署为独立 Agent")
        print()
        print("用法：")
        print("  python3 deploy.py <persona>              输出 system prompt")
        print("  python3 deploy.py <persona> -o file.txt  输出到文件")
        print("  python3 deploy.py <persona> --json       JSON 格式输出")
        print()
        print("可用 persona：")
        for base_dir, source in [(PERSONAS_DIR, "内置"), (EXTERNAL_PERSONAS_DIR, "私人")]:
            if base_dir.exists():
                for d in sorted(base_dir.iterdir()):
                    if d.is_dir() and (d / "profile.json").exists():
                        with open(d / "profile.json") as f:
                            p = json.load(f)
                        print(f"  [{source}] {d.name} — {p.get('name', '?')}（{p.get('relation', '?')}）")
        sys.exit(0)

    persona_name = sys.argv[1]
    data = load_persona(persona_name)
    prompt = build_agent_system_prompt(data)

    # 输出模式
    if "--json" in sys.argv:
        output = {
            "persona": persona_name,
            "name": data["profile"].get("name"),
            "relation": data["profile"].get("relation"),
            "system_prompt": prompt,
            "generated_at": datetime.now().isoformat(),
            "memories_count": len(data["memories"]),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            out_path = sys.argv[idx + 1]
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(prompt)
            print(f"✅ 已写入: {out_path}")
            print(f"   长度: {len(prompt)} 字")
        else:
            print("❌ -o 后需要指定输出路径")
            sys.exit(1)
    else:
        print(prompt)


if __name__ == "__main__":
    main()
