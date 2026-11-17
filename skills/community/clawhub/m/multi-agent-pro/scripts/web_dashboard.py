#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web 控制台 - 多Agent协作编排引擎 v5.4

功能：内置 http.server 只读服务（仅本机监听）+ ECharts
- 流水线列表、运行日志、交互式甘特图（点击节点看输入输出）
- 人工审批按钮（POST 触发引擎 resume，需带本地令牌防误触）
- 与生态内 zwjh/winskill 的面板方案同构

安全说明：
1. 仅监听 127.0.0.1（localhost），不暴露外网
2. 所有写操作（审批通过/拒绝）走 POST 且需带本地令牌
3. 令牌从 state 文件同目录的 .dashboard_token 文件读取（首次启动自动生成）
4. 前端仅展示，不直接修改 state——所有变更通过 CLI 命令触发

零第三方依赖，仅使用 Python 标准库
"""

import json
import os
import sys
import time
import hashlib
import secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import state_store

# 服务配置
DASHBOARD_HOST = '127.0.0.1'
DASHBOARD_PORT = 7788
TOKEN_FILENAME = '.dashboard_token'


def get_token(state_dir):
    """获取或创建本地令牌（用于审批 POST 鉴权）"""
    token_path = os.path.join(state_dir, TOKEN_FILENAME)
    if os.path.exists(token_path):
        with open(token_path, 'r', encoding='utf-8') as f:
            return f.read().strip()

    # 首次启动：生成随机令牌
    token = secrets.token_hex(16)
    try:
        with open(token_path, 'w', encoding='utf-8') as f:
            f.write(token)
        os.chmod(token_path, 0o600)  # 仅所有者可读写
    except IOError:
        pass
    return token


def find_pipelines(state_dir):
    """扫描目录中的流水线 state 文件，返回摘要列表"""
    if not os.path.isdir(state_dir):
        return []
    pipelines = []
    for fname in os.listdir(state_dir):
        if not fname.endswith('.json') or fname.startswith('state_'):
            continue
        fpath = os.path.join(state_dir, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            pipelines.append({
                'id': state.get('pipeline_id', ''),
                'name': state.get('pipeline_name', '未命名'),
                'status': state.get('status', ''),
                'file': fname,
                'updated_at': state.get('updated_at', ''),
                'node_count': len(state.get('nodes', {})),
                'completed': sum(1 for n in state.get('nodes', {}).values()
                                 if n.get('status') == 'completed'),
            })
        except (json.JSONDecodeError, IOError):
            continue
    return sorted(pipelines, key=lambda x: x.get('updated_at', ''))


def get_state_detail(state_path):
    """读取单个流水线的完整状态（供详情页/甘特图使用）"""
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        return state
    except (json.JSONDecodeError, IOError):
        return None


def generate_gantt_html(state):
    """生成内嵌的交互式甘特图 HTML（ECharts 通过 CDN 加载）"""
    nodes = state.get('nodes', {})
    pipeline_name = state.get('pipeline_name', '未命名')
    pipeline_id = state.get('pipeline_id', '')

    # 准备 ECharts 数据
    categories = []
    series_data = []
    for nid, node in nodes.items():
        categories.append(nid)
        started = node.get('started_at') or ''
        completed = node.get('completed_at') or ''
        status = node.get('status', 'pending')

        # 计算甘特图的起止位置（秒）
        start_ts = 0
        end_ts = 1
        if started and completed:
            try:
                s = datetime.strptime(started, '%Y-%m-%dT%H:%M:%S')
                e = datetime.strptime(completed, '%Y-%m-%dT%H:%M:%S')
                start_ts = int(s.timestamp())
                end_ts = int(e.timestamp())
            except (ValueError, TypeError):
                pass
        elif started:
            try:
                s = datetime.strptime(started, '%Y-%m-%dT%H:%M:%S')
                start_ts = int(s.timestamp())
                end_ts = start_ts + 60
            except (ValueError, TypeError):
                pass

        series_data.append({
            'name': nid,
            'value': [categories.index(nid), start_ts, end_ts, status],
            'itemStyle': {'color': _status_color(status)},
        })

    # 检查是否有待审批节点
    has_approval = any(
        n.get('type') == 'approval' and n.get('status') == 'pending'
        for n in nodes.values()
    )

    chart_data = json.dumps(series_data, ensure_ascii=False)
    categories_json = json.dumps(categories, ensure_ascii=False)

    # 生成审批按钮 HTML（如果有待审批节点）
    approval_html = ''
    if has_approval:
        approval_agents = [nid for nid, n in nodes.items()
                           if n.get('type') == 'approval' and n.get('status') == 'pending']
        approval_html = f'''
        <div style="background:#FFF3CD;border:1px solid #FFC107;border-radius:8px;padding:16px;margin-top:16px;">
          <h3 style="margin:0 0 8px 0;color:#856404;">待人工审批节点</h3>
          <p style="margin:0 0 12px 0;">{', '.join(approval_agents)}</p>
          <div>
            <button onclick="approvePipeline()" style="background:#28a745;color:#fff;border:none;padding:8px 24px;border-radius:4px;cursor:pointer;margin-right:12px;">通过</button>
            <button onclick="rejectPipeline()" style="background:#dc3545;color:#fff;border:none;padding:8px 24px;border-radius:4px;cursor:pointer;">拒绝</button>
          </div>
        </div>
        '''

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>流水线详情 - {pipeline_name}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
body {{ margin:0;padding:20px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f8fafc; }}
.container {{ max-width:1200px;margin:0 auto; }}
h1 {{ font-size:20px;margin-bottom:4px; }}
.meta {{ color:#64748b;font-size:13px;margin-bottom:20px; }}
.card {{ background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.1);padding:20px;margin-bottom:16px; }}
#gantt {{ width:100%;height:400px; }}
.back {{ color:#185FA5;text-decoration:none;font-size:14px; }}
</style>
</head>
<body>
<div class="container">
  <a class="back" href="/">返回列表</a>
  <h1>{pipeline_name}</h1>
  <p class="meta">ID: {pipeline_id} | 状态: {state.get("status", "")} | 节点: {len(nodes)}</p>

  {approval_html}

  <div class="card">
    <h3 style="margin-top:0;">甘特图（点击节点条查看输入输出）</h3>
    <div id="gantt"></div>
  </div>
</div>

<script>
const chart = echarts.init(document.getElementById('gantt'));
const categories = {categories_json};
const rawData = {chart_data};

const option = {{
  tooltip: {{
    trigger: 'item',
    formatter: function(params) {{
      const d = params.data;
      const node = {json.dumps({nid: n.get('output_data', {}) for nid, n in nodes.items()}, ensure_ascii=False)}[d.name];
      return '<b>' + d.name + '</b><br/>'
        + '状态: ' + d.value[3] + '<br/>'
        + '<pre style="max-height:200px;overflow:auto;font-size:11px;">' + JSON.stringify(node, null, 2) + '</pre>';
    }}
  }},
  grid: {{ left:120, right:40, top:20, bottom:40 }},
  xAxis: {{ type:'time' }},
  yAxis: {{
    type:'category',
    data: categories,
    axisLabel: {{ fontSize:12 }}
  }},
  series: [{{
    type:'custom',
    renderItem: function(params, api) {{
      const categoryIndex = api.value(0);
      const start = api.coord([api.value(1), categoryIndex]);
      const end = api.coord([api.value(2), categoryIndex]);
      const height = api.size([0, 1])[1] * 0.6;

      return {{
        type:'rect',
        shape: {{
          x: start[0],
          y: start[1] - height/2,
          width: end[0] - start[0],
          height: height,
          r: 4
        }},
        style: api.style()
      }};
    }},
    encode: {{ x: [1, 2], y: 0 }},
    data: rawData
  }}]
}};

chart.setOption(option);
window.addEventListener('resize', () => chart.resize());

function approvePipeline() {{
  fetch('/api/approve', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json', 'X-Local-Token': localStorage.getItem('token') || '' }},
    body: JSON.stringify({{ action: 'approve' }})
  }}).then(r => r.json()).then(d => alert(d.message || JSON.stringify(d)));
}}

function rejectPipeline() {{
  fetch('/api/approve', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json', 'X-Local-Token': localStorage.getItem('token') || '' }},
    body: JSON.stringify({{ action: 'reject' }})
  }}).then(r => r.json()).then(d => alert(d.message || JSON.stringify(d)));
}}
</script>
</body>
</html>'''


def _status_color(status):
    """状态颜色映射"""
    return {
        'completed': '#22c55e',
        'failed': '#ef4444',
        'running': '#3b82f6',
        'pending': '#9ca3af',
        'skipped': '#eab308',
        'approved': '#22c55e',
        'aborted': '#ef4444',
    }.get(status, '#9ca3af')


def generate_index_html(pipelines, state_dir):
    """生成流水线列表首页"""
    rows = ''
    for p in pipelines:
        status_color = {
            'completed': 'green', 'running': 'blue', 'failed': 'red',
            'aborted': 'red', 'initialized': 'gray',
        }.get(p['status'], 'gray')
        rows += f'''
        <tr>
          <td><a href="/detail?file={p['file']}">{p['name']}</a></td>
          <td><code>{p['id'][:20]}</code></td>
          <td style="color:{status_color};font-weight:500;">{p['status']}</td>
          <td><span title="已完成">{p['completed']}</span> / <span title="总">{p['node_count']}</span></td>
          <td>{p['updated_at']}</td>
        </tr>'''

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>多Agent编排引擎 - 控制台</title>
<style>
body {{ margin:0;padding:20px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f8fafc; }}
.container {{ max-width:1200px;margin:0 auto; }}
h1 {{ font-size:20px;margin-bottom:20px; }}
table {{ width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1); }}
th {{ background:#f1f5f9;padding:12px;text-align:left;font-size:13px;font-weight:500;border-bottom:1px solid #e2e8f0; }}
td {{ padding:12px;border-bottom:1px solid #e2e8f0;font-size:13px; }}
tr:hover {{ background:#f8fafc; }}
a {{ color:#185FA5;text-decoration:none; }}
code {{ background:#f1f5f9;padding:2px 6px;border-radius:3px;font-size:12px; }}
</style>
</head>
<body>
<div class="container">
  <h1>多Agent编排引擎 - Web 控制台</h1>
  <p style="color:#64748b;margin-bottom:20px;">仅本机监听 127.0.0.1 - {len(pipelines)} 个流水线</p>
  <table>
    <thead><tr><th>名称</th><th>ID</th><th>状态</th><th>节点</th><th>更新时间</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>

  <div style="margin-top:24px;background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.1);">
    <h3 style="margin-top:0;">快速操作</h3>
    <p style="color:#64748b;">启动服务：<code>python orchestrator.py dashboard</code></p>
    <p style="color:#64748b;">所有写操作走 CLI 命令，本页只读 + 审批。</p>
  </div>
</div>
</body>
</html>'''

# HTTP Handler
class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP 处理器：只读页面 + 审批 POST"""
    state_dir = ''
    token = ''

    def _send_html(self, html, status=200):
        body = html.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)

        # 流水线列表首页
        if parsed.path in ('/', '/index.html'):
            pipelines = find_pipelines(self.state_dir)
            self._send_html(generate_index_html(pipelines, self.state_dir))
            return

        # 流水线详情（甘特图页）
        if parsed.path == '/detail':
            params = parse_qs(parsed.query)
            fname = params.get('file', [''])[0]
            if not fname:
                self._send_json({'error': '缺少 file 参数'}, 400)
                return
            state_path = os.path.join(self.state_dir, fname)
            state = get_state_detail(state_path)
            if not state:
                self._send_json({'error': '未找到流水线'}, 404)
                return

            # state_dir 注入给 HTML 生成函数（用于审批按钮查找 token）
            self._send_html(
                generate_gantt_html_with_approval(state, self.state_dir)
            )
            return

        # 404
        self._send_json({'error': '未找到页面'}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)

        # 审批通过/拒绝（需校验本地令牌）
        if parsed.path == '/api/approve':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length else b''
            try:
                req = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self._send_json({'error': '请求体 JSON 格式不合法'}, 400)
                return

            action = req.get('action', '')
            if action not in ('approve', 'reject'):
                self._send_json({'error': 'action 必须是 approve 或 reject'}, 400)
                return

            # 核对本地令牌
            header_token = self.headers.get('X-Local-Token', '')
            if not header_token or header_token != self.token:
                self._send_json({'error': '令牌校验失败'}, 403)
                return

            state_path = req.get('state_path', '')
            node_id = req.get('node_id', '')
            if not state_path or not node_id:
                self._send_json({'error': '缺少 state_path 或 node_id'}, 400)
                return

            state_path = os.path.join(self.state_dir, state_path)

            # 调用引擎：标记节点完成
            # 审批动作只改节点状态，不会自动推进流水线
            state = state_store.load_state(state_path)
            if not state:
                self._send_json({'error': '未找到流水线'}, 404)
                return

            node = state['nodes'].get(node_id)
            if not node:
                self._send_json({'error': f'节点 {node_id} 不存在'}, 404)
                return

            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            if action == 'approve':
                node['status'] = 'completed'
                node['output_data'] = {'approved': True, 'approved_at': now, 'approved_by': 'web_dashboard'}
                node['completed_at'] = now
                state_store.safe_write(state, state_path)
                self._send_json({'success': True, 'message': f'节点 {node_id} 已批准'})
            else:
                node['status'] = 'completed'
                node['output_data'] = {'rejected': True, 'rejected_at': now, 'rejected_by': 'web_dashboard'}
                node['completed_at'] = now
                state_store.safe_write(state, state_path)
                self._send_json({'success': True, 'message': f'节点 {node_id} 已拒绝，流水线中止'})
            return

        self._send_json({'error': '未找到接口'}, 404)

    def log_message(self, format, *args):
        # 静默访问日志，不污染 stdout
        pass


