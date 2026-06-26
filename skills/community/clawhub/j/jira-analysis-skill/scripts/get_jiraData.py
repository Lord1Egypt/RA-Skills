# -*- coding: utf-8 -*-
"""
@author: Rain
@file: get_jiraData.py
@time: 2026/4/14 12:26

Jira Bug Data Fetcher
Pulls bug issues from Jira Server/Data Center via REST API v2,
computes aggregation statistics, and outputs structured JSON to stdout.
"""

import argparse
import json
import sys
import statistics
from datetime import datetime, timezone
from collections import Counter

import requests
import urllib3






def log(msg):
    """
    将诊断信息输出到标准错误流 (stderr)，避免污染 stdout 的 JSON 输出。
    """
    print(msg, file=sys.stderr, flush=True)


def parse_args():
    """解析命令行参数，包括 Jira 服务器地址、认证信息、项目名、日期范围等，并进行格式校验。"""
    parser = argparse.ArgumentParser(
        description="Fetch bug data from Jira Server/DC and output structured JSON."
    )
    parser.add_argument("--server", required=True, help="Jira base URL, e.g. https://jira.company.com")
    parser.add_argument("--token", help="Personal Access Token (Bearer auth)")
    parser.add_argument("--username", help="Basic Auth username")
    parser.add_argument("--password", help="Basic Auth password")
    parser.add_argument("--project", required=True, help="Jira project key, e.g. PROJ")
    parser.add_argument("--start-date", help="Filter bugs created on/after this date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Filter bugs created on/before this date (YYYY-MM-DD)")
    parser.add_argument("--max-results", type=int, default=1000, help="Max issues to fetch (default: 1000)")
    parser.add_argument("--page-size", type=int, default=100, help="Results per page (default: 100)")
    parser.add_argument("--no-verify", action="store_true", help="Disable SSL certificate verification")
    parser.add_argument("--severity-field", default="customfield_10072",
                        help="Custom field ID for severity (default: customfield_10072)")
    parser.add_argument("--issue-type", default="Bug",
                        help="Issue type name to query (default: Bug). Use '故障' for Chinese Jira instances.")

    args = parser.parse_args()

    if not args.token and not (args.username and args.password):
        parser.error("Either --token or both --username and --password are required.")

    if args.start_date:
        try:
            datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            parser.error("--start-date must be in YYYY-MM-DD format.")

    if args.end_date:
        try:
            datetime.strptime(args.end_date, "%Y-%m-%d")
        except ValueError:
            parser.error("--end-date must be in YYYY-MM-DD format.")

    args.server = args.server.rstrip("/")
    return args


def build_jql(project, issue_type="Bug", start_date=None, end_date=None):
    """根据项目名称、Issue 类型和可选的起止日期，构建 Jira 查询语言 (JQL) 查询字符串。"""
    jql = f'issuetype = {issue_type} AND project = {project}'
    if start_date:
        jql += f' AND created >= "{start_date}"'
    if end_date:
        jql += f' AND created <= "{end_date}"'
    jql += " ORDER BY created DESC"
    return jql


def build_session(args):
    """创建并配置 HTTP 会话，设置认证方式（PAT Bearer 或 Basic Auth）和 SSL 验证选项。"""
    session = requests.Session()
    if args.token:
        session.headers["Authorization"] = f"Bearer {args.token}"
    else:
        session.auth = (args.username, args.password)
    session.headers["Content-Type"] = "application/json"
    session.verify = not args.no_verify
    if args.no_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return session


