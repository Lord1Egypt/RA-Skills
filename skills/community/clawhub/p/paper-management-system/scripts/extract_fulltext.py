#!/usr/bin/env python3
"""
Full-text extraction for PDFs
写入 index.db 的 full_text 字段
"""

import fitz
import sqlite3
import os
import sys
import glob
import json
import time
from pathlib import Path

# Add project directory to path
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from config import get_config

def get_db():
    """Get database connection"""
    cfg = get_config()
    conn = sqlite3.connect(cfg.db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def get_log_path():
    """Get log file path from config"""
    cfg = get_config()
    log_dir = os.path.dirname(cfg.get("logging.path", str(Path(__file__).parent.parent / "logs" / "extract_fulltext.log")))
    return os.path.join(log_dir, "extract_fulltext.log")

def get_failed_path():
    """Get failed list path from config"""
    cfg = get_config()
    log_dir = os.path.dirname(cfg.get("logging.path", str(Path(__file__).parent.parent / "logs" / "extract_failed.json")))
    return os.path.join(log_dir, "extract_failed.json")

def extract_fulltext(pdf_path, max_pages=0):
    """Extract PDF full text, max_pages=0 means all pages"""
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        if max_pages > 0:
            pages = range(min(max_pages, total_pages))
        else:
            pages = range(total_pages)
        
        texts = []
        for i in pages:
            text = doc[i].get_text()
            if text and text.strip():
                texts.append(text.strip())
        
        doc.close()
        full = '\n\n'.join(texts)
        
        # Skip if text is too short (likely scanned PDF)
        if len(full.strip()) < 50:
            return None, f"文本不足50字符(共{total_pages}页)，可能是扫描件"
        
        return full, None
    except Exception as e:
        return None, str(e)

def extract_all():
    """Extract full text for all papers without full_text"""
    cfg = get_config()
    papers_dir = cfg.papers_dir
    
    conn = get_db()
    rows = conn.execute(
        "SELECT id, filepath, title FROM papers WHERE full_text IS NULL OR full_text = ''"
    ).fetchall()
    total = len(rows)
    success = 0
    failed = []
    
    LOG_FILE = get_log_path()
    FAILED_FILE = get_failed_path()
    
    log_lines = [f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始全文提取，共 {total} 篇待处理"]
    
    for idx, row in enumerate(rows):
        pid = row['id']
        fpath = row['filepath']
        title = (row['title'] or os.path.basename(fpath))[:60]
        
        if not os.path.exists(fpath):
            failed.append({"id": pid, "file": fpath, "title": title, "error": "文件不存在"})
            continue
        
        fsize = os.path.getsize(fpath)
        if fsize < 1024:
            failed.append({"id": pid, "file": fpath, "title": title, "error": f"文件过小({fsize}B)"})
            continue
        
        text, error = extract_fulltext(fpath)
        
        if text:
            conn.execute("UPDATE papers SET full_text = ? WHERE id = ?", (text, pid))
            success += 1
            if (idx + 1) % 20 == 0:
                conn.commit()
                print(f"  进度: {idx+1}/{total}，成功: {success}，失败: {len(failed)}", flush=True)
        else:
            failed.append({"id": pid, "file": fpath, "title": title, "error": error})
    
    conn.commit()
    conn.close()
    
    log_lines.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 提取完成: 成功 {success}, 失败 {len(failed)}")
    
    # Write logs
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        f.write('\n'.join(log_lines) + '\n')
    
    with open(FAILED_FILE, 'w') as f:
        json.dump(failed, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 完成 ===")
    print(f"成功: {success}")
    print(f"失败: {len(failed)}")
    print(f"日志: {LOG_FILE}")
    print(f"失败列表: {FAILED_FILE}")

# Keep backward compatibility
def main():
    extract_all()

if __name__ == '__main__':
    main()
