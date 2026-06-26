"""
render_email.py
根据 generate_report.py 输出的 JSON 数据 + AI 生成的文字内容，
拼装成固定格式的 HTML 邮件正文。
AI 不参与 HTML 拼装，只提供纯文字字段。
"""

import os
import json
from datetime import datetime, timezone, timedelta

GITEA_URL = os.getenv("GITEA_URL", "http://43.156.243.152:3000")

RANK_ICONS = ["🥇", "🥈", "🥉"]


def _rank_icon(i: int) -> str:
    return RANK_ICONS[i] if i < len(RANK_ICONS) else "🔹"


def _fmt_time(iso_str: str) -> str:
    """将 ISO 时间字符串格式化为 YYYY-MM-DD HH:mm"""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        dt_local = dt.astimezone(timezone(timedelta(hours=8)))
        return dt_local.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str


def render_no_commits(data: dict) -> str:
    """情况一：本期无提交"""
    repo = data["repo"]
    generated_at = data["generated_at"]
    time_range_detail = data["time_range_detail"]
    gitea_url = GITEA_URL.rstrip("/")

    return f"""<div style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto;padding:24px;color:#333;">
  <h1 style="font-size:22px;color:#1a1a2e;border-bottom:3px solid #4a90d9;padding-bottom:10px;">
    📊 项目进度报告
  </h1>
  <p style="color:#666;margin-top:4px;">{repo} · {generated_at}</p>
  <div style="background:#fff3cd;border-left:4px solid #ffc107;padding:16px;border-radius:4px;margin:24px 0;">
    <strong>本统计周期内该仓库暂无任何提交记录。</strong><br>
    <span style="color:#666;font-size:13px;">统计周期：{time_range_detail}</span>
  </div>
  <p style="color:#999;font-size:12px;margin-top:32px;border-top:1px solid #eee;padding-top:12px;">
    🤖 由 AIFusionBot 自动生成 · {generated_at}<br>
    🔗 <a href="{gitea_url}/{repo}">{gitea_url}/{repo}</a>
  </p>
</div>"""