def fetch_issues(session, server, jql, fields, max_results, page_size):
    """通过 Jira REST API v2 分页拉取 Issue 数据，包含完整的错误处理（SSL/连接/超时/HTTP 状态码）。"""
    url = f"{server}/rest/api/2/search"
    all_issues = []
    start_at = 0
    total = None

    while True:
        if total is not None and start_at >= total:
            break
        if start_at >= max_results:
            break

        current_page_size = min(page_size, max_results - start_at)
        payload = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": current_page_size,
            "fields": fields,
        }

        try:
            resp = session.post(url, json=payload, timeout=30)
        except requests.exceptions.SSLError as e:
            log(f"ERROR: SSL certificate verification failed: {e}")
            log("Hint: Use --no-verify for self-signed certificates.")
            sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            log(f"ERROR: Cannot connect to {server}: {e}")
            log("Hint: Check the server URL and your network/VPN connection.")
            sys.exit(1)
        except requests.exceptions.Timeout:
            log(f"ERROR: Request timed out after 30s. Server may be slow or unreachable.")
            sys.exit(1)

        if resp.status_code == 401:
            log("ERROR: Authentication failed (401). Check your token or username/password.")
            sys.exit(1)
        elif resp.status_code == 403:
            log("ERROR: Permission denied (403). Ensure your account has access to this project.")
            sys.exit(1)
        elif resp.status_code == 404:
            log("ERROR: Not found (404). Check the server URL. Expected REST API at /rest/api/2/search.")
            sys.exit(1)
        elif resp.status_code >= 400:
            log(f"ERROR: HTTP {resp.status_code}: {resp.text[:500]}")
            sys.exit(1)

        try:
            data = resp.json()
        except ValueError:
            log(f"WARNING: Failed to parse JSON response at startAt={start_at}. Skipping page.")
            start_at += current_page_size
            continue

        if total is None:
            total = data.get("total", 0)
            log(f"Total matching issues: {total}")

        issues = data.get("issues", [])
        all_issues.extend(issues)
        start_at += len(issues)
        log(f"Fetched {len(all_issues)}/{min(total, max_results)} issues...")

        if len(issues) == 0:
            break

    return all_issues, total or 0


def safe_get(obj, *keys, default=None):
    """
    安全地遍历嵌套字典，任意层级为 None 时返回默认值，避免 KeyError。
    """
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return default
        if current is None:
            return default
    return current


def parse_jira_datetime(dt_str):
    """
    将 Jira 返回的日期时间字符串（如 2026-01-15T10:30:00.000+0800）解析为 Python datetime 对象。
    """
    if not dt_str:
        return None
    try:
        # Jira format: 2026-01-15T10:30:00.000+0800
        # Python 3.12 can handle this with fromisoformat after replacing the tz offset
        dt_str_fixed = dt_str
        if len(dt_str) > 19 and "+" in dt_str[19:] and ":" not in dt_str[-3:]:
            # Convert +0800 to +08:00
            dt_str_fixed = dt_str[:-2] + ":" + dt_str[-2:]
        return datetime.fromisoformat(dt_str_fixed)
    except (ValueError, IndexError):
        return None


def extract_issue(raw_issue, severity_field):
    """
    从 Jira 原始 Issue 数据中提取扁平化字典，包含 key、状态、优先级、严重程度、经办人、解决天数等 15+ 个字段。
    """
    fields = raw_issue.get("fields", {})
    created_dt = parse_jira_datetime(fields.get("created"))
    resolved_dt = parse_jira_datetime(fields.get("resolutiondate"))

    resolution_days = None
    if created_dt and resolved_dt:
        resolution_days = round((resolved_dt - created_dt).total_seconds() / 86400, 2)

    severity_obj = fields.get(severity_field)
    severity = None
    if severity_obj:
        severity = severity_obj.get("value") or severity_obj.get("name")

    time_tracking = fields.get("timetracking") or {}
    original_estimate_sec = time_tracking.get("originalEstimateSeconds")
    time_spent_sec = time_tracking.get("timeSpentSeconds")

    return {
        "key": raw_issue.get("key"),
        "summary": fields.get("summary"),
        "status": safe_get(fields, "status", "name"),
        "priority": safe_get(fields, "priority", "name"),
        "severity": severity,
        "assignee": safe_get(fields, "assignee", "displayName"),
        "reporter": safe_get(fields, "reporter", "displayName"),
        "created": fields.get("created"),
        "resolved": fields.get("resolutiondate"),
        "resolution": safe_get(fields, "resolution", "name"),
        "components": [c.get("name") for c in (fields.get("components") or []) if c.get("name")],
        "labels": fields.get("labels") or [],
        "fix_versions": [v.get("name") for v in (fields.get("fixVersions") or []) if v.get("name")],
        "time_original_estimate_hours": round(original_estimate_sec / 3600, 2) if original_estimate_sec else None,
        "time_spent_hours": round(time_spent_sec / 3600, 2) if time_spent_sec else None,
        "resolution_days": resolution_days,
    }


