#!/usr/bin/env python3
"""
huo15-img-prompt — 本地 Web UI v2.6

启动一个本地 HTTP server（默认 http://127.0.0.1:7155），自动打开浏览器，
提供 88 风格预设可视化选择 + 实时 prompt 预览 + 一键复制。

启动：
  web_ui.py                       # 默认 7155 端口
  web_ui.py --port 8080           # 指定端口
  web_ui.py --no-browser          # 不自动开浏览器
  web_ui.py --host 0.0.0.0        # 局域网可访问

零第三方依赖，纯 Python 标准库 http.server + 单文件嵌入 HTML。
"""

import sys
import os
import json
import re
import argparse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import (
    build_prompt, parse_mix_preset, resolve_preset,
    parse_requirement, STYLE_PRESETS,
    preset_example_urls, compact_prompt,
)
from character import char_list, char_load

VERSION = "3.1.0"


# ─────────────────────────────────────────────────────────
# 单文件 HTML（vanilla JS + Tailwind CDN）
# ─────────────────────────────────────────────────────────
HTML_PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>火一五文生图提示词 v__VERSION__</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.tailwindcss.com"></script>
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; }
.preset-card.active { background: #1f2937; color: #fff; border-color: #1f2937; }
.preset-card { transition: all .15s ease; cursor: pointer; }
.preset-card:hover { transform: translateY(-1px); }
pre { white-space: pre-wrap; word-break: break-all; }
</style>
</head>
<body class="bg-gray-50 min-h-screen">

<div class="max-w-7xl mx-auto px-4 py-6">
  <header class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold">🔥 火一五文生图提示词 <span class="text-gray-400 text-sm">v__VERSION__</span></h1>
    <a href="https://clawhub.ai/skills/huo15-img-prompt" target="_blank" class="text-sm text-gray-500 hover:text-gray-900">📦 ClawHub →</a>
  </header>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- 左：输入 -->
    <div class="lg:col-span-1 space-y-4">
      <div class="bg-white rounded-lg p-4 shadow-sm">
        <label class="block text-sm font-medium mb-1">主体描述</label>
        <textarea id="subject" rows="3" class="w-full border rounded px-3 py-2 text-sm" placeholder="例：一只戴墨镜的猫坐在霓虹街头"></textarea>
      </div>

      <div class="bg-white rounded-lg p-4 shadow-sm space-y-3">
        <div>
          <label class="block text-sm font-medium mb-1">混合预设（可选）</label>
          <input id="secondary" class="w-full border rounded px-3 py-2 text-sm" placeholder="例：水墨（不填则单预设）">
        </div>
        <div class="flex gap-2">
          <div class="flex-1">
            <label class="block text-sm font-medium mb-1">主预设权重</label>
            <input id="mix" type="range" min="0.1" max="0.9" step="0.05" value="0.6" class="w-full">
            <span class="text-xs text-gray-500" id="mix-val">0.60</span>
          </div>
          <div class="flex-1">
            <label class="block text-sm font-medium mb-1">画质</label>
            <select id="tier" class="w-full border rounded px-3 py-2 text-sm">
              <option value="basic">basic</option>
              <option value="pro" selected>pro</option>
              <option value="master">master</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg p-4 shadow-sm space-y-3">
        <div class="flex gap-2">
          <div class="flex-1">
            <label class="block text-sm font-medium mb-1">目标模型</label>
            <select id="model" class="w-full border rounded px-3 py-2 text-sm">
              <option>通用</option>
              <option>Midjourney</option>
              <option>SD</option>
              <option>SDXL</option>
              <option>Flux</option>
              <option>DALL-E</option>
            </select>
          </div>
          <div class="flex-1">
            <label class="block text-sm font-medium mb-1">画幅</label>
            <select id="aspect" class="w-full border rounded px-3 py-2 text-sm">
              <option value="">默认</option>
              <option>1:1</option><option>3:4</option><option>4:3</option>
              <option>16:9</option><option>9:16</option><option>21:9</option>
            </select>
          </div>
        </div>

        <div class="flex items-center gap-3 text-sm">
          <label><input type="checkbox" id="compact"> 压缩到 77 token</label>
          <label><input type="checkbox" id="cs"> 角色设定图</label>
        </div>
      </div>

      <button id="go" class="w-full bg-gray-900 text-white rounded-lg py-3 hover:bg-black">⚡ 生成提示词</button>

      <div class="bg-white rounded-lg p-4 shadow-sm" id="char-section">
        <div class="text-sm font-medium mb-2">角色卡</div>
        <select id="char" class="w-full border rounded px-3 py-2 text-sm">
          <option value="">(不使用)</option>
        </select>
      </div>
    </div>

    <!-- 中：预设选择 -->
    <div class="lg:col-span-1">
      <div class="bg-white rounded-lg p-4 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-medium">88 风格预设</h2>
          <input id="preset-search" class="text-xs border rounded px-2 py-1 w-32" placeholder="搜索...">
        </div>
        <div id="preset-list" class="space-y-3 max-h-[600px] overflow-y-auto"></div>
      </div>
    </div>

    <!-- 右：输出 -->
    <div class="lg:col-span-1 space-y-4">
      <div id="output" class="hidden">
        <div class="bg-white rounded-lg p-4 shadow-sm">
          <div class="text-xs text-gray-500 mb-2 flex justify-between">
            <span>正向提示词</span>
            <button class="text-blue-500 hover:underline" data-copy="positive">📋 复制</button>
          </div>
          <pre id="positive" class="text-sm text-gray-800"></pre>
        </div>
        <div class="bg-white rounded-lg p-4 shadow-sm mt-4">
          <div class="text-xs text-gray-500 mb-2 flex justify-between">
            <span>负向提示词</span>
            <button class="text-blue-500 hover:underline" data-copy="negative">📋 复制</button>
          </div>
          <pre id="negative" class="text-xs text-gray-600"></pre>
        </div>
        <div class="bg-white rounded-lg p-4 shadow-sm mt-4">
          <div class="text-xs text-gray-500 mb-2">一致性锁</div>
          <table class="text-xs w-full">
            <tbody id="locks"></tbody>
          </table>
        </div>
        <div id="meta" class="bg-gray-100 rounded-lg p-3 mt-4 text-xs text-gray-700 font-mono"></div>
      </div>

      <div id="empty" class="bg-white rounded-lg p-12 shadow-sm text-center text-gray-400 text-sm">
        👈 选预设 + 写主体 + 点生成
      </div>
    </div>
  </div>
</div>

<script>
let presets = [];
let selectedPreset = null;

async function loadPresets() {
  const r = await fetch('/api/presets').then(x => x.json());
  presets = r.presets;
  renderPresets();
  loadChars();
}

async function loadChars() {
  try {
    const r = await fetch('/api/characters').then(x => x.json());
    const sel = document.getElementById('char');
    for (const c of r.characters || []) {
      const opt = document.createElement('option');
      opt.value = c.name;
      opt.textContent = `${c.name} (${c.preset})`;
      sel.appendChild(opt);
    }
  } catch (e) {}
}

function renderPresets(filter = '') {
  const byCat = {};
  for (const p of presets) {
    if (filter && !p.name.includes(filter) && !p.tags.toLowerCase().includes(filter.toLowerCase())) continue;
    if (!byCat[p.category]) byCat[p.category] = [];
    byCat[p.category].push(p);
  }
  const order = ['摄影', '动漫', '插画', '3D', '设计', '艺术', '场景', '游戏', '东方'];
  const html = order.filter(c => byCat[c]).map(cat => `
    <div>
      <div class="text-xs text-gray-500 mb-1">${cat} · ${byCat[cat].length}</div>
      <div class="grid grid-cols-2 gap-1">
        ${byCat[cat].map(p => `
          <button data-preset="${p.name}" class="preset-card text-xs border rounded px-2 py-1.5 text-left hover:border-gray-400 ${selectedPreset === p.name ? 'active' : ''}">
            ${p.name}
          </button>
        `).join('')}
      </div>
    </div>
  `).join('');
  document.getElementById('preset-list').innerHTML = html;
  document.querySelectorAll('[data-preset]').forEach(b => {
    b.addEventListener('click', () => {
      selectedPreset = b.dataset.preset;
      renderPresets(document.getElementById('preset-search').value);
    });
  });
}

document.getElementById('mix').addEventListener('input', e => {
  document.getElementById('mix-val').textContent = parseFloat(e.target.value).toFixed(2);
});

document.getElementById('preset-search').addEventListener('input', e => {
  renderPresets(e.target.value);
});

document.getElementById('go').addEventListener('click', async () => {
  const subject = document.getElementById('subject').value.trim();
  if (!subject) { alert('请输入主体描述'); return; }
  if (!selectedPreset) { alert('请选个预设'); return; }

  const secondary = document.getElementById('secondary').value.trim();
  const presetArg = secondary ? `${selectedPreset}+${secondary}` : selectedPreset;
  const charName = document.getElementById('char').value;

  const body = {
    subject,
    preset: presetArg,
    mix_ratio: parseFloat(document.getElementById('mix').value),
    model: document.getElementById('model').value,
    aspect: document.getElementById('aspect').value,
    tier: document.getElementById('tier').value,
    compact: document.getElementById('compact').checked,
    character_sheet: document.getElementById('cs').checked,
    char: charName || null,
  };

  const goBtn = document.getElementById('go');
  goBtn.textContent = '⏳ 生成中...';
  goBtn.disabled = true;
  try {
    const r = await fetch('/api/enhance', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body),
    }).then(x => x.json());

    if (r.error) { alert(r.error); return; }
    document.getElementById('empty').classList.add('hidden');
    document.getElementById('output').classList.remove('hidden');
    document.getElementById('positive').textContent = r.positive;
    document.getElementById('negative').textContent = r.negative;

    const locks = r.consistency_lock || {};
    document.getElementById('locks').innerHTML = Object.entries(locks)
      .filter(([_, v]) => v)
      .map(([k, v]) => `<tr><td class="font-medium pr-2 text-gray-500">${k}</td><td>${v}</td></tr>`)
      .join('');

    const meta = `seed=${r.seed_suggestion} | aspect=${r.aspect} | preset=${r.preset}${r.mix_label ? ` (mix: ${r.mix_label})` : ''}${r.compaction?.compacted ? ` | 压缩 ${r.compaction.estimated_tokens_before}→${r.compaction.estimated_tokens_after}` : ''}`;
    document.getElementById('meta').textContent = meta;
  } catch (e) {
    alert('请求失败: ' + e);
  } finally {
    goBtn.textContent = '⚡ 生成提示词';
    goBtn.disabled = false;
  }
});

