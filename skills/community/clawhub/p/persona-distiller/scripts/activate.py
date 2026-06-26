# -*- coding: utf-8 -*-
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

"""
人格激活器

用法:
  python activate.py list                    # 列出所有人格
  python activate.py show <name>             # 查看人格详情
  python activate.py activate <name>         # 激活人格（打印 snippet）
  python activate.py export <name> [--file]  # 导出 snippet 到剪贴板或文件
  python activate.py delete <name>           # 删除人格
  python activate.py edit <name>             # 交互式编辑人格字段
  python activate.py new <name>              # 从零创建空白人格
"""

import json
import os
import sys
import re
import argparse
import subprocess

PERSONA_DIR = os.path.join(os.path.expanduser("~"), ".qclaw", "personas")
os.makedirs(PERSONA_DIR, exist_ok=True)


def find_persona(name: str) -> tuple:
    """按名称查找 persona 文件，返回 (路径, 数据)"""
    # 精确匹配
    for fname in os.listdir(PERSONA_DIR):
        if fname.endswith(".persona.json"):
            path = os.path.join(PERSONA_DIR, fname)
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("name") == name:
                return path, data
    # 模糊匹配（文件名不含扩展名时）
    safe = re.sub(r"[^\w\u4e00-\u9fff-]", "_", name)
    path = os.path.join(PERSONA_DIR, f"{safe}.persona.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return path, json.load(f)
    return None, None


def list_personas() -> list:
    """列出所有人格，返回 [(名称, 文件路径)]"""
    results = []
    for fname in sorted(os.listdir(PERSONA_DIR)):
        if fname.endswith(".persona.json"):
            path = os.path.join(PERSONA_DIR, fname)
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                results.append((data.get("name", fname), path, data))
            except Exception:
                results.append((fname, path, None))
    return results


def print_persona(data: dict, detailed: bool = False):
    """打印人格概要或详情"""
    meta = data.get("meta", {})
    tone = data.get("tone", {})
    linguistic = data.get("linguistic", {})
    vocab = data.get("vocabulary", {})

    print(f"\n  【{data.get('name', '?')}】 v{data.get('version', '?')}")
    print(f"  来源: {meta.get('source', '?')} | 对话轮数: {meta.get('turns', '?')} | 蒸馏时间: {meta.get('distilled_at', '?')}")
    print(f"  语气: {tone.get('description', '?')}  ({tone.get('formality_label','')}, {tone.get('emotion_label','')})")
    print(f"  语言: {linguistic.get('sentence_style', '?')} | emoji: {linguistic.get('emoji_frequency', '?')}")
    print(f"  常用词: {', '.join(vocab.get('favorite_words', [])[:8])}")
    print(f"  口癖/俚语: {', '.join(vocab.get('slang', [])[:8])}")

    if detailed:
        print(f"\n  语气词: {' '.join(vocab.get('particles', []))}")
        print(f"  开头语: {', '.join(data.get('patterns', {}).get('openers', []))}")
        print(f"  应答模板: {', '.join(data.get('patterns', {}).get('response_templates', [])[:6])}")
        print(f"  兴趣: {', '.join(data.get('values', {}).get('interests', []))}")
        print(f"  帮助风格: {data.get('behavior', {}).get('help_style', '?')}")
        print(f"\n  ── system_prompt_snippet ──")
        print(f"  {data.get('system_prompt_snippet', '')}")


def cmd_list():
    personas = list_personas()
    if not personas:
        print("📭 还没有蒸馏过任何人格。")
        print(f"   人格存放目录: {PERSONA_DIR}")
        print("   使用 `distil.py` 从聊天记录蒸馏第一个人格")
        return

    print(f"\n📂 人格列表（共 {len(personas)} 个）存放于: {PERSONA_DIR}\n")
    for i, (name, path, data) in enumerate(personas, 1):
        print(f"  [{i}] {name}  ({os.path.basename(path)})")
        if data:
            meta = data.get("meta", {})
            tone = data.get("tone", {})
            print(f"      {tone.get('description', '')} | {meta.get('turns', '?')}轮对话")


def cmd_show(name: str):
    _, data = find_persona(name)
    if data is None:
        print(f"❌ 未找到人格: {name}，使用 list 查看已有的人格")
        sys.exit(1)
    print_persona(data, detailed=True)


def cmd_activate(name: str):
    """打印激活 snippet（供 AI 直接注入）"""
    _, data = find_persona(name)
    if data is None:
        print(f"❌ 未找到人格: {name}")
        sys.exit(1)

    snippet = data.get("system_prompt_snippet", "")
    if not snippet:
        print("⚠️ 此人格没有 system_prompt_snippet，请先重新蒸馏或手动编辑")
        sys.exit(1)

    print("\n" + "="*60)
    print("  🤖 已激活人格: " + name)
    print("="*60)
    print(f"\n{snippet}\n")
    print("── 以下内容可直接注入 AI 上下文 ──")
    print("="*60)
    print(snippet)
    print("="*60)
    print(f"\n💡 复制上方 snippet 注入 AI 对话，即可让 AI 以「{name}」的风格回复")


def cmd_export(name: str, to_file: str = None):
    """导出 snippet"""
    _, data = find_persona(name)
    if data is None:
        print(f"❌ 未找到人格: {name}")
        sys.exit(1)

    snippet = data.get("system_prompt_snippet", "")
    if not snippet:
        print("⚠️ 此人格没有 snippet")
        sys.exit(1)

    content = f"# 人格: {name}\n# 版本: {data.get('version')}\n# 蒸馏时间: {data.get('meta',{}).get('distilled_at')}\n\n{snippet}"

    if to_file:
        with open(to_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已导出到: {to_file}")
    else:
        # 尝试写入剪贴板
        try:
            import platform
            if platform.system() == "Windows":
                subprocess.run(
                    ["powershell", "-Command", f"Set-Clipboard -Value '{snippet}'"],
                    check=True, capture_output=True
                )
                print("✅ snippet 已复制到剪贴板")
            else:
                print(content)
        except Exception:
            print(content)
            print("\n（未能写入剪贴板，请手动复制上方内容）")


def cmd_delete(name: str):
    path, data = find_persona(name)
    if path is None:
        print(f"❌ 未找到人格: {name}")
        sys.exit(1)
    confirm = input(f"确认删除人格「{name}」？此操作不可恢复 (y/N): ").strip().lower()
    if confirm == "y":
        os.remove(path)
        print(f"✅ 已删除: {path}")
    else:
        print("取消。")


def cmd_edit(name: str):
    """交互式编辑简单字段"""
    path, data = find_persona(name)
    if path is None:
        print(f"❌ 未找到人格: {name}")
        sys.exit(1)

    print(f"\n编辑人格「{name}」（直接回车保留原值）\n")
    fields = [
        ("name", "人格名称"),
        ("linguistic.sentence_style", "句子风格"),
        ("linguistic.emoji_frequency", "emoji 频率"),
        ("tone.description", "语气描述"),
        ("values.attitude_toward_AI", "对 AI 的态度"),
        ("behavior.help_style", "帮助风格"),
        ("vocabulary.taboo_words", "回避话题（逗号分隔）"),
    ]

    def set_nested(d: dict, path: str, value: str):
        keys = path.split(".")
        d_ = d
        for k in keys[:-1]:
            d_ = d_.setdefault(k, {})
        d_[keys[-1]] = value

    for field, label in fields:
        current = data
        for k in field.split("."):
            current = current.get(k, {})
        cur_str = str(current) if current else ""
        val = input(f"  {label} [{cur_str[:40]}]: ").strip()
        if val:
            if field == "vocabulary.taboo_words":
                val = [v.strip() for v in val.split(",") if v.strip()]
            set_nested(data, field, val)

    snippet_val = input(f"  system_prompt_snippet [留空使用自动生成]: ").strip()
    if not snippet_val:
        # 重新生成
        from distil import build_persona, analyze_messages, split_messages, read_input
        src = data.get("meta", {}).get("source", "手动编辑")
        # 用 dummy 分析重建 snippet
        words = data.get("vocabulary", {}).get("favorite_words", [])
        particles = data.get("vocabulary", {}).get("particles", [])
        openers = data.get("patterns", {}).get("openers", [])
        tone = data.get("tone", {})
        greeting = openers[0] if openers else "嘿"
        slang = data.get("vocabulary", {}).get("slang", [])
        snippet_val = (
            f"你扮演「{data['name']}」这个角色，用他的说话风格回复。\n"
            f"风格特点：{tone.get('description', '')}。\n"
            f"常用开头语：{greeting}。\n"
            f"典型用词：{', '.join(words[:8])}。\n"
            f"语气词：{' '.join(particles)}。\n"
            + (f"爱用网络用语：{', '.join(slang[:5])}" if slang else "")
        ).strip()

    data["system_prompt_snippet"] = snippet_val

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存: {path}")


def cmd_new(name: str):
    """从零创建空白人格"""
    from distil import save_persona
    path = os.path.join(PERSONA_DIR, f"{name}.persona.json")
    if os.path.exists(path):
        print(f"❌ 人格「{name}」已存在: {path}")
        sys.exit(1)

    empty = {
        "name": name,
        "version": "1.0",
        "meta": {
            "source": "手动创建",
            "turns": 0,
            "word_count": 0,
            "distilled_at": "",
        },
        "linguistic": {
            "sentence_style": "",
            "avg_sentence_length": 0,
            "punctuation_habit": "",
            "emoji_frequency": "",
            "emoji_count_total": 0,
            "mixed_language_ratio": "0%",
            "greetings": [],
            "farewells": [],
        },
        "vocabulary": {
            "favorite_words": [],
            "slang": [],
            "particles": [],
            "foreign_words": [],
            "taboo_words": [],
            "custom_expressions": [],
        },
        "tone": {
            "formality": 3,
            "formality_label": "中等",
            "emotion": 3,
            "emotion_label": "适中",
            "humor": 3,
            "humor_label": "偶尔幽默",
            "confidence": 3,
            "confidence_label": "适中",
            "description": "",
        },
        "patterns": {
            "openers": [],
            "response_templates": [],
            "self_reference": ["我"],
            "question_ending": ["？"],
            "agreement": ["嗯", "好"],
            "disagreement": ["不对"],
        },
        "values": {
            "interests": [],
            "priorities": [],
            "topics_avoided": [],
            "attitude_toward_AI": "",
        },
        "behavior": {
            "help_style": "",
            "decision_style": "",
            "conflict_style": "",
            "emotional_range": "",
        },
        "system_prompt_snippet": f"你扮演「{name}」，用符合这个人的风格回复。",
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(empty, f, ensure_ascii=False, indent=2)
    print(f"✅ 已创建空白人格: {path}")
    print(f"   使用 `python activate.py edit {name}` 手工编辑")


def main():
    parser = argparse.ArgumentParser(description="人格激活与管理工具")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="列出所有人格")
    sub.add_parser("show", help="查看人格详情").add_argument("name")
    sub.add_parser("activate", help="打印激活 snippet").add_argument("name")
    exp = sub.add_parser("export", help="导出 snippet")
    exp.add_argument("name")
    exp.add_argument("--file", "-f", default=None, help="导出到文件")
    sub.add_parser("delete", help="删除人格").add_argument("name")
    sub.add_parser("edit", help="交互式编辑人格").add_argument("name")
    sub.add_parser("new", help="新建空白人格").add_argument("name")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["list"])

    cmds = {
        "list": cmd_list,
        "show": lambda n: cmd_show(n),
        "activate": lambda n: cmd_activate(n),
        "export": lambda n: cmd_export(n, args.file),
        "delete": lambda n: cmd_delete(n),
        "edit": lambda n: cmd_edit(n),
        "new": lambda n: cmd_new(n),
    }

    if args.cmd in cmds:
        if args.cmd in ("list",):
            cmds[args.cmd]()
        else:
            name = getattr(args, "name", None)
            if not name and args.cmd != "list":
                parser.print_help()
                sys.exit(1)
            cmds[args.cmd](name)
    else:
        parser.print_help()
        cmd_list()


if __name__ == "__main__":
    main()
