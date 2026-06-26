#!/usr/bin/env python3
"""
GitLab 智能项目洞察助手
- 多维度数据抓取：Commits / MRs / Issues / Pipelines
- 智能摘要：按功能模块聚类
- 管理洞察：阻塞点识别 + 风险预警
- 多样化输出：concise / detailed / executive
"""

import json
import os
import sys
import ssl
import re
import time
import urllib.request
import urllib.error
import urllib.parse
import concurrent.futures
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Optional, Dict, List, Any

# 忽略自签名证书
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# ── 配置 ──────────────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[错误] 配置文件不存在: {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)

# ── GitLab API ───────────────────────────────────────────────
def gitlab_get(config, path, max_retries=2):
    """调用 GitLab API，支持重试机制"""
    url = f"{config['gitlab_url'].rstrip('/')}/api/v4{path}"
    req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": config["gitlab_token"]})
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=20, context=_SSL_CTX) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                print(f"[警告] API 速率限制，等待重试...")
                time.sleep(5)
                continue
            print(f"[错误] GitLab API 请求失败: {e.code} {e.reason}")
            return None
        except Exception as e:
            if attempt < max_retries - 1:
                continue
            print(f"[错误] 请求异常: {e}")
            return None
    return None

# ── 时间处理 ─────────────────────────────────────────────────
def get_24h_ago_iso() -> str:
    """获取当前时间往前24小时的 UTC ISO 时间戳"""
    tz_offset = 8  # 默认东八区
    local_tz = timezone(timedelta(hours=tz_offset))
    now_local = datetime.now(local_tz)
    ago_24h = now_local - timedelta(hours=24)
    return ago_24h.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def get_today_range():
    """获取今天的开始和结束时间"""
    tz_offset = 8
    local_tz = timezone(timedelta(hours=tz_offset))
    now_local = datetime.now(local_tz)
    today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now_local.replace(hour=23, minute=59, second=59, microsecond=0)
    return (
        today_start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        today_end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        now_local.strftime("%Y-%m-%d")
    )

# ── 数据抓取 ─────────────────────────────────────────────────
def get_project_id(config, repo):
    """根据仓库路径获取 project id"""
    encoded = urllib.parse.quote(repo, safe="")
    data = gitlab_get(config, f"/projects/{encoded}")
    if data:
        return data["id"], data.get("name", repo.split("/")[-1])
    return None, None

def get_branches(config, project_id):
    """获取仓库所有分支名"""
    branches = []
    page = 1
    while True:
        data = gitlab_get(config, f"/projects/{project_id}/repository/branches?per_page=100&page={page}")
        if not data:
            break
        branches.extend([b["name"] for b in data])
        if len(data) < 100:
            break
        page += 1
    return branches

def get_commits(config, project_id, since_iso, until_iso):
    """获取指定时间段内的所有提交"""
    seen = set()
    commits = []
    branches = get_branches(config, project_id)
    
    for branch in branches:
        branch_enc = urllib.parse.quote(branch, safe="")
        page = 1
        while True:
            path = (f"/projects/{project_id}/repository/commits"
                   f"?ref_name={branch_enc}&since={since_iso}&until={until_iso}&per_page=100&page={page}")
            data = gitlab_get(config, path)
            if not data:
                break
            for c in data:
                if c["id"] not in seen:
                    seen.add(c["id"])
                    commits.append(c)
            if len(data) < 100:
                break
            page += 1
    return commits

def get_merge_requests(config, project_id, updated_after_iso):
    """获取过去24小时更新的 MRs"""
    # 开放的 MRs
    opened_mrs = gitlab_get(config, 
        f"/projects/{project_id}/merge_requests?state=opened&updated_after={updated_after_iso}&per_page=100")
    # 已合并的 MRs
    merged_mrs = gitlab_get(config,
        f"/projects/{project_id}/merge_requests?state=merged&updated_after={updated_after_iso}&per_page=100")
    
    mrs = []
    if opened_mrs:
        mrs.extend(opened_mrs)
    if merged_mrs:
        mrs.extend(merged_mrs)
    return mrs

