#!/usr/bin/env python3
"""
北森 iTalent 加班管理 CLI - 纯 Python 版本（无外部依赖）
支持 access_token 认证

用法:
    python3 italent-overtime-simple.py auth --key YOUR_KEY --secret YOUR_SECRET
    python3 italent-overtime-simple.py push --email zhangsan@company.com --start "2024-01-01 18:00" --end "2024-01-01 20:00"
    python3 italent-overtime-simple.py list --staff-ids 11xxxxx80 --start 2024-01-01 --end 2024-01-07
    python3 italent-overtime-simple.py cancel --overtime-id xxx-xxx-xxx
    python3 italent-overtime-simple.py --help
"""

import sys
import json
import urllib.request
import urllib.error
import os
from datetime import datetime

# API 配置
TOKEN_URL = "https://openapi.italent.cn/token"
BASE_URL = "https://openapi.italent.cn/AttendanceOpen/api/v1/AttendanceOvertime"
CONFIG_FILE = os.path.expanduser("~/.italent-overtime.conf")

# 接口端点
ENDPOINTS = {
    "push": "/PostOverTimeWithApproval",
    "cancel": "/PostRevokeOverTimeWithApproval",
    "list": "/GetScheduledOverTimeRangeList",
}


def load_config():
    """加载配置文件"""
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            pass
    return config


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_access_token(app_key, app_secret):
    """获取 access_token"""
    data = {
        "grant_type": "client_credentials",
        "app_key": app_key,
        "app_secret": app_secret
    }
    
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            TOKEN_URL, 
            data=json_data, 
            headers={"Content-Type": "application/json"},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        return {"error": f"HTTP 错误：{e.reason}", "details": error_body}
    except urllib.error.URLError as e:
        return {"error": f"网络错误：{e.reason}"}
    except Exception as e:
        return {"error": f"请求失败：{str(e)}"}


def make_request(endpoint, data, access_token):
    """发送 API 请求"""
    url = f"{BASE_URL}{endpoint}"
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            url, 
            data=json_data, 
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        return {"code": str(e.code), "message": f"HTTP 错误：{e.reason}", "details": error_body}
    except urllib.error.URLError as e:
        return {"code": "500", "message": f"网络错误：{e.reason}"}
    except Exception as e:
        return {"code": "500", "message": f"请求失败：{str(e)}"}


def print_result(result, title="结果"):
    """打印结果"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    
    code = result.get("code", result.get("error", "Unknown"))
    if code in ["200", "Succeed", 200, "200"]:
        print("✓ 成功")
    elif code in ["401", "NoPermission", "Unauthorized"]:
        print("✗ 无权限 - 请检查 access_token 是否有效")
    elif code in ["417", "Failed"]:
        print("✗ 失败")
    else:
        print(f"? 状态：{code}")
    
    if "message" in result and result["message"]:
        print(f"消息：{result['message']}")
    
    if "error" in result and result["error"]:
        print(f"错误：{result['error']}")
        if "details" in result:
            print(f"详情：{result['details']}")
    
    if "data" in result and result["data"]:
        print(f"\n数据：")
        if isinstance(result["data"], list):
            for item in result["data"]:
                print(f"  {json.dumps(item, ensure_ascii=False, indent=2)}")
        else:
            print(f"  {json.dumps(result['data'], ensure_ascii=False, indent=2)}")
    
    if "access_token" in result:
        print(f"\nAccess Token: {result['access_token'][:20]}...")
        if "expires_in" in result:
            print(f"过期时间：{result['expires_in']} 秒")
    
    print(f"{'='*60}\n")


def print_help():
    """打印帮助信息"""
    help_text = """
北森 iTalent 加班管理 CLI - 纯 Python 版本

用法:
    python3 italent-overtime-simple.py <command> [选项]

命令:
    auth      获取 access_token（首次使用必须先执行）
    push      推送加班数据至北森系统，并发起审批
    list      查询员工的安排加班数据
    cancel    撤销指定加班，并发起审批
    help      显示帮助信息

auth 命令选项:
    --key TEXT                App Key（必填）
    --secret TEXT             App Secret（必填）
    --save                    保存 token 到配置文件（推荐）

