#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests
import datetime
from pathlib import Path

# 设置输出编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 内置工作流模板
WORKFLOW_TEMPLATES = {
    "邮件自动处理": {
        "name": "邮件自动处理",
        "description": "自动收邮件、分类、提取附件、自动回复、转发到指定群",
        "nodes": [
            # 简化的节点配置，实际使用时是完整的n8n节点JSON
            {"type": "n8n-nodes-base.emailReadImap", "name": "读取邮件", "parameters": {"host": "", "port": 993, "username": "", "password": ""}},
            {"type": "n8n-nodes-base.switch", "name": "分类邮件", "parameters": {"rules": []}},
            {"type": "n8n-nodes-base.emailSend", "name": "自动回复", "parameters": {}},
            {"type": "n8n-nodes-base.webhook", "name": "转发到企业微信", "parameters": {"url": ""}}
        ]
    },
    "日报/周报自动生成": {
        "name": "日报/周报自动生成",
        "description": "自动汇总工作记录、生成日报周报、定时发送给上级",
        "nodes": []
    },
    "会议纪要自动整理": {
        "name": "会议纪要自动整理",
        "description": "自动识别会议录音转文字、提取核心要点、生成结构化纪要、发送给参会人",
        "nodes": []
    },
    "企业微信消息推送": {
        "name": "企业微信消息推送",
        "description": "支持文本、图片、文件、卡片消息推送，支持@指定人、群机器人",
        "nodes": []
    },
    "Excel数据自动同步到数据库": {
        "name": "Excel数据自动同步到数据库",
        "description": "定时读取Excel文件、自动同步到MySQL/Oracle等数据库",
        "nodes": []
    },
    "网站/接口监控": {
        "name": "网站/接口监控",
        "description": "定时监控网站/接口可用性，异常时自动推送告警",
        "nodes": []
    },
    "数据备份自动化": {
        "name": "数据备份自动化",
        "description": "定时备份数据库、文件、工作流配置，自动上传到云存储",
        "nodes": []
    },
    "定时提醒任务": {
        "name": "定时提醒任务",
        "description": "支持自定义时间提醒，比如生日提醒、待办提醒、还款提醒等",
        "nodes": []
    }
}

def cmd_list_templates(args):
    """列出所有可用模板"""
    print("📋 可用工作流模板列表:\n")
    for i, (name, info) in enumerate(WORKFLOW_TEMPLATES.items(), 1):
        print(f"{i}. 📄 {name}")
        print(f"   说明: {info['description']}\n")

def cmd_import(args):
    """导入模板到n8n"""
    template_name = args.template
    if template_name not in WORKFLOW_TEMPLATES:
        print(f"❌ 模板不存在: {template_name}")
        print("使用 list-templates 命令查看所有可用模板")
        sys.exit(1)
    
    template = WORKFLOW_TEMPLATES[template_name]
    print(f"🔽 正在导入模板: {template_name}...\n")
    
    # 调用n8n API导入工作流
    headers = {
        "X-N8N-API-KEY": args.api_key,
        "Content-Type": "application/json"
    }
    
    workflow_data = {
        "name": template["name"],
        "nodes": template["nodes"],
        "connections": {},
        "active": True
    }
    
    try:
        response = requests.post(f"{args.url.rstrip('/')}/api/v1/workflows", headers=headers, json=workflow_data, timeout=30)
        response.raise_for_status()
        result = response.json()
        print(f"✅ 模板导入成功！")
        print(f"🔗 工作流地址: {args.url}/workflow/{result['id']}")
        print("ℹ️  请打开工作流修改配置信息（比如账号密码、地址等）后启用")
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        print("请检查n8n地址是否正确、API Key是否有效")

