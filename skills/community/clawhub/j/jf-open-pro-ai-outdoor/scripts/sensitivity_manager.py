#!/usr/bin/env python3
"""
杰峰室外安防灵敏度设置脚本

功能：
- 查询设备灵敏度
- 设置设备灵敏度

API:
- GET: POST /aisvr/v3/gateway/api/outdoorSecurity/devInfo/getSensitivity
- SET: POST /aisvr/v3/gateway/api/outdoorSecurity/devInfo/setSensitivity
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
    'api_get': '/aisvr/v3/gateway/api/outdoorSecurity/devInfo/getSensitivity',
    'api_set': '/aisvr/v3/gateway/api/outdoorSecurity/devInfo/setSensitivity'
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


def get_sensitivity(sn, user, uuid, appkey, secret, movecard, auth):
    """查询设备灵敏度"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {'sn': sn, 'user': user}
    url = CONFIG['base_url'] + CONFIG['api_get']
    return make_request(url, data, headers)


def set_sensitivity(sn, user, uuid, appkey, secret, movecard, auth, sensitivity):
    """设置设备灵敏度"""
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
        'sensitivity': sensitivity
    }
    url = CONFIG['base_url'] + CONFIG['api_set']
    return make_request(url, data, headers)


def main():
    parser = argparse.ArgumentParser(description='杰峰室外安防灵敏度设置')
    parser.add_argument('--action', required=True, choices=['get', 'set'], help='操作类型：get=查询灵敏度，set=设置灵敏度')
    parser.add_argument('--sn', help='设备序列号')
    parser.add_argument('--user', help='用户 ID')
    parser.add_argument('--uuid', help='开放平台用户 uuid')
    parser.add_argument('--appkey', help='开放平台应用 appKey')
    parser.add_argument('--secret', help='开放平台应用密钥')
    parser.add_argument('--auth', help='用户认证 token (JWT)')
    parser.add_argument('--movecard', type=int, default=7, help='移动卡标识（默认：7）')
    parser.add_argument('--sensitivity', type=int, help='灵敏度值（1-10，仅 set 操作需要）')
    
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
    if not all([sn, user, uuid, appkey, secret, auth]):
        print('❌ 缺少必需参数:')
        if not sn: print('   - sn (设备序列号)')
        if not user: print('   - user (用户 ID)')
        if not uuid: print('   - uuid (开放平台用户 uuid)')
        if not appkey: print('   - appkey (开放平台应用 appKey)')
        if not secret: print('   - secret (开放平台应用密钥)')
        if not auth: print('   - auth (用户认证 token)')
        sys.exit(1)
    
    if args.action == 'set':
        if args.sensitivity is None:
            print('❌ set 操作需要 --sensitivity 参数')
            print('灵敏度范围：1-10（1=最低灵敏度，10=最高灵敏度）')
            sys.exit(1)
        if args.sensitivity < 1 or args.sensitivity > 10:
            print('❌ 灵敏度值必须在 1-10 范围内')
            sys.exit(1)
    
    print('📊 杰峰室外安防灵敏度设置')
    print('=' * 50)
    print(f'环境：{CONFIG["base_url"]}')
    print(f'设备序列号 (sn): {sn}')
    print(f'用户 ID (user): {user}')
    print(f'操作类型：{args.action}')
    print('=' * 50)
    
    try:
        if args.action == 'get':
            result = get_sensitivity(sn, user, uuid, appkey, secret, movecard, auth)
        else:
            result = set_sensitivity(sn, user, uuid, appkey, secret, movecard, auth, args.sensitivity)
        
        if result.get('code') == 2000:
            print('\n✅ 操作成功')
            if args.action == 'get':
                sensitivity = result.get('data', {}).get('sensitivity', 'N/A')
                print(f'当前灵敏度：{sensitivity}')
                print(f'\n灵敏度说明:')
                print(f'  1-3:  低灵敏度（减少误报，可能漏报）')
                print(f'  4-7:  中等灵敏度（推荐默认值）')
                print(f'  8-10: 高灵敏度（提高检测率，可能增加误报）')
            else:
                print(f'灵敏度已设置为：{args.sensitivity}')
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