push 命令选项:
    --email TEXT              员工邮箱（与 staff-id 二选一）
    --staff-id TEXT           北森 StaffId（与 email 二选一）
    --start TEXT              开始时间，格式：2024-01-01 18:00:00（必填）
    --end TEXT                结束时间，格式：2024-01-01 20:00:00（必填）
    --compensation INT        加班补偿方式（默认：1）
    --reason TEXT             加班原因
    --category TEXT           加班类别 (UUID)
    --transfer-org TEXT       支援组织
    --transfer-pos TEXT       支援职位 (UUID)
    --transfer-task TEXT      支援任务 (UUID)
    --identity-type INT       主键类型：0=员工邮箱，1=北森 UserId（默认：0）
    --json                    以 JSON 格式输出结果

list 命令选项:
    --staff-ids TEXT          员工 ID 列表，多个用逗号分隔（必填）
    --start TEXT              开始日期，格式：2024-01-01（必填）
    --end TEXT                结束日期，格式：2024-01-07（必填）
    --json                    以 JSON 格式输出结果

cancel 命令选项:
    --overtime-id TEXT        要撤销的加班 ID（必填）
    --json                    以 JSON 格式输出结果

快速开始:
    1. 获取 access_token:
       python3 italent-overtime-simple.py auth --key YOUR_KEY --secret YOUR_SECRET --save
    
    2. 推送加班:
       python3 italent-overtime-simple.py push -e zhangsan@company.com --start "2024-01-01 18:00:00" --end "2024-01-01 20:00:00" -r "项目上线"
    
    3. 查询加班:
       python3 italent-overtime-simple.py list --staff-ids 11xxxxx80 --start 2024-01-01 --end 2024-01-07
    
    4. 撤销加班:
       python3 italent-overtime-simple.py cancel --overtime-id "xxx-xxx-xxx"

配置文件:
    ~/.italent-overtime.conf (JSON 格式，保存 access_token)
