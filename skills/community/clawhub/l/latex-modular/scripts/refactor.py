r"""
refactor.py - LaTeX 代码重构引擎
将原始 LaTeX 代码重构进模块化体系，保留原文语义，按模块拆分存储
用法: python refactor.py <source.tex> [--output-dir components/] [--output-doc output.tex]
"""
import os
import re
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# 模块分类规则（按导言区顺序）
MODULE_RULES = [
    # (组件类型, 组件名, 匹配模式, 描述, 依赖宏包)
    ("preamble", "class-settings", 
     r"\\documentclass", 
     "文档类声明", []),    
    ("preamble", "packages", 
     r"\\usepackage|\\RequirePackage", 
     "宏包引入", []),    
    ("preamble", "colors", 
     r"\\usepackage{xcolor}|\\definecolor|\\colorlet|\\newcommand{\\color", 
     "颜色定义", ["xcolor"]),    
    ("preamble", "fonts", 
     r"\\setmainfont|\\setCJKmainfont|\\newfontfamily|\\newCJKfontfamily|\\setmonofont|\\ctexset.*fontset", 
     "字体设置", ["fontspec", "ctex"]),    
    ("preamble", "geometry", 
     r"\\usepackage{geometry}|\\geometry", 
     "页面设置", ["geometry"]),    
    ("preamble", "pgfplots", 
     r"\\pgfplotsset|\\usetikzlibrary|\\usepackage{pgfplots}|\\usepackage{tikz}|\\usepackage{siunitx}", 
     "作图支持", ["pgfplots", "tikz", "siunitx"]),    
    ("environments", "mylist", 
     r"\\NewDocumentEnvironment{mylist}", 
     "自定义列表环境", ["enumitem", "newunicodechar"]),    
    ("environments", "mycolumns", 
     r"\\newenvironment{mycolumns}", 
     "分栏环境", ["multicol"]),    
    ("environments", "abstract-env", 
     r"\\renewenvironment{abstract}", 
     "摘要环境", []),    
    ("commands", "title-commands", 
     r"\\newcommand{\\timu}|\\newcommand{\\yijitimu}|\\newcommand{\\erjitimu}|\\newcommand{\\sanjitimu}", 
     "标题命令", []),    
    ("commands", "font-commands", 
     r"\\newCJKfontfamily|\\newfontfamily|\\newcommand{\\zz}|\\newcommand{\\dw}|\\newcommand{\\seeref}", 
     "字体/引用命令", ["fontspec", "ctex"]),    
    ("commands", "background", 
     r"\\newcommand{\\coverbackground}|\\AddToShipoutPicture", 
     "背景命令", ["eso-pic"]),    
    ("styles", "section-style", 
     r"\\ctexset", 
     "章节样式（ctexset）", ["ctex"]),    
    ("styles", "toc-style", 
     r"\\renewcommand{\\cft.*}|\\usepackage{tocloft}|\\contentsname", 
     "目录样式", ["tocloft"]),    
    ("styles", "header-footer", 
     r"\\pagestyle{fancy}|\\fancyhf|\\fancyhead|\\fancyfoot|\\usepackage{fancyhdr}|\\usepackage{lastpage}", 
     "页眉页脚", ["fancyhdr", "lastpage"]),    
    ("styles", "list-style", 
     r"\\newlength{\\titleindent}|\\newcounter{listlevel}|\\pretocmd", 
     "列表样式", ["enumitem"]),    
    ("tables", "table-style", 
     r"\\newlength{\\tablegap}|\\usepackage{booktabs}|\\usepackage{tabularx}|\\usepackage{multirow}|\\usepackage{longtable}|\\usepackage{array}|\\usepackage{makecell}|\\usepackage{float}|\\usepackage{subcaption}", 
     "表格样式", ["tabularx", "booktabs", "multirow", "longtable", "array", "makecell", "float", "subcaption"]),    
    ("graphics", "figure-insert", 
     r"\\includegraphics", 
     "图片插入", ["graphicx"]),    
    ("graphics", "background-fig", 
     r"\\coverbackground|\\AddToShipoutPicture", 
     "背景图片", ["eso-pic"]),
]

