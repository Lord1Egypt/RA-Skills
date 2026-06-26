#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NotebookLM RAG 加強腳本 - 通用版
向 NotebookLM 發問相關問題，取得答案後存入 RAG 資料庫

使用方式：
1. 修改 QUESTIONS 陣列加入你的問題
2. 修改 CHROME_PROFILE 和 NOTEBOOK_ID
3. 執行 python rag_enhance.py
"""
import os
import sys
import json
import time
import re
import sqlite3
import subprocess
import http.client
from datetime import datetime
import io

# 設定 Windows console 編碼（避免 emoji 亂碼）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================================
# 設定區塊（請修改這裡）
# ============================================================

CHROME_PROFILE = "C:/Users/clawsPeak/AppData/Local/notebooklm-mcp/Data/chrome_profile"
NOTEBOOK_ID = "63bd43ca-5550-45bd-8da3-2b4f8b1fab2d"
OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
EMBEDDING_MODEL = "bge-m3:latest"
DB_PATH = r"D:\node_app\db\rag_embeddings.db"
OUTPUT_FILE = r"D:\node_app\rag_data\notebooklm_responses.json"

# 要問的問題清單（修改這裡加入你的問題）
QUESTIONS = [
    # 在這裡加入你想問 NotebookLM 的問題
    # 格式："問題內容"
    
    # 範例：
    # "Cloudflare Pages 是什麼？如何用它架設靜態網站？",
    # "OpenClaw 是什麼？AI 助手的核心功能有哪些？",
]

# ============================================================
# 工具函式（通常不需要修改）
# ============================================================

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

def get_embedding(text, use_warmup=True):
    """從 Ollama 取得 embedding（使用 bge-m3）"""
    try:
        if use_warmup:
            warmup_data = json.dumps({"model": EMBEDDING_MODEL, "prompt": "Testing"}).encode('utf-8')
            try:
                conn = http.client.HTTPConnection(OLLAMA_HOST, OLLAMA_PORT, timeout=10)
                conn.request("POST", "/api/embeddings", warmup_data, {"Content-Type": "application/json"})
                conn.getresponse()
                conn.close()
            except:
                pass
            time.sleep(2)

        data = json.dumps({"model": EMBEDDING_MODEL, "prompt": text}).encode('utf-8')
        conn = http.client.HTTPConnection(OLLAMA_HOST, OLLAMA_PORT, timeout=120)
        conn.request("POST", "/api/embeddings", data, {"Content-Type": "application/json"})
        resp = conn.getresponse()
        result = json.loads(resp.read().decode('utf-8'))
        conn.close()

        if "embedding" in result:
            emb = result["embedding"]
            import struct
            buf = struct.pack(f'{len(emb)}f', *emb)
            return buf
        return None
    except Exception as e:
        log(f"Embedding error: {e}")
        return None

def clean_answer(text):
    """清理 NotebookLM 答案（移除 UI 標記）"""
    if not text:
        return ""

    markers = ['keep_pin', 'copy_all', 'thumb_up', 'thumb_down',
               'keep', 'share', 'settings', '設定', '來源', '新增來源',
               'search', 'language', 'keyboard_arrow_down', 'add', 'more_horiz',
               'arrow_forward', 'arrow_back', '自訂', '建立筆記本']
    for m in markers:
        text = text.replace(m, '')

    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) < 10:
            continue
        if re.match(r'^[\d\.\,\-\s]+$', line):
            continue
        cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def ask_notebooklm(question, retries=2):
    """向 NotebookLM 提問（使用 Preview 介面）"""
    for attempt in range(retries):
        try:
            from patchright.sync_api import sync_playwright
        except ImportError:
            log("patchright not installed, installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "patchright"], check=True)
            from patchright.sync_api import sync_playwright

        if not os.path.exists(CHROME_PROFILE):
            log(f"Chrome profile not found: {CHROME_PROFILE}")
            return None

        try:
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    CHROME_PROFILE,
                    headless=False
                )
                page = context.new_page()

                url = f"https://notebooklm.google.com/notebook/{NOTEBOOK_ID}/preview"
                page.goto(url)
                time.sleep(6)

                if "Login" in page.title() or "登入" in page.title():
                    log("Not logged in to NotebookLM!")
                    context.close()
                    return None

                textareas = page.query_selector_all('textarea')
                input_box = None
                for ta in textareas:
                    if ta.is_visible():
                        input_box = ta
                        break

                if not input_box:
                    log("Input box not found!")
                    context.close()
                    return None

                input_box.click(force=True)
                time.sleep(0.5)
                page.keyboard.press("Control+a")
                time.sleep(0.3)
                page.keyboard.press("Backspace")
                time.sleep(0.5)
                page.keyboard.type(question)
                time.sleep(0.5)
                page.keyboard.press("Enter")

                log(f"Waiting 35s for response...")
                time.sleep(35)

                body = page.query_selector('body')
                if body:
                    text = body.inner_text()
                    lines = text.split('\n')

                    question_found = False
                    response_lines = []
                    for line in lines:
                        if question[:20] in line:
                            question_found = True
                            continue
                        if question_found and line.strip():
                            if len(line.strip()) > 15:
                                if any(m in line for m in ['copy_all', 'thumb_up', 'thumb_down']):
                                    break
                                response_lines.append(line)

                    if response_lines:
                        raw = '\n'.join(response_lines[:80])
                        cleaned = clean_answer(raw)
                        context.close()
                        if len(cleaned) > 30:
                            return cleaned
                        else:
                            log(f"Answer too short ({len(cleaned)} chars), retrying...")

                context.close()
                log(f"Attempt {attempt+1} failed, retrying...")
                time.sleep(5)

        except Exception as e:
            log(f"NotebookLM error: {e}")
            time.sleep(5)

    return None

def add_to_rag(question, answer):
    """新增 Q&A 到 RAG 資料庫"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute('SELECT id FROM rag_embeddings WHERE question = ?', (question,))
        if c.fetchone():
            conn.close()
            return "already_exists"

        full_text = f"問題：{question}\n回答：{answer}"
        emb = get_embedding(full_text)
        if not emb:
            conn.close()
            return "embedding_failed"

        c.execute('INSERT INTO rag_embeddings (question, answer, embedding) VALUES (?, ?, ?)',
                  (question, answer, emb))
        conn.commit()
        conn.close()
        return "success"

    except Exception as e:
        log(f"RAG insert error: {e}")
        return f"error: {e}"

