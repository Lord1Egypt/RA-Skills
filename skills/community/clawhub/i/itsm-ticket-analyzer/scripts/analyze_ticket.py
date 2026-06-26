#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嘉为蓝鲸 ITSM 工单分析脚本
支持多流程工单，字段智能映射
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 嘉为蓝鲸标准字段映射
FIELD_MAPPING = {
    # 工单标识
    "单号": "ticket_id",
    "工单号": "ticket_id",
    "ticket_id": "ticket_id",
    "id": "ticket_id",
    
    # 标题和描述
    "标题": "title",
    "标题": "title",
    "title": "title",
    "描述": "description",
    "内容": "description",
    "description": "description",
    
    # 分类字段（嘉为蓝鲸三级分类）
    "服务目录": "service_catalog",
    "服务": "service",
    "服务类型": "service_type",
    "工单类型": "ticket_type",
    "type": "ticket_type",
    "分类": "category",
    
    # 状态和流程
    "状态": "status",
    "status": "status",
    "当前步骤": "current_step",
    "当前节点": "current_step",
    "step": "current_step",
    "流程版本": "process_version",
    "version": "process_version",
    
    # 人员
    "当前处理人": "assignee",
    "处理人": "assignee",
    "assignee": "assignee",
    "创建人": "requester",
    "提单人": "requester",
    "申请人": "requester",
    "requester": "requester",
    
    # 时间字段
    "提单时间": "created_at",
    "创建时间": "created_at",
    "created_at": "created_at",
    "结束时间": "resolved_at",
    "解决时间": "resolved_at",
    "完成时间": "resolved_at",
    "resolved_at": "resolved_at",
    "挂起时间": "suspended_at",
    "suspended_at": "suspended_at",
    "恢复时间": "resumed_at",
    "resumed_at": "resumed_at",
    "SLA 截止时间": "sla_deadline",
    "sla_deadline": "sla_deadline",
    
    # 优先级
    "优先级": "priority",
    "priority": "priority",
    "紧急程度": "priority"
}

def normalize_field(field_name):
    """标准化字段名"""
    field = field_name.strip()
    return FIELD_MAPPING.get(field, field)