def get_pipelines(config, project_id, updated_after_iso):
    """获取过去24小时的 Pipelines"""
    return gitlab_get(config, 
        f"/projects/{project_id}/pipelines?updated_after={updated_after_iso}&per_page=100") or []

def get_issues(config, project_id, updated_after_iso):
    """获取过去24小时更新的 Issues"""
    # 打开的 Issues
    opened_issues = gitlab_get(config,
        f"/projects/{project_id}/issues?state=opened&updated_after={updated_after_iso}&per_page=50")
    # 已关闭的 Issues
    closed_issues = gitlab_get(config,
        f"/projects/{project_id}/issues?state=closed&updated_after={updated_after_iso}&per_page=50")
    
    issues = []
    if opened_issues:
        issues.extend(opened_issues)
    if closed_issues:
        issues.extend(closed_issues)
    return issues

def fetch_all_data(config, repo):
    """并发抓取项目的所有数据"""
    result = get_project_id(config, repo)
    if not result[0]:
        print(f"[警告] 找不到仓库: {repo}")
        return None
    
    project_id, project_name = result
    since_iso, until_iso, date_label = get_today_range()
    updated_24h = get_24h_ago_iso()
    
    # 并发请求
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_commits = executor.submit(get_commits, config, project_id, since_iso, until_iso)
        future_mrs = executor.submit(get_merge_requests, config, project_id, updated_24h)
        future_pipelines = executor.submit(get_pipelines, config, project_id, updated_24h)
        future_issues = executor.submit(get_issues, config, project_id, updated_24h)
        
        commits = future_commits.result() or []
        mrs = future_mrs.result() or []
        pipelines = future_pipelines.result() or []
        issues = future_issues.result() or []
    
    return {
        "project_id": project_id,
        "project_name": project_name,
        "repo": repo,
        "commits": commits,
        "merge_requests": mrs,
        "pipelines": pipelines,
        "issues": issues
    }

# ── 数据关联与分析 ───────────────────────────────────────────
def extract_refs(commit_message: str) -> List[str]:
    """从 Commit Message 中提取 Issue/MR 引用 (如 #123)"""
    return re.findall(r'#(\d+)', commit_message)

def categorize_commit(title: str) -> str:
    """将提交归类到功能模块"""
    title_lower = title.lower()
    
    # 关键词匹配
    if any(k in title_lower for k in ["feat", "feature", "新增", "添加", "增加", "支持", "实现"]):
        return "✨ 新功能"
    if any(k in title_lower for k in ["fix", "修复", "bug", "问题", "解决", "兼容", "错误"]):
        return "🐛 Bug 修复"
    if any(k in title_lower for k in ["refactor", "重构", "优化", "chore", "update", "调整", "perf", "提升"]):
        return "🛠️ 重构与优化"
    if any(k in title_lower for k in ["docs", "文档", "readme", "注释", "comment"]):
        return "📄 文档/配置"
    if any(k in title_lower for k in ["test", "测试", "spec", "mock"]):
        return "🧪 测试"
    if any(k in title_lower for k in ["ci", "cd", "docker", "k8s", "deploy", "部署", "pipeline"]):
        return "🚀 部署/CI"
    if any(k in title_lower for k in ["security", "安全", "权限", "auth", "登录", "token"]):
        return "🔐 安全/权限"
    
    return "📌 其他"

def analyze_commits(commits: List[Dict]) -> Dict[str, Any]:
    """分析提交数据"""
    if not commits:
        return {"total": 0, "additions": 0, "deletions": 0, "authors": set(), 
                "by_category": {}, "by_author": defaultdict(list), "refs": defaultdict(list)}
    
    # 过滤自动化构建提交
    filtered = [c for c in commits if not c.get("title", "").lower().startswith("merge")]
    
    total = len(filtered)
    authors = set()
    by_category = defaultdict(list)
    by_author = defaultdict(list)
    refs = defaultdict(list)
    
    for c in filtered:
        author = c.get("author_name") or c.get("committer_name") or "Unknown"
        authors.add(author)
        
        title = c.get("title", "").strip()
        category = categorize_commit(title)
        
        by_category[category].append({"title": title, "author": author})
        by_author[author].append(title)
        
        # 提取关联的 Issue/MR
        issue_refs = extract_refs(c.get("message", ""))
        for ref in issue_refs:
            refs[f"#{ref}"].append({"title": title, "author": author, "type": "commit"})
    
    return {
        "total": total,
        "authors": authors,
        "by_category": dict(by_category),
        "by_author": dict(by_author),
        "refs": dict(refs)
    }

