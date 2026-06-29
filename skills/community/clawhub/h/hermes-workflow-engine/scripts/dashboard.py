"""
Hermes Workflow Dashboard Generator v1.0
可视化面板 — 生成HTML实时执行状态面板
"""

import json
from pathlib import Path
from datetime import datetime


def generate_dashboard(run_dir: str = None, state: dict = None) -> str:
    """生成HTML可视化面板"""
    if run_dir:
        state_path = Path(run_dir) / 'state.json'
        if state_path.exists():
            state = json.loads(state_path.read_text())

    if not state:
        state = {
            'workflow': 'unknown',
            'status': 'created',
            'step_status': {},
            'progress': {'total': 0, 'done': 0, 'failed': 0, 'running': 0, 'paused': 0, 'percent': 0},
        }

    workflow_name = state.get('workflow', 'unknown')
    status = state.get('status', 'created')
    progress = state.get('progress', {})
    step_status = state.get('step_status', {})
    step_outputs = state.get('step_outputs', {})
    step_errors = state.get('step_errors', {})
    updated_at = state.get('updated_at', '')

    # 步骤状态颜色
    status_colors = {
        'pending': '#6b7280',
        'waiting': '#9ca3af',
        'ready': '#60a5fa',
        'running': '#f59e0b',
        'success': '#10b981',
        'failed': '#ef4444',
        'skipped': '#9ca3af',
        'paused': '#8b5cf6',
    }

    status_icons = {
        'pending': '⏳',
        'waiting': '⏸️',
        'ready': '🔵',
        'running': '🔄',
        'success': '✅',
        'failed': '❌',
        'skipped': '⏭️',
        'paused': '⏸️',
    }

    # 生成步骤HTML
    steps_html = ""
    for sid, sstatus in step_status.items():
        color = status_colors.get(sstatus, '#6b7280')
        icon = status_icons.get(sstatus, '⏳')
        error_html = ""
        if sid in step_errors:
            error_html = f'<div class="step-error">❌ {step_errors[sid][:100]}</div>'
        output_html = ""
        if sid in step_outputs:
            out = str(step_outputs[sid])[:80]
            output_html = f'<div class="step-output">📤 {out}</div>'

        steps_html += f"""
        <div class="step-card" style="border-left: 4px solid {color}">
            <div class="step-header">
                <span class="step-icon">{icon}</span>
                <span class="step-name">{sid}</span>
                <span class="step-status" style="color: {color}">{sstatus}</span>
            </div>
            {output_html}
            {error_html}
        </div>
        """

    # 进度条
    pct = progress.get('percent', 0)
    bar_color = '#10b981' if pct == 100 else '#60a5fa' if pct > 0 else '#6b7280'

    # 状态标签
    status_tags = {
        'created': ('📋 已创建', '#6b7280'),
        'running': ('🔄 运行中', '#f59e0b'),
        'paused': ('⏸️ 已暂停', '#8b5cf6'),
        'success': ('✅ 成功', '#10b981'),
        'failed': ('❌ 失败', '#ef4444'),
        'aborted': ('🚫 已中止', '#ef4444'),
    }
    tag_text, tag_color = status_tags.get(status, (status, '#6b7280'))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Workflow Dashboard</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; padding: 20px; }}
  .dashboard {{ max-width: 900px; margin: 0 auto; }}
  .header {{ background: linear-gradient(135deg, #1e293b, #334155); border-radius: 16px; padding: 24px; margin-bottom: 20px; border: 1px solid #475569; }}
  .header h1 {{ font-size: 24px; margin-bottom: 8px; }}
  .header .tag {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 13px; background: {tag_color}22; color: {tag_color}; border: 1px solid {tag_color}44; }}
  .header .meta {{ color: #94a3b8; font-size: 13px; margin-top: 8px; }}
  .progress-section {{ background: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #334155; }}
  .progress-bar {{ height: 12px; background: #334155; border-radius: 6px; overflow: hidden; margin: 10px 0; }}
  .progress-fill {{ height: 100%; background: {bar_color}; border-radius: 6px; transition: width 0.3s; }}
  .progress-stats {{ display: flex; gap: 20px; font-size: 14px; color: #94a3b8; }}
  .progress-stats span {{ color: #e2e8f0; font-weight: 600; }}
  .steps {{ display: flex; flex-direction: column; gap: 10px; }}
  .step-card {{ background: #1e293b; border-radius: 10px; padding: 14px 18px; border: 1px solid #334155; }}
  .step-header {{ display: flex; align-items: center; gap: 10px; }}
  .step-icon {{ font-size: 18px; }}
  .step-name {{ font-weight: 600; flex: 1; }}
  .step-status {{ font-size: 13px; font-weight: 500; }}
  .step-output {{ font-size: 12px; color: #94a3b8; margin-top: 6px; padding: 6px 10px; background: #0f172a; border-radius: 6px; }}
  .step-error {{ font-size: 12px; color: #ef4444; margin-top: 6px; padding: 6px 10px; background: #451a1a; border-radius: 6px; }}
  .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #475569; }}
</style>
</head>
<body>
<div class="dashboard">
  <div class="header">
    <h1>🐾 {workflow_name}</h1>
    <span class="tag">{tag_text}</span>
    <div class="meta">更新: {updated_at[:16]} | Run ID: {state.get('run_id', 'N/A')}</div>
  </div>

  <div class="progress-section">
    <div>进度: <span style="font-size:20px;font-weight:700">{pct}%</span></div>
    <div class="progress-bar"><div class="progress-fill" style="width:{pct}%"></div></div>
    <div class="progress-stats">
      <div>总计: <span>{progress.get('total', 0)}</span></div>
      <div>完成: <span style="color:#10b981">{progress.get('done', 0)}</span></div>
      <div>运行: <span style="color:#f59e0b">{progress.get('running', 0)}</span></div>
      <div>暂停: <span style="color:#8b5cf6">{progress.get('paused', 0)}</span></div>
      <div>失败: <span style="color:#ef4444">{progress.get('failed', 0)}</span></div>
    </div>
  </div>

  <div class="steps">
    {steps_html}
  </div>

  <div class="footer">🐶 小狗 Workflow Engine</div>
</div>
</body>
</html>"""
    return html


def save_dashboard(run_dir: str, output_path: str = None) -> str:
    """保存面板HTML到文件"""
    html = generate_dashboard(run_dir)
    if not output_path:
        output_path = str(Path(run_dir) / 'dashboard.html')
    Path(output_path).write_text(html, encoding='utf-8')
    return output_path