def load_ticket_data(input_file):
    """加载工单数据，自动识别字段"""
    if not Path(input_file).exists():
        return None, f"文件不存在：{input_file}"
    
    try:
        import csv
        with open(input_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig 处理 BOM
            reader = csv.DictReader(f)
            
            # 调试：打印字段名
            # print(f"原始字段：{reader.fieldnames}")
            
            # 字段映射
            tickets = []
            for row in reader:
                normalized = {}
                for key, value in row.items():
                    if key is None:
                        continue
                    norm_key = normalize_field(key)
                    normalized[norm_key] = value.strip() if value is not None else ""
                tickets.append(normalized)
            
            return tickets, None
    except Exception as e:
        import traceback
        return None, f"{str(e)}\n{traceback.format_exc()}"

def analyze_ticket(ticket, all_tickets=None):
    """分析工单并给出建议"""
    # 提取关键信息（嘉为蓝鲸三级分类）
    service_catalog = ticket.get('service_catalog', '')  # 服务目录
    service = ticket.get('service', '')                   # 服务
    service_type = ticket.get('service_type', '')         # 服务类型
    title = ticket.get('title', '')
    status = ticket.get('status', '')
    current_step = ticket.get('current_step', '')
    assignee = ticket.get('assignee', '')
    priority = ticket.get('priority', 'P3')
    
    # 确定工单分类（优先级：服务类型 > 服务 > 服务目录）
    category = service_type or service or service_catalog or "未分类"
    
    # 根据分类给出处理建议
    suggestions = generate_suggestions(category, service_catalog, service)
    
    # 查找相似历史工单
    similar_count = 0
    if all_tickets:
        similar_count = count_similar_tickets(ticket, all_tickets)
    
    # 计算 SLA 时限
    sla_hours = get_sla_hours(priority)
    
    # 计算已用时间
    time_info = calculate_time_info(ticket)
    
    return {
        "ticket_id": ticket.get('ticket_id', '未知'),
        "title": title,
        "classification": {
            "service_catalog": service_catalog,
            "service": service,
            "service_type": service_type,
            "category": category
        },
        "status": {
            "status": status,
            "current_step": current_step,
            "assignee": assignee
        },
        "analysis": {
            "priority": priority,
            "sla_hours": sla_hours,
            "similar_tickets_count": similar_count,
            "time_info": time_info,
            "suggestions": suggestions
        }
    }

def generate_suggestions(category, service_catalog, service):
    """根据分类生成处理建议"""
    suggestions_map = {
        # 网络相关
        "VPN": ["检查 VPN 配置和证书", "验证用户账号状态", "检查 VPN 网关负载", "查看网络监控告警"],
        "网络": ["检查网络连接状态", "验证交换机/路由器配置", "查看网络监控", "测试网络连通性"],
        "wifi": ["检查 AP 状态", "验证无线控制器", "检查用户认证", "查看无线信号覆盖"],
        
        # 服务器/系统相关
        "服务器": ["登录服务器检查状态", "监控 CPU/内存/磁盘", "检查关键服务", "查看系统日志"],
        "Linux": ["检查系统日志/var/log", "监控资源使用率", "验证服务状态", "检查 cron 任务"],
        "Windows": ["检查事件查看器", "监控资源使用率", "验证服务状态", "检查更新补丁"],
        
        # 应用相关
        "邮箱": ["检查邮箱账号状态", "验证邮件服务器连接", "清理邮箱缓存", "重置邮箱密码"],
        "OA": ["检查 OA 系统状态", "验证用户权限", "查看流程配置", "联系 OA 供应商"],
        "ERP": ["检查 ERP 系统状态", "验证数据库连接", "查看业务日志", "联系 ERP 顾问"],
        
        # 权限相关
        "权限": ["核实申请人身份", "确认权限范围", "按审批流程处理", "记录权限变更"],
        "账号": ["验证账号信息", "检查账号状态", "重置密码", "解锁账号"],
        
        # 硬件相关
        "打印机": ["检查打印机网络连接", "验证打印机驱动", "清理打印队列", "重启打印机"],
        "电脑": ["远程诊断问题", "检查硬件状态", "重装系统/驱动", "安排现场支持"]
    }
    
    # 匹配关键词
    suggestions = []
    for keyword, sugg in suggestions_map.items():
        if keyword in category or keyword in service or keyword in service_catalog:
            suggestions.extend(sugg)
            break
    
    # 默认建议
    if not suggestions:
        suggestions = [
            "联系用户确认详细问题",
            "查看历史记录和解决方案",
            "根据 SLA 优先级处理",
            "必要时升级给专业团队"
        ]
    
    return suggestions[:4]  # 最多 4 条建议

def count_similar_tickets(ticket, all_tickets, limit=10):
    """计算相似工单数量"""
    service_type = ticket.get('service_type', '')
    service = ticket.get('service', '')
    
    if not service_type and not service:
        return 0
    
    count = 0
    for t in all_tickets:
        if t.get('ticket_id') == ticket.get('ticket_id'):
            continue
        if service_type and t.get('service_type') == service_type:
            count += 1
        elif service and t.get('service') == service:
            count += 1
        if count >= limit:
            break
    
    return count

def get_sla_hours(priority):
    """获取 SLA 时限"""
    sla_map = {
        "P0": 1,
        "P1": 4,
        "P2": 24,
        "P3": 72,
        "紧急": 1,
        "高": 4,
        "中": 24,
        "低": 72
    }
    return sla_map.get(priority, 72)

def calculate_time_info(ticket):
    """计算时间相关信息"""
    created = parse_date(ticket.get('created_at', ''))
    resolved = parse_date(ticket.get('resolved_at', ''))
    suspended = parse_date(ticket.get('suspended_at', ''))
    resumed = parse_date(ticket.get('resumed_at', ''))
    
    info = {
        "created_at": created.strftime('%Y-%m-%d %H:%M') if created else None,
        "resolved_at": resolved.strftime('%Y-%m-%d %H:%M') if resolved else None,
        "elapsed_hours": None,
        "actual_work_hours": None,
        "is_suspended": bool(suspended and not resumed)
    }
    
    if created:
        end_time = resolved or datetime.now()
        info["elapsed_hours"] = round((end_time - created).total_seconds() / 3600, 1)
        
        # 计算实际工作时长（扣除挂起时间）
        if suspended:
            suspend_start = suspended
            suspend_end = resumed or datetime.now()
            suspend_hours = (suspend_end - suspend_start).total_seconds() / 3600
            total_hours = (end_time - created).total_seconds() / 3600
            info["actual_work_hours"] = round(max(0, total_hours - suspend_hours), 1)
    
    return info

def parse_date(date_str):
    """解析日期字符串"""
    if not date_str:
        return None
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return None

def format_output(result):
    """格式化输出"""
    output = []
    output.append(f"## 🎫 工单分析：{result['ticket_id']}")
    output.append(f"\n**标题**: {result['title']}")
    
    # 分类信息
    c = result['classification']
    output.append(f"\n### 分类信息")
    if c['service_catalog']:
        output.append(f"- **服务目录**: {c['service_catalog']}")
    if c['service']:
        output.append(f"- **服务**: {c['service']}")
    if c['service_type']:
        output.append(f"- **服务类型**: {c['service_type']}")
    
    # 状态信息
    s = result['status']
    output.append(f"\n### 当前状态")
    output.append(f"- **状态**: {s['status']}")
    output.append(f"- **当前步骤**: {s['current_step'] or '未开始'}")
    output.append(f"- **处理人**: {s['assignee'] or '未分配'}")
    
    # 分析结果
    a = result['analysis']
    output.append(f"\n### 分析结果")
    output.append(f"- **优先级**: {a['priority']}")
    output.append(f"- **SLA 时限**: {a['sla_hours']} 小时")
    output.append(f"- **相似工单**: {a['similar_tickets_count']} 个")
    
    if a['time_info']:
        t = a['time_info']
        output.append(f"- **已用时长**: {t['elapsed_hours']} 小时" if t['elapsed_hours'] else "")
        if t['actual_work_hours']:
            output.append(f"- **实际工作时长**: {t['actual_work_hours']} 小时")
        if t['is_suspended']:
            output.append(f"- ⚠️ **当前挂起中**")
    
    output.append(f"\n### 处理建议")
    for i, suggestion in enumerate(a['suggestions'], 1):
        output.append(f"{i}. {suggestion}")
    
    return "\n".join([line for line in output if line])

def main():
    parser = argparse.ArgumentParser(description='嘉为蓝鲸 ITSM 工单分析')
    parser.add_argument('--input', required=True, help='工单数据文件路径')
    parser.add_argument('--ticket-id', help='分析指定工单号')
    parser.add_argument('--output', help='输出文件路径（可选）')
    args = parser.parse_args()
    
    # 加载数据
    tickets, error = load_ticket_data(args.input)
    if error:
        print(f"❌ 错误：{error}")
        sys.exit(1)
    
    print(f"✅ 成功加载 {len(tickets)} 个工单")
    
    # 分析指定工单或全部工单
    if args.ticket_id:
        target = next((t for t in tickets if t.get('ticket_id') == args.ticket_id), None)
        if not target:
            print(f"❌ 未找到工单：{args.ticket_id}")
            sys.exit(1)
        results = [analyze_ticket(target, tickets)]
    else:
        # 默认分析最新 5 个工单
        results = [analyze_ticket(t, tickets) for t in tickets[-5:]]
    
    # 输出结果
    output_text = "\n\n---\n\n".join([format_output(r) for r in results])
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"✅ 分析完成，结果已保存到：{args.output}")
    else:
        print("\n" + output_text)

if __name__ == '__main__':
    main()
