#!/usr/bin/env python3
# compose.py - LaTeX modular composer
import json, os, re, subprocess, sys, argparse
from pathlib import Path
from typing import List, Dict, Any

PACKAGE_ORDER = [
    "ctex", "fontspec", "xunicode",
    "geometry", "fancyhdr", "lastpage",
    "xcolor", "graphicx", "eso-pic",
    "pgfplots", "tikz", "siunitx",
    "enumitem", "multicol", "float",
    "tabularx", "booktabs", "multirow",
    "pifont", "amssymb",
    "etoolbox", "newunicodechar",
    "pdflscape", "tocloft",
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

    # 0. 直接传入完整路径
    if os.path.isfile(engine):
        return engine

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
        os.path.expandvars(r"%ProgramFiles%\MiKTeX\miktex\bin\x64\{e}"),
        os.path.expandvars(r"%ProgramFiles%\MiKTeX\miktex\bin\{e}"),
        os.path.expandvars(r"%ProgramFiles(x86)%\MiKTeX\miktex\bin\{e}"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\{e}"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\MiKTeX\miktex\bin\x64\{e}"),
        r"/c/Program Files/MiKTeX/miktex/bin/x64/{e}",
        r"/c/Program Files (x86)/MiKTeX/miktex/bin/{e}",
    ]
    from datetime import datetime
    for year in range(datetime.now().year, datetime.now().year - 5, -1):
        candidates.append(os.path.expandvars(
            r"%ProgramFiles%\TeX Live\{y}\bin\win32\{e}".format(y=year, e="{e}")))
        candidates.append(r"/c/texlive/{y}/bin/win32/{e}".format(y=year, e="{e}"))

    for tmpl in candidates:
        p = tmpl.format(e=engine)
        r = _probe_path(p)
        if r:
            return r

    # 3. Unix 兜底
    for unix_p in [f"/usr/bin/{engine}", f"/usr/local/bin/{engine}"]:
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

def resolve_base_dir(manifest_path: str) -> str:
    """manifest.json 所在目录即为 base_dir。"""
    return os.path.dirname(os.path.abspath(manifest_path))

