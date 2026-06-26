#!/usr/bin/env python3
"""
杰峰室外安防通知计划管理脚本

功能：
- 查询通知计划列表
- 新增通知计划
- 更新通知计划
- 删除通知计划

API:
- QUERY: POST /aisvr/v3/gateway/api/outdoorSecurity/pushPlan/query
- ADD: POST /aisvr/v3/gateway/api/outdoorSecurity/pushPlan/add
- UPDATE: POST /aisvr/v3/gateway/api/outdoorSecurity/pushPlan/update
- DELETE: POST /aisvr/v3/gateway/api/outdoorSecurity/pushPlan/delete
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from jf_signature import generate_signature

CONFIG = {
    'uuid': 'xmeye',
    'base_url': 'https://api-cn.jftechws.com',
    'api_query': '/aisvr/v3/gateway/api/outdoorSecurity/pushPlan/query',
    'api_add': '/aisvr/v3/gateway/api/outdoorSecurity/pushPlan/add',
    'api_update': '/aisvr/v3/gateway/api/outdoorSecurity/pushPlan/update',
    'api_delete': '/aisvr/v3/gateway/api/outdoorSecurity/pushPlan/delete'
}

# 工作日枚举
WEEKDAYS = {
    1: '周一',
    2: '周二',
    3: '周三',
    4: '周四',
    5: '周五',
    6: '周六',
    7: '周日'
}


def make_request(url, data, headers):
    """发送 HTTP POST 请求"""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {'code': e.code, 'msg': f'HTTP Error: {e.reason}', 'data': None}
    except urllib.error.URLError as e:
        return {'code': 50000, 'msg': f'Network Error: {e.reason}', 'data': None}
    except Exception as e:
        return {'code': 50000, 'msg': f'Request Error: {str(e)}', 'data': None}


def query_push_plan(sn, user, uuid, appkey, secret, movecard, auth):
    """查询通知计划列表"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {'sn': sn, 'user': user}
    url = CONFIG['base_url'] + CONFIG['api_query']
    return make_request(url, data, headers)


def add_push_plan(sn, user, uuid, appkey, secret, movecard, auth, start_time, end_time, pri_days):
    """新增通知计划"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    # 解析工作日列表
    pri_days_list = [int(d.strip()) for d in pri_days.split(',')]
    
    data = {
        'sn': sn,
        'user': user,
        'monitorTimes': [{
            'startTime': start_time,
            'endTime': end_time
        }],
        'config': {
            'priDays': pri_days_list
        }
    }
    
    url = CONFIG['base_url'] + CONFIG['api_add']
    return make_request(url, data, headers)


def update_push_plan(plan_id, sn, user, uuid, appkey, secret, movecard, auth, start_time=None, end_time=None, pri_days=None):
    """更新通知计划"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {'id': plan_id}
    
    if sn:
        data['sn'] = sn
    if user:
        data['user'] = user
    
    if start_time or end_time:
        data['monitorTimes'] = [{
            'startTime': start_time or '00:00:00',
            'endTime': end_time or '23:59:59'
        }]
    
    if pri_days:
        pri_days_list = [int(d.strip()) for d in pri_days.split(',')]
        data['config'] = {'priDays': pri_days_list}
    
    url = CONFIG['base_url'] + CONFIG['api_update']
    return make_request(url, data, headers)


