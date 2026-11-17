"""
local-rag-builder Prompt 管理模块
v0.1.0
支持模板持久化、自定义、重置
"""

import os
import sys
from utils import PROMPTS_DIR

DEFAULT_TEMPLATE = """基于以下资料回答问题。如果资料中没有相关信息，请说"不知道"。

资料：
{context}

问题：{question}

请用 Markdown 格式输出，并在末尾附上引用片段编号。

回答："""

TEMPLATE_FILE = os.path.join(PROMPTS_DIR, "custom_prompt_template.txt")


def get_template_path():
    return TEMPLATE_FILE


def load_template():
    """加载 Prompt 模板，不存在则返回默认"""
    try:
        if os.path.exists(TEMPLATE_FILE):
            with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content
    except (OSError, IOError):
        pass
    return DEFAULT_TEMPLATE


def save_template(content):
    """保存自定义 Prompt 模板"""
    try:
        tmp = TEMPLATE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(content.strip())
        os.replace(tmp, TEMPLATE_FILE)
        return True
    except (OSError, IOError) as e:
        return False


def reset_template():
    """重置为默认模板"""
    save_template(DEFAULT_TEMPLATE)
    return DEFAULT_TEMPLATE


def get_default_template():
    return DEFAULT_TEMPLATE


def build_prompt(context, question, template=None):
    """构建最终 Prompt"""
    tpl = template or load_template()
    return tpl.format(context=context, question=question)


def list_saved_templates():
    """列出所有已保存的模板"""
    templates = []
    prompts_dir = PROMPTS_DIR
    if not os.path.exists(prompts_dir):
        return templates
    for f in os.listdir(prompts_dir):
        if f.endswith(".txt"):
            templates.append(f)
    return templates


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prompt 管理工具")
    parser.add_argument("--show", action="store_true", help="显示当前模板")
    parser.add_argument("--set", type=str, help="设置模板内容（多行用 \\n 分隔）")
    parser.add_argument("--set-file", type=str, help="从文件读取并设置模板")
    parser.add_argument("--reset", action="store_true", help="重置为默认模板")
    parser.add_argument("--list", action="store_true", help="列出所有已保存模板")
    parser.add_argument("--validate", type=str, help="验证模板是否包含必要占位符")

    args = parser.parse_args()

    if args.show:
        print(load_template())
    elif args.set:
        content = args.set.replace("\\n", "\n")
        save_template(content)
        print(f"[OK] 模板已保存 ({len(content)} 字符)")
    elif args.set_file:
        try:
            with open(args.set_file, "r", encoding="utf-8") as f:
                save_template(f.read())
            print(f"[OK] 已从 {args.set_file} 加载模板")
        except (OSError, IOError) as e:
            print(f"[!] 读取文件失败: {e}")
            sys.exit(1)
    elif args.reset:
        save_template(DEFAULT_TEMPLATE)
        print("[OK] 已重置为默认模板")
    elif args.list:
        templates = list_saved_templates()
        for t in templates:
            print(t)
    elif args.validate:
        try:
            with open(args.validate, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, IOError) as e:
            print(f"[!] 读取文件失败: {e}")
            sys.exit(1)
        errors = []
        if "{context}" not in content:
            errors.append("缺少 {context} 占位符")
        if "{question}" not in content:
            errors.append("缺少 {question} 占位符")
        if errors:
            print(f"[FAIL] {'; '.join(errors)}")
            sys.exit(1)
        else:
            print("[OK] 模板包含所有必需占位符")
    else:
        parser.print_help()