def is_resolved(issue):
    """
    1. resolution 字段不为空 → 已解决
    2. resolution 为空时，按 status 二次判定：已关闭/INVALID/DUPLICATED/无法复现/已解决 → 已解决
    """
    if issue["resolution"]:
        return True
    return issue["status"] in ("已关闭", "INVALID", "DUPLICATED", "无法复现", "已解决")


def compute_aggregations(issues):
    """
    基于提取后的 Issue 列表计算 15+ 种聚合统计，包括按状态/优先级/严重程度/组件/月份分布、解决时间统计、未解决 Bug 老化分析等。
    """
    agg = {}

    # Classify each issue as resolved/unresolved and store the flag
    for i in issues:
        i["_resolved"] = is_resolved(i)

    # Simple counters
    agg["by_status"] = dict(Counter(i["status"] for i in issues if i["status"]))
    agg["by_priority"] = dict(Counter(i["priority"] for i in issues if i["priority"]))
    agg["by_severity"] = dict(Counter(i["severity"] for i in issues if i["severity"]))
    agg["by_resolution"] = dict(Counter(i["resolution"] for i in issues if i["resolution"]))

    # Assignee and reporter
    agg["by_assignee"] = dict(Counter(i["assignee"] or "Unassigned" for i in issues))
    agg["by_reporter"] = dict(Counter(i["reporter"] or "Unknown" for i in issues))

    # Assignee detailed breakdown (total / resolved / unresolved / mean resolution days)
    assignee_groups = {}
    for i in issues:
        name = i["assignee"] or "Unassigned"
        if name not in assignee_groups:
            assignee_groups[name] = {"total": 0, "resolved": 0, "unresolved": 0, "resolution_days_list": []}
        assignee_groups[name]["total"] += 1
        if i["_resolved"]:
            assignee_groups[name]["resolved"] += 1
            if i["resolution_days"] is not None:
                assignee_groups[name]["resolution_days_list"].append(i["resolution_days"])
        else:
            assignee_groups[name]["unresolved"] += 1

    by_assignee_detailed = {}
    for name, data in assignee_groups.items():
        mean_rt = None
        if data["resolution_days_list"]:
            mean_rt = round(statistics.mean(data["resolution_days_list"]), 2)
        by_assignee_detailed[name] = {
            "total": data["total"],
            "resolved": data["resolved"],
            "unresolved": data["unresolved"],
            "mean_resolution_days": mean_rt,
        }
    agg["by_assignee_detailed"] = by_assignee_detailed

    # Components (one issue can have multiple)
    component_counter = Counter()
    for i in issues:
        for c in i["components"]:
            component_counter[c] += 1
    agg["by_component"] = dict(component_counter)

    # Labels
    label_counter = Counter()
    for i in issues:
        for label in i["labels"]:
            label_counter[label] += 1
    agg["by_label"] = dict(label_counter)

    # Monthly created/resolved
    month_created = Counter()
    month_resolved = Counter()
    for i in issues:
        if i["created"]:
            month_created[i["created"][:7]] += 1
        if i["resolved"]:
            month_resolved[i["resolved"][:7]] += 1
    agg["by_month_created"] = dict(sorted(month_created.items()))
    agg["by_month_resolved"] = dict(sorted(month_resolved.items()))

    # Resolution time statistics
    resolution_days_list = [i["resolution_days"] for i in issues if i["resolution_days"] is not None]
    if resolution_days_list:
        sorted_days = sorted(resolution_days_list)
        p90_index = int(len(sorted_days) * 0.9)
        agg["resolution_time_stats"] = {
            "mean_days": round(statistics.mean(sorted_days), 2),
            "median_days": round(statistics.median(sorted_days), 2),
            "p90_days": round(sorted_days[min(p90_index, len(sorted_days) - 1)], 2),
            "min_days": round(sorted_days[0], 2),
            "max_days": round(sorted_days[-1], 2),
            "count": len(sorted_days),
        }
    else:
        agg["resolution_time_stats"] = {
            "mean_days": None, "median_days": None, "p90_days": None,
            "min_days": None, "max_days": None, "count": 0,
        }

    # Resolution time by priority
    by_priority_rt = {}
    for priority in set(i["priority"] for i in issues if i["priority"]):
        days_list = [i["resolution_days"] for i in issues
                     if i["priority"] == priority and i["resolution_days"] is not None]
        if days_list:
            by_priority_rt[priority] = {
                "mean_days": round(statistics.mean(days_list), 2),
                "median_days": round(statistics.median(days_list), 2),
                "count": len(days_list),
            }
    agg["by_priority_resolution_time"] = by_priority_rt

    # Resolution time by severity
    by_severity_rt = {}
    for severity in set(i["severity"] for i in issues if i["severity"]):
        days_list = [i["resolution_days"] for i in issues
                     if i["severity"] == severity and i["resolution_days"] is not None]
        if days_list:
            by_severity_rt[severity] = {
                "mean_days": round(statistics.mean(days_list), 2),
                "median_days": round(statistics.median(days_list), 2),
                "count": len(days_list),
            }
    agg["by_severity_resolution_time"] = by_severity_rt

    # Unresolved analysis
    now = datetime.now(timezone.utc)
    unresolved = [i for i in issues if not i["_resolved"]]
    agg["unresolved_count"] = len(unresolved)
    agg["unresolved_by_priority"] = dict(Counter(
        i["priority"] or "None" for i in unresolved
    ))

    # Aging buckets for unresolved
    aging = {"0-7_days": 0, "8-30_days": 0, "31-90_days": 0, "90+_days": 0}
    for i in unresolved:
        created_dt = parse_jira_datetime(i["created"])
        if created_dt:
            if created_dt.tzinfo is None:
                age_days = (datetime.now() - created_dt).days
            else:
                age_days = (now - created_dt).days
            if age_days <= 7:
                aging["0-7_days"] += 1
            elif age_days <= 30:
                aging["8-30_days"] += 1
            elif age_days <= 90:
                aging["31-90_days"] += 1
            else:
                aging["90+_days"] += 1
    agg["unresolved_aging"] = aging

    # Quality indicators
    agg["bugs_with_no_assignee"] = sum(1 for i in issues if not i["assignee"])
    agg["bugs_with_no_component"] = sum(1 for i in issues if not i["components"])

    return agg


