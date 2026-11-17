#!/usr/bin/env python3
"""check_env.py — 环境自检：输出能力就绪矩阵。

退出码：0 = 核心能力全部就绪；1 = 核心依赖缺失（增强项缺失不影响退出码）。
用法：python3 scripts/check_env.py
"""
import importlib, shutil, subprocess, sys

CORE_PY = ["fitz", "pdfplumber", "pikepdf", "pypdf", "pandas", "openpyxl"]
OPT_PY = {"pdf2docx": "#1 转Word首选管道", "pytesseract": "#2 OCR 兜底引擎",
          "PIL": "#15 压缩图片重编码", "paddleocr": "#2 中文 OCR SOTA"}
CORE_CAPS = "#1-#15、#20、#25（转换/OCR/编辑/安全/批量/提取/压缩/替换/密文删除）"

def chk_py(mod):
    try:
        importlib.import_module(mod)
        return True
    except Exception:
        return False

def chk_bin(name):
    return shutil.which(name) is not None

def tess_langs():
    if not chk_bin("tesseract"):
        return []
    try:
        out = subprocess.run(["tesseract", "--list-langs"],
                             capture_output=True, text=True, timeout=10).stdout
        return [l.strip() for l in out.splitlines()[1:] if l.strip()]
    except Exception:
        return []

def main():
    rows, core_ok = [], True
    for m in CORE_PY:
        ok = chk_py(m)
        core_ok &= ok
        rows.append((f"python: {m}", ok, "核心"))
    for m, desc in OPT_PY.items():
        rows.append((f"python: {m}", chk_py(m), f"增强（{desc}）"))
    tess = chk_bin("tesseract")
    rows.append(("bin: tesseract", tess, "增强（#2 OCR）"))
    if tess:
        langs = tess_langs()
        rows.append(("bin: tesseract chi_sim 中文包", "chi_sim" in langs,
                     "增强（中文 OCR 必需；缺失时纯英文可用）"))
    lo = chk_bin("libreoffice") or chk_bin("soffice")
    rows.append(("bin: libreoffice", lo, "增强（#1 复杂版面降级管道）"))

    width = max(len(r[0]) for r in rows)
    print("=" * (width + 30))
    print("pdf-master 能力就绪矩阵")
    print("=" * (width + 30))
    for name, ok, tier in rows:
        mark = "✅" if ok else ("❌" if tier == "核心" else "⚪")
        print(f"{mark} {name.ljust(width)}  {'' if ok else '未安装 · '}{tier}")
    print("-" * (width + 30))
    if core_ok:
        print(f"✅ 核心能力全部就绪：{CORE_CAPS}")
        missing_opt = [r[0] for r in rows if not r[1] and r[2] != "核心"]
        if missing_opt:
            print(f"⚪ 未装增强项 {len(missing_opt)} 个（对应能力自动走降级管道，不影响使用）：")
            print("   补装：bash setup.sh --all  或  pip install -r requirements-optional.txt")
        else:
            print("✅ 增强项全部就绪：25 项能力满血运行")
        sys.exit(0)
    print("❌ 核心依赖缺失：请先运行  bash setup.sh  或  pip install -r requirements.txt")
    sys.exit(1)

if __name__ == "__main__":
    main()