"""
    print(help_text)


def parse_args(args):
    """解析命令行参数"""
    parsed = {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith('--'):
            key = arg[2:].replace('-', '_')
            if i + 1 < len(args) and not args[i + 1].startswith('--'):
                parsed[key] = args[i + 1]
                i += 2
            else:
                parsed[key] = True
                i += 1
        elif arg.startswith('-') and len(arg) == 2:
            key = arg[1:]
            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                parsed[key] = args[i + 1]
                i += 2
            else:
                parsed[key] = True
                i += 1
        else:
            parsed['_positional'] = arg
            i += 1
    return parsed


def cmd_auth(args):
    """认证命令"""
    if 'key' not in args:
        print("错误：必须提供 --key 参数")
        sys.exit(1)
    
    if 'secret' not in args:
        print("错误：必须提供 --secret 参数")
        sys.exit(1)
    
    print("正在获取 access_token...")
    result = get_access_token(args['key'], args['secret'])
    
    if 'access_token' in result:
        print_result(result, "认证成功")
        
        if args.get('save'):
            config = load_config()
            config['access_token'] = result['access_token']
            config['expires_at'] = datetime.now().timestamp() + result.get('expires_in', 7200)
            config['app_key'] = args['key']
            save_config(config)
            print(f"✓ Token 已保存到：{CONFIG_FILE}")
            print(f"  过期时间：{datetime.fromtimestamp(config['expires_at'])}")
    else:
        print_result(result, "认证失败")
        sys.exit(1)


def cmd_push(args):
    """推送加班命令"""
    # 加载配置
    config = load_config()
    access_token = config.get('access_token')
    
    if not access_token:
        print("错误：未找到 access_token")
        print("请先执行认证命令:")
        print("  python3 italent-overtime-simple.py auth --key YOUR_KEY --secret YOUR_SECRET --save")
        sys.exit(1)
    
    # 参数校验
    if 'email' not in args and 'staff_id' not in args:
        print("错误：必须提供 --staff-id 或 --email")
        sys.exit(1)
    
    if 'start' not in args:
        print("错误：必须提供 --start 参数")
        sys.exit(1)
    
    if 'end' not in args:
        print("错误：必须提供 --end 参数")
        sys.exit(1)
    
    # 构建请求数据
    overtime_data = {
        "startDate": args['start'],
        "stopDate": args['end'],
        "compensationType": int(args.get('compensation', 1)),
    }
    
    # 根据 identity_type 设置主键
    identity_type = int(args.get('identity_type', 0))
    if identity_type == 1:
        if 'staff_id' in args:
            overtime_data["staffId"] = args['staff_id']
        else:
            print("错误：identity-type=1 时必须提供 --staff-id")
            sys.exit(1)
    else:
        if 'email' in args:
            overtime_data["email"] = args['email']
        elif 'staff_id' in args:
            overtime_data["staffId"] = args['staff_id']
    
    # 可选参数
    if 'reason' in args:
        overtime_data["reason"] = args['reason']
    if 'category' in args:
        overtime_data["overtimeCategory"] = args['category']
    if 'transfer_org' in args:
        overtime_data["transferOrganization"] = args['transfer_org']
    if 'transfer_pos' in args:
        overtime_data["transferPosition"] = args['transfer_pos']
    if 'transfer_task' in args:
        overtime_data["transferTask"] = args['transfer_task']
    
    # 构建完整请求
    request_data = {
        "attendanceOverTime": overtime_data,
        "identityType": identity_type
    }
    
    # 发送请求
    print("正在推送加班数据...")
    result = make_request(ENDPOINTS["push"], request_data, access_token)
    
    if args.get('json'):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_result(result, "推送加班结果")
        
        if result.get("code") in ["200", "Succeed", 200]:
            print(f"加班 ID: {result.get('data')}")
            print("可以使用该 ID 撤销加班或查询审批状态")


def cmd_list(args):
    """查询加班命令"""
    # 加载配置
    config = load_config()
    access_token = config.get('access_token')
    
    if not access_token:
        print("错误：未找到 access_token")
        print("请先执行认证命令:")
        print("  python3 italent-overtime-simple.py auth --key YOUR_KEY --secret YOUR_SECRET --save")
        sys.exit(1)
    
    if 'staff_ids' not in args:
        print("错误：必须提供 --staff-ids 参数")
        sys.exit(1)
    
    if 'start' not in args:
        print("错误：必须提供 --start 参数")
        sys.exit(1)
    
    if 'end' not in args:
        print("错误：必须提供 --end 参数")
        sys.exit(1)
    
    # 解析员工 ID 列表
    staff_id_list = [int(sid.strip()) for sid in args['staff_ids'].split(',')]
    
    # 构建请求数据
    request_data = {
        "staffIds": staff_id_list,
        "startDate": args['start'],
        "stopDate": args['end']
    }
    
    # 发送请求
    print("正在查询加班数据...")
    result = make_request(ENDPOINTS["list"], request_data, access_token)
    
    if args.get('json'):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_result(result, "查询加班结果")
        
        if result.get("code") in ["200", "Succeed", 200] and result.get("data"):
            data = result["data"]
            if isinstance(data, list):
                print(f"找到 {len(data)} 条加班记录：\n")
                for item in data:
                    print(f"  员工 ID: {item.get('staffId')}")
                    print(f"  排班日期：{item.get('scheduledDate')}")
                    print(f"  加班时间：{item.get('overTimeStartTime')} - {item.get('overTimeEndTime')}")
                    print(f"  {'-'*40}")


def cmd_cancel(args):
    """撤销加班命令"""
    # 加载配置
    config = load_config()
    access_token = config.get('access_token')
    
    if not access_token:
        print("错误：未找到 access_token")
        print("请先执行认证命令:")
        print("  python3 italent-overtime-simple.py auth --key YOUR_KEY --secret YOUR_SECRET --save")
        sys.exit(1)
    
    if 'overtime_id' not in args:
        print("错误：必须提供 --overtime-id 参数")
        sys.exit(1)
    
    # 构建请求数据
    request_data = {
        "overTimeRevokeId": args['overtime_id']
    }
    
    # 发送请求
    print(f"正在撤销加班 {args['overtime_id']}...")
    result = make_request(ENDPOINTS["cancel"], request_data, access_token)
    
    if args.get('json'):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_result(result, "撤销加班结果")
        
        if result.get("code") in ["200", "Succeed", 200]:
            print("✓ 加班撤销申请已提交")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    
    command = sys.argv[1]
    args = parse_args(sys.argv[2:])
    
    if command in ['help', '-h', '--help']:
        print_help()
    elif command == 'auth':
        cmd_auth(args)
    elif command == 'push':
        cmd_push(args)
    elif command == 'list':
        cmd_list(args)
    elif command == 'cancel':
        cmd_cancel(args)
    else:
        print(f"未知命令：{command}")
        print("\n使用 'python3 italent-overtime-simple.py help' 查看帮助")
        sys.exit(1)


if __name__ == '__main__':
    main()
