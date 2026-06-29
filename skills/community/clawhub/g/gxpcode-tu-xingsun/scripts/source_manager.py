# GxpCode Skill — 法规源管理
# 用法:
#   python source_manager.py                     → 启动可视化面板
#   python source_manager.py list                → CLI 表格
#   python source_manager.py toggle <name>       → 切换启用/禁用
#   python source_manager.py disable <name>      → 禁用
#   python source_manager.py enable <name>       → 启用
#   python source_manager.py status              → 统计

import json
import os
import sys
import yaml
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(SKILL_DIR, "resources", "sources.yaml")

# ── 数据读写 ──────────────────────────────────────────────────

def _load():
    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _save(data):
    with open(SOURCES_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def _find(data, name):
    sources = data.get("sources", [])
    for s in sources:
        if s["name"] == name:
            return s
    return None

# ── CLI 命令 ──────────────────────────────────────────────────

def cmd_list(data):
    sources = data.get("sources", [])
    print(f"{'状态':<6}{'名称':<28}{'类型':<6}{'机构':<8}URL")
    print("-" * 90)
    for s in sources:
        status = "[ON] " if s.get("enabled", True) else "[OFF]"
        print(f"{status:<6}{s['name']:<28}{s.get('type',''):<6}{s.get('jurisdiction',''):<8}{s.get('url','')[:50]}")
    on = sum(1 for s in sources if s.get("enabled", True))
    print(f"\n活跃: {on}/{len(sources)}")

def cmd_status(data):
    sources = data.get("sources", [])
    on = sum(1 for s in sources if s.get("enabled", True))
    print(f"{on}/{len(sources)} 活跃")
    by_jur = {}
    for s in sources:
        j = s.get("jurisdiction", "other")
        by_jur.setdefault(j, {"total": 0, "on": 0})
        by_jur[j]["total"] += 1
        if s.get("enabled", True):
            by_jur[j]["on"] += 1
    for j, v in sorted(by_jur.items()):
        print(f"  {j}: {v['on']}/{v['total']}")

def cmd_toggle(data, name):
    s = _find(data, name)
    if not s:
        print(f"未找到源: {name}")
        return
    s["enabled"] = not s.get("enabled", True)
    _save(data)
    status = "[ON] 启用" if s["enabled"] else "[OFF] 禁用"
    print(f"{status}: {name}")

def cmd_enable(data, name):
    s = _find(data, name)
    if not s:
        print(f"未找到源: {name}")
        return
    s["enabled"] = True
    _save(data)
    print(f"[ON] 启用: {name}")

def cmd_disable(data, name):
    s = _find(data, name)
    if not s:
        print(f"未找到源: {name}")
        return
    s["enabled"] = False
    _save(data)
    print(f"[OFF] 禁用: {name}")

# ── 可视化面板 ────────────────────────────────────────────────

DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GxpCode 法规源管理</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Microsoft YaHei','PingFang SC',sans-serif;background:#f5f6fa;color:#2d3436;padding:24px 32px}
h1{font-size:22pt;margin-bottom:4px}
.meta{color:#636e72;font-size:10pt;margin-bottom:24px}
.bar{display:flex;align-items:center;gap:16px;margin-bottom:20px;flex-wrap:wrap}
.stats{background:#fff;padding:10px 18px;border-radius:8px;font-size:11pt;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.stats span{font-weight:bold;color:#0f3460}
#search{padding:8px 14px;border:1px solid #ddd;border-radius:8px;width:260px;font-size:10pt}
#search:focus{outline:none;border-color:#0f3460}
.actions{display:flex;gap:8px;margin-left:auto}
.btn{padding:8px 18px;border:none;border-radius:8px;cursor:pointer;font-size:10pt;font-weight:600;transition:.15s}
.btn-save{background:#e94560;color:#fff}
.btn-save:hover{background:#c0392b}
.btn-refresh{background:#dfe6e9;color:#2d3436}
.btn-refresh:hover{background:#b2bec3}
.group{margin-bottom:28px;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06)}
.group-head{display:flex;align-items:center;padding:12px 18px;background:#f0f0f4;cursor:pointer;gap:10px;user-select:none}
.group-head .badge{background:#0f3460;color:#fff;font-size:8pt;padding:2px 8px;border-radius:4px;font-weight:600}
.group-head h3{font-size:12pt;flex:1}
.group-head .toggle-all{font-size:9pt;color:#636e72;cursor:pointer;padding:4px 10px;border-radius:6px}
.group-head .toggle-all:hover{background:#dfe6e9}
.row{display:grid;grid-template-columns:60px 1fr 60px 80px 60px;align-items:center;padding:10px 18px;border-bottom:1px solid #f0f0f4;font-size:10pt;gap:8px}
.row:hover{background:#fafafa}
.row .name{font-weight:600}
.row .type{color:#636e72;text-align:center}
.row .juris{text-align:center}
.row .juris span{background:#dfe6e9;padding:1px 8px;border-radius:4px;font-size:8pt}
/* Toggle switch */
.switch{position:relative;display:inline-block;width:44px;height:24px}
.switch input{opacity:0;width:0;height:0}
.slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:#fab1a0;transition:.2s;border-radius:24px}
.slider:before{content:"";position:absolute;height:18px;width:18px;left:3px;bottom:3px;background:#fff;transition:.2s;border-radius:50%}
input:checked+.slider{background:#55efc4}
input:checked+.slider:before{transform:translateX(20px)}
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:#0f3460;color:#fff;padding:12px 28px;border-radius:10px;font-size:11pt;opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}
.toast.show{opacity:1}
@media(max-width:768px){
  body{padding:16px}
  .row{grid-template-columns:50px 1fr 0px 0px 0px}
  .row .type,.row .juris,.row .delete{display:none}
}
</style>
</head>
<body>

<h1>🔬 GxpCode 法规源管理</h1>
<div class="meta">开关源后点击「保存」写回 sources.yaml，下次法规跟踪时生效</div>

<div class="bar">
  <div class="stats" id="stats">活跃: <span id="statOn">-</span> / <span id="statTotal">-</span></div>
  <input id="search" placeholder="🔍 搜索源名称或 URL..." oninput="render()">
  <div class="actions">
    <button class="btn btn-refresh" onclick="load()">🔄 刷新</button>
    <button class="btn btn-save" onclick="save()">💾 保存</button>
  </div>
</div>

<div id="groups"></div>
<div class="toast" id="toast"></div>

<script>
let sources = [];
let changed = false;

async function load() {
  const r = await fetch('/api/sources');
  sources = await r.json();
  changed = false;
  render();
}

function render() {
  const q = document.getElementById('search').value.toLowerCase();

  // 按 jurisdiction 分组
  const groups = {};
  for (const s of sources) {
    if (q && !s.name.toLowerCase().includes(q) && !(s.url||'').toLowerCase().includes(q)) continue;
    const j = s.jurisdiction || 'other';
    if (!groups[j]) groups[j] = [];
    groups[j].push(s);
  }

  // 统计
  let on = 0, total = 0;
  for (const s of sources) {
    total++;
    if (s.enabled !== false) on++;
  }
  document.getElementById('statOn').textContent = on;
  document.getElementById('statTotal').textContent = total;

  // 渲染
  const jurisOrder = ['CDE', 'NMPA', 'PIC/S', 'FDA', 'EMA'];
  const sorted = [];
  for (const j of jurisOrder) {
    if (groups[j]) sorted.push([j, groups[j]]);
  }
  for (const [j, items] of Object.entries(groups)) {
    if (!jurisOrder.includes(j)) sorted.push([j, items]);
  }

  let html = '';
  for (const [jur, items] of sorted) {
    const jOn = items.filter(s => s.enabled !== false).length;
    html += `<div class="group">
      <div class="group-head" onclick="this.nextElementSibling.classList.toggle('hidden')">
        <span class="badge">${jur}</span>
        <h3>${jur} (${jOn}/${items.length})</h3>
        <span class="toggle-all" onclick="event.stopPropagation();toggleJurisdiction('${jur}',true)">全部启用</span>
        <span class="toggle-all" onclick="event.stopPropagation();toggleJurisdiction('${jur}',false)">全部禁用</span>
      </div>
      <div>`;
    for (const s of items) {
      html += `<div class="row">
        <label class="switch">
          <input type="checkbox" ${s.enabled !== false ? 'checked' : ''} onchange="toggle('${s.name}',this.checked)">
          <span class="slider"></span>
        </label>
        <div class="name">${s.name}</div>
        <div class="type">${s.type||''}</div>
        <div class="juris"><span>${s.jurisdiction||''}</span></div>
        <div style="font-size:8pt;color:#b2bec3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${s.url||''}">${(s.url||'').replace('https://','')}</div>
      </div>`;
    }
    html += '</div></div>';
  }
  document.getElementById('groups').innerHTML = html;
}

function toggle(name, checked) {
  const s = sources.find(x => x.name === name);
  if (s) { s.enabled = checked; changed = true; }
  render();
  toast(`已${checked ? '启用' : '禁用'}: ${name}`);
}

function toggleJurisdiction(jur, enabled) {
  for (const s of sources) {
    if (s.jurisdiction === jur) s.enabled = enabled;
  }
  changed = true;
  render();
  toast(`${jur}: 全部${enabled ? '启用' : '禁用'}`);
}

async function save() {
  if (!changed) { toast('无变更'); return; }
  const r = await fetch('/api/sources', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({sources})
  });
  if (r.ok) {
    changed = false;
    toast('✅ 已保存到 sources.yaml');
  } else {
    toast('❌ 保存失败');
  }
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

load();
</script>
</body>
</html>'''

class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
        elif self.path == "/api/sources":
            data = _load()
            # 只返回 sources 列表，不返回其他顶层字段
            sources = data.get("sources", [])
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(sources, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/sources":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            payload = json.loads(body)
            data = _load()
            data["sources"] = payload.get("sources", [])
            _save(data)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # 静默日志


def cmd_serve(data):
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8888
    print(f"GxpCode 法规源管理面板: http://localhost:{port}")
    print("   按 Ctrl+C 退出")
    from socketserver import ThreadingMixIn
    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        allow_reuse_address = True
    server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已退出")
        server.server_close()

# ── 入口 ───────────────────────────────────────────────────────

if __name__ == "__main__":
    data = _load()

    if len(sys.argv) == 1:
        cmd_serve(data)
    elif sys.argv[1] == "list":
        cmd_list(data)
    elif sys.argv[1] == "status":
        cmd_status(data)
    elif sys.argv[1] == "toggle" and len(sys.argv) >= 3:
        cmd_toggle(data, sys.argv[2])
    elif sys.argv[1] == "enable" and len(sys.argv) >= 3:
        cmd_enable(data, sys.argv[2])
    elif sys.argv[1] == "disable" and len(sys.argv) >= 3:
        cmd_disable(data, sys.argv[2])
    else:
        print(__doc__)
