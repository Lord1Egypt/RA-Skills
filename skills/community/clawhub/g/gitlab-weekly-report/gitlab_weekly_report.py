#!/usr/bin/env python3
"""
GitLab 周报生成器
查询个人提交记录并整理成周报格式
"""

import subprocess
import json
import argparse
from datetime import datetime, timedelta

GITLAB_URL = "自己公司内部的git地址"


def curl_request(url, token=None):
    """使用 curl 请求 API（更稳定），绕过代理"""
    cmd = ["curl", "-s", "-k", "--noproxy", "*"]  # --noproxy 绕过代理
    if token:
        cmd.extend(["-H", f"PRIVATE-TOKEN: {token}"])
    cmd.append(url)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"curl failed: {result.stderr}")
    return result.stdout


def get_events(token, user_id, after, before=None):
    """获取用户的提交事件"""
    params = f"action=pushed&author_id={user_id}&after={after}&per_page=100"
    if before:
        params += f"&before={before}"
    
    url = f"{GITLAB_URL}/api/v4/events?{params}"
    response = curl_request(url, token)
    return json.loads(response)


def get_project(token, project_id):
    """获取项目信息"""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}"
    response = curl_request(url, token)
    return json.loads(response)


def get_commits(token, project_id, ref_name, since, until, author_name=None):
    """获取指定分支的提交记录"""
    params = f"ref_name={ref_name}&since={since}&until={until}&per_page=100"
    if author_name:
        params += f"&author={author_name}"
    
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/commits?{params}"
    response = curl_request(url, token)
    return json.loads(response)


def generate_weekly_report(events, token, after, before):
    """生成周报"""
    # 收集需要查询的项目+分支组合（去重）
    project_branches = {}
    
    for event in events:
        project_id = event.get("project_id")
        if not project_id:
            continue
        
        ref = event.get("push_data", {}).get("ref", "")
        if not ref:
            continue
        
        key = (project_id, ref)
        if key not in project_branches:
            project_branches[key] = True
    
    # 获取项目名称并生成报告
    report_lines = []
    seen_commits = set()  # 整个报告去重
    
    for (project_id, ref_name), _ in project_branches.items():
        try:
            # 获取项目名称
            project_info = get_project(token, project_id)
            project_name = project_info.get("name_with_namespace", f"项目 {project_id}")
        except Exception:
            project_name = f"项目 {project_id}"
        
        # 获取该分支的完整提交
        try:
            commits = get_commits(token, project_id, ref_name, after, before or "2026-12-31", author_name="zhouyi")
        except Exception as e:
            print(f"  获取提交失败: {e}")
            commits = []
        
        if not commits:
            continue
        
        project_added = False
        
        for commit in commits:
            # 可能是错误响应字符串
            if isinstance(commit, str):
                continue
            
            title = commit.get("title", "无标题")
            message = commit.get("message", "")
            
            # 整个报告去重（用 commit id）
            commit_id = commit.get("id", "")
            if commit_id in seen_commits:
                continue
            seen_commits.add(commit_id)
            
            # 避免 title 和 message 相同时的重复显示
            msg_content = message.strip() if message else ""
            title_stripped = title.strip()
            
            if not project_added:
                report_lines.append(f"### {project_name}")
                project_added = True
            
            if msg_content and msg_content != title_stripped:
                report_lines.append(f"- {title}\n{msg_content}")
            else:
                report_lines.append(f"- {title}")
        
        if project_added:
            report_lines.append("")
    
    return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="GitLab 周报生成器")
    parser.add_argument("--token", required=True, help="GitLab Personal Access Token")
    parser.add_argument("--user-id", type=int, required=True, help="GitLab 用户 ID")
    parser.add_argument("--after", required=True, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--before", help="结束日期 (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    print(f"查询提交记录: {args.after} ~ {args.before or '现在'}")
    
    events = get_events(args.token, args.user_id, args.after, args.before)
    print(f"Events API 返回 {len(events)} 条事件")
    
    if not events:
        print("没有找到提交事件")
        return
    
    report = generate_weekly_report(events, args.token, args.after, args.before or "2026-12-31")
    
    print("\n" + "="*50)
    print("周报生成完成:")
    print("="*50)
    print(report)


if __name__ == "__main__":
    main()
