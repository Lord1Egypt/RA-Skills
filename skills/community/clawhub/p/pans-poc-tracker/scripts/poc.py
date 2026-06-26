#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI算力销售POC追踪器
管理POC全生命周期，记录技术卡点，提醒跟进，生成转化报告
"""

import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# 数据存储路径
DATA_DIR = Path.home() / ".qclaw/skills/pans-poc-tracker/data"
POCS_FILE = DATA_DIR / "pocs.json"

# POC阶段定义
STAGES = [
    "申请阶段",
    "资源准备",
    "环境部署",
    "测试执行",
    "结果评估",
    "商务转化",
]

STAGE_PROGRESS = {
    "申请阶段": 10,
    "资源准备": 30,
    "环境部署": 50,
    "测试执行": 70,
    "结果评估": 85,
    "商务转化": 95,
}


def load_pocs():
    """加载POC数据"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not POCS_FILE.exists():
        return []
    try:
        with open(POCS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_pocs(pocs):
    """保存POC数据"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(POCS_FILE, "w", encoding="utf-8") as f:
        json.dump(pocs, f, ensure_ascii=False, indent=2)


def find_poc(pocs, poc_id):
    """根据ID查找POC"""
    for poc in pocs:
        if poc["poc_id"] == poc_id:
            return poc
    return None


def generate_poc_id():
    """生成POC ID"""
    return f"POC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"


def cmd_create():
    """创建新POC"""
    print("\n" + "=" * 50)
    print("创建新POC")
    print("=" * 50)
    
    customer = input("客户名称: ").strip()
    if not customer:
        print("客户名称不能为空")
        return
    
    poc_name = input("POC名称: ").strip()
    if not poc_name:
        print("POC名称不能为空")
        return
    
    gpu_config = input("GPU配置 (如 H100x8): ").strip() or "待确认"
    test_scenario = input("测试场景: ").strip() or "待确认"
    start_date = input("开始日期 (YYYY-MM-DD, 默认今天): ").strip()
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    
    end_date = input("预计结束日期 (YYYY-MM-DD): ").strip()
    tech_owner = input("技术负责人: ").strip()
    biz_owner = input("商务负责人: ").strip()
    conversion_prob = input("初始转化概率 (0-100, 默认50): ").strip()
    conversion_prob = int(conversion_prob) if conversion_prob.isdigit() else 50
    
    poc = {
        "poc_id": generate_poc_id(),
        "customer": customer,
        "poc_name": poc_name,
        "gpu_config": gpu_config,
        "test_scenario": test_scenario,
        "start_date": start_date,
        "end_date": end_date,
        "tech_owner": tech_owner,
        "biz_owner": biz_owner,
        "stage": "申请阶段",
        "progress": 10,
        "blockers": [],
        "solutions": [],
        "feedback": [],
        "conversion_prob": conversion_prob,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "closed_at": None,
        "closed_reason": None,
    }
    
    pocs = load_pocs()
    pocs.append(poc)
    save_pocs(pocs)
    
    print(f"\nPOC创建成功!")
    print(f"   POC ID: {poc['poc_id']}")
    print(f"   客户: {customer}")
    print(f"   名称: {poc_name}")
    print(f"   阶段: 申请阶段")


def cmd_list():
    """列出所有POC"""
    pocs = load_pocs()
    
    if not pocs:
        print("\n暂无POC记录")
        return
    
    # 按状态和创建时间排序
    active = [p for p in pocs if p["status"] == "active"]
    closed = [p for p in pocs if p["status"] != "active"]
    
    print("\n" + "=" * 80)
    print(f"{'POC ID':<20} {'客户':<12} {'阶段':<8} {'进度':<8} {'概率':<8} {'状态':<12}")
    print("-" * 80)
    
    for poc in active + closed:
        status_icon = "[O]" if poc["status"] == "active" else ("[OK]" if "success" in poc["status"] else "[X]")
        status_text = "进行中" if poc["status"] == "active" else ("成功" if "success" in poc["status"] else "失败")
        print(f"{poc['poc_id']:<20} {poc['customer']:<12} {poc['stage']:<8} {poc['progress']:<6}% {poc['conversion_prob']:<6}% {status_icon} {status_text:<8}")
    
    print("=" * 80)
    print(f"总计: {len(pocs)} 个POC ({len(active)} 进行中, {len(closed)} 已关闭)")
    
    # 风险预警
    at_risk = [p for p in active if p.get("blockers") or p["progress"] < 30]
    if at_risk:
        print(f"\n风险提示: {len(at_risk)} 个POC存在风险或卡点")


def cmd_update(poc_id):
    """更新POC信息"""
    pocs = load_pocs()
    poc = find_poc(pocs, poc_id)
    
    if not poc:
        print(f"未找到POC: {poc_id}")
        return
    
    print(f"\n更新POC: {poc['poc_id']}")
    print("-" * 40)
    
    fields = {
        "customer": "客户名称",
        "poc_name": "POC名称",
        "gpu_config": "GPU配置",
        "test_scenario": "测试场景",
        "end_date": "预计结束日期",
        "tech_owner": "技术负责人",
        "biz_owner": "商务负责人",
        "conversion_prob": "转化概率",
    }
    
    for key, label in fields.items():
        current = poc.get(key, "")
        new_val = input(f"{label} (当前: {current}): ").strip()
        if new_val:
            if key == "conversion_prob":
                try:
                    poc[key] = int(new_val)
                except ValueError:
                    print("转化概率必须为数字")
            else:
                poc[key] = new_val
    
    poc["updated_at"] = datetime.now().isoformat()
    save_pocs(pocs)
    print("POC更新成功")


def cmd_stage(poc_id, stage_name):
    """更新POC阶段"""
    pocs = load_pocs()
    poc = find_poc(pocs, poc_id)
    
    if not poc:
        print(f"未找到POC: {poc_id}")
        return
    
    # 匹配阶段名
    matched_stage = None
    for stage in STAGES:
        if stage_name in stage or stage in stage_name:
            matched_stage = stage
            break
    
    if not matched_stage:
        print(f"无效阶段: {stage_name}")
        print(f"可选阶段: {', '.join(STAGES)}")
        return
    
    old_stage = poc["stage"]
    poc["stage"] = matched_stage
    poc["progress"] = STAGE_PROGRESS[matched_stage]
    poc["updated_at"] = datetime.now().isoformat()
    
    save_pocs(pocs)
    print(f"阶段更新: {old_stage} -> {matched_stage} (进度: {poc['progress']}%)")


def cmd_blocker(poc_id, description):
    """记录技术卡点"""
    if not description:
        print("请提供卡点描述")
        return
    
    pocs = load_pocs()
    poc = find_poc(pocs, poc_id)
    
    if not poc:
        print(f"未找到POC: {poc_id}")
        return
    
    blocker = {
        "id": len(poc.get("blockers", [])) + 1,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "resolved": False,
        "resolved_at": None,
    }
    
    if "blockers" not in poc:
        poc["blockers"] = []
    poc["blockers"].append(blocker)
    poc["updated_at"] = datetime.now().isoformat()
    
    # 自动降低转化概率
    poc["conversion_prob"] = max(0, poc["conversion_prob"] - 10)
    
    save_pocs(pocs)
    print(f"卡点已记录 (共 {len(poc['blockers'])} 个卡点)")
    print(f"转化概率已调整: {poc['conversion_prob']}%")


def cmd_feedback(poc_id, feedback_text):
    """记录客户反馈"""
    if not feedback_text:
        print("请提供反馈内容")
        return
    
    pocs = load_pocs()
    poc = find_poc(pocs, poc_id)
    
    if not poc:
        print(f"未找到POC: {poc_id}")
        return
    
    feedback = {
        "id": len(poc.get("feedback", [])) + 1,
        "text": feedback_text,
        "created_at": datetime.now().isoformat(),
        "sentiment": None,
    }
    
    if "feedback" not in poc:
        poc["feedback"] = []
    poc["feedback"].append(feedback)
    poc["updated_at"] = datetime.now().isoformat()
    
    save_pocs(pocs)
    print(f"反馈已记录 (共 {len(poc['feedback'])} 条反馈)")


def cmd_close(poc_id, result, reason=""):
    """关闭POC"""
    pocs = load_pocs()
    poc = find_poc(pocs, poc_id)
    
    if not poc:
        print(f"未找到POC: {poc_id}")
        return
    
    if poc["status"] != "active":
        print("该POC已经关闭")
        return
    
    if result == "success":
        poc["status"] = "closed_success"
        poc["progress"] = 100
        poc["conversion_prob"] = 100
    else:
        poc["status"] = "closed_failed"
        poc["conversion_prob"] = 0
    
    poc["closed_at"] = datetime.now().isoformat()
    poc["closed_reason"] = reason or ("测试通过，转化成功" if result == "success" else "测试未通过")
    poc["updated_at"] = datetime.now().isoformat()
    
    save_pocs(pocs)
    status_text = "成功" if result == "success" else "失败"
    print(f"POC已关闭: {status_text}")
    print(f"   原因: {poc['closed_reason']}")


def cmd_report(poc_id=None):
    """生成POC报告"""
    pocs = load_pocs()
    
    if poc_id:
        poc = find_poc(pocs, poc_id)
        if not poc:
            print(f"未找到POC: {poc_id}")
            return
        report_pocs = [poc]
    else:
        report_pocs = [p for p in pocs if p["status"] == "active"]
        if not report_pocs:
            print("没有进行中的POC")
            return
    
    print("\n" + "=" * 60)
    print("POC 状态报告")
    print("=" * 60)
    
    for poc in report_pocs:
        print(f"\n{'-' * 60}")
        print(f"POC ID: {poc['poc_id']}")
        print(f"客户: {poc['customer']}")
        print(f"名称: {poc['poc_name']}")
        print(f"GPU配置: {poc['gpu_config']}")
        print(f"测试场景: {poc['test_scenario']}")
        print(f"阶段: {poc['stage']} ({poc['progress']}%)")
        print(f"开始日期: {poc['start_date']}")
        print(f"预计结束: {poc['end_date']}")
        print(f"技术负责人: {poc['tech_owner'] or '未分配'}")
        print(f"商务负责人: {poc['biz_owner'] or '未分配'}")
        print(f"转化概率: {poc['conversion_prob']}%")
        
        if poc.get("blockers"):
            print(f"\n技术卡点 ({len(poc['blockers'])} 个):")
            for b in poc["blockers"]:
                status = "[V]" if b.get("resolved") else "[ ]"
                print(f"  {status} [{b['id']}] {b['description']}")
        
        if poc.get("feedback"):
            print(f"\n客户反馈 ({len(poc['feedback'])} 条):")
            for f in poc["feedback"][-3:]:
                text = f['text'][:80] + "..." if len(f['text']) > 80 else f['text']
                print(f"  - {text}")
        
        # 风险评估
        days_left = None
        if poc.get("end_date"):
            try:
                end = datetime.strptime(poc["end_date"], "%Y-%m-%d")
                days_left = (end - datetime.now()).days
            except:
                pass
        
        if days_left is not None and days_left < 0:
            print(f"\n警告: POC已逾期 {abs(days_left)} 天")
        elif days_left is not None and days_left <= 3:
            print(f"\n提醒: 距离结束还有 {days_left} 天")
    
    print(f"\n{'=' * 60}")
    print(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def cmd_remind():
    """显示今日待跟进"""
    pocs = load_pocs()
    today = datetime.now()
    
    print("\n" + "=" * 60)
    print(f"[DATE] POC待跟进提醒: {today.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    reminders = []
    
    for poc in pocs:
        if poc["status"] != "active":
            continue
        
        # 检查卡点
        if poc.get("blockers"):
            unresolved = [b for b in poc["blockers"] if not b.get("resolved")]
            if unresolved:
                reminders.append({
                    "type": "blocker",
                    "poc": poc,
                    "content": f"存在 {len(unresolved)} 个未解决卡点",
                    "priority": "high",
                })
        
        # 检查即将到期
        if poc.get("end_date"):
            try:
                end = datetime.strptime(poc["end_date"], "%Y-%m-%d")
                days_left = (end - today).days
                
                if days_left < 0:
                    reminders.append({
                        "type": "overdue",
                        "poc": poc,
                        "content": f"已逾期 {abs(days_left)} 天",
                        "priority": "critical",
                    })
                elif days_left <= 3:
                    reminders.append({
                        "type": "deadline",
                        "poc": poc,
                        "content": f"距离结束还有 {days_left} 天",
                        "priority": "medium",
                    })
            except:
                pass
        
        # 检查低进度
        if poc["progress"] < 30:
            reminders.append({
                "type": "low_progress",
                "poc": poc,
                "content": f"进度仅 {poc['progress']}%",
                "priority": "medium",
            })
    
    if not reminders:
        print("\n暂无需要跟进的POC")
        return
    
    # 按优先级排序
    priority_order = {"critical": 0, "high": 1, "medium": 2}
    reminders.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    for r in reminders:
        icon = {"critical": "[!]", "high": "[*]", "medium": "[~]"}.get(r["priority"], "[ ]")
        print(f"\n{icon} [{r['priority'].upper()}] {r['poc']['poc_id']}")
        print(f"   客户: {r['poc']['customer']}")
        print(f"   阶段: {r['poc']['stage']} ({r['poc']['progress']}%)")
        print(f"   事项: {r['content']}")
        if r['poc']['tech_owner']:
            print(f"   技术负责人: {r['poc']['tech_owner']}")
        if r['poc']['biz_owner']:
            print(f"   商务负责人: {r['poc']['biz_owner']}")
    
    print(f"\n{'=' * 60}")
    print(f"共 {len(reminders)} 项待跟进")


def show_help():
    """显示帮助信息"""
    print("""
AI算力销售POC追踪器

用法: python3 poc.py [命令] [参数]

命令:
  --create              创建新POC (交互式)
  --list                列出所有POC
  --update <poc_id>     更新POC信息
  --stage <poc_id> <阶段名>  更新POC阶段
  --blocker <poc_id> <描述>  记录技术卡点
  --feedback <poc_id> <内容>  记录客户反馈
  --close <poc_id> <success|failed> [原因]  关闭POC
  --report [poc_id]     生成POC报告
  --remind              显示今日待跟进
  --help                显示帮助信息

阶段名称:
  申请阶段, 资源准备, 环境部署, 测试执行, 结果评估, 商务转化

示例:
  python3 poc.py --create
  python3 poc.py --list
  python3 poc.py --stage POC-20240101-ABCD 测试执行
  python3 poc.py --blocker POC-20240101-ABCD 网络延迟过高
  python3 poc.py --report
  python3 poc.py --remind
""")


def main():
    args = sys.argv[1:]
    
    if not args or "--help" in args or "-h" in args:
        show_help()
        return
    
    cmd = args[0] if args else None
    
    if cmd == "--create":
        cmd_create()
    elif cmd == "--list":
        cmd_list()
    elif cmd == "--update":
        if len(args) < 2:
            print("请提供POC ID")
            return
        cmd_update(args[1])
    elif cmd == "--stage":
        if len(args) < 3:
            print("请提供POC ID和阶段名称")
            return
        cmd_stage(args[1], args[2])
    elif cmd == "--blocker":
        if len(args) < 3:
            print("请提供POC ID和卡点描述")
            return
        cmd_blocker(args[1], args[2])
    elif cmd == "--feedback":
        if len(args) < 3:
            print("请提供POC ID和反馈内容")
            return
        cmd_feedback(args[1], args[2])
    elif cmd == "--close":
        if len(args) < 3:
            print("请提供POC ID和结果 (success/failed)")
            return
        result = args[2]
        reason = args[3] if len(args) > 3 else ""
        cmd_close(args[1], result, reason)
    elif cmd == "--report":
        poc_id = args[1] if len(args) > 1 else None
        cmd_report(poc_id)
    elif cmd == "--remind":
        cmd_remind()
    else:
        print(f"未知命令: {cmd}")
        show_help()


if __name__ == "__main__":
    main()