def analyze_merge_requests(mrs: List[Dict], updated_24h_ago: datetime) -> Dict[str, Any]:
    """分析 MR 数据，识别阻塞点和风险"""
    if not mrs:
        return {"total": 0, "opened": 0, "merged": 0, "blocked": [], "risks": []}
    
    opened = []
    merged = []
    blocked = []
    risks = []
    
    now = datetime.now(timezone.utc)
    
    for mr in mrs:
        state = mr.get("state")  # opened, merged, closed
        
        if state == "opened":
            opened.append(mr)
            
            # 检查是否阻塞超过24小时
            updated_at = mr.get("updated_at", "")
            if updated_at:
                try:
                    mr_time = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                    hours_open = (now - mr_time).total_seconds() / 3600
                    
                    # 阻塞条件：超过24小时未合并
                    if hours_open > 24:
                        # 检查是否有冲突
                        has_conflicts = mr.get("has_conflicts", False)
                        # 检查评审者
                        reviewers = mr.get("reviewers", [])
                        approvals_required = mr.get("approvals_required", 0)
                        
                        blocked.append({
                            "iid": mr.get("iid"),
                            "title": mr.get("title"),
                            "author": mr.get("author", {}).get("name", "Unknown"),
                            "hours_open": int(hours_open),
                            "has_conflicts": has_conflicts,
                            "reviewers_count": len(reviewers),
                            "web_url": mr.get("web_url")
                        })
                except:
                    pass
                    
        elif state == "merged":
            merged.append(mr)
    
    return {
        "total": len(mrs),
        "opened": len(opened),
        "merged": len(merged),
        "blocked": blocked,
        "risks": risks
    }

def analyze_pipelines(pipelines: List[Dict]) -> Dict[str, Any]:
    """分析 Pipeline 状态"""
    if not pipelines:
        return {"total": 0, "success": 0, "failed": 0, "running": 0, "failed_pipelines": []}
    
    status_counts = defaultdict(int)
    failed_pipelines = []
    
    for p in pipelines:
        status = p.get("status", "unknown")
        status_counts[status] += 1
        
        if status == "failed":
            failed_pipelines.append({
                "id": p.get("id"),
                "ref": p.get("ref"),
                "status": status,
                "web_url": p.get("web_url")
            })
    
    return {
        "total": len(pipelines),
        "success": status_counts.get("success", 0),
        "failed": status_counts.get("failed", 0),
        "running": status_counts.get("running", 0),
        "failed_pipelines": failed_pipelines
    }

def check_risks(commits: List[Dict]) -> List[str]:
    """检查高风险代码变动"""
    risks = []
    sensitive_patterns = [r"\.env", r"sql/", r"security/", r"config/credentials", r"\.key$", r"password"]
    
    for c in commits:
        # 检查敏感文件
        diff_refs = c.get("parent_ids", [])
        
        # 检查大量代码删除
        # 注意：GitLab commit API 默认不返回 diff，需要单独请求
        # 这里简化处理：检查 commit message 中是否有危险关键词
        title = c.get("title", "").lower()
        
        if any(re.search(p, title) for p in ["删除", "remove", "delete", "drop", "安全", "security", "凭证", "credential"]):
            # 简单标记为潜在风险
            pass
    
    # 检测敏感文件路径的变更（需要 diff API，这里简化）
    return risks

# ── 报告生成 ─────────────────────────────────────────────────
def calculate_activity_level(total_commits: int, active_members: int) -> str:
    """计算代码变动活跃度"""
    if total_commits >= 30 or (total_commits >= 15 and active_members >= 5):
        return "High"
    elif total_commits >= 10 or (total_commits >= 5 and active_members >= 3):
        return "Med"
    return "Low"