def read_tex(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def dedupe_pkg_lines(pkg_lines: List[str]) -> List[str]:
    """对 usepackage 行去重并按 PACKAGE_ORDER 排序。"""
    seen = set()
    unique = []
    for ln in pkg_lines:
        s = ln.strip()
        # 规范化：去除所有内联注释和多余空格，提高匹配率
        normalized = re.sub(r"\s+", " ", s)
        if normalized not in seen:
            seen.add(normalized)
            unique.append(s)  # 保留原始行（仅去重，不改内容）
    order_map = {k: i for i, k in enumerate(PACKAGE_ORDER)}
    def _key(ln):
        m = re.search(r"\\usepackage(?:\[.*?\])?{(.*?)}", ln)
        if not m:
            return (999, ln)
        for n in [x.strip() for x in m.group(1).split(",")]:
            if n in order_map:
                return (order_map[n], ln)
        return (999, ln)
    unique.sort(key=_key)
    return unique

def build_document(manifest: Dict, base_dir: str, author: str = "", title: str = "") -> str:
    """根据 manifest 组装完整 LaTeX 文档，保证正确顺序。
    
    Args:
        manifest: 组件清单
        base_dir: 组件文件所在目录
        author: 作者名，替换 body 中的 __AUTHOR__
        title: 标题，替换 body 中的 __TITLE__
    """
    doc_class = None
    pkg_lines = []       # 所有 \usepackage 行
    preamble_cmds = []   # 其他 preamble 命令块
    body_content = ""

    for comp in manifest.get("components", []):
        rel = comp.get("path", "")
        fpath = os.path.join(base_dir, rel)
        if not os.path.isfile(fpath):
            print(f"[WARN] 组件不存在: {fpath}")
            continue
        content = read_tex(fpath).strip()
        typ = comp.get("type", "")
        name = comp.get("name", "")

        # 1. documentclass：从 class-settings.txt 里提取
        if name == "class-settings":
            for ln in content.splitlines():
                if ln.strip().startswith("\\documentclass"):
                    doc_class = ln.strip()
                    break
            continue

        # 2. usepackage 行（只收集 usepackage 行，非专有组件不跳过其余内容）
        has_pkg = any(
            l.strip().startswith("\\usepackage")
            for l in content.splitlines()
        )
        is_pkg_comp = (typ == "packages" or name == "packages")
        if is_pkg_comp or has_pkg:
            for ln in content.splitlines():
                s = ln.strip()
                if s.startswith("\\usepackage"):
                    pkg_lines.append(s)
            if is_pkg_comp:
                continue  # 纯宏包组件：提取后跳过
            # 非纯宏包组件（如 environments/*.tex 中混有 usepackage）：
            # 去掉 usepackage 行后，剩余内容继续进 preamble_cmds
            non_pkg_lines = [
                l for l in content.splitlines()
                if not l.strip().startswith("\\usepackage")
            ]
            if non_pkg_lines:
                preamble_cmds.append("\n".join(non_pkg_lines))
            continue

        # 3. body
        if typ == "body" or name == "body":
            body_content = content
            continue

        # 4. 其余 preamble（字体设置、命令、环境、页眉页脚等）
        preamble_cmds.append(content)

    # ── 替换动态占位符 ────────────────────────────────
    if body_content:
        body_content = body_content.replace("__AUTHOR__", author or "作者")
        body_content = body_content.replace("__TITLE__", title or "文档标题")

    # ── 组装文档 ──────────────────────────────────────
    doc_lines = []

    # (1) documentclass
    if doc_class:
        doc_lines.append(doc_class)
    else:
        doc_lines.append("\\documentclass[a4paper,12pt]{article}")

    # (2) usepackage 行 — 去重 + 排序
    unique_pkg = dedupe_pkg_lines(pkg_lines)
    doc_lines.extend(unique_pkg)

    # (3) 其他 preamble 内容（字体、命令、环境、页眉页脚等）
    for blk in preamble_cmds:
        doc_lines.append(blk)

    # (4) begin{document}
    doc_lines.append("\\begin{document}")

    # (5) body
    if body_content:
        doc_lines.append(body_content)

    # (6) end{document}
    doc_lines.append("\\end{document}")

    return "\n".join(l for l in doc_lines if l.strip()) + "\n"

def find_manifest(base_dir: str) -> str:
    for c in [os.path.join(base_dir, "scripts", "components", "manifest.json"),
               os.path.join(base_dir, "components", "manifest.json"),
               os.path.join(base_dir, "manifest.json")]:
        if os.path.isfile(c):
            return c
    return ""

def main():
    parser = argparse.ArgumentParser(description="LaTeX modular composer")
    parser.add_argument("--manifest", help="manifest.json path")
    parser.add_argument("--output", "-o", default="output.tex", help="output .tex path")
    parser.add_argument("--author", default="", help="作者名，替换 body 中的 __AUTHOR__ 占位符")
    parser.add_argument("--title", default="", help="文档标题，替换 body 中的 __TITLE__ 占位符")
    parser.add_argument("--validate", action="store_true", help="validate with lualatex")
    parser.add_argument("--engine", default="lualatex", help="LaTeX 引擎（lualatex/xelatex）")
    args = parser.parse_args()

    manifest_path = args.manifest or find_manifest(os.getcwd())
    if not manifest_path or not os.path.isfile(manifest_path):
        print("[ERROR] manifest.json not found")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    if isinstance(manifest, list):
        manifest = {"components": manifest, "version": "1.0.0"}
    # dict-format 兼容转换（旧版兼容）
    if isinstance(manifest.get("components"), dict):
        old = manifest["components"]
        new_list = []
        for key, val in old.items():
            typ, name = key.split("/", 1) if "/" in key else ("unknown", key)
            new_list.append({
                "type": typ,
                "name": name,
                "path": val.get("file", f"{typ}/{name}.txt"),
                "category": val.get("category", ""),
                "description": val.get("desc", "")
            })
        manifest["components"] = new_list

    base_dir = resolve_base_dir(manifest_path)
    document = build_document(manifest, base_dir, author=args.author, title=args.title)

    out_path = args.output
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(document)

    print(f"[OK] Generated: {out_path}")
    print(f"[INFO] Components: {len(manifest.get('components', []))}")

    if args.validate:
        engine_path = find_engine(args.engine)
        if not engine_path:
            print(f"[ERROR] 找不到 {args.engine} 可执行文件，请检查 LaTeX 安装")
            print(f"  安装 MiKTeX（推荐）：https://miktex.org/download")
            print(f"    CTAN 镜像：https://mirrors.tuna.tsinghua.edu.cn/ctan/systems/texlive/tlnet/")
            print(f"    阿里云镜像：https://mirrors.aliyun.com/CTAN/systems/texlive/tlnet/")
            print(f"  安装 TeX Live：https://tug.org/texlive/")
            print(f"  或将 {args.engine} 所在目录加入系统 PATH 环境变量")
            sys.exit(1)
        result = subprocess.run(
            [engine_path, "--interaction=nonstopmode", out_path],
            capture_output=True, text=True
        )
        log_path = out_path.replace(".tex", ".log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            f.write(result.stderr)
        if result.returncode == 0:
            print(f"[OK] {args.engine} passed")
        else:
            print(f"[ERROR] {args.engine} failed, see: {log_path}")

if __name__ == "__main__":
    main()
