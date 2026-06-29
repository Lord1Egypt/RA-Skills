r"""
validate.py - LaTeX 编译验证器
使用 lualatex/xelatex 编译 .tex 文件，解析错误并给出修复建议
用法: python validate.py <file.tex> [--engine lualatex] [--fix]
"""
import os
import re
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path

# 常见错误模式及修复建议
ERROR_PATTERNS = [
    (r"Undefined control sequence", 
     "未定义的命令", 
     "检查是否遗漏 \\usepackage 或命令拼写错误"),
    (r"Missing \$ inserted",
     "缺少数学模式符号 $",
     "检查是否在数学公式中遗漏了 $...$ 包裹"),
    (r"Extra \}", 
     "多余的右花括号",
     "检查 {} 是否配对，常见原因是 \\begin{...} 和 \\end{...} 不匹配"),
    (r"Missing \}",
     "缺少右花括号",
     "检查 {} 是否配对"),
    (r"Environment .* undefined",
     "环境未定义",
     "检查 \\begin{...} 中的环境名是否已通过 \\usepackage 引入"),
    (r"File .* not found",
     "文件未找到",
     "检查 \\includegraphics 或 \\input 的文件路径是否正确"),
    (r"Undefined color",
     "未定义的颜色",
     "检查是否 \\usepackage{xcolor}，颜色名是否拼写正确"),
    (r"Font .* not found",
     "字体未找到",
     "检查系统中是否安装了该字体，或改用可用字体"),
    (r"Missing \\begin\{document\}",
     "缺少 \\begin{document}",
     "检查导言区是否正确结束"),
    (r"\\begin\{document\} ended by \\end\{.*\}",
     "环境不匹配",
     "检查 \\begin{...} 和 \\end{...} 是否配对"),
    (r"Package .* Error",
     "宏包错误",
     "查看具体宏包错误信息，通常是参数或用法错误"),
    (r"Improper \\spacefactor",
     "空格因子错误（中文常见）",
     "检查中文排版设置，确保 ctex 宏包正确配置"),
    (r"Unicode character .* not set up for use with LaTeX",
     "Unicode 字符未定义",
     "使用 \\usepackage{fontspec} + \\setmainfont 或 \\usepackage[UTF8]{ctex}"),
    (r"Missing package .*",
     "缺少宏包",
     "在导言区添加 \\usepackage{包名}"),
]

WARNING_PATTERNS = [
    (r"Reference .* undefined",
     "引用未定义",
     "检查 \\label 和 \\ref 是否配对，需要编译两次"),
    (r"Citation .* undefined",
     "引用未定义（bibtex）",
     "检查 .bib 文件，运行 bibtex/biber"),
    (r"Float too large",
     "浮动体过大",
     "调整图片/表格大小，或使用 [H] 选项（需 \\usepackage{float}）"),
    (r"Overfull \\hbox",
     "行溢出（hbox 过宽）",
     "调整换行、字体大小或页面边距"),
    (r"Underfull \\vbox",
     "垂直盒子填充不足",
     "通常是段落结尾警告，可接受或调整 \\parskip"),
]


def _probe_path(path: str) -> str:
    """检查路径是否存在（兼容 Windows 无后缀和有 .exe 的情况）"""
    if os.path.exists(path):
        return path
    if not path.endswith(".exe"):
        pext = path + ".exe"
        if os.path.exists(pext):
            return pext
    return ""

def _registry_miktex_root() -> str:
    """从 Windows 注册表读取 MiKTeX 安装根目录"""
    try:
        import winreg
        for hive, flag in [(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY),
                           (winreg.HKEY_CURRENT_USER, winreg.KEY_WOW64_64KEY),
                           (winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)]:
            try:
                key = winreg.OpenKey(hive, r"SOFTWARE\MiKTeX\MiKTeX", 0, winreg.KEY_READ | flag)
                try:
                    val, _ = winreg.QueryValueEx(key, "Install Root")
                    return val.strip()
                finally:
                    winreg.CloseKey(key)
            except WindowsError:
                continue
    except Exception:
        pass
    return ""