def generate_summary(commits_analysis: Dict, mrs_analysis: Dict, pipelines_analysis: Dict) -> str:
    """生成智能摘要（按功能模块聚类）"""
    by_category = commits_analysis.get("by_category", {})
    if not by_category:
        return "今日暂无功能提交记录"
    
    lines = []
    for category, items in sorted(by_category.items()):
        count = len(items)
        # 取前3个代表性的提交
        samples = [item["title"][:60] + "..." if len(item["title"]) > 60 else item["title"] 
                   for item in items[:3]]
        
        if count <= 3:
            detail = "、".join(samples)
        else:
            detail = "、".join(samples) + f" 等{count}项"
        
        lines.append(f"  {category} ({count}项): {detail}")
    
    return "\n".join(lines)

def format_report_concise(data: Dict, date_label: str) -> str:
    """极简格式"""
    total_commits = data["commits_analysis"]["total"]
    active_members = len(data["commits_analysis"]["authors"])
    activity = calculate_activity_level(total_commits, active_members)
    
    blocked = data["mrs_analysis"]["blocked"]
    failed = data["pipelines_analysis"]["failed"]
    
    lines = [
        f"📅 [{data['project_name']}] 每日进度报告 ({date_label})",
        f"📊 代码变动: {total_commits} commits | {active_members} 成员 | 活跃度: {activity}",
    ]
    
    if blocked or failed:
        lines.append(f"⚠️ 需关注: {len(blocked)} 个阻塞 MR, {failed} 个失败 Pipeline")
    
    return "\n".join(lines)

def format_report_detailed(data: Dict, date_label: str) -> str:
    """详细格式"""
    commits_analysis = data["commits_analysis"]
    mrs_analysis = data["mrs_analysis"]
    pipelines_analysis = data["pipelines_analysis"]
    
    total_commits = commits_analysis["total"]
    active_members = len(commits_analysis["authors"])
    activity = calculate_activity_level(total_commits, active_members)
    
    lines = [
        f"📅 [{data['project_name']}] 每日进度报告 ({date_label})",
        "=" * 50,
        "🚀 核心进展",
    ]
    
    # 按功能模块显示
    summary = generate_summary(commits_analysis, mrs_analysis, pipelines_analysis)
    lines.append(summary)
    
    # 风险与阻塞
    lines.append("\n⚠️ 风险与阻塞")
    blocked = mrs_analysis["blocked"]
    if blocked:
        for b in blocked[:5]:
            lines.append(f"  • MR !{b['iid']}: {b['title'][:50]} (卡住 {b['hours_open']}h)")
    else:
        lines.append("  ✓ 无阻塞 MR")
    
    failed_pipelines = pipelines_analysis.get("failed_pipelines", [])
    if failed_pipelines:
        for p in failed_pipelines[:3]:
            lines.append(f"  • Pipeline #{p['id']}: {p['ref']} 失败")
    else:
        lines.append("  ✓ 无失败 Pipeline")
    
    # 统计
    lines.append("\n📊 统计洞察")
    lines.append(f"  代码提交: {total_commits} 次 | 活跃成员: {active_members} 人")
    lines.append(f"  MR: {mrs_analysis['opened']} 开放, {mrs_analysis['merged']} 已合并")
    lines.append(f"  Pipeline: {pipelines_analysis['success']} 成功, {pipelines_analysis['failed']} 失败")
    lines.append(f"  活跃度评级: {activity}")
    
    return "\n".join(lines)