def main():
    """主入口函数：解析参数、构建查询、拉取数据、提取字段、计算聚合统计，最终将结果以 JSON 格式输出到 stdout。"""
    args = parse_args()

    jql = build_jql(args.project, args.issue_type, args.start_date, args.end_date)
    log(f"JQL: {jql}")

    fields = [
        "summary", "status", "priority", "assignee", "reporter",
        "created", "resolutiondate", "resolution", "components",
        "labels", "fixVersions", "timetracking", "issuetype", "updated",
        args.severity_field,
    ]

    session = build_session(args)
    raw_issues, total_matching = fetch_issues(
        session, args.server, jql, fields, args.max_results, args.page_size
    )

    log(f"Extracting and processing {len(raw_issues)} issues...")
    extracted = [extract_issue(ri, args.severity_field) for ri in raw_issues]

    log("Computing aggregations...")
    aggregations = compute_aggregations(extracted)

    result = {
        "metadata": {
            "server": args.server,
            "project": args.project,
            "jql": jql,
            "total_fetched": len(extracted),
            "total_matching": total_matching,
            "date_range": {
                "start": args.start_date,
                "end": args.end_date,
            },
            "fetched_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "severity_field": args.severity_field,
        },
        "aggregations": aggregations,
        "issues": extracted,
    }

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    log("\nDone. JSON output written to stdout.")


if __name__ == "__main__":
    main()
