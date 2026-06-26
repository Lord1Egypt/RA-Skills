#!/usr/bin/env python3
"""
PingCode API Client - 自动生成项目周报
"""

import requests
import json
import sys
import os
import argparse
from datetime import datetime, timedelta

# PingCode API 配置
BASE_URL = "https://open.pingcode.com"

# 从环境变量读取凭证（不要硬编码）
CLIENT_ID = os.environ.get("PINGCODE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PINGCODE_CLIENT_SECRET")

def get_access_token():
    """获取企业令牌"""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("错误：请设置环境变量 PINGCODE_CLIENT_ID 和 PINGCODE_CLIENT_SECRET", file=sys.stderr)
        sys.exit(1)
    
    url = f"{BASE_URL}/v1/auth/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"获取令牌失败: {e}", file=sys.stderr)
        # 不打印 response.text，避免泄露敏感信息
        return None

def get_project_workitems(access_token, project_id=None, start_date=None, end_date=None):
    """获取工作项列表"""
    url = f"{BASE_URL}/v1/project/work_items"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "page_size": 100,
        "page_index": 0
    }
    if project_id:
        params["project_id"] = project_id
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取工作项失败: {e}", file=sys.stderr)
        return None

def get_iterations(access_token, project_id=None):
    """获取迭代列表"""
    url = f"{BASE_URL}/v1/agile/iterations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "page_size": 50,
        "page_index": 0
    }
    if project_id:
        params["project_id"] = project_id
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取迭代失败: {e}", file=sys.stderr)
        return None

def analyze_workitems(workitems_data, start_date=None, end_date=None):
    """分析工作项数据"""
    if not workitems_data or "values" not in workitems_data:
        return None
    
    items = workitems_data["values"]
    
    stats = {
        "total": len(items),
        "completed": 0,
        "in_progress": 0,
        "todo": 0,
        "delayed": 0,
        "bugs": 0,
        "stories": 0,
        "tasks": 0,
        "high_priority": 0
    }
    
    completed_items = []
    in_progress_items = []
    delayed_items = []
    
    for item in items:
        status_obj = item.get("status") or {}
        status = status_obj.get("name", "") if isinstance(status_obj, dict) else ""
        
        type_obj = item.get("type") or {}
        item_type = type_obj.get("name", "").lower() if isinstance(type_obj, dict) else ""
        
        priority_obj = item.get("priority") or {}
        priority = priority_obj.get("name", "") if isinstance(priority_obj, dict) else ""
        
        # 统计类型
        if "bug" in item_type or "缺陷" in item_type:
            stats["bugs"] += 1
        elif "story" in item_type or "需求" in item_type:
            stats["stories"] += 1
        elif "task" in item_type or "任务" in item_type:
            stats["tasks"] += 1
        
        # 统计优先级
        if "高" in priority or "high" in priority.lower():
            stats["high_priority"] += 1
        
        # 统计状态
        if any(s in status for s in ["完成", "done", "closed", "已关闭"]):
            stats["completed"] += 1
            completed_items.append(item)
        elif any(s in status for s in ["进行中", "progress", "处理中"]):
            stats["in_progress"] += 1
            in_progress_items.append(item)
        else:
            stats["todo"] += 1
        
        # 检查延期（简化判断：如果截止日期已过且未完成）
        due_date = item.get("due_date")
        if due_date and any(s in status for s in ["完成", "done", "closed"]) == False:
            try:
                due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                if due < datetime.now().astimezone():
                    stats["delayed"] += 1
                    delayed_items.append(item)
            except:
                pass
    
    return {
        "stats": stats,
        "completed_items": completed_items[:10],  # 取前10个
        "in_progress_items": in_progress_items[:10],
        "delayed_items": delayed_items[:5]
    }

def generate_weekly_report(analysis, project_name="项目"):
    """生成周报文本"""
    if not analysis:
        return "暂无数据"
    
    stats = analysis["stats"]
    completed = analysis["completed_items"]
    in_progress = analysis["in_progress_items"]
    delayed = analysis["delayed_items"]
    
    # 计算完成率
    completion_rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    
    report = []
    report.append(f"# 📊 {project_name} 周报")
    report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # 概览
    report.append("## 📈 数据概览")
    report.append(f"- 工作项总数：{stats['total']}")
    report.append(f"- 本周完成：{stats['completed']} ({completion_rate:.1f}%)")
    report.append(f"- 进行中：{stats['in_progress']}")
    report.append(f"- 待处理：{stats['todo']}")
    report.append(f"- 延期风险：{stats['delayed']}")
    report.append("")
    
    # 类型分布
    report.append("## 📋 类型分布")
    report.append(f"- 需求：{stats['stories']}")
    report.append(f"- 任务：{stats['tasks']}")
    report.append(f"- Bug：{stats['bugs']}")
    report.append(f"- 高优先级：{stats['high_priority']}")
    report.append("")
    
    # 完成情况
    if completed:
        report.append("## ✅ 本周完成")
        for item in completed[:5]:  # 只显示前5个
            title = item.get("title", "无标题")
            item_type = item.get("type", {}).get("name", "")
            report.append(f"- [{item_type}] {title}")
        report.append("")
    
    # 进行中
    if in_progress:
        report.append("## 🔄 进行中")
        for item in in_progress[:5]:
            title = item.get("title", "无标题")
            assignee = item.get("assignee", {}).get("display_name", "未分配")
            report.append(f"- {title} (@{assignee})")
        report.append("")
    
    # 延期风险
    if delayed:
        report.append("## ⚠️ 延期风险")
        report.append(f"发现 {len(delayed)} 个工作项已延期，建议优先处理：")
        for item in delayed[:3]:
            title = item.get("title", "无标题")
            due_date = item.get("due信息由于安全原因被截断")
            report.append(f"- {title} (截止：{due_date})")
        report.append("")
    
    # 下周计划
    report.append("## 📌 下周重点")
    report.append(f"1. 跟进 {stats['in_progress']} 个进行中的工作项")
    if delayed:
        report.append(f"2. 处理 {len(delayed)} 个延期项")
    if stats["high_priority"] > 0:
        report.append(f"3. 优先处理 {stats['high_priority']} 个高优先级项")
    report.append("")
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='生成 PingCode 项目周报')
    parser.add_argument('--project_id', help='项目ID（可选）')
    parser.add_argument('--project_name', default='项目', help='项目名称')
    parser.add_argument('--output', help='输出文件路径（可选）')
    args = parser.parse_args()
    
    print("正在获取数据...")
    
    # 获取令牌
    token = get_access_token()
    if not token:
        sys.exit(1)
    
    # 获取工作项
    workitems = get_project_workitems(token, args.project_id)
    if not workitems:
        print("获取工作项失败")
        sys.exit(1)
    
    # 分析数据
    print("正在分析数据...")
    analysis = analyze_workitems(workitems)
    
    # 生成周报
    print("正在生成周报...")
    report = generate_weekly_report(analysis, args.project_name)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"周报已保存到：{args.output}")
    else:
        print("\n" + "="*50)
        print(report)
        print("="*50)

if __name__ == "__main__":
    main()
