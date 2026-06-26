#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG HTTP Server - 處理學員即時問答
LINE Webhook 透過 HTTP 呼叫此 Server 取得 RAG 回覆

使用方式：
python rag_server.py
Server 會監聽 http://127.0.0.1:3002/query
"""
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen, Request
import sqlite3
import numpy as np

# ============================================================
# 設定區塊（請修改這裡）
# ============================================================

DB_PATH = r"D:\node_app\db\rag_embeddings.db"
OLLAMA_URL = "http://127.0.0.1:11434"
EMBEDDING_MODEL = "bge-m3:latest"
LLM_MODEL = "gemma3:4b-cloud"
PORT = 3002

# ============================================================
# HTTP Server
# ============================================================

class RAGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != '/query':
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            req_data = json.loads(post_data.decode('utf-8'))

            question = req_data.get('question', '')
            history_json = req_data.get('history', '[]')
            user_id = req_data.get('user_id', 'anonymous')

            result = self.process_question(question, history_json, user_id)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
            self.log_message("Error in do_POST: %s", str(e))

    def process_question(self, question, history_json, user_id):
        """處理問題並回傳答案 + 建議"""
        # 讀取知識庫
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, question, answer, embedding FROM rag_embeddings LIMIT 50)
        rows = c.fetchall()
        conn.close()

        # 解析歷史
        try:
            history = json.loads(history_json) if history_json else []
        except:
            history = []

        # 組成對話 context
        conversation_context = ""
        if history:
            conversation_context = "【對話歷史】\n"
            for entry in history[-3:]:
                role = entry.get('role', 'user')
                content = entry.get('content', '')
                conversation_context += f"{role}: {content}\n"

        # 取得問題 embedding
        emb_data = json.dumps({
            "model": EMBEDDING_MODEL,
            "prompt": question
        }).encode('utf-8')

        req = Request(
            f"{OLLAMA_URL}/api/embeddings",
            data=emb_data,
            headers={"Content-Type": "application/json"}
        )

        with urlopen(req, timeout=30) as resp:
            emb_result = json.loads(resp.read().decode('utf-8'))
            query_embedding = emb_result.get("embedding", [])

        # 計算相似度
        similarities = []
        for row in rows:
            doc_emb = np.frombuffer(row[3], dtype=np.float32)
            dot = sum(a*b for a,b in zip(query_embedding, doc_emb))
            norm_q = sum(a*a for a in query_embedding) ** 0.5
            norm_d = sum(a*a for a in doc_emb) ** 0.5
            sim = dot / (norm_q * norm_d) if (norm_q * norm_d) > 0 else 0

            if sim >= 0.25:
                similarities.append((row[1], row[2], sim))

        similarities.sort(key=lambda x: x[2], reverse=True)

        if not similarities:
            rag_context = "（沒有找到相關知識庫資料）"
            suggestions = []
        else:
            rag_context = "\n\n【知識庫資料】\n" + "\n\n".join([
                f"相關問題：「{q}」\n參考答案：「{a}」"
                for q, a, s in similarities[:5]
            ])

        # 組成 prompt
        prompt = f"""你是峰爪，一隻住在科技水族箱的數位龍蝦。

請根據以下資料回答客戶問題。如果資料不足，請說「爪子還在學習中，請稍後再問～」。

{conversation_context}{rag_context}

客戶最新問題：{question}

回答：請用繁體中文回答，語氣活潑有趣，適當使用 emoji。

回答完成後，請在最後一行附加：
【延續問題建議】
1. [第一個延續問題，務必8-12字]
2. [第二個延續問題，務必8-12字]
3. [第三個延續問題，務必8-12字]

請根據回答內容推薦3個最相關的延續問題，嚴格限制：每個問題8-12個中文字，不要超過12字。"""

        # 問 LLM
        llm_data = json.dumps({
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }).encode('utf-8')

        req = Request(
            f"{OLLAMA_URL}/api/chat",
            data=llm_data,
            headers={"Content-Type": "application/json"}
        )

        with urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            full_response = result["message"]["content"]

        # 解析答案和建議
        suggestions = []
        if "【延續問題建議】" in full_response:
            parts = full_response.split("【延續問題建議】")
            answer = parts[0].strip()
            suggestions_text = parts[1].strip()
            for line in suggestions_text.split('\n'):
                line = line.strip()
                if line and line[0].isdigit():
                    idx = line.find('.')
                    if idx >= 0:
                        suggestion = line[idx+1:].strip()
                        if suggestion:
                            suggestions.append(suggestion)
        else:
            answer = full_response

        return {
            "answer": answer,
            "suggestions": suggestions[:3]
        }

    def log_message(self, format, *args):
        pass

def run_server():
    """啟動 RAG Server"""
    server = HTTPServer(('127.0.0.1', PORT), RAGHandler)
    print(f"RAG Server running on http://127.0.0.1:{PORT}")
    print(f"Endpoint: http://127.0.0.1:{PORT}/query")
    print("Press Ctrl+C to stop")
    server.serve_forever()

if __name__ == '__main__':
    run_server()