#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from config import build_ssh_tunnel_command, build_web_url, get_runtime_summary, load_install_info
from runtime_state import build_page_state, parse_basic_auth
from channel_store import activate_channel, create_channel, export_channel_auth, import_channel_auth
from oauth_flow import oauth_status_label, read_oauth_sessions, start_oauth_session, submit_oauth_callback
from version_info import get_public_version

HOST = os.environ.get('OPENAI_AUTH_SWITCHER_HOST', '127.0.0.1')
PORT = int(os.environ.get('OPENAI_AUTH_SWITCHER_PORT', '9527'))


def is_authorized(handler: BaseHTTPRequestHandler) -> bool:
    install = load_install_info()
    expected_user = install.get('username', 'admin')
    expected_password = install.get('password', '')
    creds = parse_basic_auth(handler.headers.get('Authorization'))
    return bool(creds and creds[0] == expected_user and creds[1] == expected_password)


def require_auth(handler: BaseHTTPRequestHandler) -> bool:
    if is_authorized(handler):
        return True
    handler.send_response(401)
    handler.send_header('WWW-Authenticate', 'Basic realm="OpenAI Auth Switcher Public"')
    handler.end_headers()
    return False


def build_html() -> str:
    install = load_install_info()
    version = get_public_version()
    summary = get_runtime_summary()
    runtime = summary['runtime']
    mode = summary['mode']
    auth_ready = summary['auth_ready']
    username = install.get('username', 'admin')
    password = install.get('password', '<generated-at-install>')
    port = install.get('port', PORT)
    local_url = build_web_url('127.0.0.1', int(port))
    ssh_cmd = build_ssh_tunnel_command(int(port))
    page_state = build_page_state()
    channels = page_state.get('channels') or []
    oauth_sessions = read_oauth_sessions()
    pending_session = next((item for item in reversed(oauth_sessions) if item.get('status') in ('starting', 'waiting_callback', 'processing')), None)
    oauth_session_items = ''.join(
      f"<div class='oauth-session-item'><div><strong>{item.get('displayName') or item.get('slot')}</strong></div><div class='muted'>状态：{oauth_status_label(item.get('status'))} · 通道：{item.get('slot')}</div><div class='muted'>任务ID：{item.get('sessionId')}</div></div>"
      for item in reversed(oauth_sessions[-5:])
    ) or "<div class='muted'>暂无授权任务</div>"
    channel_summary = page_state.get('channel_summary') or {}
    current_slot = channel_summary.get('current_slot')
    live_current = channel_summary.get('live_current_account') or {}
    headline = '账号通道管理台'
    lead = '安装完成后，你可以直接新增账号通道、查看当前通道，并逐步接入一键切换能力。'
    service = install.get('service') or {}
    service_mode = service.get('mode', 'unknown')
    service_ready = bool(install.get('ready') or service.get('ready') or service.get('ok'))
    mode_badge = '<span class="badge badge-warn">账号尚未接入</span>' if not auth_ready else '<span class="badge badge-ok">账号已接入</span>'
    service_badge = '<span class="badge badge-ok">服务已就绪</span>' if service_ready else '<span class="badge badge-warn">服务启动中</span>'
    current_channel_card = f'''
      <section class="panel">
        <h2>当前通道</h2>
        <div class="kv">
          <div><strong>当前选中通道：</strong>{current_slot or '未设置'}</div>
          <div><strong>当前已接管账号：</strong>{live_current.get('account_id') or '暂无'}</div>
          <div><strong>通道总数：</strong>{len(channels)}</div>
        </div>
      </section>
    '''
    empty_state = '''
      <section class="panel warn">
        <h2>还没有账号通道</h2>
        <p>你现在可以直接点击“新增账号”，先创建一个空通道。后续再补授权或接入信息。</p>
      </section>
    ''' if not channels else ''
    channel_items = ''.join(
      f"<div class='channel-item'><div><div class='channel-title'>{row.get('display_name') or row.get('slot')}</div><div class='muted'>通道标识：{row.get('slot')} · 状态：{'已授权' if row.get('has_auth_file') else '待授权'} · {'当前通道' if row.get('is_current') else '未选中'}</div><div class='muted'>账号ID：{row.get('account_id') or '未配置'}</div></div><div class='toolbar'><button type='button' class='activate-channel-btn' data-slot='{row.get('slot')}'>设为当前</button><button type='button' class='oauth-start-btn' data-slot='{row.get('slot')}' data-name='{row.get('display_name') or row.get('slot')}'>开始授权</button><button type='button' class='oauth-finish-btn' data-slot='{row.get('slot')}'>完成授权</button></div></div>"
      for row in channels
    ) or "<div class='muted'>暂无通道</div>"
    channel_list_panel = f'''
      <section class="panel">
        <h2>账号通道列表</h2>
        <div class="channel-list">{channel_items}</div>
      </section>
    '''
    create_panel = '''
      <section class="panel">
        <h2>新增账号</h2>
        <form id="create-channel-form">
          <label class="label">账号名称</label>
          <input id="channel-name" type="text" placeholder="例如：主账号A" />
          <label class="label">邮箱 / 标识（可选）</label>
          <input id="channel-email" type="text" placeholder="例如：xxx@example.com" />
          <label class="label">备注（可选）</label>
          <input id="channel-note" type="text" placeholder="例如：备用 / 测试 / 主力" />
          <button type="submit">新增账号通道</button>
        </form>
        <div id="create-channel-result" class="muted"></div>
      </section>
    '''
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OpenAI Auth Switcher Public {version}</title>
  <style>
    :root {{
      --bg: #f4f9ff;
      --card: rgba(255,255,255,.82);
      --card-strong: #ffffff;
      --line: rgba(148,184,255,.24);
      --text: #12304f;
      --muted: #5f7694;
      --primary: #2563eb;
      --primary-soft: #dbeafe;
      --warn-bg: #fff7ed;
      --warn-line: #fdba74;
      --ok-bg: #dcfce7;
      --ok-text: #166534;
      --shadow: 0 18px 42px rgba(59,130,246,.12);
    }}
    * {{ box-sizing:border-box; }}
    body {{
      font-family: Arial, sans-serif;
      margin:0;
      color:var(--text);
      background:
        radial-gradient(circle at top right, rgba(125,211,252,.22), transparent 26%),
        radial-gradient(circle at top left, rgba(191,219,254,.28), transparent 22%),
        linear-gradient(180deg,#f8fbff 0%,var(--bg) 100%);
    }}
    .wrap {{ max-width: 1120px; margin:0 auto; padding:20px; }}
    .hero, .panel {{
      background:var(--card);
      border:1px solid var(--line);
      box-shadow:var(--shadow);
      backdrop-filter: blur(16px);
    }}
    .hero {{ border-radius:22px; padding:22px; margin-bottom:16px; }}
    .hero h1 {{ margin:10px 0 8px; color:var(--text); }}
    .hero p {{ margin:0; color:var(--muted); line-height:1.7; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }}
    .panel {{ border-radius:18px; padding:18px; margin-bottom:16px; }}
    .warn {{ border:1px solid var(--warn-line); background:var(--warn-bg); }}
    pre {{ background:#eaf4ff; color:#16365d; padding:12px; border-radius:14px; overflow:auto; white-space:pre-wrap; border:1px solid rgba(147,197,253,.28); }}
    .kv {{ line-height:1.9; word-break:break-word; }}
    .pill {{ display:inline-block; padding:5px 10px; border-radius:999px; background:var(--primary-soft); color:var(--primary); font-size:12px; font-weight:700; }}
    .badge {{ display:inline-block; padding:5px 10px; border-radius:999px; font-size:12px; font-weight:700; }}
    .badge-ok {{ background:var(--ok-bg); color:var(--ok-text); }}
    .badge-warn {{ background:#fef3c7; color:#92400e; }}
    .status-row {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:12px; }}
    .status-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; margin-top:16px; }}
    .status-card {{ background:rgba(255,255,255,.72); border:1px solid rgba(147,197,253,.26); border-radius:16px; padding:14px; }}
    .status-card .k {{ font-size:12px; color:var(--muted); margin-bottom:6px; font-weight:700; }}
    .status-card .v {{ font-size:16px; font-weight:800; word-break:break-word; color:var(--text); }}
    h2 {{ margin-top:0; }}
    .label {{ display:block; font-size:12px; font-weight:700; margin-bottom:6px; color:#475569; }}
    input {{ width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:12px; box-sizing:border-box; margin-bottom:10px; background:#fff; }}
    .toolbar {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:10px; }}
    .channel-list {{ display:flex; flex-direction:column; gap:12px; }}
    .channel-item {{ display:flex; justify-content:space-between; gap:12px; align-items:center; padding:14px; border:1px solid rgba(147,197,253,.28); border-radius:14px; background:rgba(255,255,255,.72); }}
    .channel-title {{ font-size:16px; font-weight:800; }}
    .flash {{ margin:0 0 16px; padding:14px 16px; border-radius:14px; border:1px solid rgba(147,197,253,.28); background:#eff6ff; display:none; }}
    .flash.show {{ display:block; }}
    .flash.success {{ background:#ecfdf5; border-color:#86efac; color:#166534; }}
    .flash.error {{ background:#fef2f2; border-color:#fca5a5; color:#991b1b; }}
    .flash.warn {{ background:#fff7ed; border-color:#fdba74; color:#9a3412; }}
    .auth-box {{ margin-top:16px; padding:16px; border-radius:16px; border:1px solid rgba(147,197,253,.28); background:#f8fbff; }}
    .oauth-session-list {{ display:flex; flex-direction:column; gap:10px; margin-top:14px; }}
    .oauth-session-item {{ padding:12px; border-radius:12px; background:rgba(255,255,255,.72); border:1px solid rgba(147,197,253,.28); }}
    textarea {{ width:100%; min-height:88px; padding:12px; border:1px solid #cbd5e1; border-radius:12px; box-sizing:border-box; background:#fff; resize:vertical; }}
    .copy-link {{ word-break:break-all; font-weight:700; color:#1d4ed8; }}
    button {{ padding:11px 15px; border:none; border-radius:12px; background:linear-gradient(135deg,#3b82f6 0%,#2563eb 100%); color:#fff; font-weight:700; cursor:pointer; box-shadow:0 10px 22px rgba(37,99,235,.16); }}
    button:hover {{ filter:brightness(.98); }}
    .muted {{ color:var(--muted); font-size:12px; margin-top:8px; }}
    .success {{ color:#166534; }}
    .error {{ color:#991b1b; }}
    @media (max-width: 900px) {{ .grid {{ grid-template-columns:1fr; }} .status-grid {{ grid-template-columns:1fr; }} }}
    @media (max-width: 640px) {{ .wrap {{ padding:14px; }} .hero, .panel {{ padding:16px; border-radius:16px; }} .status-row, .toolbar {{ flex-direction:column; align-items:stretch; }} button {{ width:100%; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <div id="flash-message" class="flash"></div>
    <div class="hero">
      <span class="pill">{version}</span>
      <h1>OpenAI Auth Switcher Public</h1>
      <p>{headline}：{lead}</p>
      <div class="status-row">{mode_badge}{service_badge}<span class="pill">端口 {port}</span><span class="pill">服务模式 {service_mode}</span></div>
      <div class="status-grid">
        <div class="status-card"><div class="k">当前运行模式</div><div class="v">{'预览管理台' if mode else '未知'}</div></div>
        <div class="status-card"><div class="k">服务状态</div><div class="v">{'已就绪' if service_ready else '启动中'}</div></div>
        <div class="status-card"><div class="k">下一步</div><div class="v">{'新增账号并开始授权' if not auth_ready else '选择账号后开始授权或设为当前'}</div></div>
        <div class="status-card"><div class="k">本地地址</div><div class="v">{local_url}</div></div>
        <div class="status-card"><div class="k">登录用户名</div><div class="v">{username}</div></div>
        <div class="status-card"><div class="k">数据目录</div><div class="v">{summary['state_base_dir']}</div></div>
        <div class="status-card"><div class="k">系统托管状态</div><div class="v">{service.get('status', {}).get('active_state', 'n/a')}</div></div>
        <div class="status-card"><div class="k">托管子状态</div><div class="v">{service.get('status', {}).get('sub_state', 'n/a')}</div></div>
        <div class="status-card"><div class="k">日志文件</div><div class="v">{service.get('log_path', 'n/a')}</div></div>
      </div>
    </div>

    <details class="panel">
      <summary><strong>安装与连接信息（高级）</strong></summary>
      <div class="grid" style="margin-top:16px;">
        <section class="panel">
          <h2>安装信息</h2>
          <div class="kv">
            <div><strong>本地地址：</strong>{local_url}</div>
            <div><strong>默认用户名：</strong>{username}</div>
            <div><strong>默认密码：</strong>{password}</div>
            <div><strong>模式：</strong>{mode}</div>
            <div><strong>服务模式：</strong>{service_mode}</div>
            <div><strong>服务就绪：</strong>{'yes' if service_ready else 'no'}</div>
            <div><strong>ActiveState：</strong>{service.get('status', {}).get('active_state', 'n/a')}</div>
            <div><strong>SubState：</strong>{service.get('status', {}).get('sub_state', 'n/a')}</div>
            <div><strong>日志文件：</strong>{service.get('log_path', 'n/a')}</div>
            <div><strong>状态目录：</strong>{summary['state_base_dir']}</div>
          </div>
        </section>
        <section class="panel">
          <h2>SSH 隧道</h2>
          <pre>{ssh_cmd}</pre>
          <div>本地浏览器打开：<strong>{local_url}</strong></div>
        </section>
      </div>
    </details>

    <div class="grid">
      {current_channel_card}
      {create_panel}
    </div>

    {empty_state}
    {channel_list_panel}

    <section class="panel" id="oauth-panel">
      <h2>账号授权</h2>
      <div class="muted">主流程：新增账号 → 开始授权 → 浏览器完成登录 → 粘贴回调地址 → 设为当前</div>
      <div class="auth-box">
        <div><strong>当前授权对象：</strong><span id="oauth-target">{(pending_session or {}).get('displayName') or (pending_session or {}).get('slot') or '未选择'}</span></div>
        <div class="muted">当前授权状态：<span id="oauth-status">{(pending_session or {}).get('status') or '暂无待授权任务'}</span></div>
        <div class="toolbar">
          <button type="button" id="oauth-start-current">开始授权</button>
        </div>
        <div id="oauth-link-wrap" class="muted" style="margin-top:10px; display:{'block' if (pending_session or {}).get('authUrl') else 'none'};">
          <div><strong>授权链接：</strong></div>
          <div id="oauth-link" class="copy-link">{(pending_session or {}).get('authUrl') or ''}</div>
        </div>
        <div style="margin-top:12px;">
          <label class="label">完成授权后，把浏览器最后跳转的网址完整粘到这里</label>
          <textarea id="oauth-callback" placeholder="例如：http://localhost:1455/auth/callback?code=...&state=..."></textarea>
          <div class="toolbar">
            <button type="button" id="oauth-submit-current">提交回调并完成授权</button>
          </div>
          <div class="muted" style="margin-top:8px;">如果你刚完成登录，看见浏览器跳回一个地址，把完整地址粘贴到上面即可。</div>
        </div>
        <div class="oauth-session-list">
          {oauth_session_items}
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>高级入口</h2>
      <div class="muted">这里保留给高级用户的兼容能力，可直接导入/导出授权文件。</div>
      <div class="toolbar">
        <button type="button" id="advanced-import-btn">导入授权文件</button>
        <button type="button" id="advanced-export-btn">导出当前通道授权文件</button>
      </div>
      <pre id="runtime-json">{json.dumps(runtime, ensure_ascii=False, indent=2)}</pre>
    </section>
  </div>
  <script>
    const API_BASE = window.location.origin;
    const BASIC_AUTH = 'Basic ' + btoa('{username}:{password}');
    async function apiFetch(path, options = {{}}) {{
      const headers = Object.assign({{}}, options.headers || {{}}, {{ 'Authorization': BASIC_AUTH }});
      return fetch(API_BASE + path, Object.assign({{}}, options, {{ headers }}));
    }}
    function showFlash(message, level='success') {{
      const box = document.getElementById('flash-message');
      if (!box) return;
      box.className = 'flash show ' + level;
      box.textContent = message;
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}
    async function reloadState() {{
      try {{
        const resp = await apiFetch('/api/state');
        const data = await resp.json();
        const runtimeEl = document.getElementById('runtime-json');
        if (runtimeEl) runtimeEl.textContent = JSON.stringify(data.runtime.runtime, null, 2);
        return data;
      }} catch (err) {{
        return null;
      }}
    }}
    const createForm = document.getElementById('create-channel-form');
    if (createForm) {{
      createForm.addEventListener('submit', async (e) => {{
        e.preventDefault();
        const name = document.getElementById('channel-name').value.trim();
        const email = document.getElementById('channel-email').value.trim();
        const note = document.getElementById('channel-note').value.trim();
        const resultEl = document.getElementById('create-channel-result');
        resultEl.textContent = '正在新增账号通道...';
        resultEl.className = 'muted';
        try {{
          const resp = await apiFetch('/api/create-channel', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ name, email, note }})
          }});
          const data = await resp.json();
          if (data.ok) {{
            resultEl.textContent = '新增成功，页面将在 1 秒后刷新。';
            resultEl.className = 'muted success';
            setTimeout(() => window.location.reload(), 1000);
          }} else {{
            resultEl.textContent = '新增失败：' + (data.error || '未知错误');
            resultEl.className = 'muted error';
          }}
        }} catch (err) {{
          resultEl.textContent = '新增失败：' + err;
          resultEl.className = 'muted error';
        }}
      }});
    }}
    document.querySelectorAll('.activate-channel-btn').forEach((btn) => {{
      btn.addEventListener('click', async () => {{
        const slot = btn.getAttribute('data-slot');
        const oldText = btn.textContent;
        btn.disabled = true;
        btn.textContent = '切换中...';
        try {{
          const resp = await apiFetch('/api/activate-channel', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ slot }})
          }});
          const data = await resp.json();
          showFlash(data.message || (data.ok ? '切换成功' : '切换失败'), data.ok ? 'success' : 'warn');
          if (data.ok) {{
            setTimeout(() => window.location.reload(), 800);
          }} else {{
            btn.disabled = false;
            btn.textContent = oldText;
          }}
        }} catch (err) {{
          showFlash('切换失败：' + err, 'error');
          btn.disabled = false;
          btn.textContent = oldText;
        }}
      }});
    }});
    let focusedSlot = null;
    let latestPendingSessionId = null;
    function focusOauthSlot(slot, displayName) {{
      focusedSlot = slot;
      document.getElementById('oauth-target').textContent = `${{displayName || slot}}（${{slot}}）`;
      document.getElementById('oauth-panel').scrollIntoView({{ behavior: 'smooth' }});
    }}
    function oauthStatusText(status) {{
      switch (status) {{
        case 'starting': return '正在生成授权链接';
        case 'waiting_callback': return '等待完成授权';
        case 'processing': return '正在处理回调';
        case 'completed': return '已完成授权';
        case 'failed': return '授权失败';
        case 'superseded': return '已被新的授权任务替代';
        default: return status || '未知状态';
      }}
    }}
    async function startOauthFor(slot, displayName) {{
      focusOauthSlot(slot, displayName);
      showFlash('正在生成授权链接，请稍等…', 'warn');
      const resp = await apiFetch('/api/oauth/start', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ slot, display_name: displayName || slot }})
      }});
      const data = await resp.json();
      if (!data.ok) {{
        showFlash('生成授权链接失败：' + (data.error || '未知错误'), 'error');
        return;
      }}
      latestPendingSessionId = data?.session?.sessionId || null;
      const authUrl = data?.session?.authUrl || '';
      const authStatus = data?.session?.status || 'waiting_callback';
      const linkWrap = document.getElementById('oauth-link-wrap');
      const linkEl = document.getElementById('oauth-link');
      const statusEl = document.getElementById('oauth-status');
      if (statusEl) statusEl.textContent = oauthStatusText(authStatus);
      if (authUrl) {{
        linkWrap.style.display = 'block';
        linkEl.textContent = authUrl;
      }}
      showFlash('授权链接已生成，请打开链接完成登录。', 'success');
    }}
    async function submitOauthCallback() {{
      const callback_url = document.getElementById('oauth-callback').value.trim();
      if (!latestPendingSessionId) return showFlash('当前没有等待中的授权任务，请先点“开始授权”。', 'warn');
      if (!callback_url) return showFlash('请先粘贴登录完成后的地址。', 'warn');
      showFlash('正在提交授权结果，请稍等…', 'warn');
      const resp = await apiFetch('/api/oauth/callback-submit', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ sessionId: latestPendingSessionId, callback_url }})
      }});
      const data = await resp.json();
      showFlash(data.message || (data.ok ? '授权完成，账号已接入。' : ('授权失败：' + (data.error || '未知错误'))), data.ok ? 'success' : 'error');
      if (data.ok) setTimeout(() => window.location.reload(), 1000);
    }}
    document.querySelectorAll('.oauth-start-btn').forEach((btn) => {{
      btn.addEventListener('click', async () => {{
        await startOauthFor(btn.getAttribute('data-slot'), btn.getAttribute('data-name'));
      }});
    }});
    document.querySelectorAll('.oauth-finish-btn').forEach((btn) => {{
      btn.addEventListener('click', async () => {{
        focusOauthSlot(btn.getAttribute('data-slot'), btn.getAttribute('data-slot'));
      }});
    }});
    const oauthStartCurrent = document.getElementById('oauth-start-current');
    if (oauthStartCurrent) {{
      oauthStartCurrent.addEventListener('click', async () => {{
        if (!focusedSlot) return showFlash('请先在列表中选择一个账号，再开始授权。', 'warn');
        await startOauthFor(focusedSlot, focusedSlot);
      }});
    }}
    const oauthSubmitCurrent = document.getElementById('oauth-submit-current');
    if (oauthSubmitCurrent) {{
      oauthSubmitCurrent.addEventListener('click', submitOauthCallback);
    }}
    const advancedImportBtn = document.getElementById('advanced-import-btn');
    if (advancedImportBtn) {{
      advancedImportBtn.addEventListener('click', async () => {{
        if (!focusedSlot) return showFlash('请先在列表中选择一个账号通道。', 'warn');
        const source = window.prompt('请输入要导入的授权文件路径');
        if (!source) return;
        const resp = await apiFetch('/api/advanced/import-auth', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ slot: focusedSlot, source }})
        }});
        const data = await resp.json();
        showFlash(data.ok ? '高级导入成功，页面即将刷新。' : ('高级导入失败：' + (data.error || '未知错误')), data.ok ? 'success' : 'error');
        if (data.ok) setTimeout(() => window.location.reload(), 1000);
      }});
    }}
    const advancedExportBtn = document.getElementById('advanced-export-btn');
    if (advancedExportBtn) {{
      advancedExportBtn.addEventListener('click', async () => {{
        if (!focusedSlot) return showFlash('请先在列表中选择一个账号通道。', 'warn');
        const resp = await apiFetch('/api/advanced/export-auth', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ slot: focusedSlot }})
        }});
        const data = await resp.json();
        showFlash(data.ok ? ('授权文件路径：' + data.path) : ('导出失败：' + (data.error || '未知错误')), data.ok ? 'success' : 'error');
      }});
    }}
  </script>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not require_auth(self):
            return
        if self.path in ('/', '/index.html'):
            body = build_html().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/state':
            body = json.dumps(build_page_state(), ensure_ascii=False, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/health':
            payload = {'ok': True, 'service': 'openai-auth-switcher-public-web-preview'}
            body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/channels':
            body = json.dumps(build_page_state().get('channels', []), ensure_ascii=False, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/oauth-sessions':
            body = json.dumps({'ok': True, 'items': read_oauth_sessions()}, ensure_ascii=False, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if not require_auth(self):
            return
        if self.path == '/api/create-channel':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            name = (payload.get('name') or '').strip()
            email = (payload.get('email') or '').strip()
            note = (payload.get('note') or '').strip()
            if not name:
                body = json.dumps({'ok': False, 'error': 'missing name'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            try:
                result = create_channel(name, email=email, note=note)
                body = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
            except Exception as e:
                body = json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/activate-channel':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            slot = (payload.get('slot') or '').strip()
            if not slot:
                body = json.dumps({'ok': False, 'error': 'missing slot'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            try:
                result = activate_channel(slot)
                body = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200 if result.get('ok') else 400)
            except Exception as e:
                body = json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/import-channel-auth':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            slot = (payload.get('slot') or '').strip()
            source = (payload.get('source') or '').strip()
            if not slot or not source:
                body = json.dumps({'ok': False, 'error': 'missing slot or source'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            try:
                result = import_channel_auth(slot, source)
                body = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
            except Exception as e:
                body = json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/oauth/start':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            slot = (payload.get('slot') or '').strip()
            display_name = (payload.get('display_name') or slot).strip()
            if not slot:
                body = json.dumps({'ok': False, 'error': 'missing slot'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
            else:
                result = start_oauth_session(slot, display_name)
                body = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200 if result.get('ok') else 400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/oauth/callback-submit':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            session_id = (payload.get('sessionId') or '').strip()
            callback_url = (payload.get('callback_url') or '').strip()
            if not session_id or not callback_url:
                body = json.dumps({'ok': False, 'error': 'missing sessionId or callback_url'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
            else:
                result = submit_oauth_callback(session_id, callback_url)
                body = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200 if result.get('ok') else 400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/advanced/import-auth':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            slot = (payload.get('slot') or '').strip()
            source = (payload.get('source') or '').strip()
            if not slot or not source:
                body = json.dumps({'ok': False, 'error': 'missing slot or source'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
            else:
                try:
                    result = import_channel_auth(slot, source)
                    body = json.dumps(result, ensure_ascii=False).encode('utf-8')
                    self.send_response(200)
                except Exception as e:
                    body = json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8')
                    self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/advanced/export-auth':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            slot = (payload.get('slot') or '').strip()
            if not slot:
                body = json.dumps({'ok': False, 'error': 'missing slot'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
            else:
                try:
                    result = export_channel_auth(slot)
                    body = json.dumps(result, ensure_ascii=False).encode('utf-8')
                    self.send_response(200)
                except Exception as e:
                    body = json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8')
                    self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'OpenAI Auth Switcher Public web preview listening on http://{HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
