r"""
component_inject.py — 向现有 .tex 增量插入组件

功能：
  将组件库中的组件增量插入到现有 .tex 文件。
  自动将组件的导言区内容（宏包、命令定义等）追加到目标文件的导言区，
  将正文内容插入到用户指定的位置。

  支持自动检测目标文档的 LaTeX 引擎：
  - LuaLaTeX / XeLaTeX: 直接注入 lualatex 语法组件
  - pdfLaTeX: 将组件内的 LuaLaTeX 特有语法转换为 pdfLaTeX 兼容语法

用法:
  python scripts/component_inject.py --input doc.tex --component table-style --after "\\section{数据}"
  python scripts/component_inject.py --input doc.tex --component figure-insert --at-begin-document
  python scripts/component_inject.py --input doc.tex -c table-style --engine pdflatex --before "\\end{document}"
  python scripts/component_inject.py --list-components
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path


# ── 引擎检测规则 ───────────────────────────────────────────
ENGINE_RULES = [
    ("lualatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{fontspec\}'),
    ("lualatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{luacode\}'),
    ("lualatex", r'\\directlua'),
    ("xelatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{fontspec\}'),
    ("xelatex", r'\\XeTeX'),
    ("pdflatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{inputenc\}'),
    ("pdflatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{fontenc\}'),
    ("pdflatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{CJK\}'),
    ("pdflatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{times\}'),
    ("pdflatex", r'\\usepackage\s*(?:\[.*?\])?\s*\{mathptmx\}'),
]

# ── 组件 → pdfLaTeX 转换规则 ──────────────────────────────
PDFTEX_CONVERSION_RULES = [
    (r'^\s*\\usepackage\s*(?:\[.*?\])?\s*\{fontspec\}\s*', "", "删除 fontspec（pdflatex 不支持）"),
    (r'^\s*\\setmainfont\s*(?:\[.*?\])?\s*\{.*?\}\s*', "", "删除 \\setmainfont"),
    (r'^\s*\\setsansfont\s*(?:\[.*?\])?\s*\{.*?\}\s*', "", "删除 \\setsansfont"),
    (r'^\s*\\setmonofont\s*(?:\[.*?\])?\s*\{.*?\}\s*', "", "删除 \\setmonofont"),
    (r'^\s*\\newfontfamily\s*\\[a-zA-Z]+\s*(?:\[.*?\])?\s*\{.*?\}\s*', "", "删除 \\newfontfamily"),
    (r'^\s*\\defaultfontfeatures\s*\{.*?\}\s*', "", "删除 \\defaultfontfeatures"),
]

# ── 组件默认 body 模板 ────────────────────────────────────
COMPONENT_BODY_TEMPLATES = {
    "table-style": r"""
% --- 插入的表格 ---
\begin{table}[H]
\centering
\caption{表格标题}
\begin{tabularx}{\linewidth}{|l|X|}
\hline
\textbf{项目} & \textbf{说明} \\ \hline
项目1 & 说明内容 \\ \hline
项目2 & 说明内容 \\ \hline
\end{tabularx}
\end{table}
""",
    "figure-insert": r"""