def find_engine(engine: str) -> str:
    """查找 LaTeX 引擎路径，扫描常见安装位置 + 注册表 + PATH"""

    # 1. 注册表优先（用户自定义安装路径）
    root = _registry_miktex_root()
    if root:
        for sub in [r"miktex\bin\x64", r"miktex\bin"]:
            p = os.path.join(root, sub, engine)
            r = _probe_path(p)
            if r:
                return r

    # 2. 常见路径扫描
    candidates = [
        # MiKTeX 系统级安装
        os.path.expandvars(r"%ProgramFiles%\MiKTeX\miktex\bin\x64\{e}"),
        os.path.expandvars(r"%ProgramFiles%\MiKTeX\miktex\bin\{e}"),
        os.path.expandvars(r"%ProgramFiles(x86)%\MiKTeX\miktex\bin\{e}"),
        # MiKTeX 用户级安装
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\{e}"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\MiKTeX\miktex\bin\x64\{e}"),
        # Git Bash 映射路径
        r"/c/Program Files/MiKTeX/miktex/bin/x64/{e}",
        r"/c/Program Files (x86)/MiKTeX/miktex/bin/{e}",
        # TeX Live — 扫描最近 5 个版本年份
    ]
    from datetime import datetime
    for year in range(datetime.now().year, datetime.now().year - 5, -1):
        candidates.append(os.path.expandvars(
            r"%ProgramFiles%\TeX Live\{y}\bin\win32\{e}".format(y=year, e="{e}")))
        candidates.append(r"/c/texlive/{y}/bin/win32/{e}".format(y=year, e="{e}"))

    # 按候选路径查找
    for tmpl in candidates:
        p = tmpl.format(e=engine)
        r = _probe_path(p)
        if r:
            return r

    # 3. Unix 路径（macOS / Linux 兜底）
    for unix_p in [f"/usr/bin/{engine}", f"/usr/local/bin/{engine}",
                   f"/opt/texlive/*/bin/*/{engine}"]:
        r = _probe_path(unix_p)
        if r:
            return r

    # 4. PATH / where 命令
    try:
        if sys.platform == "win32":
            result = subprocess.run(["where", engine], capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(["which", engine], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            path = result.stdout.strip().split("\n")[0].strip()
            if path:
                return path
    except Exception:
        pass

    return ""

def compile_tex(tex_path: str, engine: str = "lualatex", timeout: int = 120) -> dict:
    """编译 .tex 文件，返回编译结果"""
    result = {
        "success": False,
        "engine": engine,
        "tex_path": tex_path,
        "pdf_path": "",
        "stdout": "",
        "stderr": "",
        "returncode": -1,
        "log_file": "",
        "errors": [],
        "warnings": [],
        "suggestions": []
    }
    
    engine_path = find_engine(engine)
    if not engine_path:
        result["errors"].append(f"找不到 {engine} 可执行文件，请检查 LaTeX 安装")
        result["suggestions"].extend([
            f"安装 MiKTeX（推荐）：https://miktex.org/download",
            f"  CTAN 镜像：https://mirrors.tuna.tsinghua.edu.cn/ctan/systems/texlive/tlnet/",
            f"  ️ 阿里云镜像：https://mirrors.aliyun.com/CTAN/systems/texlive/tlnet/",
            f"安装 TeX Live：https://tug.org/texlive/",
            f"或将 {engine} 所在目录加入系统 PATH 环境变量",
        ])
        return result
    
    work_dir = str(Path(tex_path).parent)
    tex_filename = Path(tex_path).name
    
    try:
        proc = subprocess.run(
            [engine_path, "-interaction=nonstopmode", "-halt-on-error", tex_filename],
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
        result["returncode"] = proc.returncode
        
        # 检查 PDF 是否生成
        pdf_path = Path(tex_path).with_suffix(".pdf")
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            result["success"] = True
            result["pdf_path"] = str(pdf_path)
        
        # 读取 .log 文件
        log_path = Path(tex_path).with_suffix(".log")
        if log_path.exists():
            result["log_file"] = str(log_path)
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                log_content = f.read()
            result["log_content"] = log_content
        
    except subprocess.TimeoutExpired:
        result["errors"].append(f"编译超时（>{timeout}秒），可能是文档过大或进入死循环")
    except Exception as e:
        result["errors"].append(f"编译异常: {type(e).__name__}: {e}")
    
    return result

def parse_errors_and_warnings(result: dict) -> dict:
    """解析编译输出中的错误和警告"""
    all_text = result.get("stdout", "") + "\n" + result.get("stderr", "")
    if "log_content" in result and result["log_content"]:
        all_text += "\n" + result["log_content"]
    
    errors = []
    warnings = []
    suggestions = []
    
    # 解析错误
    for pattern, desc, suggestion in ERROR_PATTERNS:
        for m in re.finditer(pattern, all_text, re.IGNORECASE):
            context = extract_context(all_text, m.start())
            errors.append({
                "pattern": pattern,
                "desc": desc,
                "context": context,
                "line": extract_line_number(context)
            })
            if suggestion not in suggestions:
                suggestions.append(suggestion)
    
    # 解析警告
    for pattern, desc, suggestion in WARNING_PATTERNS:
        for m in re.finditer(pattern, all_text, re.IGNORECASE):
            context = extract_context(all_text, m.start())
            warnings.append({
                "pattern": pattern,
                "desc": desc,
                "context": context,
                "line": extract_line_number(context)
            })
            if suggestion not in suggestions:
                suggestions.append(suggestion)
    
    # 如果 stdout 中有 ! 开头的行，也视为错误
    for line in all_text.splitlines():
        if line.strip().startswith("!"):
            if not any(e["context"] == line.strip() for e in errors):
                errors.append({
                    "pattern": "general",
                    "desc": "LaTeX 错误",
                    "context": line.strip(),
                    "line": extract_line_number(line)
                })
    
    result["errors"] = errors
    result["warnings"] = warnings
    result["suggestions"] = list(set(suggestions))
    
    return result

def extract_context(text: str, pos: int, context_lines: int = 3) -> str:
    """提取错误周围的上下文"""
    lines = text[:pos].splitlines()
    if not lines:
        return ""
    current_line_num = len(lines)
    
    all_lines = text.splitlines()
    start = max(0, current_line_num - context_lines)
    end = min(len(all_lines), current_line_num + context_lines)
    
    context = []
    for i in range(start, end):
        prefix = ">> " if i == current_line_num - 1 else "   "
        context.append(f"{prefix}{all_lines[i]}")
    
    return "\n".join(context)

def extract_line_number(context: str) -> int:
    """尝试从错误上下文中提取行号"""
    # LaTeX 错误格式: "l.xxx" 或 "line xxx"
    m = re.search(r"l\.(\d+)", context)
    if m:
        return int(m.group(1))
    m = re.search(r"line\s+(\d+)", context, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return -1

def attempt_auto_fix(tex_path: str, errors: list) -> dict:
    """尝试自动修复常见错误"""
    fixes_applied = []
    
    with open(tex_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    modified = False
    new_content = content
    
    for err in errors:
        desc = err.get("desc", "")
        
        # 修复1: 未定义颜色 -> 添加 \usepackage{xcolor}
        if "未定义的颜色" in desc and r"\usepackage{xcolor}" not in new_content:
            # 在 \documentclass 后插入
            new_content = re.sub(
                r"(\\documentclass.*?\n)",
                r"\1\\usepackage{xcolor}\n",
                new_content
            )
            fixes_applied.append("添加 \\usepackage{xcolor}")
            modified = True
        
        # 修复2: 未定义命令（常见 \mathbb 等） -> 添加 \usepackage{amssymb}
        if "未定义的命令" in desc:
            if "mathbb" in new_content and r"\usepackage{amssymb}" not in new_content:
                new_content = re.sub(
                    r"(\\documentclass.*?\n)",
                    r"\1\\usepackage{amssymb}\n",
                    new_content
                )
                fixes_applied.append("添加 \\usepackage{amssymb}")
                modified = True
        
        # 修复3: 环境未定义（常见 figure/table）-> 确保相关宏包已加载
        if "环境未定义" in desc:
            env_match = re.search(r"Environment\s+(\w+)\s+undefined", new_content)
            if env_match:
                env = env_match.group(1)
                if env in ["figure", "table"] and r"\usepackage{float}" not in new_content:
                    new_content = re.sub(
                        r"(\\documentclass.*?\n)",
                        r"\1\\usepackage{float}\n",
                        new_content
                    )
                    fixes_applied.append(f"添加 \\usepackage{{float}} (修复 {env} 环境)")
                    modified = True
    
    if modified:
        backup_path = tex_path + ".bak"
        shutil.copy2(tex_path, backup_path)
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return {"success": True, "fixes": fixes_applied, "backup": backup_path}
    
    return {"success": False, "fixes": [], "backup": None}

def print_report(result: dict):
    """打印验证报告"""
    print("=" * 60)
    print(f"  LaTeX 编译验证报告")
    print("=" * 60)
    print(f"  文件: {result['tex_path']}")
    print(f"  引擎: {result['engine']}")
    print(f"  状态: {'✓ 成功' if result['success'] else '✗ 失败'}")
    if result["pdf_path"]:
        print(f"  PDF:  {result['pdf_path']}")
    print("-" * 60)
    
    if result["errors"]:
        print(f"\n  ️ 错误 ({len(result['errors'])} 条):")
        for i, err in enumerate(result["errors"][:10], 1):
            print(f"  [{i}] {err['desc']}")
            if err.get("line", -1) > 0:
                print(f"       行号: {err['line']}")
            if err.get("context"):
                print(f"       上下文:\n{err['context']}")
        if len(result["errors"]) > 10:
            print(f"  ... 还有 {len(result['errors']) - 10} 条错误未显示")
    
    if result["warnings"]:
        print(f"\n  ⚠️  警告 ({len(result['warnings'])} 条):")
        for i, w in enumerate(result["warnings"][:5], 1):
            print(f"  [{i}] {w['desc']}")
        if len(result["warnings"]) > 5:
            print(f"  ... 还有 {len(result['warnings']) - 5} 条警告未显示")
    
    if result["suggestions"]:
        print(f"\n  💡 修复建议:")
        for i, s in enumerate(result["suggestions"], 1):
            print(f"  [{i}] {s}")
    
    print("\n" + "=" * 60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="LaTeX 编译验证器")
    parser.add_argument("tex_file", help="要验证的 .tex 文件路径")
    parser.add_argument("--engine", default="lualatex", help="编译引擎（lualatex/xelatex/pdflatex）")
    parser.add_argument("--fix", action="store_true", help="尝试自动修复常见错误")
    parser.add_argument("--output-json", default="", help="将结果输出为 JSON 文件")
    parser.add_argument("--keep-logs", action="store_true", help="保留编译日志文件")
    parser.add_argument("--workflow", default="", help="流程线 ID，启用步骤守卫")
    parser.add_argument("--lines", default="", help="处理范围 START-END")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.tex_file):
        print(f"错误: 文件不存在 - {args.tex_file}")
        sys.exit(1)
    
    print(f"[validate] 开始编译验证: {args.tex_file}")
    print(f"[validate] 使用引擎: {args.engine}")
    
    result = compile_tex(args.tex_file, args.engine)
    result = parse_errors_and_warnings(result)
    
    if args.fix and result["errors"]:
        print("[validate] 尝试自动修复...")
        fix_result = attempt_auto_fix(args.tex_file, result["errors"])
        if fix_result["success"]:
            print(f"[validate] 已应用修复: {', '.join(fix_result['fixes'])}")
            print(f"[validate] 备份文件: {fix_result['backup']}")
            print("[validate] 重新编译验证...")
            result = compile_tex(args.tex_file, args.engine)
            result = parse_errors_and_warnings(result)
        else:
            print("[validate] 无可用自动修复")
    
    print_report(result)
    
    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[validate] 结果已保存到: {args.output_json}")
    
    if not args.keep_logs:
        # 清理辅助文件
        for ext in [".log", ".aux", ".out", ".toc", ".lof", ".lot", ".bbl", ".blg"]:
            aux_file = Path(args.tex_file).with_suffix(ext)
            if aux_file.exists():
                try:
                    aux_file.unlink()
                except:
                    pass
    
    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