def read_source(source_path: str) -> str:
    r"""读取源 LaTeX 文件"""
    with open(source_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def split_document(content: str) -> dict:
    r"""将文档分割为导言区和正文区"""
    # 查找 \begin{document}
    m_begin = re.search(r"\\begin\s*\{\s*document\s*\}", content)
    if not m_begin:
        return {"error": r"未找到 \begin{document}"}
    
    preamble = content[:m_begin.start()].strip()
    
    # 查找 \end{document}
    m_end = re.search(r"\\end\s*\{\s*document\s*\}", content)
    if m_end:
        body = content[m_begin.end():m_end.start()].strip()
        tail = content[m_end.end():].strip()
    else:
        body = content[m_begin.end():].strip()
        tail = ""
    
    return {
        "preamble": preamble,
        "body": body,
        "tail": tail
    }

def classify_preamble(preamble: str) -> dict:
    r"""将导言区内容分类到不同模块"""
    modules = {}  # key: "category/name"
    preamble_lines = preamble.splitlines()
    
    # 按行扫描，将内容分配到对应模块
    current_module = None
    current_lines = []
    i = 0
    
    while i < len(preamble_lines):
        line = preamble_lines[i]
        matched = False
        
        for cat, name, pattern, desc, deps in MODULE_RULES:
            if re.search(pattern, line):
                # 保存上一个模块
                if current_module and current_lines:
                    modules[current_module] = {
                        "content": "\n".join(current_lines),
                        "desc": "",
                        "deps": []
                    }
                    # 查找描述
                    for _, _, _, d, _ in MODULE_RULES:
                        if current_module.endswith(d.split()[-1] if d else ""):
                            break                
                current_module = f"{cat}/{name}"
                current_lines = [line]
                matched = True
                break
        
        if not matched:
            if current_module:
                current_lines.append(line)
            # 如果不在任何模块中，忽略（或存入 __header__）        
        
        i += 1
    
    # 保存最后一个模块
    if current_module and current_lines:
        modules[current_module] = {
            "content": "\n".join(current_lines),
            "desc": "",
            "deps": []
        }
    
    # 填充描述
    for key in modules:
        cat = key.split("/")[0]
        name = key.split("/")[1]
        for _, n, _, desc, deps in MODULE_RULES:
            if n == name:
                modules[key]["desc"] = desc
                modules[key]["deps"] = deps
                break
    
    return modules

def save_modules(modules: dict, output_dir: str) -> dict:
    r"""将模块保存到文件，返回 manifest（list 格式，与 compose.py 兼容）"""
    output = Path(output_dir)
    manifest = {
        "version": "1.0.0",
        "components": [],
        "body_file": "body.txt"
    }
    
    for key, data in modules.items():
        cat = key.split("/")[0]
        name = key.split("/")[1]
        
        cat_dir = output / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{name}.txt"
        filepath = cat_dir / filename
        rel_path = f"{cat}/{filename}"
        
        content = data["content"].strip()
        if not content:
            continue
        
        # 写入组件文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        
        manifest["components"].append({
            "type": cat,
            "name": name,
            "path": rel_path,
            "category": data.get("cat", ""),
            "description": data["desc"]
        })
    
    # 保存 manifest
    manifest_path = output / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    return manifest

def _find_comp(components, type_name, name):
    """在 list-format components 中按 type+name 查找"""
    for c in components:
        if c.get("type") == type_name and c.get("name") == name:
            return c
    return None

def generate_modular_document(manifest: dict, body: str, output_doc: str, comps_dir: str = "components"):
    r"""生成模块化主文档（使用 \input 引入各组件）
    自动计算组件目录相对于输出文档的路径。
    comps_dir: 组件目录（相对或绝对）
    """
    lines = []
    comps = manifest.get("components", [])

    # 计算组件目录相对输出文档的路径
    out_path = Path(output_doc).resolve().parent
    comps_abs = Path(comps_dir).resolve()
    try:
        rel_to_comps = os.path.relpath(comps_abs, out_path).replace("\\", "/")
    except ValueError:
        rel_to_comps = str(comps_abs).replace("\\", "/")
    if not rel_to_comps.endswith("/"):
        rel_to_comps += "/"
    
    # 1. 文档类
    class_comp = _find_comp(comps, "preamble", "class-settings")
    if class_comp:
        lines.append(r"% --- 文档类设置 ---")
        lines.append(rf"\input{{{rel_to_comps}{class_comp['path']}}}")
        lines.append("")
    
    # 2. 宏包
    pkg_comp = _find_comp(comps, "preamble", "packages")
    if pkg_comp:
        lines.append(r"% --- 宏包引入 ---")
        lines.append(rf"\input{{{rel_to_comps}{pkg_comp['path']}}}")
        lines.append("")
    
    # 3. 其他导言区组件（按分类顺序）
    category_order = ["preamble", "environments", "commands", "styles", "tables", "graphics"]
    for cat in category_order:
        for comp in comps:
            if comp.get("type") != cat:
                continue
            if comp["name"] in ("class-settings", "packages"):
                continue  # 已处理
            lines.append(rf"% --- {comp.get('description', comp['name'])} ---")
            lines.append(rf"\input{{{rel_to_comps}{comp['path']}}}")
            lines.append("")
    
    # 4. 文档开始
    lines.append(r"\begin{document}")
    lines.append("")
    
    # 5. 正文
    if body.strip():
        lines.append(body.strip())
        lines.append("")
    
    # 6. 文档结束  
    lines.append(r"\end{document}")
    
    # 写入文件
    output_path = Path(output_doc)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    
    return str(output_path)

def validate_refactored(output_doc: str, engine: str = "lualatex") -> dict:
    r"""验证重构后的文档能否编译"""
    # 调用 validate.py 的逻辑
    validate_script = Path(__file__).parent / "validate.py"
    if not validate_script.exists():
        return {"success": False, "error": "validate.py 不存在，跳过编译验证"}
    
    import subprocess
    try:
        result = subprocess.run(
            ["python", str(validate_script), output_doc, "--engine", engine],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(Path(__file__).parent)
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    import argparse
    parser = argparse.ArgumentParser(description="LaTeX 代码重构引擎")
    parser.add_argument("source", help="原始 LaTeX 文件路径")
    parser.add_argument("--output-dir", default="scripts/components", help="组件输出目录")
    parser.add_argument("--output-doc", default="", help="输出的模块化主文档路径")
    parser.add_argument("--engine", default="lualatex", help="验证用编译引擎")
    parser.add_argument("--no-validate", action="store_true", help="跳过编译验证")
    parser.add_argument("--keep-body", action="store_true", help="保留 body.tex 文件")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"错误: 文件不存在 - {args.source}")
        sys.exit(1)
    
    print(f"[refactor] 读取源文件: {args.source}")
    content = read_source(args.source)
    
    print(f"[refactor] 分割文档...")
    doc = split_document(content)
    if "error" in doc:
        print(f"错误: {doc['error']}")
        sys.exit(1)
    
    print(f"[refactor] 导言区: {len(doc['preamble'].splitlines())} 行")
    print(f"[refactor] 正文区: {len(doc['body'].splitlines())} 行")
    
    print(f"[refactor] 分类组件...")
    modules = classify_preamble(doc["preamble"])
    print(f"[refactor] 分类到 {len(modules)} 个组件")
    
    print(f"[refactor] 保存组件到: {args.output_dir}")
    manifest = save_modules(modules, args.output_dir)
    print(f"[refactor] 已保存 {len(manifest['components'])} 个组件")
    
    # 保存正文
    if args.keep_body or not args.output_doc:
        body_path = Path(args.output_dir) / "body.txt"
        with open(body_path, "w", encoding="utf-8") as f:
            f.write(doc["body"] + "\n")
        print(f"[refactor] 正文已保存: {body_path}")
        manifest["body_file"] = "body.txt"
        # 更新 manifest
        manifest_path = Path(args.output_dir) / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    # 生成模块化主文档
    if args.output_doc:
        print(f"[refactor] 生成模块化主文档: {args.output_doc}")
        output_path = generate_modular_document(manifest, doc["body"], args.output_doc, args.output_dir)
        print(f"[refactor] 已生成: {output_path}")
        
        # 编译验证
        if not args.no_validate:
            print(f"[refactor] 编译验证 ({args.engine})...")
            val_result = validate_refactored(args.output_doc, args.engine)
            if val_result.get("success"):
                print(f"[refactor] ✓ 编译成功")
            else:
                print(f"[refactor] ✗ 编译失败:")
                print(val_result.get("stdout", "")[:500])
                print(val_result.get("stderr", "")[:500])
    
    print(f"[refactor] 完成！")
    print(f"[refactor] 组件清单: {Path(args.output_dir) / 'manifest.json'}")

if __name__ == "__main__":
    main()