% --- 插入的图片 ---
\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{图片路径}
\caption{图片标题}
\end{figure}
""",
}


# ── 工具函数 ──────────────────────────────────────────────

def find_skill_dir() -> str:
    return str(Path(__file__).resolve().parent.parent)


def read_manifest() -> dict:
    for p in [
        os.path.join(find_skill_dir(), "scripts", "components", "manifest.json"),
        os.path.join(find_skill_dir(), "components", "manifest.json"),
    ]:
        if os.path.isfile(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return {"components": []}


def list_components() -> list:
    manifest = read_manifest()
    comps = manifest.get("components", [])
    if isinstance(comps, dict):
        return [{"name": k, "path": v.get("file", ""),
                 "type": v.get("type", ""), "description": v.get("desc", "")}
                for k, v in comps.items()]
    return [{"name": c.get("name", ""), "path": c.get("path", ""),
             "type": c.get("type", ""), "description": c.get("description", "")}
            for c in comps]


def find_component_path(component_name: str) -> str:
    if os.path.isfile(component_name):
        return component_name
    base = os.path.join(find_skill_dir(), "scripts", "components")
    manifest = read_manifest()
    comps = manifest.get("components", [])
    if isinstance(comps, dict):
        comps = [{"name": k, "path": v.get("file", ""),
                  "type": v.get("type", "")} for k, v in comps.items()]
    for c in comps:
        if c.get("name") == component_name:
            p = os.path.join(base, c.get("path", ""))
            if os.path.isfile(p):
                return p
    for c in comps:
        if component_name.lower() in c.get("name", "").lower():
            p = os.path.join(base, c.get("path", ""))
            if os.path.isfile(p):
                return p
    return ""


def detect_engine(content: str) -> str:
    preamble_end = content.find(r"\begin{document}")
    preamble = content[:preamble_end] if preamble_end != -1 else content
    for engine, pattern in ENGINE_RULES:
        if re.search(pattern, preamble, re.IGNORECASE):
            return engine
    return "lualatex"


def split_component(component_text: str) -> tuple:
    """将组件内容拆分为导言区部分和正文部分
    
    Returns:
        (preamble_part, body_part)
    """
    lines = component_text.split("\n")
    preamble_lines = []
    body_lines = []
    in_body_context = False

    for line in lines:
        stripped = line.strip()
        # 导言区特征行
        is_preamble_line = (
            stripped.startswith(r"\usepackage")
            or stripped.startswith(r"\newcommand")
            or stripped.startswith(r"\renewcommand")
            or stripped.startswith(r"\providecommand")
            or stripped.startswith(r"\newenvironment")
            or stripped.startswith(r"\renewenvironment")
            or stripped.startswith(r"\newlength")
            or stripped.startswith(r"\setlength")
            or stripped.startswith(r"\newcolumntype")
            or stripped.startswith(r"\newfontfamily")
            or stripped.startswith(r"\setmainfont")
            or stripped.startswith(r"\setsansfont")
            or stripped.startswith(r"\setmonofont")
            or stripped.startswith(r"\ctexset")
            or stripped.startswith(r"\pagestyle")
            or stripped.startswith(r"\fancyhead")
            or stripped.startswith(r"\fancyfoot")
            or stripped.startswith(r"\fancyhf")
            # 设置类命令
            or stripped.startswith(r"\geometry")
            or stripped.startswith(r"\setCJKmainfont")
            or stripped.startswith(r"\setCJKsansfont")
            or stripped.startswith(r"\setCJKmonofont")
        )
        if is_preamble_line:
            preamble_lines.append(line)
        elif stripped.startswith("%"):
            # 注释行归入导言区（组件文件的注释通常是说明性的）
            preamble_lines.append(line)
        elif stripped == "":
            # 空行按照上下文归属
            if not body_lines:
                preamble_lines.append(line)
            else:
                body_lines.append(line)
        else:
            body_lines.append(line)
            in_body_context = True

    return "\n".join(preamble_lines), "\n".join(body_lines)


def convert_to_pdflatex(text: str) -> tuple:
    """将 LuaLaTeX 语法转换为 pdfLaTeX 兼容语法"""
    lines = text.split("\n")
    result = []
    changes = []
    for line in lines:
        applied = False
        for pattern, replacement, desc in PDFTEX_CONVERSION_RULES:
            m = re.match(pattern, line)
            if m:
                if replacement:
                    result.append(replacement)
                changes.append(f"  {desc}: {line.strip()[:50]}")
                applied = True
                break
        if not applied:
            result.append(line)
    return "\n".join(result), changes


def get_body_template(component_name: str) -> str:
    """获取组件的默认 body 模板"""
    name_only = Path(component_name).stem
    return COMPONENT_BODY_TEMPLATES.get(name_only, "")


def inject(input_path: str, component_name: str, position: str,
           position_value: str, engine: str, backup: bool = True) -> dict:
    """执行增量注入"""
    result = {
        "success": False,
        "input": input_path,
        "component": component_name,
        "position": position,
        "changes": [],
        "warnings": [],
        "backup_path": "",
    }

    # 1. 查找组件文件
    component_path = find_component_path(component_name)
    if not component_path:
        result["error"] = f"未找到组件: {component_name}"
        return result

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    with open(component_path, "r", encoding="utf-8") as f:
        component_text = f.read()

    # 2. 清理占位符
    component_text = re.sub(r"__\w+__", "", component_text)

    # 3. 拆分组件的导言区和正文
    preamble_part, body_part = split_component(component_text)

    # 4. 如果没有正文部分，尝试使用默认 body 模板
    if not body_part.strip():
        body_part = get_body_template(component_name)
        if body_part:
            result["changes"].append(f"使用默认 body 模板 (组件 '{component_name}' 无正文内容)")

    # 5. 检测引擎
    detected_engine = detect_engine(content)
    if engine == "auto" or not engine:
        engine = detected_engine
    result["engine"] = engine
    result["detected_engine"] = detected_engine

    # 6. 如果目标是 pdfLaTeX，转换语法
    converter_changes = []
    for part_name, part_text in [("导言区", preamble_part), ("正文", body_part)]:
        if part_text.strip():
            converted, changes = convert_to_pdflatex(part_text)
            if part_name == "导言区":
                preamble_part = converted
            else:
                body_part = converted
            converter_changes.extend(changes)

    if converter_changes:
        result["changes"].append("pdfLaTeX 兼容转换:")
        result["changes"].extend(converter_changes)

    # 7. 备份
    if backup:
        backup_path = input_path + ".bak"
        shutil.copy2(input_path, backup_path)
        result["backup_path"] = backup_path

    # 8. 定位插入点
    doc_begin = content.find(r"\begin{document}")
    doc_end = content.find(r"\end{document}")

    if position == "after":
        pattern = re.compile(position_value, re.MULTILINE)
        match = pattern.search(content)
        if not match:
            result["error"] = f"未找到匹配模式: {position_value}"
            return result
        insert_pos = match.end()
        body_insert = content[:insert_pos] + "\n" + body_part + content[insert_pos:]
        result["changes"].append(f"在 '{position_value}' 之后插入正文")
        result["position_detail"] = f"行 {content[:insert_pos].count(chr(10)) + 1}"

    elif position == "before":
        pattern = re.compile(position_value, re.MULTILINE)
        match = pattern.search(content)
        if not match:
            result["error"] = f"未找到匹配模式: {position_value}"
            return result
        insert_pos = match.start()
        body_insert = content[:insert_pos] + body_part + "\n" + content[insert_pos:]
        result["changes"].append(f"在 '{position_value}' 之前插入正文")
        result["position_detail"] = f"行 {content[:insert_pos].count(chr(10)) + 1}"

    elif position == "replace":
        pattern = re.compile(position_value, re.MULTILINE)
        match = pattern.search(content)
        if not match:
            result["error"] = f"未找到匹配模式: {position_value}"
            return result
        body_insert = content[:match.start()] + body_part + content[match.end():]
        result["changes"].append(f"替换 '{position_value}'")
        result["position_detail"] = f"行 {content[:match.start()].count(chr(10)) + 1}"

    elif position == "at-begin-document":
        if doc_begin == -1:
            result["error"] = "未找到 \\begin{document}"
            return result
        pos = doc_begin + len(r"\begin{document}")
        body_insert = content[:pos] + "\n" + body_part + content[pos:]
        result["changes"].append("在 \\begin{document} 之后插入正文")

    elif position == "at-end-document":
        if doc_end == -1:
            result["error"] = "未找到 \\end{document}"
            return result
        body_insert = content[:doc_end] + body_part + "\n" + content[doc_end:]
        result["changes"].append("在 \\end{document} 之前插入正文")

    else:
        result["error"] = f"未知插入位置: {position}"
        return result

    # 9. 将导言区内容追加到导言区
    if preamble_part.strip():
        if doc_begin != -1:
            # 在 \begin{document} 之前插入
            preamble_insert = preamble_part + "\n"
            body_insert = body_insert[:doc_begin] + preamble_insert + body_insert[doc_begin:]
            result["changes"].append(f"导言区追加 {len(preamble_part.splitlines())} 行")

    # 10. 写入
    tmp_path = input_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(body_insert)
    os.replace(tmp_path, input_path)

    result["success"] = True
    return result


def main():
    parser = argparse.ArgumentParser(
        description="向现有 .tex 增量插入组件（不破坏已有内容）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument("--input", "-i", default="", help="目标 .tex 文件路径")
    parser.add_argument("--component", "-c", default="", help="组件名或组件文件路径")
    parser.add_argument("--list-components", action="store_true", help="列出可用组件")

    pos = parser.add_argument_group("插入位置（五选一）")
    pos.add_argument("--after", default="", help="在匹配行后插入正文")
    pos.add_argument("--before", default="", help="在匹配行前插入正文")
    pos.add_argument("--replace", default="", help="替换匹配内容")
    pos.add_argument("--at-begin-document", action="store_true", help="插入到 \\begin{document} 之后")
    pos.add_argument("--at-end-document", action="store_true", help="插入到 \\end{document} 之前")

    parser.add_argument("--engine", default="auto", help="目标引擎: auto/lualatex/xelatex/pdflatex")
    parser.add_argument("--no-backup", action="store_true", help="不备份原文件")
    parser.add_argument("--workflow", default="", help="流程线 ID (line1/2/3/4)，启用步骤守卫")
    parser.add_argument("--lines", default="", help="处理范围 START-END，大文件局部处理")
    parser.add_argument("--encoding", default="utf-8", help="文件编码（默认 utf-8）")

    args = parser.parse_args()

    # ── 流程守卫 ──────────────────────────────────────
    if args.workflow:
        try:
            from workflow_state import guard
            allowed = guard(args.workflow, "inject")
            if not allowed:
                print("[inject] ⛔ 流程守卫拦截，请完成前置步骤后再试")
                sys.exit(1)
        except ImportError:
            pass  # workflow_state 不存在时降级

    # ── 行范围处理 ────────────────────────────────────
    line_start, line_end = 0, 0
    if args.lines:
        parts = args.lines.split("-")
        if len(parts) == 2:
            try:
                line_start = int(parts[0])
                line_end = int(parts[1])
                print(f"[inject] 行范围: {line_start}-{line_end}")
            except ValueError:
                pass

    if args.list_components:
        comps = list_components()
        print(f"可用组件 ({len(comps)} 个):")
        print(f"  {'名称':<20s} {'分类':<15s} {'描述'}")
        print(f"  {'-'*55}")
        for c in comps:
            print(f"  {c['name']:<20s} {c.get('type', ''):<15s} {c.get('description', '')}")
        return

    if not args.input or not args.component:
        parser.print_help()
        print("\n[ERROR] --input 和 --component 是必填参数")
        sys.exit(1)

    position = None
    position_value = ""
    if args.after:
        position, position_value = "after", args.after
    elif args.before:
        position, position_value = "before", args.before
    elif args.replace:
        position, position_value = "replace", args.replace
    elif args.at_begin_document:
        position, position_value = "at-begin-document", ""
    elif args.at_end_document:
        position, position_value = "at-end-document", ""
    else:
        print("[ERROR] 请指定插入位置")
        sys.exit(1)

    r = inject(args.input, args.component, position, position_value,
               args.engine, backup=not args.no_backup)

    if r["success"]:
        print(f"[OK] 注入完成: {r['input']}")
        if r.get("backup_path"):
            print(f"  备份: {r['backup_path']}")
        print(f"  引擎: {r['engine']} (检测: {r.get('detected_engine', 'auto')})")
        print(f"  位置: {r['position']} {r.get('position_detail', '')}")
        print(f"  组件: {args.component}")
        for c in r["changes"]:
            print(f"  {c}")
        for w in r.get("warnings", []):
            print(f"  ⚠ {w}")
    else:
        print(f"[ERROR] {r.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