def format_report_executive(data: Dict, date_label: str) -> str:
    """管理层汇报格式"""
    commits_analysis = data["commits_analysis"]
    mrs_analysis = data["mrs_analysis"]
    pipelines_analysis = data["pipelines_analysis"]
    
    total_commits = commits_analysis["total"]
    active_members = len(commits_analysis["authors"])
    activity = calculate_activity_level(total_commits, active_members)
    
    # 按类别统计
    by_category = commits_analysis.get("by_category", {})
    category_counts = {cat: len(items) for cat, items in by_category.items()}
    
    blocked_count = len(mrs_analysis["blocked"])
    failed_count = pipelines_analysis["failed"]
    
    # 风险评估
    risk_level = "🟢 低" if blocked_count == 0 and failed_count == 0 else \
                 "🟡 中" if blocked_count <= 2 and failed_count <= 1 else "🔴 高"
    
    lines = [
        f"📋 [执行摘要] {data['project_name']} - {date_label}",
        "─" * 50,
        f"✅ 今日产出: {total_commits} 次代码提交, {active_members} 位成员活跃",
        f"📈 活跃度: {activity} | 风险等级: {risk_level}",
    ]
    
    if category_counts:
        lines.append("\n📌 产出分布:")
        for cat, cnt in sorted(category_counts.items(), key=lambda x: -x[1])[:4]:
            lines.append(f"  • {cat}: {cnt}")
    
    if blocked_count > 0:
        lines.append(f"\n⚠️ 阻塞事项: {blocked_count} 个 MR 超过24小时未处理")
    else:
        lines.append("\n✓ 无阻塞事项")
    
    if failed_count > 0:
        lines.append(f"⚠️ 构建问题: {failed_count} 个 Pipeline 失败")
    else:
        lines.append("✓ 构建正常")
    
    # 成员产出
    by_author = commits_analysis.get("by_author", {})
    if by_author:
        top_member = max(by_author.items(), key=lambda x: len(x[1]))
        lines.append(f"\n🏆 今日之星: {top_member[0]} ({len(top_member[1])} 次提交)")
    
    return "\n".join(lines)

def format_feishu_message(data: Dict, date_label: str, output_style: str = "detailed") -> Dict:
    """生成飞书富文本消息"""
    commits_analysis = data["commits_analysis"]
    mrs_analysis = data["mrs_analysis"]
    pipelines_analysis = data["pipelines_analysis"]
    
    total = commits_analysis["total"]
    activity = calculate_activity_level(total, len(commits_analysis["authors"]))
    
    # 根据风格生成不同格式
    if output_style == "concise":
        report_text = format_report_concise(data, date_label)
    elif output_style == "executive":
        report_text = format_report_executive(data, date_label)
    else:
        report_text = format_report_detailed(data, date_label)
    
    # 构建飞书消息
    lines = report_text.split("\n")
    content_lines = [[{"tag": "text", "text": line}] for line in lines]
    
    # 添加详细进展（仅 detailed 模式）
    if output_style == "detailed":
        by_category = commits_analysis.get("by_category", {})
        if by_category:
            content_lines.append([{"tag": "text", "text": ""}])
            content_lines.append([{"tag": "text", "text": "📋 详细变更:"}])
            
            for category, items in sorted(by_category.items()):
                content_lines.append([{"tag": "text", "text": f"\n{category} ({len(items)}项):"}])
                for item in items[:5]:
                    title = item["title"][:70] + "..." if len(item["title"]) > 70 else item["title"]
                    content_lines.append([{"tag": "text", "text": f"  • {title}"}])
    
    # 添加阻塞 MR 详情
    blocked = mrs_analysis.get("blocked", [])
    if blocked and output_style != "concise":
        content_lines.append([{"tag": "text", "text": ""}])
        content_lines.append([{"tag": "text", "text": "🚧 阻塞中的 MR:"}])
        for b in blocked[:3]:
            content_lines.append([{"tag": "text", "text": f"  !{b['iid']} - {b['title'][:50]} (卡住 {b['hours_open']}h)"}])
    
    title_suffix = {"concise": "📝 极简", "detailed": "📋 详细", "executive": "📊 管理层"}[output_style]
    
    return {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"🔍 [{data['project_name']}] {title_suffix}报告 ({date_label})",
                    "content": content_lines
                }
            }
        }
    }

# ── 飞书推送 ─────────────────────────────────────────────────
def send_feishu(webhook_url: str, message: Dict):
    """发送消息到飞书"""
    data = json.dumps(message).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=_SSL_CTX) as resp:
            result = json.loads(resp.read().decode())
            if result.get("code") == 0 or result.get("StatusCode") == 0:
                return True, "发送成功"
            else:
                return False, f"返回异常: {result}"
    except Exception as e:
        return False, str(e)

