#!/usr/bin/env python3
"""
OpenClaw History Viewer - Web Server
Provides a web interface to browse and view OpenClaw chat history.
"""

import json
import os
import sys
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from pathlib import Path
from datetime import datetime
import html

SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
SESSIONS_FILE = SESSIONS_DIR / "sessions.json"
BACKUP_DIR = Path.home() / ".openclaw" / "workspace" / "history"
BACKUP_INDEX_FILE = BACKUP_DIR / "backup_index.json"

# OpenClaw 自动创建的 .reset. 备份文件模式
# 格式：<session-id>.jsonl.reset.<timestamp>
RESET_FILE_PATTERN = re.compile(r"^(.+)\.jsonl\.reset\.(.+)$")


def clean_question_preview(text):
    """
    清理问题预览，移除 OpenClaw 元数据，只保留用户实际输入
    
    移除的内容：
    - Sender (untrusted metadata) 行
    - JSON 元数据块
    - 时间戳行 [Sun 2026-03-15 13:18 GMT+8]
    - System: 开头的系统消息
    """
    if not text:
        return ""
    
    lines = text.split('\n')
    cleaned_lines = []
    
    skip_until_bracket = False  # 跳过 ``` 块
    skip_metadata = False  # 跳过元数据后的内容
    
    for line in lines:
        line_stripped = line.strip()
        
        # 跳过空的代码块标记
        if line_stripped == '```':
            skip_until_bracket = not skip_until_bracket
            continue
        
        if skip_until_bracket:
            continue
        
        # 跳过 Sender metadata 行
        if line_stripped.startswith("Sender (untrusted metadata)"):
            skip_metadata = True
            continue
        
        # 跳过 JSON 块开始
        if line_stripped.startswith('```json'):
            skip_until_bracket = True
            continue
        
        # 跳过时间戳行 [Sun 2026-03-15 13:18 GMT+8] 或 [2026-03-15 18:15:25 GMT+8]
        if re.match(r'^\[(Sun|Mon|Tue|Wed|Thu|Fri|Sat)?\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})? GMT[+-]\d+\]', line_stripped):
            # 提取时间戳后的内容
            match = re.match(r'^\[.*?\]\s*(.*)', line_stripped)
            if match and match.group(1):
                cleaned_lines.append(match.group(1))
            continue
        
        # 处理 System: 开头的行 - 提取后面的内容并清理时间戳
        if line_stripped.startswith("System:"):
            # 提取 System: 后的内容
            content_after_system = line_stripped[7:].strip()
            if content_after_system:
                # 如果内容以时间戳开头，清理时间戳
                ts_match = re.match(r'^\[.*?\]\s*(.*)', content_after_system)
                if ts_match and ts_match.group(1):
                    cleaned_lines.append(ts_match.group(1))
                else:
                    cleaned_lines.append(content_after_system)
            continue
        
        # 如果是元数据模式，跳过 JSON 内容
        if skip_metadata:
            if line_stripped.startswith('```'):
                skip_metadata = False
            continue
        
        # 跳过纯 JSON 行
        if line_stripped.startswith('{') or line_stripped.startswith('}') or \
           line_stripped.startswith('"label"') or line_stripped.startswith('"id"') or \
           (line_stripped.startswith('"') and ':' in line_stripped):
            continue
        
        # 保留有效内容
        if line_stripped:
            cleaned_lines.append(line_stripped)
    
    return '\n'.join(cleaned_lines).strip()


def render_markdown(text):
    """Simple Markdown to HTML renderer"""
    if not text:
        return ""
    
    # Escape HTML first
    text = html.escape(text)
    
    # Code blocks (```code```)
    text = re.sub(
        r'```(\w*)\n(.*?)```',
        r'<div class="code-block"><pre>\2</pre></div>',
        text,
        flags=re.DOTALL
    )
    
    # Inline code (`code`)
    text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
    
    # Bold (**text** or __text__)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
    
    # Italic (*text* or _text_)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
    
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    
    # Headers (# Header)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Tables - must be processed before line breaks
    lines = text.split('\n')
    result_lines = []
    in_table = False
    table_rows = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Check if this is a table row (contains |)
        if '|' in stripped and stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            
            # Skip separator row (|---|---|)
            if not re.match(r'^\|?\s*[-:|]+\s*\|?$', stripped):
                cells = [cell.strip() for cell in stripped.split('|')]
                cells = [c for c in cells if c]
                if cells:
                    cell_tag = 'th' if len(table_rows) == 0 else 'td'
                    row_html = ''.join(f'<{cell_tag}>{c}</{cell_tag}>' for c in cells)
                    table_rows.append(f'<tr>{row_html}</tr>')
        else:
            # End of table
            if in_table and table_rows:
                rows_html = ''
                for idx, row in enumerate(table_rows):
                    if idx == 0:
                        rows_html += row.replace('<td>', '<th>').replace('</td>', '</th>')
                    else:
                        rows_html += row
                result_lines.append(f'<table class="md-table"><tbody>{rows_html}</tbody></table>')
                in_table = False
                table_rows = []
            
            if stripped:  # Only add non-empty lines
                result_lines.append(stripped)
    
    # Handle table at end of text
    if in_table and table_rows:
        rows_html = ''
        for idx, row in enumerate(table_rows):
            if idx == 0:
                rows_html += row.replace('<td>', '<th>').replace('</td>', '</th>')
            else:
                rows_html += row
        result_lines.append(f'<table class="md-table"><tbody>{rows_html}</tbody></table>')
    
    text = '\n'.join(result_lines)
    
    # Unordered lists (- item or * item)
    text = re.sub(r'^[-*] (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*</li>\n?)+', lambda m: f'<ul>{m.group(0)}</ul>', text)
    
    # Line breaks - only add <br> between non-empty content lines
    # Don't add <br> after block elements
    text = re.sub(r'\n(?!</?(?:ul|ol|li|table|tbody|tr|td|th|div|p|h[1-6]|pre)[^>]*>)', '<br>\n', text)
    
    # Clean up multiple consecutive <br>
    text = re.sub(r'(<br>\s*){3,}', '<br><br>', text)
    
    return text

class HistoryHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/":
            self.send_html(self.render_chat_list())
        elif parsed.path == "/list":
            self.send_html(self.render_session_list())
        elif parsed.path == "/session":
            query = parse_qs(parsed.query)
            session_id = query.get("id", [None])[0]
            if session_id:
                self.send_html(self.render_session(session_id))
            else:
                self.send_error(400, "Missing session id")
        elif parsed.path == "/chat":
            query = parse_qs(parsed.query)
            session_id = query.get("id", [None])[0]
            if session_id:
                self.send_html(self.render_chat_view(session_id))
            else:
                self.send_html(self.render_chat_list())
        elif parsed.path == "/api/sessions":
            self.send_json(self.get_sessions())
        elif parsed.path == "/api/session":
            query = parse_qs(parsed.query)
            session_id = query.get("id", [None])[0]
            if session_id:
                self.send_json(self.get_session(session_id))
            else:
                self.send_error(400, "Missing session id")
        else:
            self.send_error(404, "Not Found")
    
    def delete_session(self, session_id):
        """Delete a session file (including .reset. backup files)"""
        import shutil
        
        deleted_files = []
        
        # 1. 尝试从当前活跃会话中删除
        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    sessions_data = json.load(f)
            except json.JSONDecodeError:
                sessions_data = {}
            
            # 查找并删除对应的 session 文件
            for key, session in list(sessions_data.items()):
                if session.get("sessionId") == session_id or key.split(":")[-1] == session_id:
                    session_file = session.get("sessionFile")
                    if session_file and Path(session_file).exists():
                        try:
                            Path(session_file).unlink()
                            deleted_files.append(session_file)
                        except Exception as e:
                            print(f"删除会话文件失败 {session_file}: {e}")
                    
                    # 从 sessions.json 中移除
                    del sessions_data[key]
                    
                    try:
                        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
                            json.dump(sessions_data, f, indent=2, ensure_ascii=False)
                    except Exception as e:
                        print(f"更新 sessions.json 失败：{e}")
                    break
        
        # 2. 尝试删除 .reset. 备份文件
        if SESSIONS_DIR.exists():
            try:
                for filename in SESSIONS_DIR.iterdir():
                    if not filename.is_file():
                        continue
                    
                    match = RESET_FILE_PATTERN.match(filename.name)
                    if match and match.group(1) == session_id:
                        try:
                            filename.unlink()
                            deleted_files.append(str(filename))
                        except Exception as e:
                            print(f"删除 .reset. 文件失败 {filename}: {e}")
            except Exception as e:
                print(f"扫描 .reset. 文件失败：{e}")
        
        # 3. 尝试从手动备份中删除
        if BACKUP_INDEX_FILE.exists():
            try:
                with open(BACKUP_INDEX_FILE, "r", encoding="utf-8") as f:
                    backup_index = json.load(f)
            except json.JSONDecodeError:
                backup_index = {"backups": {}}
            
            if session_id in backup_index.get("backups", {}):
                backup_data = backup_index["backups"][session_id]
                for backup_file_info in backup_data.get("files", []):
                    backup_file = backup_file_info.get("file", "")
                    if backup_file and Path(backup_file).exists():
                        try:
                            Path(backup_file).unlink()
                            deleted_files.append(backup_file)
                        except Exception as e:
                            print(f"删除备份文件失败 {backup_file}: {e}")
                
                # 从索引中移除
                del backup_index["backups"][session_id]
                try:
                    with open(BACKUP_INDEX_FILE, "w", encoding="utf-8") as f:
                        json.dump(backup_index, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"更新 backup_index.json 失败：{e}")
        
        if deleted_files:
            print(f"已删除会话 {session_id} 的文件：{deleted_files}")
            return {"success": True, "deletedFiles": deleted_files}
        else:
            return {"success": False, "error": "未找到会话文件"}
    
    def do_POST(self):
        """Handle POST requests"""
        parsed = urlparse(self.path)
        if parsed.path == "/api/delete":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                delete_request = json.loads(post_data.decode('utf-8'))
                session_id = delete_request.get('sessionId')
                if session_id:
                    result = self.delete_session(session_id)
                    self.send_json(result)
                else:
                    self.send_json({"success": False, "error": "Missing sessionId"})
            except json.JSONDecodeError:
                self.send_json({"success": False, "error": "Invalid JSON"})
        else:
            self.send_error(404, "Not Found")
    
    def send_html(self, content):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
    
    def get_sessions(self):
        """Get list of all sessions (including backups)"""
        sessions = []
        seen_session_ids = set()
        
        # 1. 读取当前活跃会话
        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    sessions_data = json.load(f)
            except json.JSONDecodeError:
                sessions_data = {}
            
            for key, session in sessions_data.items():
                # Get timestamp - handle both milliseconds and seconds
                updated_at = session.get("updatedAt", 0)
                updated_at_str = "Unknown"
                
                if updated_at:
                    try:
                        # If timestamp is in milliseconds (> year 2100 in seconds), convert to seconds
                        if updated_at > 4102444800:  # Year 2100 in seconds
                            updated_at = updated_at / 1000
                        # Validate reasonable year (1970-2100)
                        if 0 < updated_at < 4102444800:
                            updated_at_str = datetime.fromtimestamp(updated_at).strftime("%Y-%m-%d %H:%M:%S")
                    except (ValueError, OSError, OverflowError):
                        updated_at_str = "Unknown"
                
                session_id = session.get("sessionId", "")
                seen_session_ids.add(session_id)
                
                session_info = {
                    "key": key,
                    "sessionId": session_id,
                    "updatedAt": updated_at,
                    "updatedAtStr": updated_at_str,
                    "channel": session.get("lastChannel", session.get("deliveryContext", {}).get("channel", "unknown")),
                    "chatType": session.get("chatType", "unknown"),
                    "sessionFile": session.get("sessionFile", ""),
                    "firstQuestion": "",
                    "isBackup": False,
                }
                
                # Try to get message count and first question from jsonl file
                session_file = session.get("sessionFile")
                if session_file and Path(session_file).exists():
                    try:
                        with open(session_file, "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            message_count = len(lines)
                            session_info["messageCount"] = message_count
                            
                            # Find first user message (skip metadata/system messages)
                            first_user_text = ""
                            first_system_text = ""
                            
                            for line in lines:
                                try:
                                    entry = json.loads(line.strip())
                                    if entry.get("type") == "message":
                                        msg_data = entry.get("message", {})
                                        role = msg_data.get("role", "")
                                        content_parts = msg_data.get("content", [])
                                        texts = []
                                        for part in content_parts:
                                            if isinstance(part, dict) and part.get("type") == "text":
                                                texts.append(part.get("text", ""))
                                            elif isinstance(part, str):
                                                texts.append(part)
                                        
                                        msg_text = "\n".join(texts).strip()
                                        
                                        # 跳过内容以 System: 开头的伪 user 消息（这是 OpenClaw 的系统提示）
                                        if role == "user" and msg_text.startswith("System:"):
                                            if not first_system_text:
                                                first_system_text = clean_question_preview(msg_text)
                                            continue
                                        
                                        # 优先记录用户消息
                                        if role == "user" and not first_user_text:
                                            # 清理 OpenClaw 元数据，只保留用户实际问题
                                            first_user_text = clean_question_preview(msg_text)
                                        # 如果没有用户消息，记录第一条系统/助手消息作为备选
                                        elif role in ("system", "assistant") and not first_system_text:
                                            first_system_text = clean_question_preview(msg_text)
                                        
                                        # 如果已经找到用户消息，可以提前退出
                                        if first_user_text:
                                            break
                                except json.JSONDecodeError:
                                    continue
                            
                            # 优先使用用户消息，没有则使用系统消息
                            if first_user_text:
                                session_info["firstQuestion"] = first_user_text[:150] + "..." if len(first_user_text) > 150 else first_user_text
                            elif first_system_text:
                                session_info["firstQuestion"] = first_system_text[:150] + "..." if len(first_system_text) > 150 else first_system_text
                            else:
                                session_info["firstQuestion"] = "新会话"
                    except:
                        session_info["messageCount"] = 0
                        session_info["firstQuestion"] = ""
                else:
                    session_info["messageCount"] = 0
                
                sessions.append(session_info)
        
        # 2. 读取 OpenClaw 自动创建的 .reset. 备份文件
        if SESSIONS_DIR.exists():
            try:
                for filename in SESSIONS_DIR.iterdir():
                    if not filename.is_file():
                        continue
                    
                    match = RESET_FILE_PATTERN.match(filename.name)
                    if not match:
                        continue
                    
                    # 解析 .reset. 文件名：<session-id>.reset.<timestamp>.jsonl
                    session_id = match.group(1)
                    timestamp_str = match.group(2)
                    
                    # 跳过已在活跃会话中的 session
                    if any(s["sessionId"] == session_id for s in sessions):
                        continue
                    
                    # 解析时间戳 (格式：2026-03-15T09-36-51.540Z)
                    try:
                        # 替换 - 为 : 用于时间解析
                        ts_formatted = timestamp_str.replace("T", " ").replace("-", ":", 2)
                        # 尝试多种格式
                        for fmt in ["%Y-%m-%d:%H:%M:%S.%fZ", "%Y-%m-%d:%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"]:
                            try:
                                reset_dt = datetime.strptime(ts_formatted, fmt)
                                reset_updated_at = reset_dt.timestamp()
                                reset_updated_at_str = reset_dt.strftime("%Y-%m-%d %H:%M:%S")
                                break
                            except ValueError:
                                continue
                        else:
                            # 如果都失败，使用文件修改时间
                            reset_updated_at = filename.stat().st_mtime
                            reset_updated_at_str = datetime.fromtimestamp(reset_updated_at).strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        reset_updated_at = filename.stat().st_mtime
                        reset_updated_at_str = datetime.fromtimestamp(reset_updated_at).strftime("%Y-%m-%d %H:%M:%S")
                    
                    # 获取文件大小和消息数
                    file_size = filename.stat().st_size
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            message_count = sum(1 for _ in f)
                    except:
                        message_count = 0
                    
                    session_info = {
                        "key": f"reset:{session_id}",
                        "sessionId": session_id,
                        "updatedAt": reset_updated_at,
                        "updatedAtStr": reset_updated_at_str,
                        "channel": "reset-backup",
                        "chatType": "archived",
                        "sessionFile": str(filename),
                        "firstQuestion": "",
                        "isBackup": True,
                        "isResetFile": True,
                        "messageCount": message_count,
                        "fileSize": file_size,
                    }
                    
                    # 尝试读取第一条消息
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            first_user_text = ""
                            first_system_text = ""
                            
                            for line in f:
                                try:
                                    entry = json.loads(line.strip())
                                    if entry.get("type") == "message":
                                        msg_data = entry.get("message", {})
                                        role = msg_data.get("role", "")
                                        content_parts = msg_data.get("content", [])
                                        texts = []
                                        for part in content_parts:
                                            if isinstance(part, dict) and part.get("type") == "text":
                                                texts.append(part.get("text", ""))
                                            elif isinstance(part, str):
                                                texts.append(part)
                                        
                                        msg_text = "\n".join(texts).strip()
                                        
                                        # 跳过内容以 System: 开头的伪 user 消息（这是 OpenClaw 的系统提示）
                                        if role == "user" and msg_text.startswith("System:"):
                                            if not first_system_text:
                                                first_system_text = clean_question_preview(msg_text)
                                            continue
                                        
                                        # 优先记录用户消息
                                        if role == "user" and not first_user_text:
                                            first_user_text = clean_question_preview(msg_text)
                                        # 如果没有用户消息，记录第一条系统/助手消息作为备选
                                        elif role in ("system", "assistant") and not first_system_text:
                                            first_system_text = clean_question_preview(msg_text)
                                        
                                        # 如果已经找到用户消息，可以提前退出
                                        if first_user_text:
                                            break
                                except json.JSONDecodeError:
                                    continue
                            
                            # 优先使用用户消息，没有则使用系统消息
                            if first_user_text:
                                session_info["firstQuestion"] = first_user_text[:150] + "..." if len(first_user_text) > 150 else first_user_text
                            elif first_system_text:
                                session_info["firstQuestion"] = first_system_text[:150] + "..." if len(first_system_text) > 150 else first_system_text
                            else:
                                session_info["firstQuestion"] = "已归档会话"
                    except:
                        session_info["firstQuestion"] = "已归档会话"
                    
                    sessions.append(session_info)
            except Exception as e:
                print(f"读取 .reset. 文件失败：{e}")
        
        # 3. 读取手动备份的会话（backup_index.json）
        if BACKUP_INDEX_FILE.exists():
            try:
                with open(BACKUP_INDEX_FILE, "r", encoding="utf-8") as f:
                    backup_index = json.load(f)
            except json.JSONDecodeError:
                backup_index = {"backups": {}}
            
            for session_id, backup_data in backup_index.get("backups", {}).items():
                # 跳过已在活跃会话中的 session
                if session_id in seen_session_ids:
                    continue
                
                # 获取最新的备份文件
                files = backup_data.get("files", [])
                if not files:
                    continue
                
                # 按时间戳排序，获取最新备份
                files.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
                latest_backup = files[0]
                
                backup_file_path = Path(latest_backup.get("file", ""))
                if not backup_file_path.exists():
                    continue
                
                # 解析备份文件名获取时间戳
                backup_timestamp_str = latest_backup.get("timestamp", "Unknown")
                try:
                    backup_dt = datetime.fromisoformat(backup_timestamp_str.replace("Z", "+00:00"))
                    backup_updated_at = backup_dt.timestamp()
                    backup_updated_at_str = backup_dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    backup_updated_at = 0
                    backup_updated_at_str = "Unknown"
                
                session_info = {
                    "key": f"backup:{session_id}",
                    "sessionId": session_id,
                    "updatedAt": backup_updated_at,
                    "updatedAtStr": backup_updated_at_str,
                    "channel": "backup",
                    "chatType": "archived",
                    "sessionFile": str(backup_file_path),
                    "firstQuestion": "",
                    "isBackup": True,
                    "backupCount": backup_data.get("total_backups", 1),
                    "messageCount": latest_backup.get("message_count", 0),
                }
                
                # 尝试读取第一条消息
                try:
                    with open(backup_file_path, "r", encoding="utf-8") as f:
                        first_user_text = ""
                        first_system_text = ""
                        
                        for line in f:
                            try:
                                entry = json.loads(line.strip())
                                if entry.get("type") == "message":
                                    msg_data = entry.get("message", {})
                                    role = msg_data.get("role", "")
                                    content_parts = msg_data.get("content", [])
                                    texts = []
                                    for part in content_parts:
                                        if isinstance(part, dict) and part.get("type") == "text":
                                            texts.append(part.get("text", ""))
                                        elif isinstance(part, str):
                                            texts.append(part)
                                    
                                    msg_text = "\n".join(texts).strip()
                                    
                                    # 跳过内容以 System: 开头的伪 user 消息（这是 OpenClaw 的系统提示）
                                    if role == "user" and msg_text.startswith("System:"):
                                        if not first_system_text:
                                            first_system_text = clean_question_preview(msg_text)
                                        continue
                                    
                                    # 优先记录用户消息
                                    if role == "user" and not first_user_text:
                                        first_user_text = clean_question_preview(msg_text)
                                    # 如果没有用户消息，记录第一条系统/助手消息作为备选
                                    elif role in ("system", "assistant") and not first_system_text:
                                        first_system_text = clean_question_preview(msg_text)
                                    
                                    # 如果已经找到用户消息，可以提前退出
                                    if first_user_text:
                                        break
                            except json.JSONDecodeError:
                                continue
                        
                        # 优先使用用户消息，没有则使用系统消息
                        if first_user_text:
                            session_info["firstQuestion"] = first_user_text[:150] + "..." if len(first_user_text) > 150 else first_user_text
                        elif first_system_text:
                            session_info["firstQuestion"] = first_system_text[:150] + "..." if len(first_system_text) > 150 else first_system_text
                        else:
                            session_info["firstQuestion"] = "已归档会话"
                except:
                    session_info["firstQuestion"] = "已归档会话"
                
                sessions.append(session_info)
        
        # Sort by updatedAt descending
        sessions.sort(key=lambda x: x["updatedAt"], reverse=True)
        
        return {"sessions": sessions, "total": len(sessions)}
    
    def get_session(self, session_id):
        """Get messages from a specific session (including backups)"""
        session_info = None
        session_file = None
        
        # 1. 先尝试从当前活跃会话中查找
        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    sessions_data = json.load(f)
            except json.JSONDecodeError:
                sessions_data = {}
            
            for key, session in sessions_data.items():
                if session.get("sessionId") == session_id or key.split(":")[-1] == session_id:
                    # Process timestamp for session_info
                    updated_at = session.get("updatedAt", 0)
                    updated_at_str = "Unknown"
                    if updated_at:
                        try:
                            if updated_at > 4102444800:
                                updated_at = updated_at / 1000
                            if 0 < updated_at < 4102444800:
                                updated_at_str = datetime.fromtimestamp(updated_at).strftime("%Y-%m-%d %H:%M:%S")
                        except (ValueError, OSError, OverflowError):
                            pass
                    
                    session_info = {
                        "sessionId": session.get("sessionId", ""),
                        "lastChannel": session.get("lastChannel", session.get("deliveryContext", {}).get("channel", "unknown")),
                        "chatType": session.get("chatType", "unknown"),
                        "updatedAtStr": updated_at_str,
                        "updatedAt": session.get("updatedAt", 0),
                        "isBackup": False,
                    }
                    session_file = session.get("sessionFile")
                    break
        
        # 2. 如果没找到，尝试从 .reset. 文件中查找
        if not session_file:
            try:
                for filename in SESSIONS_DIR.iterdir():
                    if not filename.is_file():
                        continue
                    
                    match = RESET_FILE_PATTERN.match(filename.name)
                    if not match:
                        continue
                    
                    reset_session_id = match.group(1)
                    if reset_session_id == session_id:
                        # 解析时间戳
                        timestamp_str = match.group(2)
                        try:
                            ts_formatted = timestamp_str.replace("T", " ").replace("-", ":", 2)
                            for fmt in ["%Y-%m-%d:%H:%M:%S.%fZ", "%Y-%m-%d:%H:%M:%SZ"]:
                                try:
                                    reset_dt = datetime.strptime(ts_formatted, fmt)
                                    reset_updated_at = reset_dt.timestamp()
                                    reset_updated_at_str = reset_dt.strftime("%Y-%m-%d %H:%M:%S")
                                    break
                                except ValueError:
                                    continue
                            else:
                                reset_updated_at = filename.stat().st_mtime
                                reset_updated_at_str = datetime.fromtimestamp(reset_updated_at).strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            reset_updated_at = filename.stat().st_mtime
                            reset_updated_at_str = datetime.fromtimestamp(reset_updated_at).strftime("%Y-%m-%d %H:%M:%S")
                        
                        session_info = {
                            "sessionId": session_id,
                            "lastChannel": "reset-backup",
                            "chatType": "archived",
                            "updatedAtStr": reset_updated_at_str,
                            "updatedAt": reset_updated_at,
                            "isBackup": True,
                            "isResetFile": True,
                        }
                        session_file = str(filename)
                        break
            except:
                pass
        
        # 3. 如果还没找到，尝试从手动备份中查找
        if not session_file and BACKUP_INDEX_FILE.exists():
            try:
                with open(BACKUP_INDEX_FILE, "r", encoding="utf-8") as f:
                    backup_index = json.load(f)
            except json.JSONDecodeError:
                backup_index = {"backups": {}}
            
            if session_id in backup_index.get("backups", {}):
                backup_data = backup_index["backups"][session_id]
                files = backup_data.get("files", [])
                if files:
                    # 获取最新备份
                    files.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
                    latest_backup = files[0]
                    backup_file_path = Path(latest_backup.get("file", ""))
                    
                    if backup_file_path.exists():
                        backup_timestamp_str = latest_backup.get("timestamp", "Unknown")
                        try:
                            backup_dt = datetime.fromisoformat(backup_timestamp_str.replace("Z", "+00:00"))
                            backup_updated_at = backup_dt.timestamp()
                            backup_updated_at_str = backup_dt.strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            backup_updated_at = 0
                            backup_updated_at_str = "Unknown"
                        
                        session_info = {
                            "sessionId": session_id,
                            "lastChannel": "backup",
                            "chatType": "archived",
                            "updatedAtStr": backup_updated_at_str,
                            "updatedAt": backup_updated_at,
                            "isBackup": True,
                            "backupCount": backup_data.get("total_backups", 1),
                        }
                        session_file = str(backup_file_path)
        
        if not session_file or not Path(session_file).exists():
            return {"error": f"Session file not found for {session_id}"}
        
        messages = []
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        entry = json.loads(line.strip())
                        messages.append({
                            "line": line_num,
                            "type": entry.get("type", "unknown"),
                            "timestamp": entry.get("timestamp", ""),
                            "id": entry.get("id", ""),
                            "data": entry
                        })
                    except json.JSONDecodeError:
                        messages.append({
                            "line": line_num,
                            "type": "error",
                            "error": "Invalid JSON line",
                            "raw": line[:200] if len(line) > 200 else line
                        })
        except Exception as e:
            return {"error": f"Failed to read session file: {str(e)}"}
        
        return {
            "sessionId": session_id,
            "sessionInfo": session_info,
            "messages": messages,
            "total": len(messages)
        }
    
    def render_session_list(self):
        """Render HTML session list"""
        data = self.get_sessions()
        sessions = data.get("sessions", [])
        total = data.get("total", 0)
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw 历史记录</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💬</text></svg>" type="image/svg+xml">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ 
            color: #333; 
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #007bff;
        }}
        .stats {{
            background: #fff;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .session-list {{ 
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .session-item {{
            padding: 15px 20px;
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
            cursor: pointer;
        }}
        .session-item:hover {{
            background: #f8f9fa;
        }}
        .session-item:last-child {{
            border-bottom: none;
        }}
        .session-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .session-id {{
            font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
            font-size: 14px;
            color: #007bff;
            word-break: break-all;
        }}
        .session-meta {{
            display: flex;
            gap: 15px;
            font-size: 13px;
            color: #666;
        }}
        .badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        .badge-channel {{ background: #e3f2fd; color: #1976d2; }}
        .badge-type {{ background: #f3e5f5; color: #7b1fa2; }}
        .message-count {{
            background: #e8f5e9;
            color: #388e3c;
        }}
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }}
        .refresh-btn {{
            display: inline-block;
            padding: 10px 20px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin-bottom: 20px;
            transition: background 0.2s;
        }}
        .refresh-btn:hover {{ background: #0056b3; }}
        .view-link {{
            color: #007bff;
            text-decoration: none;
            font-weight: 500;
        }}
        .view-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📜 OpenClaw 历史记录</h1>
        
        <div class="stats">
            <strong>总会话数:</strong> {total}
        </div>
        
        <a href="/" class="refresh-btn">🔄 刷新列表</a>
        
        <div class="session-list">
"""
        
        if not sessions:
            html_content += """
            <div class="empty-state">
                <p>暂无会话记录</p>
            </div>
"""
        else:
            for session in sessions:
                html_content += f"""
            <div class="session-item" onclick="window.location.href='/session?id={html.escape(session['sessionId'])}'">
                <div class="session-header">
                    <span class="session-id">{html.escape(session['sessionId'])}</span>
                    <a href="/session?id={html.escape(session['sessionId'])}" class="view-link">查看详情 →</a>
                </div>
                <div class="session-meta">
                    <span class="badge badge-channel">📱 {html.escape(session['channel'])}</span>
                    <span class="badge badge-type">💬 {html.escape(session['chatType'])}</span>
                    <span class="badge message-count">💾 {session['messageCount']} 条消息</span>
                    <span>🕐 {html.escape(session['updatedAtStr'])}</span>
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
</body>
</html>
"""
        return html_content
    
    def render_session(self, session_id):
        """Render HTML for a specific session"""
        data = self.get_session(session_id)
        
        if "error" in data:
            return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>错误</title>
    <style>
        body {{ font-family: system-ui; padding: 40px; background: #f5f5f5; }}
        .error {{ background: #ffebee; color: #c62828; padding: 20px; border-radius: 8px; }}
        a {{ color: #007bff; }}
    </style>
</head>
<body>
    <div class="error">
        <h2>❌ 错误</h2>
        <p>{html.escape(data['error'])}</p>
        <p><a href="/">← 返回列表</a></p>
    </div>
</body>
</html>"""
        
        messages = data.get("messages", [])
        session_info = data.get("sessionInfo", {})
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>会话详情 - {html.escape(session_id)}</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💬</text></svg>" type="image/svg+xml">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ 
            color: #333; 
            margin-bottom: 10px;
            font-size: 20px;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #007bff;
            text-decoration: none;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        .session-info {{
            background: #fff;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .info-row {{
            display: flex;
            gap: 20px;
            font-size: 14px;
            color: #666;
            flex-wrap: wrap;
        }}
        .messages {{
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .message {{
            padding: 15px 20px;
            border-bottom: 1px solid #eee;
        }}
        .message:last-child {{ border-bottom: none; }}
        .message-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 12px;
            color: #999;
        }}
        .message-type {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            background: #e3f2fd;
            color: #1976d2;
            font-family: monospace;
        }}
        .message-content {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            font-family: "SF Mono", Monaco, monospace;
            font-size: 13px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 400px;
            overflow-y: auto;
        }}
        .stats {{
            margin-bottom: 20px;
            color: #666;
        }}
        .toggle-btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 5px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 8px;
        }}
        .toggle-btn:hover {{ background: #0056b3; }}
        .full-content {{ display: none; }}
        .full-content.show {{ display: block; }}
    </style>
</head>
<body>
    <div class="container">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <a href="/" class="back-link">← 返回列表</a>
            <button class="refresh-btn" onclick="refreshRaw()" style="background:rgba(26,115,232,0.1);color:var(--primary);border:1px solid rgba(26,115,232,0.2);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:600;">🔄 重新加载</button>
        </div>
        
        <div class="session-info">
            <div class="info-row">
                <span><strong>Session ID:</strong> {html.escape(session_id)}</span>
                <span><strong>消息数:</strong> {len(messages)}</span>
                <span><strong>Channel:</strong> {html.escape(session_info.get('lastChannel', 'unknown'))}</span>
                <span><strong>Chat Type:</strong> {html.escape(session_info.get('chatType', 'unknown'))}</span>
            </div>
        </div>
        
        <div class="stats">显示 {min(len(messages), 100)} / {len(messages)} 条消息 (仅显示前 100 条)</div>
        
        <div class="messages" id="raw-messages">
"""
        
        for msg in messages[:100]:
            msg_type = msg.get("type", "unknown")
            timestamp = msg.get("timestamp", "")
            msg_id = msg.get("id", "")
            
            # Extract content from message data
            content = ""
            data = msg.get("data", {})
            
            if msg_type == "message":
                message_data = data.get("message", {})
                role = message_data.get("role", "")
                content_parts = message_data.get("content", [])
                
                content = f"Role: {role}\n"
                for part in content_parts:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            content += part.get("text", "")
                        elif part.get("type") == "thinking":
                            content += f"\n[Thinking]: {part.get('thinking', '')}"
                        elif part.get("type") == "toolCall":
                            content += f"\n[Tool Call]: {part.get('name', '')}({part.get('arguments', {})})"
                        elif part.get("type") == "toolResult":
                            tool_content = part.get("content", [])
                            for tc in tool_content:
                                if isinstance(tc, dict) and tc.get("type") == "text":
                                    content += f"\n[Tool Result]: {tc.get('text', '')[:500]}"
                    elif isinstance(part, str):
                        content += part
            
            elif msg_type == "session":
                content = json.dumps(data, indent=2, ensure_ascii=False)
            elif msg_type == "model_change":
                content = f"Provider: {data.get('provider', '')}\nModel: {data.get('modelId', '')}"
            elif msg_type == "thinking_level_change":
                content = f"Thinking Level: {data.get('thinkingLevel', '')}"
            elif msg_type == "custom":
                content = json.dumps(data, indent=2, ensure_ascii=False)[:1000]
            else:
                content = json.dumps(data, indent=2, ensure_ascii=False)[:500]
            
            # Truncate for preview
            preview = content[:500] if len(content) > 500 else content
            has_more = len(content) > 500
            
            html_content += f"""
            <div class="message">
                <div class="message-header">
                    <span><span class="message-type">{html.escape(msg_type)}</span> | ID: {html.escape(msg_id)}</span>
                    <span>{html.escape(timestamp)}</span>
                </div>
                <div class="message-content">{html.escape(preview)}</div>
                {f'<button class="toggle-btn" onclick="this.nextElementSibling.classList.toggle(\'show\'); this.textContent = this.nextElementSibling.classList.contains(\'show\') ? \'收起\' : \'展开更多\'">展开更多</button><div class="message-content full-content">{html.escape(content)}</div>' if has_more else ''}
            </div>
"""
        
        html_content += f"""
        </div>
    </div>
    <script>
        function refreshRaw() {{
            const messagesDiv = document.getElementById('raw-messages');
            const btn = event.target;
            
            // 保存当前滚动位置
            const currentScrollTop = messagesDiv.scrollTop;
            const currentScrollHeight = messagesDiv.scrollHeight;
            
            const originalText = btn.textContent;
            btn.textContent = '🔄 加载中...';
            btn.disabled = true;
            btn.style.opacity = '0.6';
            
            fetch(window.location.href)
                .then(res => res.text())
                .then(html => {{
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newMessages = doc.getElementById('raw-messages');
                    
                    if (newMessages) {{
                        messagesDiv.innerHTML = newMessages.innerHTML;
                        
                        // 恢复滚动位置，保持当前屏幕内容不变
                        const newScrollHeight = messagesDiv.scrollHeight;
                        const heightDiff = newScrollHeight - currentScrollHeight;
                        messagesDiv.scrollTop = Math.max(0, currentScrollTop + heightDiff);
                        
                        btn.textContent = '✅ 已加载';
                        setTimeout(() => {{
                            btn.textContent = originalText;
                            btn.disabled = false;
                            btn.style.opacity = '1';
                        }}, 1500);
                    }}
                }})
                .catch(err => {{
                    btn.textContent = '❌ 失败';
                    setTimeout(() => {{
                        btn.textContent = originalText;
                        btn.disabled = false;
                        btn.style.opacity = '1';
                    }}, 2000);
                }});
        }}
    </script>
</body>
</html>
"""
        return html_content
    
    def render_chat_list(self):
        """Render chat-style session list"""
        data = self.get_sessions()
        sessions = data.get("sessions", [])
        total = data.get("total", 0)
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw 聊天记录</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            width: 95%;
            max-width: 1800px;
            min-width: 800px;
            margin: 0 auto;
            padding: 12px;
        }}
        h1 {{ 
            color: white; 
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .session-card {{ 
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .session-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        }}
        .session-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
            gap: 12px;
        }}
        .session-header-content {{
            flex: 1;
            min-width: 0;
        }}
        .session-title {{
            font-size: 15px;
            font-weight: 600;
            color: #333;
            display: block;
            margin-bottom: 6px;
            word-break: break-all;
            font-family: "SF Mono", Monaco, monospace;
        }}
        .session-question {{
            color: #666;
            font-size: 14px;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            cursor: help;
            position: relative;
            max-width: 100%;
        }}
        .session-question:hover {{
            color: #333;
            text-decoration: underline;
        }}
        /* Custom tooltip for full text */
        .session-question:hover::before {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 0;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
            max-width: 500px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            margin-bottom: 8px;
            opacity: 0;
            animation: fadeInTooltip 0.2s ease forwards;
            pointer-events: none;
        }}
        @keyframes fadeInTooltip {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .session-preview {{
            color: #666;
            font-size: 14px;
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        .session-meta {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 13px;
            color: #888;
        }}
        .delete-btn-inline {{
            padding: 3px 8px;
            background: #e0e0e0;
            color: #666;
            border: none;
            border-radius: 4px;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s;
            margin-left: 8px;
        }}
        .delete-btn-inline:hover {{
            background: #d0d0d0;
            color: #333;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            transform: scale(1.05);
        }}
        .delete-btn-inline:active {{ transform: scale(0.98); }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }}
        .badge-webchat {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .badge-discord {{ background: linear-gradient(135deg, #5865F2, #4752C4); color: white; }}
        .badge-telegram {{ background: linear-gradient(135deg, #0088cc, #0066aa); color: white; }}
        .badge-default {{ background: #f0f0f0; color: #666; }}
        .empty-state {{
            background: white;
            border-radius: 16px;
            padding: 60px 20px;
            text-align: center;
            color: #999;
        }}
        .nav-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
        }}
        .nav-tab {{
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.2s;
        }}
        .nav-tab:hover {{ background: rgba(255,255,255,0.3); }}
        .nav-tab.active {{ background: white; color: #667eea; }}
        /* Modal styles */
        .modal-overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 10000;
            justify-content: center;
            align-items: center;
        }}
        .modal-overlay.active {{ display: flex; }}
        .modal {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            max-width: 420px;
            width: 90%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: modalSlideIn 0.3s ease;
        }}
        @keyframes modalSlideIn {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .modal-title {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 12px;
        }}
        .modal-message {{
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }}
        .modal-session-id {{
            font-family: "SF Mono", Monaco, monospace;
            background: #f5f5f5;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            color: #667eea;
            word-break: break-all;
            margin-bottom: 20px;
        }}
        .modal-buttons {{
            display: flex;
            gap: 12px;
            justify-content: flex-end;
        }}
        .modal-btn {{
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            border: none;
        }}
        .modal-btn-cancel {{
            background: #f0f0f0;
            color: #666;
        }}
        .modal-btn-cancel:hover {{
            background: #e0e0e0;
        }}
        .modal-btn-delete {{
            background: linear-gradient(135deg, #dc3545, #c82333);
            color: white;
        }}
        .modal-btn-delete:hover {{
            box-shadow: 0 4px 12px rgba(220, 53, 69, 0.4);
            transform: translateY(-1px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>💬 OpenClaw 聊天记录</h1>
        
        <div class="session-list">
"""
        
        if not sessions:
            html_content += """
            <div class="empty-state">
                <p style="font-size: 48px; margin-bottom: 16px;">📭</p>
                <p>暂无聊天会话</p>
            </div>
"""
        else:
            for session in sessions:
                badge_class = f"badge-{session['channel']}" if session['channel'] in ['webchat', 'discord', 'telegram'] else "badge-default"
                first_question = session.get('firstQuestion', '')
                session_id = session['sessionId']
                is_backup = session.get('isBackup', False)
                
                html_content += f"""
            <div class="session-card" onclick="window.location.href='/chat?id={html.escape(session_id)}'">
                <div class="session-card-header">
                    <div class="session-header-content">
                        <span class="session-title">💬 {html.escape(session_id)}</span>
                        {f'<div class="session-question" data-tooltip=\'{html.escape(first_question) if first_question else ""}\'>{html.escape(first_question)}</div>' if first_question else ''}
                    </div>
                    <span class="badge {badge_class}">{html.escape(session['channel'])}</span>
                </div>
                <div class="session-meta">
                    <span class="meta-item">📱 {html.escape(session['chatType'])}</span>
                    <span class="meta-item">💾 {session['messageCount']} 条</span>
                    <span class="meta-item">🕐 {session['updatedAtStr']}</span>
                    {f'<button class="delete-btn-inline" onclick="event.stopPropagation(); showDeleteConfirm(\'{html.escape(session_id)}\')">🗑️ 删除</button>' if is_backup else ''}
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div class="modal-overlay" id="deleteModal">
        <div class="modal">
            <div class="modal-title">⚠️ 确认删除</div>
            <div class="modal-message">确定要删除这个会话吗？此操作不可恢复，会话文件将被永久删除。</div>
            <div class="modal-session-id" id="deleteSessionIdDisplay"></div>
            <div class="modal-buttons">
                <button class="modal-btn modal-btn-cancel" onclick="hideDeleteConfirm()">取消</button>
                <button class="modal-btn modal-btn-delete" onclick="confirmDelete()">删除</button>
            </div>
        </div>
    </div>
    
    <script>
        let sessionToDelete = null;
        
        function showDeleteConfirm(sessionId) {
            sessionToDelete = sessionId;
            document.getElementById('deleteSessionIdDisplay').textContent = sessionId;
            document.getElementById('deleteModal').classList.add('active');
        }
        
        function hideDeleteConfirm() {
            sessionToDelete = null;
            document.getElementById('deleteModal').classList.remove('active');
        }
        
        function confirmDelete() {
            if (!sessionToDelete) return;
            
            fetch('/api/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sessionId: sessionToDelete })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 刷新页面
                    window.location.reload();
                } else {
                    alert('删除失败：' + (data.error || '未知错误'));
                    hideDeleteConfirm();
                }
            })
            .catch(err => {
                alert('删除失败：' + err.message);
                hideDeleteConfirm();
            });
        }
        
        // Close modal on overlay click
        document.getElementById('deleteModal').addEventListener('click', function(e) {
            if (e.target === this) {
                hideDeleteConfirm();
            }
        });
        
        // Close modal on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                hideDeleteConfirm();
            }
        });
    </script>
</body>
</html>
"""
        return html_content
    
    def _extract_message_content(self, msg):
        """Extract readable content from a message"""
        msg_type = msg.get("type", "unknown")
        data = msg.get("data", {})
        
        if msg_type == "message":
            message_data = data.get("message", {})
            role = message_data.get("role", "")
            content_parts = message_data.get("content", [])
            
            texts = []
            thinking = None
            tool_calls = []
            tool_results = []
            
            for part in content_parts:
                if isinstance(part, dict):
                    ptype = part.get("type", "")
                    if ptype == "text":
                        texts.append(part.get("text", ""))
                    elif ptype == "thinking":
                        thinking = part.get("thinking", "")
                    elif ptype == "toolCall":
                        tool_calls.append({
                            "name": part.get("name", ""),
                            "arguments": part.get("arguments", {})
                        })
                    elif ptype == "toolResult":
                        tool_content = part.get("content", [])
                        for tc in tool_content:
                            if isinstance(tc, dict) and tc.get("type") == "text":
                                tool_results.append(tc.get("text", "")[:1000])
                elif isinstance(part, str):
                    texts.append(part)
            
            return {
                "role": role,
                "texts": texts,
                "thinking": thinking,
                "tool_calls": tool_calls,
                "tool_results": tool_results,
                "full_content": message_data
            }
        
        elif msg_type == "session":
            return {"type": "system", "content": "会话开始", "data": data}
        elif msg_type == "model_change":
            return {"type": "system", "content": f"切换到模型：{data.get('modelId', '')}", "data": data}
        elif msg_type == "thinking_level_change":
            return {"type": "system", "content": f"思考级别：{data.get('thinkingLevel', '')}", "data": data}
        else:
            return {"type": "system", "content": f"[{msg_type}]", "data": data}
    
    def render_chat_view(self, session_id):
        """Render chat-style conversation view"""
        data = self.get_session(session_id)
        
        if "error" in data:
            return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>错误</title>
    <style>
        body {{ font-family: system-ui; padding: 40px; background: #f5f5f5; }}
        .error {{ background: #ffebee; color: #c62828; padding: 20px; border-radius: 8px; }}
        a {{ color: #007bff; }}
    </style>
</head>
<body>
    <div class="error">
        <h2>❌ 错误</h2>
        <p>{html.escape(data['error'])}</p>
        <p><a href="/chat">← 返回聊天列表</a></p>
    </div>
</body>
</html>"""
        
        messages = data.get("messages", [])
        session_info = data.get("sessionInfo", {})
        total_messages = len(messages)
        
        # Process all messages for chat view
        chat_messages = []
        for msg in messages:
            extracted = self._extract_message_content(msg)
            extracted["_raw"] = msg
            chat_messages.append(extracted)
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>聊天详情 - {html.escape(session_id[:8])}</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💬</text></svg>" type="image/svg+xml">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            margin: 0;
            padding: 0;
        }}
        body {{
            display: flex;
            flex-direction: column;
        }}
        .container {{ 
            width: 95%;
            max-width: 1800px;
            min-width: 800px;
            margin: 0 auto; 
            padding: 12px;
            flex: 1;
            display: flex;
            flex-direction: column;
            min-height: 0;
        }}
        
        /* Header - 单行布局 */
        .chat-header {{
            background: rgba(255,255,255,0.9);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .header-left {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .back-btn {{
            display: inline-flex;
            align-items: center;
            padding: 5px 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 12px;
            transition: transform 0.2s;
            white-space: nowrap;
        }}
        .back-btn:hover {{ transform: translateX(-2px); }}
        
        .view-switcher {{
            display: flex;
            gap: 6px;
        }}
        .view-btn {{
            padding: 5px 10px;
            background: white;
            color: #667eea;
            border: 2px solid white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            text-decoration: none;
            transition: all 0.2s;
            white-space: nowrap;
            font-weight: 600;
        }}
        .view-btn:hover {{ 
            background: #f8f9fa;
            border-color: #f8f9fa;
        }}
        .view-btn.active {{ 
            background: white; 
            color: #667eea;
            border-color: white;
        }}
        .view-btn.inactive {{ 
            background: transparent;
            color: white;
            border-color: rgba(255,255,255,0.5);
        }}
        .view-btn.inactive:hover {{ 
            background: rgba(255,255,255,0.2);
            color: white;
            border-color: white;
        }}
        
        .chat-title {{
            font-size: 14px;
            font-weight: 600;
            color: #333;
            white-space: nowrap;
        }}
        .chat-meta {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            font-size: 11px;
            color: #666;
        }}
        .chat-meta span {{
            white-space: nowrap;
        }}
        
        /* Chat Messages */
        .chat-container {{
            background: rgba(255,255,255,0.9);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            overflow: hidden;
            flex: 1;
            display: flex;
            flex-direction: column;
            min-height: 0;
        }}
        .messages {{
            padding: 12px;
            flex: 1;
            overflow-y: auto;
        }}
        .message {{
            margin-bottom: 12px;
            animation: fadeIn 0.2s ease;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .message-user {{
            display: flex;
            justify-content: flex-end;
        }}
        .message-assistant {{
            display: flex;
            justify-content: flex-start;
        }}
        .message-system {{
            display: flex;
            justify-content: center;
        }}
        .message-bubble {{
            max-width: 90%;
            padding: 10px 14px;
            border-radius: 12px;
            position: relative;
        }}
        .message-user .message-bubble {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-right-radius: 4px;
        }}
        .message-assistant .message-bubble {{
            background: #f0f0f0;
            color: #333;
            border-bottom-left-radius: 4px;
        }}
        .message-system .message-bubble {{
            background: #e8f4fd;
            color: #0066cc;
            font-size: 12px;
            padding: 6px 12px;
            border-radius: 16px;
        }}
        .message-meta {{
            font-size: 10px;
            opacity: 0.7;
            margin-top: 4px;
            text-align: right;
        }}
        .message-assistant .message-meta {{
            text-align: left;
        }}
        .message-content {{
            word-break: break-word;
            line-height: 1.4;
            font-size: 14px;
        }}
        .message-content p {{
            margin: 0;
            display: inline;
        }}
        .message-content strong {{
            font-weight: 600;
            color: inherit;
        }}
        .message-content em {{
            font-style: italic;
            opacity: 0.9;
        }}
        .message-content a {{
            color: #667eea;
            text-decoration: underline;
        }}
        .message-content .code-block {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 12px;
            border-radius: 6px;
            font-family: "SF Mono", Monaco, monospace;
            font-size: 13px;
            overflow-x: auto;
            margin: 8px 0;
            display: block;
            max-width: 100%;
            width: auto;
        }}
        .message-content .inline-code {{
            background: rgba(0,0,0,0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "SF Mono", Monaco, monospace;
            font-size: 13px;
        }}
        .message-user .message-content .inline-code {{
            background: rgba(255,255,255,0.2);
        }}
        .message-content ul, .message-content ol {{
            margin: 4px 0;
            padding-left: 20px;
        }}
        .message-content li {{
            margin: 2px 0;
        }}
        .message-content h1, .message-content h2, .message-content h3 {{
            margin: 6px 0 3px 0;
            font-weight: 600;
            display: block;
        }}
        .message-content h1 {{ font-size: 18px; }}
        .message-content h2 {{ font-size: 16px; }}
        .message-content h3 {{ font-size: 15px; }}
        .message-content .md-table {{
            margin: 6px 0;
        }}
        
        /* Table styles */
        .message-content .md-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0;
            font-size: 13px;
        }}
        .message-content .md-table th,
        .message-content .md-table td {{
            border: 1px solid rgba(0,0,0,0.15);
            padding: 8px 12px;
            text-align: left;
        }}
        .message-content .md-table th {{
            background: rgba(0,0,0,0.05);
            font-weight: 600;
        }}
        .message-content .md-table tr:nth-child(even) {{
            background: rgba(0,0,0,0.02);
        }}
        .message-user .message-content .md-table th {{
            background: rgba(255,255,255,0.15);
        }}
        .message-user .message-content .md-table td {{
            border-color: rgba(255,255,255,0.3);
        }}
        .message-user .message-content .md-table tr:nth-child(even) {{
            background: rgba(255,255,255,0.05);
        }}
        
        /* Thinking block */
        .thinking-block {{
            background: rgba(0,0,0,0.03);
            border-left: 2px solid #667eea;
            padding: 6px 10px;
            margin: 6px 0;
            border-radius: 0 6px 6px 0;
            font-size: 12px;
            color: #555;
        }}
        .thinking-label {{
            font-weight: 600;
            color: #667eea;
            font-size: 11px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        /* Tool call block */
        .tool-block {{
            background: #fff8e1;
            border: 1px solid #ffe082;
            border-radius: 6px;
            padding: 6px 10px;
            margin: 6px 0;
            font-size: 12px;
        }}
        .tool-label {{
            font-weight: 600;
            color: #f57c00;
            font-size: 11px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .tool-args {{
            background: rgba(0,0,0,0.03);
            padding: 6px;
            border-radius: 3px;
            font-family: "SF Mono", Monaco, monospace;
            font-size: 11px;
            overflow-x: auto;
        }}
        
        /* Tool result block */
        .tool-result-block {{
            background: #e8f5e9;
            border: 1px solid #a5d6a7;
            border-radius: 6px;
            padding: 6px 10px;
            margin: 6px 0;
            font-size: 12px;
        }}
        .tool-result-label {{
            font-weight: 600;
            color: #2e7d32;
            font-size: 11px;
            margin-bottom: 4px;
        }}
        
        /* Refresh button */
        .refresh-btn {{
            background: rgba(26,115,232,0.1);
            color: var(--primary);
            border: 1px solid rgba(26,115,232,0.2);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 11px;
            font-weight: 600;
            transition: all 0.2s;
            margin-left: 10px;
            white-space: nowrap;
        }}
        .refresh-btn:hover {{
            background: rgba(26,115,232,0.15);
            border-color: rgba(26,115,232,0.3);
        }}
        .header-left {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        /* Toggle button */
        .toggle-btn {{
            background: rgba(0,0,0,0.1);
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 8px;
            color: inherit;
            transition: background 0.2s;
        }}
        .toggle-btn:hover {{ background: rgba(0,0,0,0.2); }}
        .full-content {{ display: none; margin-top: 10px; }}
        .full-content.show {{ display: block; }}
        
        /* Code block */
        .code-block {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 12px;
            border-radius: 8px;
            font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
            font-size: 13px;
            overflow-x: auto;
            margin: 8px 0;
        }}
        
        /* Scrollbar */
        .messages::-webkit-scrollbar {{
            width: 8px;
        }}
        .messages::-webkit-scrollbar-track {{
            background: rgba(0,0,0,0.05);
            border-radius: 4px;
        }}
        .messages::-webkit-scrollbar-thumb {{
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
        }}
        .messages::-webkit-scrollbar-thumb:hover {{
            background: rgba(0,0,0,0.3);
        }}
        

    </style>
</head>
<body>
    <div class="container">
        <div class="chat-header">
            <div class="header-left">
                <a href="/" class="back-btn">← 返回</a>
                <div class="view-switcher">
                    <a href="/chat?id={html.escape(session_id)}" class="view-btn active">💬 聊天</a>
                    <a href="/session?id={html.escape(session_id)}" class="view-btn inactive">📋 Raw</a>
                </div>
                <button class="refresh-btn" onclick="refreshChat()" title="重新加载最新数据">🔄 重新加载</button>
            </div>
            <div class="chat-meta">
                <span>📱 {html.escape(session_info.get('lastChannel', 'unknown'))}</span>
                <span>💾 {len(messages)} 条</span>
                <span>🕐 {session_info.get('updatedAtStr', 'Unknown')}</span>
            </div>
        </div>
        
        <div class="chat-container">
            <div class="messages">
"""
        
        for msg in chat_messages:
            msg_type = msg.get("type", "unknown")
            raw = msg.get("_raw", {})
            timestamp = raw.get("timestamp", "")[:19].replace("T", " ")
            
            # Skip system messages at the beginning (session start, model changes, etc.)
            # Only show actual conversation messages
            if msg.get("role") == "user":
                # User message
                texts = msg.get("texts", [])
                content = "\n".join(texts)
                rendered_content = render_markdown(content)
                html_content += f"""
                <div class="message message-user">
                    <div class="message-bubble">
                        <div class="message-content">{rendered_content}</div>
                        <div class="message-meta">{timestamp}</div>
                    </div>
                </div>
"""
            elif msg.get("role") == "assistant":
                # Assistant message
                texts = msg.get("texts", [])
                thinking = msg.get("thinking")
                tool_calls = msg.get("tool_calls", [])
                tool_results = msg.get("tool_results", [])
                
                bubble_content = ""
                
                # Add thinking block if exists
                if thinking:
                    preview = thinking[:200] if len(thinking) > 200 else thinking
                    has_more = len(thinking) > 200
                    bubble_content += f"""
                    <div class="thinking-block">
                        <div class="thinking-label">🤔 思考过程</div>
                        <div>{html.escape(preview)}</div>
                        {f'<button class="toggle-btn" onclick="this.nextElementSibling.classList.toggle(\'show\'); this.textContent = this.nextElementSibling.classList.contains(\'show\') ? \'收起\' : \'展开更多\'">展开更多</button><div class="full-content">{html.escape(thinking)}</div>' if has_more else ''}
                    </div>
"""
                
                # Add text content
                if texts:
                    rendered_text = render_markdown("".join(texts))
                    bubble_content += f'<div class="message-content">{rendered_text}</div>'
                
                # Add tool calls
                for tool in tool_calls:
                    tool_name = tool.get("name", "")
                    tool_args = json.dumps(tool.get("arguments", {}), ensure_ascii=False, indent=2)
                    args_preview = tool_args[:150] if len(tool_args) > 150 else tool_args
                    has_more = len(tool_args) > 150
                    bubble_content += f"""
                    <div class="tool-block">
                        <div class="tool-label">🔧 工具调用：{html.escape(tool_name)}</div>
                        <div class="tool-args">{html.escape(args_preview)}</div>
                        {f'<button class="toggle-btn" onclick="this.nextElementSibling.classList.toggle(\'show\'); this.textContent = this.nextElementSibling.classList.contains(\'show\') ? \'收起\' : \'展开更多\'">展开更多</button><div class="tool-args full-content">{html.escape(tool_args)}</div>' if has_more else ''}
                    </div>
"""
                
                # Add tool results
                for result in tool_results:
                    result_preview = result[:300] if len(result) > 300 else result
                    has_more = len(result) > 300
                    bubble_content += f"""
                    <div class="tool-result-block">
                        <div class="tool-result-label">✅ 工具结果</div>
                        <div class="message-content">{html.escape(result_preview)}</div>
                        {f'<button class="toggle-btn" onclick="this.nextElementSibling.classList.toggle(\'show\'); this.textContent = this.nextElementSibling.classList.contains(\'show\') ? \'收起\' : \'展开更多\'">展开更多</button><div class="full-content"><div class="message-content">{html.escape(result)}</div></div>' if has_more else ''}
                    </div>
"""
                
                html_content += f"""
                <div class="message message-assistant">
                    <div class="message-bubble">
                        {bubble_content}
                        <div class="message-meta">{timestamp}</div>
                    </div>
                </div>
"""
        
        html_content += f"""
            </div>
        </div>
    </div>
    <script>
        // 刷新聊天数据，保持当前滚动位置
        function refreshChat() {{
            const messagesDiv = document.querySelector('.messages');
            const btn = document.querySelector('.refresh-btn');
            
            // 保存当前滚动位置
            const currentScrollTop = messagesDiv.scrollTop;
            const currentScrollHeight = messagesDiv.scrollHeight;
            
            // 显示加载状态
            const originalText = btn.textContent;
            btn.textContent = '🔄 加载中...';
            btn.disabled = true;
            btn.style.opacity = '0.6';
            
            // 重新加载当前页面数据
            fetch(window.location.href)
                .then(res => res.text())
                .then(html => {{
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newMessages = doc.querySelector('.messages');
                    
                    if (newMessages) {{
                        // 替换内容
                        messagesDiv.innerHTML = newMessages.innerHTML;
                        
                        // 恢复滚动位置（保持当前屏幕内容不变）
                        // 通过计算新旧内容高度差来调整
                        const newScrollHeight = messagesDiv.scrollHeight;
                        const heightDiff = newScrollHeight - currentScrollHeight;
                        
                        // 如果有新内容，scrollHeight 会增加，需要相应调整 scrollTop
                        messagesDiv.scrollTop = Math.max(0, currentScrollTop + heightDiff);
                        
                        // 显示成功提示
                        btn.textContent = '✅ 已加载';
                        setTimeout(() => {{
                            btn.textContent = originalText;
                            btn.disabled = false;
                            btn.style.opacity = '1';
                        }}, 1500);
                    }} else {{
                        throw new Error('无法加载消息');
                    }}
                }})
                .catch(err => {{
                    console.error('刷新失败:', err);
                    btn.textContent = '❌ 失败';
                    setTimeout(() => {{
                        btn.textContent = originalText;
                        btn.disabled = false;
                        btn.style.opacity = '1';
                    }}, 2000);
                }});
        }}
    </script>
</body>
</html>
"""
        return html_content
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass


def main():
    port = 8765
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}")
            sys.exit(1)
    
    server_address = ("", port)
    httpd = HTTPServer(server_address, HistoryHandler)
    
    print(f"🚀 OpenClaw History Viewer 已启动")
    print(f"📍 访问地址：http://localhost:{port}")
    print(f"📁 会话目录：{SESSIONS_DIR}")
    print(f"\n按 Ctrl+C 停止服务")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        httpd.shutdown()


if __name__ == "__main__":
    main()