def init_db():
    """初始化 RAG 資料庫（第一次使用時呼叫）"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rag_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            embedding BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    log("Database initialized.")

# ============================================================
# 主程式
# ============================================================

def main():
    print("=" * 60)
    print("NotebookLM RAG Enhance")
    print("=" * 60)
    
    if not QUESTIONS:
        log("No questions defined. Please add questions to QUESTIONS array.")
        return
    
    log(f"Questions: {len(QUESTIONS)}")
    log(f"DB: {DB_PATH}")
    log("")
    
    # 初始化資料庫
    init_db()

    results = []

    for i, q in enumerate(QUESTIONS):
        log(f"\n[{i+1}/{len(QUESTIONS)}] Q: {q[:40]}...")
        
        answer = ask_notebooklm(q)
        
        if answer and len(answer) > 30:
            cleaned = clean_answer(answer)
            log(f"  -> Got {len(cleaned)} chars")
            
            status = add_to_rag(q, cleaned)
            if status == "success":
                log(f"  -> [OK] RAG saved")
                results.append({"question": q, "answer": cleaned, "status": "success"})
            elif status == "already_exists":
                log(f"  -> [SKIP] Already exists")
                results.append({"question": q, "answer": cleaned, "status": "already_exists"})
            else:
                log(f"  -> [WARN] Failed: {status}")
                results.append({"question": q, "answer": cleaned, "status": status})
        else:
            log(f"  -> [FAIL] No answer")
            results.append({"question": q, "answer": "", "status": "failed"})

        if i < len(QUESTIONS) - 1:
            log(f"  Waiting 5s...")
            time.sleep(5)

    # 儲存結果
    log("\n" + "=" * 60)
    log("Saving results...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"Saved to {OUTPUT_FILE}")

    # 統計
    success_count = len([r for r in results if r['status'] == 'success'])
    exists_count = len([r for r in results if r['status'] == 'already_exists'])
    failed_count = len([r for r in results if r['status'] == 'failed'])

    log("\n" + "=" * 60)
    log(f"Complete! New: {success_count}, Existed: {exists_count}, Failed: {failed_count}")
    log("=" * 60)

if __name__ == "__main__":
    main()