def render_full_report(data: dict, ai_content: dict) -> str:
    """
    情况二：本期有提交
    data       — generate_report.py 输出的单个仓库 JSON
    ai_content — AI 生成的纯文字字段 JSON，结构：
        {
          "ai_overview":    "现状评估文字",
          "ai_suggestion":  "下一步建议文字",
          "member_summaries": { "用户名": "该成员工作摘要" },
          "risk_notes":     "风险提示文字（纯文本，多条用换行分隔）"
        }
    """
    repo = data["repo"]
    generated_at = data["generated_at"]
    generated_date = generated_at.split(" ")[0]
    time_range_detail = data["time_range_detail"]
    overview = data["overview"]
    members = data["members"]
    inactive_members = data.get("inactive_members", [])
    gitea_url = GITEA_URL.rstrip("/")

    ai_overview = ai_content.get("ai_overview", "")
    ai_suggestion = ai_content.get("ai_suggestion", "")
    member_summaries = ai_content.get("member_summaries", {})
    risk_notes = ai_content.get("risk_notes", "")

    # ── 成员贡献排行 ──────────────────────────────────────────────
    sorted_members = sorted(members.items(), key=lambda x: x[1]["commits"], reverse=True)
    total_commits = overview["total_commits"]

    rank_rows = ""
    for i, (name, stat) in enumerate(sorted_members):
        bg = "#f9f9f9" if i % 2 == 0 else "#ffffff"
        icon = _rank_icon(i)
        pct = round(stat["commits"] / total_commits * 100) if total_commits else 0
        bar_width = pct  # max 100px
        rank_rows += f"""    <tr style="background:{bg};">
      <td style="padding:8px 12px;border:1px solid #eee;">{icon} #{i+1}</td>
      <td style="padding:8px 12px;border:1px solid #eee;"><strong>{name}</strong></td>
      <td style="padding:8px 12px;border:1px solid #eee;">{stat['commits']} 次</td>
      <td style="padding:8px 12px;border:1px solid #eee;">-{stat['deletions']} 行</td>
      <td style="padding:8px 12px;border:1px solid #eee;">
        <div style="background:#e0e8f5;border-radius:4px;height:14px;width:100px;display:inline-block;vertical-align:middle;">
          <div style="background:#4a90d9;border-radius:4px;height:14px;width:{bar_width}px;"></div>
        </div>
        {pct}%
      </td>
    </tr>\n"""

    # ── 成员详情 ──────────────────────────────────────────────────
    member_detail_blocks = ""
    for name, stat in sorted_members:
        branches_str = "、".join(stat.get("branches", []))
        ft = stat.get("file_type_summary", {})
        commit_count = stat["commits"]
        summary_text = member_summaries.get(name, "")

        # 进度判断
        if commit_count >= 3:
            progress_label = "🟢 活跃"
        elif commit_count >= 1:
            progress_label = "🟡 正常"
        else:
            progress_label = "🔴 低活跃"

        # 逐条提交记录
        commit_items = ""
        for c in stat.get("commit_details", []):
            time_str = _fmt_time(c.get("time", ""))
            msg = c.get("message", "")
            files_html = ""
            for f in c.get("files", []):
                fname = f.get("filename", "")
                fdel = f.get("deletions", 0)
                files_html += f"""      <div style="color:#666;">📁 {fname} &nbsp;
        <span style="color:#e74c3c;">-{fdel}</span>
      </div>\n"""
            commit_items += f"""    <div style="border-left:2px solid #e0e8f5;padding:8px 12px;margin-bottom:8px;font-size:13px;">
      <div style="color:#888;">🕐 {time_str}</div>
      <div style="margin:4px 0;"><strong>{msg}</strong></div>
{files_html}    </div>\n"""

        member_detail_blocks += f"""  <div style="border:1px solid #e0e8f5;border-radius:6px;padding:16px;margin-bottom:16px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <h3 style="margin:0;font-size:15px;color:#1a1a2e;">👤 {name}</h3>
      <span style="font-size:13px;">{progress_label} &nbsp; 提交 {commit_count} 次</span>
    </div>
    <p style="margin:8px 0 4px 0;font-size:13px;color:#666;">
      🌿 活跃分支：{branches_str} &nbsp;|&nbsp;
      📁 改动文件类型：代码 {ft.get('code',0)}个 / 文档 {ft.get('doc',0)}个 / 数据 {ft.get('data',0)}个 / 图片 {ft.get('image',0)}个 / 其他 {ft.get('other',0)}个
    </p>
    <div style="background:#f5f8ff;border-left:3px solid #4a90d9;padding:10px 14px;border-radius:4px;margin:10px 0;font-size:14px;">
      💡 <strong>工作摘要：</strong>{summary_text}
    </div>
    <p style="margin:10px 0 6px 0;font-size:13px;color:#666;"><strong>📝 提交记录（共 {commit_count} 次）</strong></p>
{commit_items}  </div>\n"""

    # ── 本期无提交成员 ────────────────────────────────────────────
    inactive_block = ""
    if inactive_members:
        inactive_rows = ""
        for m in inactive_members:
            days_str = f"{m['inactive_days']} 天" if m['inactive_days'] >= 0 else "无记录"
            inactive_rows += f"""    <tr>
      <td style="padding:8px 12px;border:1px solid #eee;">{m['name']}</td>
      <td style="padding:8px 12px;border:1px solid #eee;color:#e74c3c;"><strong>{days_str}</strong></td>
      <td style="padding:8px 12px;border:1px solid #eee;">{m['last_commit_date']}</td>
    </tr>\n"""
        inactive_block = f"""  <h2 style="font-size:17px;color:#4a90d9;margin-top:28px;">😴 本期无提交成员</h2>
  <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <tr style="background:#f5f5f5;">
      <th style="padding:8px 12px;text-align:left;border:1px solid #eee;">成员</th>
      <th style="padding:8px 12px;text-align:left;border:1px solid #eee;">连续未提交天数</th>
      <th style="padding:8px 12px;text-align:left;border:1px solid #eee;">上次提交日期</th>
    </tr>
{inactive_rows}  </table>\n"""

    # ── 风险提示 ──────────────────────────────────────────────────
    if risk_notes.strip():
        risk_lines = "".join(
            f'    <div>{line}</div>\n'
            for line in risk_notes.strip().splitlines()
            if line.strip()
        )
        risk_content = risk_lines
    else:
        risk_content = '    <div><span style="color:green;">✅ 本期暂无风险提示</span></div>\n'

    # ── 拼装完整 HTML ─────────────────────────────────────────────
    return f"""<div style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto;padding:24px;color:#333;">

  <!-- 标题 -->
  <h1 style="font-size:22px;color:#1a1a2e;border-bottom:3px solid #4a90d9;padding-bottom:10px;">
    📊 项目进度报告
  </h1>
  <p style="color:#666;margin-top:4px;">{repo} · {generated_date}</p>

  <!-- 情况总览 -->
  <h2 style="font-size:17px;color:#4a90d9;margin-top:28px;">◆ 情况总览</h2>
  <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <tr>
      <td style="padding:8px 12px;background:#f5f8ff;border:1px solid #e0e8f5;width:40%;"><strong>统计周期</strong></td>
      <td style="padding:8px 12px;border:1px solid #e0e8f5;">{time_range_detail}</td>
    </tr>
    <tr>
      <td style="padding:8px 12px;background:#f5f8ff;border:1px solid #e0e8f5;"><strong>提交次数</strong></td>
      <td style="padding:8px 12px;border:1px solid #e0e8f5;">{overview['total_commits']} 次</td>
    </tr>
    <tr>
      <td style="padding:8px 12px;background:#f5f8ff;border:1px solid #e0e8f5;"><strong>参与成员</strong></td>
      <td style="padding:8px 12px;border:1px solid #e0e8f5;">{overview['total_members']} 人</td>
    </tr>
  </table>

  <!-- AI 综合评估 -->
  <h2 style="font-size:17px;color:#4a90d9;margin-top:28px;">🤖 AI 综合评估</h2>
  <div style="background:#f0f7ff;border-left:4px solid #4a90d9;padding:16px;border-radius:4px;">
    <p style="margin:0 0 10px 0;"><strong>现状：</strong>{ai_overview}</p>
    <p style="margin:0;"><strong>下一步建议：</strong>{ai_suggestion}</p>
  </div>

  <!-- 成员贡献排行 -->
  <h2 style="font-size:17px;color:#4a90d9;margin-top:28px;">🏆 成员贡献排行</h2>
  <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <tr style="background:#4a90d9;color:white;">
      <th style="padding:8px 12px;text-align:left;">排名</th>
      <th style="padding:8px 12px;text-align:left;">成员</th>
      <th style="padding:8px 12px;text-align:left;">提交次数</th>
      <th style="padding:8px 12px;text-align:left;">删除行数</th>
      <th style="padding:8px 12px;text-align:left;">占比</th>
    </tr>
{rank_rows}  </table>

  <!-- 成员详情 -->
  <h2 style="font-size:17px;color:#4a90d9;margin-top:28px;">👤 成员详情</h2>
{member_detail_blocks}
{inactive_block}
  <!-- 风险提示 -->
  <h2 style="font-size:17px;color:#4a90d9;margin-top:28px;">⚠️ 风险提示</h2>
  <div style="background:#fff8f0;border-left:4px solid #f39c12;padding:16px;border-radius:4px;font-size:14px;">
{risk_content}  </div>

  <!-- 页脚 -->
  <p style="color:#999;font-size:12px;margin-top:32px;border-top:1px solid #eee;padding-top:12px;">
    🤖 由 AIFusionBot 自动生成 · {generated_at}<br>
    🔗 <a href="{gitea_url}/{repo}" style="color:#4a90d9;">{gitea_url}/{repo}</a>
  </p>

</div>"""


def render(data: dict, ai_content: dict = None) -> str:
    """对外统一入口，根据 has_commits 自动选择渲染方式"""
    if not data.get("has_commits"):
        return render_no_commits(data)
    return render_full_report(data, ai_content or {})
