#!/usr/bin/env python3
"""Validate paper-format source types, including legacy DOC and LaTeX ZIP projects."""
from __future__ import annotations
import json, re, sys, zipfile
from pathlib import Path, PurePosixPath

OLE_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")
MAX_FILES = 5000
MAX_UNCOMPRESSED = 512 * 1024 * 1024

def emit(payload, code):
    print(json.dumps(payload, ensure_ascii=False, indent=2)); return code

def safe_member(name):
    normalized = name.replace("\\", "/"); path = PurePosixPath(normalized)
    return not path.is_absolute() and ".." not in path.parts and not re.match(r"^[A-Za-z]:", normalized)

def decode_tex(data):
    for encoding in ("utf-8-sig", "gb18030", "latin-1"):
        try: return data.decode(encoding)
        except UnicodeDecodeError: pass
    return None

def inspect_latex_zip(path):
    try:
        with zipfile.ZipFile(path) as package:
            infos = package.infolist()
            if len(infos) > MAX_FILES: return {"status":"invalid","message":f"ZIP 文件数量超过安全上限 {MAX_FILES}。"}, 2
            if sum(i.file_size for i in infos) > MAX_UNCOMPRESSED: return {"status":"invalid","message":"ZIP 解压后体积超过 512 MB 安全上限。"}, 2
            unsafe = [i.filename for i in infos if not safe_member(i.filename)]
            if unsafe: return {"status":"invalid","message":"ZIP 包含不安全路径，已拒绝解压。","unsafe_members":unsafe[:10]}, 2
            encrypted = [i.filename for i in infos if i.flag_bits & 1]
            if encrypted: return {"status":"invalid","message":"ZIP 包含加密文件，无法验证 LaTeX 工程。","encrypted_members":encrypted[:10]}, 2
            tex_files = [i for i in infos if not i.is_dir() and i.filename.lower().endswith(".tex")]
            candidates = []
            for info in tex_files:
                if info.file_size > 10 * 1024 * 1024: continue
                text = decode_tex(package.read(info))
                if text and re.search(r"\\documentclass(?:\[[^]]*\])?\{", text) and "\\begin{document}" in text:
                    candidates.append(info.filename)
    except (zipfile.BadZipFile, OSError, RuntimeError):
        return {"status":"invalid","message":"文件不是可读取的 ZIP 压缩包。"}, 2
    if not candidates: return {"status":"unsupported","message":"ZIP 中未找到包含 documentclass 和 document 环境的 LaTeX 主文件。"}, 3
    preferred = [n for n in candidates if PurePosixPath(n).name.lower() in {"main.tex","paper.tex","thesis.tex"}]
    pool = preferred or candidates; depth = min(len(PurePosixPath(n).parts) for n in pool); pool = [n for n in pool if len(PurePosixPath(n).parts)==depth]
    if len(pool) != 1:
        return {"status":"needs_main_selection","format":"latex-zip","message":"ZIP 中存在多个可能的 LaTeX 主文件，请用户指定主 .tex 文件。","candidates":sorted(candidates)}, 4
    return {"status":"supported","format":"latex-zip","extension":".zip","main_tex":pool[0],"tex_files":len(tex_files),"message":"已验证为 LaTeX 工程 ZIP。"}, 0

def main():
    if len(sys.argv)!=2: return emit({"status":"error","message":"用法：check_supported_input.py <论文文件>"},2)
    path=Path(sys.argv[1])
    if not path.is_file(): return emit({"status":"invalid","message":"输入文件不存在或不是普通文件。"},2)
    suffix=path.suffix.lower()
    if suffix==".docx":
        try:
            with zipfile.ZipFile(path) as z:
                if "word/document.xml" not in z.namelist(): raise zipfile.BadZipFile
        except (zipfile.BadZipFile,OSError): return emit({"status":"invalid","message":"文件不是真实的 Word DOCX 文档。"},2)
        return emit({"status":"supported","format":"word-docx","extension":suffix,"message":"输入格式受支持。"},0)
    if suffix==".doc":
        try:
            with path.open("rb") as source: valid=source.read(8)==OLE_SIGNATURE
        except OSError: valid=False
        if not valid: return emit({"status":"invalid","message":"文件不是真实的旧版 Word DOC 文档。"},2)
        return emit({"status":"supported","format":"word-doc-legacy","extension":suffix,"requires_conversion":"docx","message":"旧版 .doc 受支持，但必须先转换为临时 .docx 再排版。"},0)
    if suffix==".tex":
        try: text=decode_tex(path.read_bytes())
        except OSError: text=None
        if not text or not re.search(r"\\documentclass(?:\[[^]]*\])?\{",text) or "\\begin{document}" not in text:
            return emit({"status":"invalid","message":"文件不是可独立编译的 LaTeX 主文件（缺少 documentclass 或 document 环境）。"},2)
        return emit({"status":"supported","format":"latex-tex","extension":suffix,"message":"输入格式受支持。"},0)
    if suffix==".zip":
        payload,code=inspect_latex_zip(path); return emit(payload,code)
    return emit({"status":"unsupported","extension":suffix or None,"supported_extensions":[".doc",".docx",".tex",".zip (LaTeX project)"],"message":"论文排版仅支持 Word（.doc/.docx）和 LaTeX（.tex 或工程 ZIP）源文件。PDF、图片及其他格式不支持直接排版。"},3)

if __name__=="__main__": raise SystemExit(main())
