#!/usr/bin/env python3
"""
知识库文档分析脚本 - v2.0（kreuzberg 统一提取层 + antiword .doc 极速提取）
BATCH_SIZE=100，每批超时280秒，增量断点续传
"""
import os
import json
import glob
import time
from datetime import datetime
from utils import (
    load_state, save_state,
    extract_pdf_text, extract_doc_text, extract_docx_text,
    extract_xlsx_text, extract_pptx_text, extract_via_kreuzberg,
    convert_old_office, is_gibberish
)

KNOWLEDGE_DIR = os.path.expanduser("~/.openclaw/workspace/knowledge")
STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".analysis/analysis_state.json")
SUMMARY_DIR = os.path.join(KNOWLEDGE_DIR, ".analysis/summaries")
BATCH_SIZE = 100
BATCH_TIMEOUT = 280

os.makedirs(SUMMARY_DIR, exist_ok=True)

def get_all_files():
    patterns = [
        "**/*.pdf", "**/*.doc", "**/*.docx",
        "**/*.xls", "**/*.xlsx", "**/*.ppt", "**/*.pptx",
        "**/*.md", "**/*.csv", "**/*.txt"
    ]
    files = []
    for pattern in patterns:
        for f in glob.glob(os.path.join(KNOWLEDGE_DIR, pattern), recursive=True):
            if ".analysis" not in f and ".interpret" not in f and ".storage" not in f:
                files.append(f)
    return files

def analyze_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == ".pdf":
            return extract_pdf_text(filepath)
        elif ext == ".doc":
            return extract_doc_text(filepath)
        elif ext == ".docx":
            return extract_docx_text(filepath)
        elif ext == ".xls":
            success, converted = convert_old_office(filepath, ext)
            if success:
                try:
                    return extract_xlsx_text(converted)
                finally:
                    try:
                        os.remove(converted)
                    except:
                        pass
            return "【XLS转换失败】"
        elif ext == ".xlsx":
            return extract_xlsx_text(filepath)
        elif ext == ".ppt":
            success, converted = convert_old_office(filepath, ext)
            if success:
                try:
                    return extract_pptx_text(converted)
                finally:
                    try:
                        os.remove(converted)
                    except:
                        pass
            return "【PPT转换失败】"
        elif ext == ".pptx":
            return extract_pptx_text(filepath)
        elif ext == ".md":
            text = extract_via_kreuzberg(filepath)
            if not text:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()[:3000]
            return text
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()[:3000]
    except Exception as e:
        return f"【分析失败】{str(e)}"

def main():
    state = load_state()
    all_files = get_all_files()
    analyzed_set = set(state.get("analyzed_files", []))
    pending = [f for f in all_files if os.path.basename(f) not in analyzed_set]

    if not pending:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 没有新文件需要分析")
        return

    if not state.get("pending_files"):
        state["pending_files"] = [os.path.basename(f) for f in pending]
        save_state(state)

    pending_names = state["pending_files"]
    batch_names = pending_names[:BATCH_SIZE]
    remaining_names = pending_names[BATCH_SIZE:]

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 待处理队列：{len(pending_names)} 个文件")
    print(f"本批处理：{len(batch_names)} 个，剩余：{len(remaining_names)} 个")

    batch_start = time.time()
    summaries = []

    for filename in batch_names:
        file_start = time.time()
        filepath_candidates = [f for f in all_files if os.path.basename(f) == filename]
        if not filepath_candidates:
            print(f"  ⚠️  文件不存在，跳过：{filename}")
            continue
        filepath = filepath_candidates[0]

        print(f"  分析中: {filename}")
        content = analyze_file(filepath)

        summary_file = os.path.join(
            SUMMARY_DIR,
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}.summary.txt"
        )
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(content)

        summaries.append({
            "filename": filename,
            "filepath": filepath,
            "summary_file": summary_file,
            "analyzed_at": datetime.now().isoformat()
        })

        state["analyzed_files"].append(filename)

        file_elapsed = time.time() - file_start
        batch_elapsed = time.time() - batch_start
        print(f"    耗时: {file_elapsed:.1f}秒")

        if batch_elapsed > BATCH_TIMEOUT:
            print(f"  ⚠️  本批耗时已达 {batch_elapsed:.0f}秒，超过{BATCH_TIMEOUT}秒限制，立即保存退出")
            state["pending_files"] = remaining_names
            state["last_run"] = datetime.now().isoformat()
            state["last_batch_at"] = datetime.now().isoformat()
            state["summaries"] = summaries
            save_state(state)
            print(f"  ✅ 进度已保存：{len(summaries)} 个文件已分析，剩余 {len(remaining_names)} 个待处理")
            return

    state["pending_files"] = remaining_names
    state["last_run"] = datetime.now().isoformat()
    state["last_batch_at"] = datetime.now().isoformat()
    state["summaries"] = summaries
    save_state(state)

    done = len(state["analyzed_files"])
    total = len(pending) + done
    print(f"✅ 本批完成 {len(summaries)} 个，累计已完成 {done}/{total}，剩余 {len(remaining_names)} 个")
    if remaining_names:
        print(f"提示：下次 cron 触发时会自动继续处理剩余文件")

if __name__ == "__main__":
    main()
