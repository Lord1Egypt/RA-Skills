#!/usr/bin/env python3
"""
杰峰室外安防报警记录查询脚本

功能：
- 查询报警记录列表（分页）

API:
- PAGE: POST /aisvr/v3/gateway/api/child/alarm/page
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from jf_signature import generate_signature

CONFIG = {
    'uuid': 'xmeye',
    'base_url': 'https://api-cn.jftechws.com',
    'api_page': '/aisvr/v3/gateway/api/child/alarm/page'
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


def query_alarm_page(sn, user, uuid, appkey, secret, movecard, auth, start_time, end_time, msg_type=None, page=1, rows=10):
    """查询报警记录列表"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {
        'sn': sn,
        'user': user,
        'startTime': str(start_time),
        'endTime': str(end_time),
        'page': page,
        'rows': rows
    }
    
    if msg_type:
        data['msgType'] = msg_type
    
    url = CONFIG['base_url'] + CONFIG['api_page']
    return make_request(url, data, headers)


def main():
    parser = argparse.ArgumentParser(description='杰峰室外安防报警记录查询')
    parser.add_argument('--action', default='page', choices=['page'], help='操作类型：page=查询报警列表')
    parser.add_argument('--sn', help='设备序列号')
    parser.add_argument('--user', help='用户 ID')
    parser.add_argument('--uuid', help='开放平台用户 uuid')
    parser.add_argument('--appkey', help='开放平台应用 appKey')
    parser.add_argument('--secret', help='开放平台应用密钥')
    parser.add_argument('--auth', help='用户认证 token (JWT)')
    parser.add_argument('--movecard', type=int, default=7, help='移动卡标识（默认：7）')
    parser.add_argument('--start-time', type=int, help='开始时间（秒级时间戳）')
    parser.add_argument('--end-time', type=int, help='结束时间（秒级时间戳）')
    parser.add_argument('--msg-type', help='异常类型（可选）')
    parser.add_argument('--page', type=int, default=1, help='页码（默认：1）')
    parser.add_argument('--rows', type=int, default=10, help='每页条数（默认：10）')
    
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
    start_time = args.start_time
    end_time = args.end_time
    
    # 检查必需参数
    if not all([sn, user, uuid, appkey, secret, auth]):
        print('❌ 缺少必需参数:')
        if not sn: print('   - sn (设备序列号)')
        if not user: print('   - user (用户 ID)')
        if not uuid: print('   - uuid (开放平台用户 uuid)')
        if not appkey: print('   - appkey (开放平台应用 appKey)')
        if not secret: print('   - secret (开放平台应用密钥)')
        if not auth: print('   - auth (用户认证 token)')
        sys.exit(1)
    
    # 如果没有提供时间参数，默认查询最近 7 天
    if not start_time or not end_time:
        end_time = int(time.time())
        start_time = end_time - (7 * 24 * 60 * 60)
        print(f'⚠️  未提供时间参数，使用默认值：最近 7 天')
        print(f'   开始时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')
        print(f'   结束时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))}')
    
    print('📊 杰峰室外安防报警记录查询')
    print('=' * 50)
    print(f'环境：{CONFIG["base_url"]}')
    print(f'设备序列号 (sn): {sn}')
    print(f'用户 ID (user): {user}')
    print(f'查询时间范围：{time.strftime("%Y-%m-%d", time.localtime(start_time))} 至 {time.strftime("%Y-%m-%d", time.localtime(end_time))}')
    print('=' * 50)
    
    try:
        result = query_alarm_page(
            sn, user, uuid, appkey, secret, movecard, auth,
            start_time, end_time, args.msg_type, args.page, args.rows
        )
        
        if result.get('code') == 2000:
            print('\n✅ 查询成功')
            data = result.get('data', {})
            total = data.get('total', 0)
            records = data.get('records', [])
            
            print(f'总记录数：{total}')
            print(f'当前页：{args.page}')
            print(f'每页条数：{args.rows}')
            print(f'本页记录数：{len(records)}')
            
            if records:
                print('\n报警记录列表:')
                for i, record in enumerate(records, 1):
                    alarm_id = record.get('alarmId', 'N/A')
                    alarm_time = record.get('alarmTime', 'N/A')
                    msg_type = record.get('msgType', 'N/A')
                    pic_url = record.get('picUrl', '')
                    print(f'  {i}. ID: {alarm_id}, 类型：{msg_type}, 时间：{alarm_time}')
                    if pic_url:
                        print(f'     图片：{pic_url}')
            
            print(f'\n完整响应:')
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            error_code = result.get('code', 'Unknown')
            error_msg = result.get('msg', 'Unknown error')
            print(f'\n❌ 查询失败')
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