def delete_push_plan(plan_id, sn=None, user=None, uuid=None, appkey=None, secret=None, movecard=None, auth=None):
    """删除通知计划"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {'id': plan_id}
    if sn:
        data['sn'] = sn
    if user:
        data['user'] = user
    
    url = CONFIG['base_url'] + CONFIG['api_delete']
    return make_request(url, data, headers)


def main():
    parser = argparse.ArgumentParser(description='杰峰室外安防通知计划管理')
    parser.add_argument('--action', required=True, choices=['query', 'add', 'update', 'delete'], help='操作类型')
    parser.add_argument('--sn', help='设备序列号')
    parser.add_argument('--user', help='用户 ID')
    parser.add_argument('--uuid', help='开放平台用户 uuid')
    parser.add_argument('--appkey', help='开放平台应用 appKey')
    parser.add_argument('--secret', help='开放平台应用密钥')
    parser.add_argument('--auth', help='用户认证 token (JWT)')
    parser.add_argument('--movecard', type=int, default=7, help='移动卡标识（默认：7）')
    parser.add_argument('--id', type=int, help='计划 ID（update/delete 操作需要）')
    parser.add_argument('--start-time', help='开始时间（HH:mm:ss 格式）')
    parser.add_argument('--end-time', help='结束时间（HH:mm:ss 格式）')
    parser.add_argument('--pri-days', help='值岗工作日（1-7，逗号分隔，1=周一）')
    
    args = parser.parse_args()
    
    # 从环境变量获取默认值
    env_uuid = os.environ.get('JF_UUID')
    env_appkey = os.environ.get('JF_APP_KEY')
    env_secret = os.environ.get('JF_APP_SECRET')
    env_movecard = os.environ.get('JF_MOVE_CARD', '7')
    env_sn = os.environ.get('JF_DEVICE_SN')
    env_auth = os.environ.get('JF_AUTHORIZATION')
    env_user = os.environ.get('JF_USER')
    
    uuid = args.uuid or env_uuid
    appkey = args.appkey or env_appkey
    secret = args.secret or env_secret
    movecard = args.movecard or int(env_movecard)
    sn = args.sn or env_sn
    auth = args.auth or env_auth
    user = args.user or env_user
    
    # 检查必需参数
    if not all([uuid, appkey, secret, auth]):
        print('❌ 缺少必需参数:')
        if not uuid: print('   - uuid (开放平台用户 uuid)')
        if not appkey: print('   - appkey (开放平台应用 appKey)')
        if not secret: print('   - secret (开放平台应用密钥)')
        if not auth: print('   - auth (用户认证 token)')
        sys.exit(1)
    
    if args.action in ['query'] and not sn:
        print('❌ query 操作需要 --sn 参数')
        sys.exit(1)
    
    if args.action == 'add':
        if not sn:
            print('❌ add 操作需要 --sn 参数')
            sys.exit(1)
        if not args.start_time or not args.end_time:
            print('❌ add 操作需要 --start-time 和 --end-time 参数')
            sys.exit(1)
        if not args.pri_days:
            print('❌ add 操作需要 --pri-days 参数')
            sys.exit(1)
    
    if args.action in ['update', 'delete'] and not args.id:
        print(f'❌ {args.action} 操作需要 --id 参数')
        sys.exit(1)
    
    print('📅 杰峰室外安防通知计划管理')
    print('=' * 50)
    print(f'环境：{CONFIG["base_url"]}')
    print(f'设备序列号 (sn): {sn}')
    print(f'用户 ID (user): {user}')
    print(f'操作类型：{args.action}')
    print('=' * 50)
    
    try:
        if args.action == 'query':
            result = query_push_plan(sn, user, uuid, appkey, secret, movecard, auth)
        elif args.action == 'add':
            result = add_push_plan(sn, user, uuid, appkey, secret, movecard, auth, args.start_time, args.end_time, args.pri_days)
        elif args.action == 'update':
            result = update_push_plan(args.id, sn, user, uuid, appkey, secret, movecard, auth, args.start_time, args.end_time, args.pri_days)
        else:  # delete
            result = delete_push_plan(args.id, sn, user, uuid, appkey, secret, movecard, auth)
        
        if result.get('code') == 2000:
            print('\n✅ 操作成功')
            if args.action == 'query':
                data = result.get('data', [])
                print(f'共查询到 {len(data)} 个通知计划')
                for plan in data:
                    plan_id = plan.get('id', 'N/A')
                    config = plan.get('config', {})
                    pri_days = config.get('priDays', [])
                    days_str = ', '.join([WEEKDAYS.get(d, str(d)) for d in pri_days])
                    monitor_times = plan.get('monitorTimes', [])
                    time_str = ', '.join([f"{t.get('startTime', '')}-{t.get('endTime', '')}" for t in monitor_times])
                    print(f'  - 计划 ID: {plan_id}, 时间：{time_str}, 工作日：{days_str}')
            elif args.action == 'add':
                print('通知计划已新增')
            elif args.action == 'update':
                print('通知计划已更新')
            else:
                print('通知计划已删除')
            print(f'\n完整响应:')
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            error_code = result.get('code', 'Unknown')
            error_msg = result.get('msg', 'Unknown error')
            print(f'\n❌ 操作失败')
            print(f'错误码：{error_code}')
            print(f'错误信息：{error_msg}')
            
            if error_code == 12504:
                print('\n💡 处理建议：设备未开通室外安防套餐')
            elif error_code == 28007:
                print('\n💡 处理建议：Header 参数错误')
            elif error_code == 40103:
                print('\n💡 处理建议：Token 已过期')
            
            sys.exit(1)
            
    except Exception as e:
        print(f'\n❌ 请求异常：{str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()
