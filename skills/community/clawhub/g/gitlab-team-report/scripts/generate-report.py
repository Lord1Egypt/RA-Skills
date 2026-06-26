#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import datetime as dt
import html
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

UTC = dt.timezone.utc
TZ8 = dt.timezone(dt.timedelta(hours=8))
MAX_MRS_PER_SUBCATEGORY = 5

DEFAULT_CLASSIFICATION = {
    "产品与体验": [
        {"name": "平台与基础能力", "repo_keywords": ["platform", "workspace", "infra"], "mr_keywords": ["backup", "restore", "infra", "deploy", "environment"], "label_keywords": []},
        {"name": "CDN/网络", "repo_keywords": ["cdn"], "mr_keywords": ["cdn", "网络", "域名"], "label_keywords": []},
        {"name": "稳定性与监控", "repo_keywords": [], "mr_keywords": ["ssh", "探活", "卡死", "稳定性", "监控", "metrics", "指标", "日志", "log"], "label_keywords": []},
        {"name": "安全与配置", "repo_keywords": ["auth", "config", "secret"], "mr_keywords": ["权限", "配置", "download", "proxy", "rewrite"], "label_keywords": []},
        {"name": "客户端体验", "repo_keywords": ["client", "mobile", "ios", "android", "frontend"], "mr_keywords": ["ui", "ux", "交互", "体验"], "label_keywords": []},
    ],
    "业务与运营": [
        {"name": "账号与登录", "repo_keywords": ["account", "auth", "passport"], "mr_keywords": ["账号", "邮箱", "登录", "注册", "验证", "identity"], "label_keywords": []},
        {"name": "商业化与计费", "repo_keywords": ["billing", "payment", "subscription"], "mr_keywords": ["billing", "计费", "订阅", "套餐", "支付", "rate limit", "按量"], "label_keywords": []},
        {"name": "后台与管理工具", "repo_keywords": ["admin", "console"], "mr_keywords": ["admin", "后台", "管理台", "审批", "dashboard", "tooling"], "label_keywords": []},
        {"name": "用户运营", "repo_keywords": ["growth", "retention"], "mr_keywords": ["增长", "转化", "留存", "运营", "裂变"], "label_keywords": []},
    ],
    "核心平台能力": [
        {"name": "会话管理", "repo_keywords": ["chat", "conversation", "session"], "mr_keywords": ["会话", "session", "conversation", "入口", "新建"], "label_keywords": []},
        {"name": "消息收发", "repo_keywords": ["message", "render"], "mr_keywords": ["chat", "message", "消息", "发送", "渲染", "保存", "save msg"], "label_keywords": []},
        {"name": "自动化与工具集成", "repo_keywords": ["agent", "plugin", "mcp"], "mr_keywords": ["agent", "plugin", "插件", "tool", "工具", "integration", "技能", "workflow"], "label_keywords": []},
        {"name": "上下文与记忆", "repo_keywords": ["memory", "context"], "mr_keywords": ["memory", "记忆", "上下文", "context", "recall"], "label_keywords": []},
        {"name": "模型与推理", "repo_keywords": ["model", "llm", "router"], "mr_keywords": ["model", "模型", "推理", "router", "provider"], "label_keywords": []},
    ],
}

REPO_CATEGORY_OVERRIDES = {
    "billing": ("业务与运营", "商业化与计费"),
    "payment": ("业务与运营", "商业化与计费"),
    "growth": ("业务与运营", "用户运营"),
    "marketing": ("业务与运营", "用户运营"),
    "retention": ("业务与运营", "用户运营"),
    "account": ("业务与运营", "账号与登录"),
    "auth": ("业务与运营", "账号与登录"),
    "admin": ("业务与运营", "后台与管理工具"),
    "console": ("业务与运营", "后台与管理工具"),
    "chat": ("核心平台能力", "会话管理"),
    "conversation": ("核心平台能力", "会话管理"),
    "message": ("核心平台能力", "消息收发"),
    "memory": ("核心平台能力", "上下文与记忆"),
    "agent": ("核心平台能力", "自动化与工具集成"),
    "mcp": ("核心平台能力", "自动化与工具集成"),
    "llm": ("核心平台能力", "模型与推理"),
    "model": ("核心平台能力", "模型与推理"),
    "infra": ("产品与体验", "平台与基础能力"),
    "ci": ("产品与体验", "平台与基础能力"),
    "monitor": ("产品与体验", "稳定性与监控"),
    "otel": ("产品与体验", "稳定性与监控"),
    "security": ("产品与体验", "安全与配置"),
    "config": ("产品与体验", "安全与配置"),
    "frontend": ("产品与体验", "客户端体验"),
    "mobile": ("产品与体验", "客户端体验"),
    "cdn": ("产品与体验", "CDN/网络"),
}

