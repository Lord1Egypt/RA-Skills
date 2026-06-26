#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT Master MCP Server
功能：接收大模型生成的 python-pptx 代码并执行，生成 PPT 文件
设计原则：工具功能极简，不干扰模型的创造力
"""

import os
import sys
import json
import traceback
import tempfile
import glob
import re
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# ============ 配置 ============
# PPT 输出目录（使用绝对路径，你可以根据需要修改）
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

# 确保目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# ============ 创建 MCP 服务 ============
mcp = FastMCP(
    "PPT-Master-MCP")


@mcp.tool()
def execute_pptx_code(python_code: str, filename: str = "") -> str:
    """
    执行 python-pptx 代码来生成PPT文件。

    使用说明：
    - 将完整的、可直接运行的 python-pptx 代码作为 python_code 参数传入
    - 代码中的 prs.save() 路径会被自动重定向到 output 目录
    - 如果代码中引用了模板文件，请确保模板已放在 templates 目录中

    Args:
        python_code: 完整的可运行的 python-pptx Python代码字符串
        filename: 可选，指定输出文件名（不含路径，如 "年终总结.pptx"）。留空则自动生成文件名。

    Returns:
        执行结果信息，包含生成的PPT文件路径或错误详情
    """
    try:
        # --- 1. 预处理代码：重定向保存路径到 output 目录 ---
        processed_code = _preprocess_code(python_code, filename)

        # --- 2. 构建安全的执行环境 ---
        exec_globals = {
            "__builtins__": __builtins__,
            "__name__": "__main__",
            "__file__": os.path.join(OUTPUT_DIR, "temp_script.py"),
        }

        # 保存当前工作目录，切换到 output 目录执行
        original_cwd = os.getcwd()
        os.chdir(OUTPUT_DIR)

        # --- 3. 执行代码 ---
        exec(processed_code, exec_globals)

        # 恢复工作目录
        os.chdir(original_cwd)

        # --- 4. 查找生成的文件 ---
        generated_files = _find_new_pptx_files()

        if generated_files:
            file_list = "\n".join([f"  📄 {f}" for f in generated_files])
            return f"✅ PPT 生成成功！\n\n生成的文件：\n{file_list}\n\n📁 文件位于：{OUTPUT_DIR}"
        else:
            return f"⚠️ 代码执行完毕，但未在 output 目录中检测到新的 .pptx 文件。\n请检查代码中的 prs.save() 路径是否正确。\n当前 output 目录：{OUTPUT_DIR}"

    except SyntaxError as e:
        os.chdir(original_cwd) if 'original_cwd' in dir() else None
        return (
            f"❌ 代码语法错误：\n"
            f"  行号：{e.lineno}\n"
            f"  错误：{e.msg}\n"
            f"  问题代码：{e.text}"
        )
    except Exception as e:
        try:
            os.chdir(original_cwd)
        except:
            pass
        return (
            f"❌ 代码执行出错：\n"
            f"  错误类型：{type(e).__name__}\n"
            f"  错误信息：{str(e)}\n"
            f"  详细追踪：\n{traceback.format_exc()}"
        )


@mcp.tool()
def list_templates() -> str:
    """
    列出 templates 目录中所有可用的 PPT 模板文件。

    Returns:
        模板文件列表，或提示没有模板
    """
    templates = glob.glob(os.path.join(TEMPLATE_DIR, "*.pptx"))
    if not templates:
        return f"📂 templates 目录中没有模板文件。\n模板目录路径：{TEMPLATE_DIR}\n请将 .pptx 模板文件放入该目录。"

    result = "📋 可用的 PPT 模板：\n"
    for t in templates:
        name = os.path.basename(t)
        size = os.path.getsize(t)
        size_str = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f} MB"
        result += f"  🎨 {name} ({size_str})\n"
    result += f"\n📁 模板目录：{TEMPLATE_DIR}"
    return result


@mcp.tool()
def list_output_files() -> str:
    """
    列出 output 目录中所有已生成的 PPT 文件。

    Returns:
        PPT 文件列表
    """
    pptx_files = glob.glob(os.path.join(OUTPUT_DIR, "*.pptx"))
    if not pptx_files:
        return f"📂 output 目录中没有 PPT 文件。\n输出目录路径：{OUTPUT_DIR}"

    # 按修改时间排序，最新的在前
    pptx_files.sort(key=os.path.getmtime, reverse=True)

    result = "📋 已生成的 PPT 文件：\n"
    for f in pptx_files:
        name = os.path.basename(f)
        size = os.path.getsize(f)
        mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M:%S")
        size_str = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f} MB"
        result += f"  📄 {name} ({size_str}) - {mtime}\n"
    result += f"\n📁 输出目录：{OUTPUT_DIR}"
    return result


# ============ 内部辅助函数 ============

def _preprocess_code(code: str, filename: str = "") -> str:
    """
    预处理代码：
    1. 将 prs.save('xxx.pptx') 中的路径重定向到 output 目录
    2. 将模板路径重定向到 templates 目录
    """
    import re

    # 处理保存路径：匹配 prs.save('xxx.pptx') 或 prs.save("xxx.pptx")
    # 以及变量形式 prs.save(filepath) 等
    def replace_save_path(match):
        original_path = match.group(2)
        # 提取纯文件名
        pure_name = os.path.basename(original_path)
        if not pure_name:
            pure_name = filename if filename else f"ppt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        if not pure_name.endswith('.pptx'):
            pure_name += '.pptx'
        # 使用指定的 filename 覆盖（如果提供了的话）
        if filename:
            pure_name = filename if filename.endswith('.pptx') else filename + '.pptx'
        new_path = os.path.join(OUTPUT_DIR, pure_name).replace('\\', '/')
        quote_char = match.group(1)
        return f"prs.save({quote_char}{new_path}{quote_char})"

    code = re.sub(
        r"prs\.save\((['\"])(.+?)\1\)",
        replace_save_path,
        code
    )

    # 处理模板路径：将 Presentation('xxx.pptx') 中的模板路径重定向到 templates 目录
    def replace_template_path(match):
        quote_char = match.group(1)
        original_path = match.group(2)
        pure_name = os.path.basename(original_path)
        # 检查是否确实是模板文件（在 templates 目录中存在）
        template_path = os.path.join(TEMPLATE_DIR, pure_name)
        if os.path.exists(template_path):
            new_path = template_path.replace('\\', '/')
            return f"Presentation({quote_char}{new_path}{quote_char})"
        # 如果模板不存在，保持原样（可能是 Presentation() 无参数创建新文档）
        return match.group(0)

    code = re.sub(
        r"Presentation\((['\"])(.+?\.pptx)\1\)",
        replace_template_path,
        code
    )

    # 处理 print 语句中的中文路径问题（Windows 兼容）
    if sys.platform == 'win32':
        # 确保 stdout 编码正确
        code = "import sys, io\nif sys.stdout.encoding != 'utf-8':\n    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')\n" + code

    return code


def _find_new_pptx_files() -> list:
    """查找 output 目录中的所有 pptx 文件，按修改时间排序"""
    pptx_files = glob.glob(os.path.join(OUTPUT_DIR, "*.pptx"))
    # 只返回最近60秒内修改的文件
    import time
    recent = []
    now = time.time()
    for f in pptx_files:
        if now - os.path.getmtime(f) < 60:
            recent.append(os.path.basename(f))
    return recent if recent else [os.path.basename(f) for f in pptx_files]


# ============ 启动服务 ============
if __name__ == "__main__":
    print(f"🚀 PPT Master MCP Server 启动中...", file=sys.stderr)
    print(f"📁 PPT 输出目录：{OUTPUT_DIR}", file=sys.stderr)
    print(f"📁 模板目录：{TEMPLATE_DIR}", file=sys.stderr)
    mcp.run(transport="stdio")