# ── 主流程 ───────────────────────────────────────────────────
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="GitLab 智能项目洞察助手")
    parser.add_argument("--style", choices=["concise", "detailed", "executive"], 
                       default="detailed", help="输出风格")
    parser.add_argument("--preview", action="store_true", help="仅预览不推送")
    parser.add_argument("--raw", action="store_true", help="输出原始 JSON 数据供 AI 分析")
    args = parser.parse_args()
    
    config = load_config()
    since_iso, until_iso, date_label = get_today_range()
    updated_24h = get_24h_ago_iso()
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始拉取 GitLab 数据...")
    
    all_data = []
    for repo in config["repositories"]:
        print(f"📦 抓取 {repo}...")
        repo_data = fetch_all_data(config, repo)
        if repo_data:
            # 分析数据
            commits_analysis = analyze_commits(repo_data["commits"])
            mrs_analysis = analyze_merge_requests(repo_data["merge_requests"], 
                                                   datetime.fromisoformat(updated_24h.replace("Z", "+00:00")))
            pipelines_analysis = analyze_pipelines(repo_data["pipelines"])
            
            repo_data["commits_analysis"] = commits_analysis
            repo_data["mrs_analysis"] = mrs_analysis
            repo_data["pipelines_analysis"] = pipelines_analysis
            
            all_data.append(repo_data)
            print(f"  ✓ Commits: {commits_analysis['total']}, MRs: {mrs_analysis['total']}, Pipelines: {pipelines_analysis['total']}")
    
    # 汇总报告
    total_commits = sum(d["commits_analysis"]["total"] for d in all_data)
    total_members = set()
    for d in all_data:
        total_members.update(d["commits_analysis"]["authors"])
    
    print(f"\n📊 汇总: {total_commits} 次提交, {len(total_members)} 位成员")
    
    # 生成并显示报告
    for repo_data in all_data:
        print(f"\n{'='*50}")
        print(f"📁 {repo_data['project_name']}")
        print('='*50)
        
        if args.style == "concise":
            print(format_report_concise(repo_data, date_label))
        elif args.style == "executive":
            print(format_report_executive(repo_data, date_label))
        else:
            print(format_report_detailed(repo_data, date_label))
    
    # 输出原始数据供 AI 分析
    if args.raw:
        print("\n" + "=" * 60)
        print("📦 原始数据 (JSON)")
        print("=" * 60)
        
        # 构建 AI 友好的数据结构
        raw_output = {
            "date": date_label,
            "summary": {
                "total_commits": total_commits,
                "active_members": len(total_members),
                "repositories": [d["project_name"] for d in all_data]
            },
            "projects": []
        }
        
        for repo_data in all_data:
            proj = {
                "name": repo_data["project_name"],
                "commits": {
                    "total": repo_data["commits_analysis"]["total"],
                    "by_category": repo_data["commits_analysis"]["by_category"],
                    "by_author": repo_data["commits_analysis"]["by_author"],
                    "active_members": list(repo_data["commits_analysis"]["authors"])
                },
                "merge_requests": {
                    "total": repo_data["mrs_analysis"]["total"],
                    "opened": repo_data["mrs_analysis"]["opened"],
                    "merged": repo_data["mrs_analysis"]["merged"],
                    "blocked": repo_data["mrs_analysis"]["blocked"]
                },
                "pipelines": {
                    "total": repo_data["pipelines_analysis"]["total"],
                    "success": repo_data["pipelines_analysis"]["success"],
                    "failed": repo_data["pipelines_analysis"]["failed"],
                    "failed_list": repo_data["pipelines_analysis"]["failed_pipelines"]
                }
            }
            raw_output["projects"].append(proj)
        
        print(json.dumps(raw_output, ensure_ascii=False, indent=2))
    
    # 发送飞书
    if not args.preview:
        print(f"\n🚀 推送到飞书 ({args.style} 模式)...")
        for repo_data in all_data:
            message = format_feishu_message(repo_data, date_label, args.style)
            
            for webhook in config["feishu_webhooks"]:
                if webhook.startswith("http"):
                    success, msg = send_feishu(webhook, message)
                    if success:
                        print(f"  ✅ {repo_data['project_name']}: {msg}")
                    else:
                        print(f"  ❌ {repo_data['project_name']}: {msg}")
    
    print("\n✨ 完成!")

if __name__ == "__main__":
    main()