HIGH_SIGNAL_PATTERNS = [
    r"feat", r"feature", r"support", r"add", r"新增", r"接入", r"上线", r"优化", r"重构", r"refactor", r"improve", r"ability", r"workflow"
]
LOW_SIGNAL_PATTERNS = [
    r"chore", r"deps?", r"bump", r"lint", r"format", r"typo", r"docs?", r"test", r"ci", r"merge branch"
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("-c", "--config", required=True)
    p.add_argument("-s", "--start-date")
    p.add_argument("-e", "--end-date")
    p.add_argument("-o", "--output")
    p.add_argument("--no-charts", action="store_true")
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def request_json(url: str, headers: dict[str, str]) -> Any:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def paginate(url: str, headers: dict[str, str], max_pages: int = 8) -> list[Any]:
    items: list[Any] = []
    for page in range(1, max_pages + 1):
        sep = '&' if '?' in url else '?'
        data = request_json(f"{url}{sep}page={page}&per_page=100", headers)
        if not data:
            break
        if isinstance(data, list):
            items.extend(data)
            if len(data) < 100:
                break
        else:
            return data
    return items


def parse_dt(s: str) -> dt.datetime:
    if s.endswith('Z'):
        s = s.replace('Z', '+00:00')
    return dt.datetime.fromisoformat(s)


def daterange_default() -> tuple[str, str]:
    today = dt.date.today()
    start = today - dt.timedelta(days=7)
    return start.isoformat(), today.isoformat()


def markdown_link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def load_rule_config(root_dir: Path) -> dict[str, Any]:
    rules_path = root_dir / "config" / "classification.rules.json"
    if rules_path.exists():
        return load_json(rules_path)
    return {
        "priority": ["repo", "label", "title", "branch", "classification", "default"],
        "default_category": {"category": "产品与体验", "subcategory": "平台与基础能力"},
        "repo_rules": [],
        "keyword_rules": [],
    }


def compact_text(text: str, limit: int = 90) -> str:
    s = re.sub(r"\s+", " ", (text or "").strip())
    return s[:limit] + ("…" if len(s) > limit else "")


def normalize_text(*parts: str) -> str:
    return " ".join([p for p in parts if p]).lower()


def score_text(text: str, patterns: list[str], weight: int) -> int:
    total = 0
    for pat in patterns:
        if re.search(pat, text, re.I):
            total += weight
    return total


def classification_score_from_matrix(mr: dict[str, Any], classification: dict[str, list[dict[str, Any]]]) -> tuple[str, str, str, int]:
    repo = (mr.get("repo_name") or "").lower()
    labels = " ".join(mr.get("labels") or []).lower()
    text = normalize_text(mr.get("title", ""), mr.get("description", ""), labels, mr.get("source_branch", ""), mr.get("target_branch", ""))

    for key, (primary, secondary) in REPO_CATEGORY_OVERRIDES.items():
        if key in repo:
            return primary, secondary, "repo_override", 100

    best: tuple[int, str, str] | None = None
    for primary, subcats in classification.items():
        for sub in subcats[:5]:
            score = 0
            for kw in sub.get("repo_keywords", []):
                if kw.lower() in repo:
                    score += 10
            for kw in sub.get("label_keywords", []):
                if kw.lower() in labels:
                    score += 7
            for kw in sub.get("mr_keywords", []):
                if kw.lower() in text:
                    score += 5
            if best is None or score > best[0]:
                best = (score, primary, sub.get("name", "未分类"))
    if not best or best[0] <= 0:
        return "产品与体验", "平台与基础能力", "fallback", 0
    mode = "rule" if best[0] >= 10 else "fallback"
    return best[1], best[2], mode, best[0]


def match_any(text: str, patterns: list[str]) -> bool:
    text = (text or "").lower()
    return any(p.lower() in text for p in patterns)


def classify_mr(mr: dict[str, Any], classification: dict[str, list[dict[str, Any]]], rule_config: dict[str, Any]) -> tuple[str, str, str, int]:
    repo = (mr.get("repo_name") or "")
    labels = " ".join(mr.get("labels") or [])
    title = mr.get("title") or ""
    branch = normalize_text(mr.get("source_branch", ""), mr.get("target_branch", ""))
    fallback = classification_score_from_matrix(mr, classification)
    default_category = rule_config.get("default_category", {"category": fallback[0], "subcategory": fallback[1]})

    field_values = {
        "repo": repo,
        "label": labels,
        "title": title,
        "branch": branch,
    }
    priority = rule_config.get("priority") or ["repo", "label", "title", "branch", "classification", "default"]

    for layer in priority:
        if layer == "repo":
            for rule in rule_config.get("repo_rules", []):
                if match_any(repo, rule.get("match", [])):
                    return rule["category"], rule["subcategory"], "config_repo", 1000
        elif layer in {"label", "title", "branch"}:
            for rule in rule_config.get("keyword_rules", []):
                if rule.get("field") == layer and match_any(field_values[layer], rule.get("match", [])):
                    return rule["category"], rule["subcategory"], f"config_{layer}", 900
        elif layer == "classification":
            return fallback
        elif layer == "default":
            return default_category["category"], default_category["subcategory"], "config_default", 1

    return fallback


def mr_priority(mr: dict[str, Any]) -> int:
    state_score = {"merged": 30, "opened": 18, "closed": 8}.get(mr.get("state"), 0)
    text = normalize_text(mr.get("title", ""), mr.get("description", ""), " ".join(mr.get("labels") or []))
    keyword_score = score_text(text, HIGH_SIGNAL_PATTERNS, 4) - score_text(text, LOW_SIGNAL_PATTERNS, 3)
    change_count = mr.get("changes_count_num", 0)
    recency = 0
    updated = mr.get("updated_at") or ""
    if updated:
        recency = int(re.sub(r"\D", "", updated[:19]) or "0") % 1000000
    return state_score + keyword_score + min(change_count, 20) + min(recency // 10000, 20)


def summarize_overflow(mrs: list[dict[str, Any]]) -> str:
    if not mrs:
        return ""
    merged = sum(1 for x in mrs if x["state"] == "merged")
    opened = sum(1 for x in mrs if x["state"] == "opened")
    closed = sum(1 for x in mrs if x["state"] == "closed")
    repos = [x["repo_name"].split("/")[-1] for x in mrs]
    top_repos = [name for name, _ in collections.Counter(repos).most_common(3)]
    repo_text = " / ".join(top_repos) if top_repos else "多个仓库"
    return f"其余 {len(mrs)} 个 MR（{merged} merged / {opened} opened / {closed} closed），主要涉及 {repo_text}。"


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines += [f"# {report['title']}", "", f"时间范围：`{report['start']}` 至 `{report['end']}`", ""]
    lines += ["## 参与成员", ""]
    for user in report["users"]:
        lines.append(f"- {markdown_link(user['name'], user['web_url'])} (`{user['username']}`)")
    lines += ["", "## 一、产品功能", ""]

    for primary in report["product_sections"]:
        lines += [f"### {primary['name']}", ""]
        for sub in primary["subsections"]:
            lines += [f"#### {sub['name']}（{sub['mr_total']} 个 MR）", ""]
            if sub["mr_total"] == 0:
                lines += ["- 本周暂无归入该分类的 MR", ""]
                continue
            for mr in sub["top_mrs"]:
                lines.append(f"- {markdown_link(f'!{mr['iid']} {mr['title']}', mr['web_url'])} ｜ 提交人：{markdown_link(mr['author_name'], mr['author_url'])} ｜ 仓库：`{mr['repo_name']}` ｜ 状态：**{mr['state_cn']}**")
            if sub.get("overflow_summary"):
                lines.append(f"- {sub['overflow_summary']}")
            lines.append("")

    lines += ["## 二、人员统计", ""]
    for person in report["people_sections"]:
        lines += [f"### {markdown_link(person['name'], person['web_url'])}", ""]
        lines.append(f"- 主要贡献仓库数：**{person['repo_count']}**")
        lines.append(f"- MR 总数：**{person['mr_total']}**（已合并 {person['mr_merged']} / 进行中 {person['mr_opened']} / 已关闭 {person['mr_closed']}）")
        lines.append(f"- Commit 总数：**{person['commit_total']}**")
        top_repos = [r for r in person["repos"] if r["mr_total"] > 0 or r["commit_total"] > 0][:4]
        if top_repos:
            lines.append("- 重点仓库：")
            for repo in top_repos:
                lines.append(f"  - `{repo['repo_name']}`：MR {repo['mr_total']}（merged {repo['mr_merged']} / opened {repo['mr_opened']} / closed {repo['mr_closed']}），Commit {repo['commit_total']}；{repo['summary']}")
        lines.append("")

    stats = report["stats"]
    lines += ["## 三、团队整体产出统计", ""]
    lines.append(f"- 总 MR：**{stats['mr_total']}**")
    lines.append(f"- 总 Commit：**{stats['commit_total']}**")
    lines.append(f"- 活跃仓库数：**{stats['repo_total']}**")
    lines.append(f"- 活跃成员数：**{stats['user_total']}**")
    lines += ["", "### 统计摘要", ""]
    lines.append(f"- MR 状态分布：**Merged {stats['mr_merged']} / Opened {stats['mr_opened']} / Closed {stats['mr_closed']}**")
    lines.append(f"- 每日最高活动：**{stats['busiest_day']}**")
    lines.append(f"- 最高产出仓库：`{stats['top_repo']}`")
    if report.get("top_contributors"):
        lines.append("- 成员产出排行：")
        for item in report["top_contributors"]:
            lines.append(f"  - {item['name']}：MR {item['mr_total']}，Commit {item['commit_total']}")
    if report.get("top_categories"):
        lines.append("- 产品方向分布：")
        for item in report["top_categories"]:
            lines.append(f"  - {item['name']}：{item['mr_total']} 个 MR")
    lines += ["", f"_报告生成时间：{report['generated_at']}_", ""]
    return "\n".join(lines)


def json_for_js(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_html(report: dict[str, Any], stats_payload: dict[str, Any]) -> str:
    dashboard_cards = f"""
    <div class='metric'><span>总 MR</span><strong>{report['stats']['mr_total']}</strong></div>
    <div class='metric'><span>总 Commit</span><strong>{report['stats']['commit_total']}</strong></div>
    <div class='metric'><span>活跃仓库</span><strong>{report['stats']['repo_total']}</strong></div>
    <div class='metric'><span>活跃成员</span><strong>{report['stats']['user_total']}</strong></div>
    """

    product_sections_html = []
    for primary in report["product_sections"]:
        subs = []
        for sub in primary["subsections"]:
            items = []
            for mr in sub["top_mrs"]:
                items.append(f"<li><a href='{html.escape(mr['web_url'])}' target='_blank'>!{mr['iid']} {html.escape(mr['title'])}</a><span>{html.escape(mr['repo_name'])} · {html.escape(mr['author_name'])} · {html.escape(mr['state_cn'])}</span></li>")
            overflow = f"<p class='overflow'>{html.escape(sub['overflow_summary'])}</p>" if sub.get("overflow_summary") else ""
            empty = "<p class='empty'>本周暂无归入该分类的 MR</p>" if sub["mr_total"] == 0 else ""
            subs.append(f"<section class='subcat'><h4>{html.escape(sub['name'])}<em>{sub['mr_total']} 个 MR</em></h4>{empty}<ul>{''.join(items)}</ul>{overflow}</section>")
        product_sections_html.append(f"<section class='primary'><h3>{html.escape(primary['name'])}</h3>{''.join(subs)}</section>")

    people_html = []
    for person in report["people_sections"]:
        repo_blocks = []
        for repo in person["repos"][:6]:
            top_mrs = "".join([f"<li><a href='{html.escape(m['web_url'])}' target='_blank'>!{m['iid']} {html.escape(m['title'])}</a></li>" for m in repo['top_mrs'][:3]])
            repo_blocks.append(f"<div class='repo-card'><h4>{html.escape(repo['repo_name'])}</h4><p>MR {repo['mr_total']} · Commit {repo['commit_total']}</p><p>{html.escape(repo['summary'])}</p><ul>{top_mrs}</ul></div>")
        people_html.append(f"<section class='person'><h3><a href='{html.escape(person['web_url'])}' target='_blank'>{html.escape(person['name'])}</a></h3><p>MR {person['mr_total']}（merged {person['mr_merged']} / opened {person['mr_opened']} / closed {person['mr_closed']}） · Commit {person['commit_total']}</p><div class='repo-grid'>{''.join(repo_blocks)}</div></section>")

    return f"""<!doctype html>
<html lang='zh-CN'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{html.escape(report['title'])}</title>
<script src='https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js'></script>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Arial,PingFang SC,Microsoft YaHei,sans-serif;background:#0b1020;color:#e5e7eb;margin:0;padding:0}}
.wrapper{{max-width:1280px;margin:0 auto;padding:24px}}
.hero{{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;margin-bottom:24px}}
.hero h1{{margin:0;font-size:34px}} .hero p{{color:#94a3b8}}
.metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:20px 0 28px}}
.metric,.panel,.primary,.person{{background:#111827;border:1px solid #1f2937;border-radius:16px;padding:18px;box-shadow:0 8px 24px rgba(0,0,0,.2)}}
.metric span{{display:block;color:#94a3b8;font-size:13px;margin-bottom:10px}} .metric strong{{font-size:30px}}
.charts{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-bottom:28px}} .chart{{height:340px}}
.section-title{{margin:28px 0 14px;font-size:22px}}
.primary{{margin-bottom:18px}} .subcat{{padding:14px 0;border-top:1px solid #1f2937}} .subcat:first-of-type{{border-top:none;padding-top:0}}
.subcat h4{{margin:0 0 10px;display:flex;justify-content:space-between;align-items:center}} .subcat em{{font-style:normal;color:#94a3b8;font-size:12px}}
ul{{margin:0;padding-left:18px}} li{{margin:6px 0}} li span{{color:#94a3b8;font-size:13px;display:block;margin-top:2px}}
a{{color:#60a5fa;text-decoration:none}} a:hover{{text-decoration:underline}}
.overflow,.empty{{color:#94a3b8;margin-top:10px}}
.repo-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}} .repo-card{{background:#0f172a;border:1px solid #1f2937;border-radius:12px;padding:14px}}
@media (max-width: 960px){{.metrics,.charts,.repo-grid{{grid-template-columns:1fr}} .hero{{display:block}}}}
</style>
</head>
<body>
<div class='wrapper'>
  <div class='hero'>
    <div>
      <h1>{html.escape(report['title'])}</h1>
      <p>时间范围：{html.escape(report['start'])} 至 {html.escape(report['end'])}</p>
    </div>
    <div><p>生成时间：{html.escape(report['generated_at'])}</p></div>
  </div>
  <div class='metrics'>{dashboard_cards}</div>
  <h2 class='section-title'>团队整体产出统计</h2>
  <div class='charts'>
    <div class='panel'><div id='chart-commits' class='chart'></div></div>
    <div class='panel'><div id='chart-mr' class='chart'></div></div>
    <div class='panel'><div id='chart-daily' class='chart'></div></div>
    <div class='panel'><div id='chart-projects' class='chart'></div></div>
  </div>
  <h2 class='section-title'>产品功能</h2>
  {''.join(product_sections_html)}
  <h2 class='section-title'>人员统计</h2>
  {''.join(people_html)}
</div>
<script>
const stats = {json_for_js(stats_payload)};
const commitsChart = echarts.init(document.getElementById('chart-commits'));
commitsChart.setOption({{backgroundColor:'transparent',title:{{text:'提交数分布',textStyle:{{color:'#e5e7eb'}}}},tooltip:{{trigger:'axis'}},xAxis:{{type:'category',data:Object.keys(stats.commits_by_user),axisLabel:{{color:'#cbd5e1',rotate:20}}}},yAxis:{{type:'value',axisLabel:{{color:'#cbd5e1'}}}},series:[{{type:'bar',data:Object.values(stats.commits_by_user),itemStyle:{{color:'#34d399'}},barMaxWidth:42}}]}});
const mrChart = echarts.init(document.getElementById('chart-mr'));
mrChart.setOption({{backgroundColor:'transparent',title:{{text:'MR 状态分布',textStyle:{{color:'#e5e7eb'}}}},tooltip:{{trigger:'item'}},series:[{{type:'pie',radius:['45%','70%'],data:[{{name:'Merged',value:stats.mr_stats.merged}},{{name:'Opened',value:stats.mr_stats.opened}},{{name:'Closed',value:stats.mr_stats.closed}}]}}]}});
const dailyChart = echarts.init(document.getElementById('chart-daily'));
dailyChart.setOption({{backgroundColor:'transparent',title:{{text:'每日活动趋势',textStyle:{{color:'#e5e7eb'}}}},tooltip:{{trigger:'axis'}},xAxis:{{type:'category',data:Object.keys(stats.daily_activity),axisLabel:{{color:'#cbd5e1',rotate:20}}}},yAxis:{{type:'value',axisLabel:{{color:'#cbd5e1'}}}},series:[{{type:'line',smooth:true,data:Object.values(stats.daily_activity),lineStyle:{{color:'#60a5fa'}},itemStyle:{{color:'#60a5fa'}}}}]}});
const projectEntries = Object.entries(stats.projects).sort((a,b)=>b[1]-a[1]).slice(0,10);
const projectChart = echarts.init(document.getElementById('chart-projects'));
projectChart.setOption({{backgroundColor:'transparent',title:{{text:'项目分布',textStyle:{{color:'#e5e7eb'}}}},tooltip:{{trigger:'axis'}},grid:{{left:140,right:30,top:50,bottom:20}},xAxis:{{type:'value',axisLabel:{{color:'#cbd5e1'}}}},yAxis:{{type:'category',data:projectEntries.map(x=>x[0]),axisLabel:{{color:'#cbd5e1'}}}},series:[{{type:'bar',data:projectEntries.map(x=>x[1]),itemStyle:{{color:'#f59e0b'}}}}]}});
window.addEventListener('resize', ()=>[commitsChart,mrChart,dailyChart,projectChart].forEach(c=>c.resize()));
</script>
</body></html>"""


def generate_index_html(output_dir: Path, title_prefix: str = "GitLab Weekly Report") -> None:
    report_dirs = sorted([p for p in output_dir.iterdir() if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2}", p.name)], reverse=True)
    cards = []
    for rd in report_dirs:
        stats_file = rd / "stats.json"
        meta = load_json(stats_file) if stats_file.exists() else {}
        summary = meta.get("dashboard", {})
        cards.append(f"<div class='card'><h2><a href='./{rd.name}/weekly_report.html'>{rd.name}</a></h2><p>MR {summary.get('mr_total','-')} · Commit {summary.get('commit_total','-')} · Repo {summary.get('repo_total','-')}</p><p><a href='./{rd.name}/weekly_report.md'>Markdown</a> · <a href='./{rd.name}/weekly_report.html'>HTML</a></p></div>")
    html_doc = f"""<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{html.escape(title_prefix)} 仪表盘</title><style>body{{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Arial,PingFang SC,Microsoft YaHei,sans-serif;max-width:1100px;margin:40px auto;padding:0 24px;background:#fafafa;color:#111827}}.hero{{background:#111827;color:#fff;padding:24px;border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:24px}}.card{{background:white;border:1px solid #e5e7eb;border-radius:16px;padding:18px}}a{{color:#2563eb;text-decoration:none}}</style></head><body><div class='hero'><h1>{html.escape(title_prefix)} 仪表盘</h1><p>历史周报入口与关键统计</p></div><div class='grid'>{''.join(cards) or '<p>暂无周报</p>'}</div></body></html>"""
    (output_dir / "index.html").write_text(html_doc, encoding="utf-8")


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).expanduser().resolve()
    cfg = load_json(config_path)
    start, end = args.start_date, args.end_date
    if not start or not end:
        start, end = daterange_default()

    root_dir = config_path.parent.parent
    output_dir = Path(args.output or cfg.get("report", {}).get("output_dir") or (root_dir / "reports"))
    if not output_dir.is_absolute():
        output_dir = (root_dir / output_dir).resolve()
    report_dir = output_dir / f"{start}_to_{end}"
    charts_dir = report_dir / "charts"
    report_dir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)

    headers = {"PRIVATE-TOKEN": cfg["gitlab"]["token"]}
    base = cfg["gitlab"]["url"].rstrip("/")
    classification = cfg.get("classification", DEFAULT_CLASSIFICATION)
    rule_config = load_rule_config(root_dir)
    users_cfg = cfg["users"]
    excluded_repos = set(cfg.get("report", {}).get("exclude_repos", []))

    def is_excluded_repo(repo_name: str) -> bool:
        repo_name = (repo_name or "").strip()
        if not repo_name:
            return False
        return any(repo_name == item or repo_name.endswith(item) or item in repo_name for item in excluded_repos)

    start_utc = parse_dt(f"{start}T00:00:00+08:00").astimezone(UTC)
    end_utc = parse_dt(f"{end}T23:59:59+08:00").astimezone(UTC)

    users_out, all_mrs, all_commits = [], [], []
    daily_activity, repo_activity, commits_by_user, mr_state = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    project_cache: dict[int, dict[str, Any]] = {}

    def get_project(project_id: int | None) -> dict[str, Any]:
        if not project_id:
            return {}
        if project_id not in project_cache:
            project_cache[project_id] = request_json(f"{base}/api/v4/projects/{project_id}", headers)
        return project_cache[project_id]

    for user in users_cfg:
        user_detail = request_json(f"{base}/api/v4/users/{user['id']}", headers)
        user_web = user_detail.get("web_url") or f"{base}/{user['username']}"
        users_out.append({"id": user["id"], "username": user["username"], "name": user["name"], "web_url": user_web})

        events_before = (parse_dt(f"{end}T00:00:00+08:00") + dt.timedelta(days=1)).strftime("%Y-%m-%d")
        events = paginate(f"{base}/api/v4/users/{user['id']}/events?action=pushed&after={start}&before={events_before}", headers)
        for event in events:
            created = event.get("created_at")
            if not created:
                continue
            created_dt = parse_dt(created)
            if not (start_utc <= created_dt <= end_utc):
                continue
            push = event.get("push_data") or {}
            commit_count = max(1, int(push.get("commit_count") or 1))
            title = push.get("commit_title") or push.get("commit_from") or "Commit"
            project = get_project(event.get("project_id"))
            repo_name = project.get("path_with_namespace") or str(event.get("project_id") or "unknown")
            if is_excluded_repo(repo_name):
                continue
            repo_activity[repo_name] += commit_count
            commits_by_user[user["name"]] += commit_count
            daily_activity[created_dt.astimezone(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d")] += commit_count
            all_commits.append({"author_id": user["id"], "author_name": user["name"], "author_url": user_web, "repo_name": repo_name, "title": title, "created_at": created, "short_id": (push.get("commit_from") or "")[:8] or re.sub(r"[^a-zA-Z0-9]", "", title)[:8], "count": commit_count})

        created_mrs = paginate(f"{base}/api/v4/merge_requests?author_id={user['id']}&created_after={start}T00:00:00Z&created_before={end}T23:59:59Z&scope=all", headers)
        updated_mrs = paginate(f"{base}/api/v4/merge_requests?author_id={user['id']}&updated_after={start}T00:00:00Z&updated_before={end}T23:59:59Z&scope=all", headers)
        merged = {mr["id"]: mr for mr in created_mrs + updated_mrs if mr.get("id")}
        for mr in merged.values():
            project = get_project(mr.get("project_id"))
            repo_name = project.get("path_with_namespace") or mr.get("references", {}).get("full", "").split("!")[0] or str(mr.get("project_id") or "unknown")
            if is_excluded_repo(repo_name):
                continue
            changes_raw = str(mr.get("changes_count", "0")).replace("+", "")
            changes_num = int(changes_raw) if changes_raw.isdigit() else 0
            primary, sub, mode, class_score = classify_mr({**mr, "repo_name": repo_name}, classification, rule_config)
            item = {
                "id": mr["id"], "iid": mr.get("iid"), "title": mr.get("title", ""), "description": mr.get("description", ""),
                "web_url": mr.get("web_url"), "repo_name": repo_name, "state": mr.get("state", "opened"),
                "state_cn": {"merged": "已合并", "opened": "进行中", "closed": "已关闭"}.get(mr.get("state", "opened"), mr.get("state", "opened")),
                "labels": mr.get("labels", []), "author_id": user["id"], "author_name": user["name"], "author_url": user_web,
                "classification_primary": primary, "classification_secondary": sub, "classification_mode": mode, "classification_score": class_score,
                "updated_at": mr.get("updated_at"), "created_at": mr.get("created_at"), "changes_count_num": changes_num,
            }
            item["priority_score"] = mr_priority(item)
            all_mrs.append(item)
            mr_state[item["state"]] += 1
            repo_activity[repo_name] += 1
            raw_day = item.get("updated_at") or item.get("created_at") or ""
            day = parse_dt(raw_day).astimezone(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d") if raw_day else ""
            if day:
                daily_activity[day] += 1

    product_sections = []
    for primary, subcats in classification.items():
        primary_block = {"name": primary, "subsections": []}
        for sub in subcats[:5]:
            items = [m for m in all_mrs if m["classification_primary"] == primary and m["classification_secondary"] == sub["name"]]
            items.sort(key=lambda x: (x["priority_score"], x.get("updated_at") or ""), reverse=True)
            top_mrs = items[:MAX_MRS_PER_SUBCATEGORY]
            overflow = items[MAX_MRS_PER_SUBCATEGORY:]
            primary_block["subsections"].append({
                "name": sub["name"], "mr_total": len(items), "top_mrs": top_mrs,
                "overflow_summary": summarize_overflow(overflow),
            })
        product_sections.append(primary_block)

    commits_by_person_repo: dict[tuple[int, str], list[dict[str, Any]]] = collections.defaultdict(list)
    mrs_by_person_repo: dict[tuple[int, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for c in all_commits:
        commits_by_person_repo[(c["author_id"], c["repo_name"])].append(c)
    for mr in all_mrs:
        mrs_by_person_repo[(mr["author_id"], mr["repo_name"])].append(mr)

    people_sections = []
    for user in users_out:
        repos = []
        repo_names = sorted({r for (uid, r) in set(list(commits_by_person_repo.keys()) + list(mrs_by_person_repo.keys())) if uid == user["id"]})
        for repo_name in repo_names:
            commits = commits_by_person_repo.get((user["id"], repo_name), [])
            mrs = mrs_by_person_repo.get((user["id"], repo_name), [])
            mrs.sort(key=lambda x: x["priority_score"], reverse=True)
            mr_merged = sum(1 for x in mrs if x["state"] == "merged")
            mr_opened = sum(1 for x in mrs if x["state"] == "opened")
            mr_closed = sum(1 for x in mrs if x["state"] == "closed")
            commit_total = sum(c["count"] for c in commits)
            score = commit_total + mr_merged * 8 + mr_opened * 5 + mr_closed * 3 + sum(m["priority_score"] for m in mrs[:3])
            focus = [m["classification_secondary"] for m in mrs[:3] if m.get("classification_secondary")]
            summary = f"本周在 `{repo_name}` 主要推进了 {len(mrs)} 个 MR、{commit_total} 次提交，重点集中在 {'、'.join(dict.fromkeys(focus)) if focus else '日常迭代与问题修复'}"
            repos.append({"repo_name": repo_name, "mr_total": len(mrs), "mr_merged": mr_merged, "mr_opened": mr_opened, "mr_closed": mr_closed, "commit_total": commit_total, "score": score, "top_mrs": mrs[:5], "summary": summary})
        repos.sort(key=lambda x: x["score"], reverse=True)
        user_mrs = [m for m in all_mrs if m["author_id"] == user["id"]]
        people_sections.append({"name": user["name"], "web_url": user["web_url"], "repo_count": len(repos), "repos": repos, "mr_total": len(user_mrs), "mr_merged": sum(1 for m in user_mrs if m["state"] == "merged"), "mr_opened": sum(1 for m in user_mrs if m["state"] == "opened"), "mr_closed": sum(1 for m in user_mrs if m["state"] == "closed"), "commit_total": sum(c["count"] for c in all_commits if c["author_id"] == user["id"])})

    stats = {"mr_total": len(all_mrs), "commit_total": sum(c["count"] for c in all_commits), "repo_total": len(set([m["repo_name"] for m in all_mrs] + [c["repo_name"] for c in all_commits])), "user_total": len(users_out), "mr_merged": mr_state["merged"], "mr_opened": mr_state["opened"], "mr_closed": mr_state["closed"], "busiest_day": max(daily_activity.items(), key=lambda x: x[1])[0] if daily_activity else "-", "top_repo": max(repo_activity.items(), key=lambda x: x[1])[0] if repo_activity else "-"}

    top_contributors = sorted([
        {"name": p["name"], "mr_total": p["mr_total"], "commit_total": p["commit_total"]}
        for p in people_sections
    ], key=lambda x: (x["mr_total"], x["commit_total"]), reverse=True)
    top_categories = []
    for primary in product_sections:
        top_categories.append({
            "name": primary["name"],
            "mr_total": sum(sub["mr_total"] for sub in primary["subsections"]),
        })
    top_categories.sort(key=lambda x: x["mr_total"], reverse=True)

    stats_payload = {"period": {"start": start, "end": end}, "commits_by_user": dict(commits_by_user), "mr_stats": {"merged": mr_state["merged"], "opened": mr_state["opened"], "closed": mr_state["closed"]}, "daily_activity": dict(sorted(daily_activity.items())), "projects": dict(repo_activity), "dashboard": {"start": start, "end": end, **stats}, "top_contributors": top_contributors, "top_categories": top_categories}
    stats_file = report_dir / "stats.json"
    stats_file.write_text(json.dumps(stats_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.no_charts:
        try:
            subprocess.run([sys.executable, str((Path(__file__).parent / "generate-charts.py").resolve()), str(stats_file), str(charts_dir)], check=True)
        except Exception:
            pass

    report_title_prefix = cfg.get("report", {}).get("title_prefix", "GitLab Weekly Report")
    report = {"title": f"{report_title_prefix} {start} ~ {end}", "start": start, "end": end, "users": users_out, "product_sections": product_sections, "people_sections": people_sections, "stats": stats, "top_contributors": top_contributors[:5], "top_categories": top_categories[:5], "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    md = render_markdown(report)
    (report_dir / "weekly_report.md").write_text(md, encoding="utf-8")
    (report_dir / "weekly_report.html").write_text(render_html(report, stats_payload), encoding="utf-8")

    latest = output_dir / "latest"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(report_dir, target_is_directory=True)
    generate_index_html(output_dir, report_title_prefix)

    print(f"Report: {report_dir / 'weekly_report.md'}")
    print(f"HTML: {report_dir / 'weekly_report.html'}")
    print(f"Stats: {stats_file}")
    print(f"Index: {output_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
