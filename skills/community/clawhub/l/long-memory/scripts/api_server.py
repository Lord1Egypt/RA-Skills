#!/usr/bin/env python3
"""REST API 服务器：提供 HTTP 接口访问记忆系统"""

import argparse
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import sys
sys.path.insert(0, str(Path(__file__).parent))

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


class MemoryAPIHandler(BaseHTTPRequestHandler):
    """REST API 请求处理器"""
    
    memory_dir = DEFAULT_MEMORY_DIR

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        routes = {
            "/api/health": self.handle_health,
            "/api/stats": self.handle_stats,
            "/api/conversations": self.handle_list_conversations,
            "/api/search": self.handle_search,
            "/api/topics": self.handle_topics,
            "/api/tags": self.handle_tags,
        }

        handler = routes.get(path)
        if handler:
            handler(params)
        else:
            self.send_json(404, {"error": "Not found", "routes": list(routes.keys())})

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        routes = {
            "/api/conversations": self.handle_create_conversation,
            "/api/archive": self.handle_archive,
        }

        handler = routes.get(parsed.path)
        if handler:
            handler(data)
        else:
            self.send_json(404, {"error": "Not found"})

    def send_json(self, code: int, data: dict):
        response = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def handle_health(self, params):
        self.send_json(200, {"status": "ok", "timestamp": datetime.now().isoformat()})

    def handle_stats(self, params):
        conv_dir = self.memory_dir / "conversations"
        stats = {"total_files": 0, "total_sessions": 0, "total_size": 0}
        if conv_dir.exists():
            import re
            for fp in conv_dir.glob("*.md"):
                stats["total_files"] += 1
                content = fp.read_text(encoding="utf-8")
                stats["total_sessions"] += content.count("## [")
                stats["total_size"] += fp.stat().st_size
        self.send_json(200, stats)

    def handle_list_conversations(self, params):
        conv_dir = self.memory_dir / "conversations"
        files = []
        if conv_dir.exists():
            import re
            for fp in sorted(conv_dir.glob("*.md")):
                content = fp.read_text(encoding="utf-8")
                files.append({
                    "date": fp.stem,
                    "size": fp.stat().st_size,
                    "sessions": content.count("## ["),
                    "topics": re.findall(r'###\s*话题[：:]\s*(.+)', content),
                })
        limit = int(params.get("limit", [20])[0])
        self.send_json(200, {"files": files[-limit:], "total": len(files)})

    def handle_search(self, params):
        query = params.get("q", [""])[0]
        if not query:
            self.send_json(400, {"error": "Missing query parameter 'q'"})
            return
        tag = params.get("tag", [None])[0]
        days = int(params.get("days", [0])[0]) or None

        # 简单搜索
        import re
        results = []
        conv_dir = self.memory_dir / "conversations"
        if conv_dir.exists():
            for fp in sorted(conv_dir.glob("*.md"), reverse=True):
                content = fp.read_text(encoding="utf-8")
                if query.lower() not in content.lower():
                    continue
                if tag and tag.lower() not in content.lower():
                    continue
                results.append({
                    "date": fp.stem,
                    "match": True,
                    "topics": re.findall(r'###\s*话题[：:]\s*(.+)', content),
                })
        self.send_json(200, {"query": query, "results": results[:20]})

    def handle_topics(self, params):
        import re
        conv_dir = self.memory_dir / "conversations"
        topics = {}
        if conv_dir.exists():
            for fp in sorted(conv_dir.glob("*.md")):
                content = fp.read_text(encoding="utf-8")
                for t in re.findall(r'###\s*话题[：:]\s*(.+)', content):
                    topics[t.strip()] = topics.get(t.strip(), 0) + 1
        self.send_json(200, {"topics": topics})

    def handle_tags(self, params):
        import re
        conv_dir = self.memory_dir / "conversations"
        tags = {}
        if conv_dir.exists():
            for fp in sorted(conv_dir.glob("*.md")):
                content = fp.read_text(encoding="utf-8")
                for tl in re.findall(r'\*\*标签[：:]\*\*\s*(.+)', content):
                    for t in tl.split("，"):
                        t = t.strip()
                        if t:
                            tags[t] = tags.get(t, 0) + 1
        self.send_json(200, {"tags": tags})

    def handle_create_conversation(self, data):
        date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        session = data.get("session", "api")
        topic = data.get("topic", "API 归档")
        content = data.get("content", "")
        tags = data.get("tags", [])

        conv_dir = self.memory_dir / "conversations"
        conv_dir.mkdir(parents=True, exist_ok=True)
        fp = conv_dir / f"{date}.md"

        entry = f"\n## [{datetime.now().strftime('%H:%M')}] Session: {session}\n"
        entry += f"### 话题：{topic}\n"
        if tags:
            entry += f"**标签：** {', '.join(tags)}\n\n"
        entry += f"{content}\n"

        if fp.exists():
            fp.write_text(fp.read_text(encoding="utf-8") + entry, encoding="utf-8")
        else:
            fp.write_text(f"# {date} 对话记录\n{entry}", encoding="utf-8")

        self.send_json(201, {"status": "created", "date": date, "file": str(fp)})

    def handle_archive(self, data):
        self.handle_create_conversation(data)

    def log_message(self, format, *args):
        # 静默日志
        pass


def run_server(memory_dir: Path, port: int = 8765):
    MemoryAPIHandler.memory_dir = memory_dir
    server = HTTPServer(("127.0.0.1", port), MemoryAPIHandler)
    print(f"🚀 Long Memory API 服务已启动: http://127.0.0.1:{port}")
    print(f"   接口: /api/health, /api/stats, /api/search, /api/conversations")
    print(f"   按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ 服务已停止")
        server.server_close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="REST API 服务器")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    run_server(md, args.port)