def cmd_export(args):
    """导出所有工作流备份"""
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    headers = {
        "X-N8N-API-KEY": args.api_key,
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🔄 正在导出工作流...")
        response = requests.get(f"{args.url.rstrip('/')}/api/v1/workflows", headers=headers, timeout=30)
        response.raise_for_status()
        workflows = response.json()
        
        backup_file = os.path.join(output_dir, f"n8n工作流备份_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(workflows, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 导出完成！共导出{len(workflows)}个工作流")
        print(f"💾 备份文件: {backup_file}")
    except Exception as e:
        print(f"❌ 导出失败: {str(e)}")

def cmd_schedule(args):
    """配置定时任务"""
    try:
        headers = {
            "X-N8N-API-KEY": args.api_key,
            "Content-Type": "application/json"
        }
        
        # 先获取工作流ID
        response = requests.get(f"{args.url.rstrip('/')}/api/v1/workflows", headers=headers, timeout=30)
        response.raise_for_status()
        workflows = response.json()
        workflow_id = None
        for wf in workflows:
            if wf["name"] == args.workflow:
                workflow_id = wf["id"]
                break
        
        if not workflow_id:
            print(f"❌ 工作流不存在: {args.workflow}")
            sys.exit(1)
        
        # 配置定时触发器
        workflow_data = {
            "name": args.workflow,
            "nodes": [
                {"type": "n8n-nodes-base.cron", "name": "定时触发", "parameters": {"cronExpression": args.cron}},
            ],
            "active": True
        }
        
        response = requests.patch(f"{args.url.rstrip('/')}/api/v1/workflows/{workflow_id}", headers=headers, json=workflow_data, timeout=30)
        response.raise_for_status()
        
        print(f"✅ 定时任务配置成功！")
        print(f"⏰ 执行规则: {args.cron}")
        print(f"🔗 工作流地址: {args.url}/workflow/{workflow_id}")
    except Exception as e:
        print(f"❌ 配置失败: {str(e)}")

def cmd_monitor(args):
    """监控工作流运行状态"""
    try:
        headers = {
            "X-N8N-API-KEY": args.api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{args.url.rstrip('/')}/api/v1/executions", headers=headers, params={"limit": 10, "status": "error"}, timeout=30)
        response.raise_for_status()
        executions = response.json()
        
        if executions:
            print(f"⚠️  发现{len(executions)}个失败的执行记录:\n")
            for exec in executions:
                print(f"❌ 工作流: {exec['workflow']['name']}")
                print(f"   时间: {exec['startedAt']}")
                print(f"   错误: {exec['error']['message']}\n")
            
            # 推送告警
            if args.alarm_channel == "企业微信" and args.webhook:
                try:
                    content = f"⚠️ n8n工作流异常告警\n共发现{len(executions)}个失败任务：\n"
                    for exec in executions:
                        content += f"- 工作流：{exec['workflow']['name']}\n  错误：{exec['error']['message']}\n"
                    requests.post(args.webhook, json={"msgtype": "text", "text": {"content": content}})
                    print("✅ 告警已推送到企业微信")
                except:
                    pass
        else:
            print("✅ 当前没有失败的执行记录，所有工作流运行正常")
    except Exception as e:
        print(f"❌ 监控失败: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="n8n工作流自动化工具")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 列出模板命令
    list_parser = subparsers.add_parser("list-templates", help="列出所有可用工作流模板")
    
    # 导入模板命令
    import_parser = subparsers.add_parser("import", help="导入模板到n8n")
    import_parser.add_argument("--template", required=True, help="要导入的模板名称")
    import_parser.add_argument("--url", required=True, help="n8n访问地址，比如http://localhost:5678")
    import_parser.add_argument("--api-key", required=True, help="n8n API Key")
    
    # 导出备份命令
    export_parser = subparsers.add_parser("export", help="导出所有工作流备份")
    export_parser.add_argument("--output", required=True, help="备份保存目录")
    export_parser.add_argument("--url", required=True, help="n8n访问地址")
    export_parser.add_argument("--api-key", required=True, help="n8n API Key")
    
    # 配置定时任务命令
    schedule_parser = subparsers.add_parser("schedule", help="配置工作流定时任务")
    schedule_parser.add_argument("--workflow", required=True, help="工作流名称")
    schedule_parser.add_argument("--cron", required=True, help="Cron表达式，比如0 0 * * * 表示每天0点执行")
    schedule_parser.add_argument("--url", required=True, help="n8n访问地址")
    schedule_parser.add_argument("--api-key", required=True, help="n8n API Key")
    
    # 监控命令
    monitor_parser = subparsers.add_parser("monitor", help="监控工作流运行状态")
    monitor_parser.add_argument("--url", required=True, help="n8n访问地址")
    monitor_parser.add_argument("--api-key", required=True, help="n8n API Key")
    monitor_parser.add_argument("--alarm-channel", choices=["企业微信", "钉钉", "飞书", "邮件"], default="企业微信", help="告警渠道")
    monitor_parser.add_argument("--webhook", help="告警机器人webhook地址")
    
    args = parser.parse_args()
    
    if args.command == "list-templates":
        cmd_list_templates(args)
    elif args.command == "import":
        cmd_import(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "schedule":
        cmd_schedule(args)
    elif args.command == "monitor":
        cmd_monitor(args)

if __name__ == "__main__":
    main()
