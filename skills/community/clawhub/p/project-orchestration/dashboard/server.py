#!/usr/bin/env python3
"""Orchestration Dashboard — serves state info for debugging.
   Reads data from $ORCHESTRATOR_DATA_DIR or ../orchestrator-data/"""

import json, os, re, http.server, urllib.parse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("ORCHESTRATOR_DATA_DIR",
                          os.path.join(os.path.dirname(os.path.dirname(SKILL_DIR)), "orchestrator-data"))
PORT = int(os.environ.get("DASHBOARD_PORT", "8766"))

def read_file(path):
    if not os.path.exists(path): return None
    with open(path) as f: return f.read()

def parse_session_log():
    content = read_file(os.path.join(DATA_DIR, "session_log.md"))
    if not content: return {"sessions": [], "count": 0}
    sessions = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("|") and not line.startswith("|---") and not line.startswith("| Date"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 5:
                sessions.append({"date": parts[0], "project": parts[1], "task": parts[2],
                                 "model": parts[3], "status": parts[4],
                                 "notes": parts[5] if len(parts) > 5 else ""})
    return {"sessions": sessions, "count": len(sessions)}

def parse_price_log():
    content = read_file(os.path.join(DATA_DIR, "price_changes.log"))
    if not content: return {"entries": [], "count": 0}
    entries = [{"text": l.strip()} for l in content.split("\n") if l.strip() and not l.startswith("#")]
    return {"entries": entries, "count": len(entries)}

def load_models():
    content = read_file(os.path.join(DATA_DIR, "models.json"))
    if not content: return {"models": [], "total": 0, "active": 0, "broken": 0, "removed": 0}
    data = json.loads(content)
    models = []
    for m in data.get("models", []):
        models.append({
            "id": m.get("id", "?"), "provider": m.get("provider", m.get("host", "?")),
            "speed": m.get("speed_rating", "?"), "context": m.get("context_window", 0),
            "agent_ready": m.get("agent_ready", True), "status": m.get("status", "active"),
            "cost_type": m.get("cost", {}).get("type", "?"),
            "notes": (m.get("user_notes") or m.get("research_notes") or "")[:80]
        })
    active = sum(1 for m in models if m["agent_ready"] and m["status"] != "removed")
    broken = sum(1 for m in models if not m["agent_ready"])
    removed = sum(1 for m in models if m["status"] == "removed")
    return {"models": models, "total": len(models), "active": active, "broken": broken, "removed": removed}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            self.serve_file("index.html", "text/html")
        elif path == "/api/sessions": self.send_json(parse_session_log())
        elif path == "/api/models": self.send_json(load_models())
        elif path == "/api/prices": self.send_json(parse_price_log())
        elif path == "/api/status":
            pl = os.path.exists(os.path.join(DATA_DIR, "price_changes.log"))
            self.send_json({"nightly_price_check": "Configured (2 AM)" if pl else "Not configured",
                            "price_log_exists": pl, "data_dir": DATA_DIR})
        elif path == "/api/all":
            self.send_json({"sessions": parse_session_log(), "models": load_models(),
                            "prices": parse_price_log(),
                            "status": {"nightly_price_check": "Configured (2 AM)",
                                       "price_log_exists": os.path.exists(os.path.join(DATA_DIR, "price_changes.log")),
                                       "data_dir": DATA_DIR}})
        else: self.send_error(404)
    def serve_file(self, name, ct):
        p = os.path.join(os.path.dirname(__file__), name)
        if not os.path.exists(p): return self.send_error(404)
        with open(p) as f: c = f.read()
        self.send_response(200); self.send_header("Content-Type", ct)
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
        self.wfile.write(c.encode())
    def send_json(self, d):
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
        self.wfile.write(json.dumps(d, indent=2).encode())
    def log_message(self, fmt, *a): print(f"[Dashboard] {a[0]} {a[1]} {a[2]}")

if __name__ == "__main__":
    print(f"━━━ Orchestration Dashboard ━━━")
    print(f"Server: http://localhost:{PORT}")
    print(f"Data:   {DATA_DIR}")
    print(f"Set ORCHESTRATOR_DATA_DIR to override data path")
    print(f"Press Ctrl+C to stop\n")
    s = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    try: s.serve_forever()
    except KeyboardInterrupt: print("\nStopped."); s.server_close()