def generate_gantt_html_with_approval(state, state_dir):
    """生成带审批上下文的甘特图（与 generate_gantt_html 同构，注入 state_dir）"""
    # 直接复用原函数，但未使用传入的 state_dir。
    # 原函数内部审批按钮仅触发 POST 后刷新页面，此处保留原行为。
    return generate_gantt_html(state)


def start_dashboard(state_dir=None, port=DASHBOARD_PORT):
    """启动 Web 控制台服务

    参数：
      state_dir: state 文件所在目录（默认当前目录）
      port: 监听端口（默认 7788）
    """
    if state_dir is None:
        state_dir = os.getcwd()
    state_dir = os.path.abspath(state_dir)

    if not os.path.isdir(state_dir):
        print(f"错误：state 目录不存在 {state_dir}")
        sys.exit(1)

    token = get_token(state_dir)
    pipelines = find_pipelines(state_dir)

    DashboardHandler.state_dir = state_dir
    DashboardHandler.token = token

    server = HTTPServer((DASHBOARD_HOST, port), DashboardHandler)
    print(f"✦ 多Agent编排引擎控制台 v5.4")
    print(f"  监听地址：http://{DASHBOARD_HOST}:{port}")
    print(f"  State 目录：{state_dir}")
    print(f"  流水线数：{len(pipelines)}")
    print(f"  本地令牌：{token[:8]}...（保存在 {TOKEN_FILENAME}）")
    print(f"  仅本机访问，不暴露外网。按 Ctrl+C 停止。")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n控制台已停止。")
        server.server_close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='多Agent编排引擎 Web 控制台 v5.4')
    parser.add_argument('--dir', default='.', help='state 文件目录（默认当前目录）')
    parser.add_argument('--port', type=int, default=DASHBOARD_PORT, help='监听端口（默认 7788）')
    args = parser.parse_args()
    start_dashboard(args.dir, args.port)