document.querySelectorAll('[data-copy]').forEach(b => {
  b.addEventListener('click', () => {
    const text = document.getElementById(b.dataset.copy).textContent;
    navigator.clipboard.writeText(text);
    b.textContent = '✅ 已复制';
    setTimeout(() => { b.textContent = '📋 复制'; }, 1500);
  });
});

loadPresets();
</script>
</body>
</html>
""".replace("__VERSION__", VERSION)


# ─────────────────────────────────────────────────────────
# HTTP handlers
# ─────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # 静默

    def _send_json(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, code: int, html: str):
        body = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "/index.html":
            self._send_html(200, HTML_PAGE)
        elif path == "/api/presets":
            data = []
            for name, p in STYLE_PRESETS.items():
                data.append({
                    "name": name,
                    "category": p["category"],
                    "tags": p["tags"],
                    "aspect": p.get("aspect", "1:1"),
                })
            self._send_json(200, {"version": VERSION, "presets": data})
        elif path == "/api/characters":
            self._send_json(200, {"characters": char_list()})
        elif path == "/api/preset-examples":
            qs = parse_qs(urlparse(self.path).query)
            preset = (qs.get("preset") or [""])[0]
            resolved = resolve_preset(preset) or preset
            if resolved not in STYLE_PRESETS:
                self._send_json(404, {"error": f"未知预设 {preset}"})
                return
            self._send_json(200, preset_example_urls(resolved))
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(body_bytes.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid JSON"})
            return

        if path == "/api/enhance":
            try:
                subject = body.get("subject", "")
                raw_preset = body.get("preset", "写实摄影")
                primary, secondary = parse_mix_preset(raw_preset)
                if secondary:
                    p1, p2 = resolve_preset(primary), resolve_preset(secondary)
                    if not p1 or not p2:
                        self._send_json(400, {"error": f"未知预设 {primary} 或 {secondary}"})
                        return
                    preset, mix_secondary = p1, p2
                else:
                    preset = resolve_preset(primary) or "写实摄影"
                    mix_secondary = None

                # 角色卡注入
                char_name = body.get("char")
                if char_name:
                    card = char_load(char_name)
                    if card:
                        if card.get("subject_description"):
                            subject = f"{card['subject_description']}, {subject}"
                        body.setdefault("seed", card.get("seed"))

                aspect = body.get("aspect") or STYLE_PRESETS[preset].get("aspect", "1:1")

                result = build_prompt(
                    subject, preset, body.get("model", "通用"), aspect,
                    extra_negatives="", seed=body.get("seed"),
                    quality_tier=body.get("tier", "pro"),
                    character_sheet=bool(body.get("character_sheet", False)),
                    mix_secondary=mix_secondary,
                    mix_ratio=float(body.get("mix_ratio", 0.6)),
                )

                if body.get("compact"):
                    compacted, meta = compact_prompt(result["positive"])
                    result["positive_original"] = result["positive"]
                    result["positive"] = compacted
                    result["compaction"] = meta

                self._send_json(200, result)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        else:
            self._send_json(404, {"error": "not found"})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt web_ui v{VERSION} — 本地 Web UI",
    )
    parser.add_argument("--host", default="127.0.0.1", help="监听地址（默认 127.0.0.1）")
    parser.add_argument("--port", type=int, default=7155, help="端口（默认 7155）")
    parser.add_argument("--no-browser", action="store_true", help="不自动开浏览器")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}"
    print(f"🌐 huo15-img-prompt Web UI v{VERSION}")
    print(f"   → {url}")
    print(f"   按 Ctrl+C 停止\n")

    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 已停止")
        server.shutdown()


if __name__ == "__main__":
    main()
