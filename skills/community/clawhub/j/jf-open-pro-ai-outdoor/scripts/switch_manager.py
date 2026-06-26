#!/usr/bin/env python3
"""
杰峰室外安防服务开关管理脚本

功能：
- 查询室外安防服务状态
- 开启/关闭室外安防服务

API:
- GET:  POST /aisvr/v3/gateway/api/outdoorSecurity/ai/analysis/switch/get
- CHANGE: POST /aisvr/v3/gateway/api/outdoorSecurity/ai/analysis/switch/change
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error

# 添加脚本目录到路径，以便导入 jf_signature
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from jf_signature import generate_signature

# 配置
CONFIG = {
    'uuid': 'xmeye',
    'base_url': 'https://api-cn.jftechws.com',
    'api_get': '/aisvr/v3/gateway/api/outdoorSecurity/ai/analysis/switch/get',
    'api_change': '/aisvr/v3/gateway/api/outdoorSecurity/ai/analysis/switch/change'
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


def query_switch(sn, user, uuid, appkey, secret, movecard, auth):
    """查询室外安防服务状态"""
    # 生成签名
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    # 构建请求头
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    # 构建请求数据
    data = {'sn': sn, 'user': user}
    
    # 发送请求
    url = CONFIG['base_url'] + CONFIG['api_get']
    result = make_request(url, data, headers)
    
    return result


def change_switch(sn, user, uuid, appkey, secret, movecard, auth, enable):
    """开关室外安防服务"""
    # 生成签名
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    # 构建请求头
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    # 构建请求数据
    data = {
        'sn': sn,
        'user': user,
        'aiAnalysisSwitch': enable
    }
    
    # 发送请求
    url = CONFIG['base_url'] + CONFIG['api_change']
    result = make_request(url, data, headers)
    
    return result


def check_env_vars():
    """检查必需的环境变量"""
    required_vars = {
        'JF_UUID': '开放平台用户 uuid',
        'JF_APP_KEY': '开放平台应用 appKey',
        'JF_APP_SECRET': '开放平台应用密钥',
        'JF_MOVE_CARD': '移动卡标识（用于签名）',
        'JF_DEVICE_SN': '设备序列号',
        'JF_AUTHORIZATION': '用户 token (JWT)',
        'JF_USER': '用户 ID'
    }
    
    missing = []
    for var, desc in required_vars.items():
        if not os.environ.get(var):
            missing.append(f'{var} ({desc})')
    
    if missing:
        print('❌ 缺少必需的环境变量:')
        for var in missing:
            print(f'   - {var}')
        print('\n请先配置这些环境变量后再使用本脚本。')
        print('配置示例:')
        print('  export JF_UUID="your-uuid"')
        print('  export JF_APP_KEY="your-appkey"')
        print('  export JF_APP_SECRET="your-secret"')
        print('  export JF_MOVE_CARD="7"')
        print('  export JF_DEVICE_SN="your-device-sn"')
        print('  export JF_AUTHORIZATION="your-auth"')
        print('  export JF_USER="your-user"')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='杰峰室外安防服务开关管理')
    parser.add_argument('--action', required=True, choices=['get', 'change'], help='操作类型：get=查询状态，change=开关控制')
    parser.add_argument('--sn', help='设备序列号')
    parser.add_argument('--user', help='用户 ID')
    parser.add_argument('--uuid', help='开放平台用户 uuid')
    parser.add_argument('--appkey', help='开放平台应用 appKey')
    parser.add_argument('--secret', help='开放平台应用密钥')
    parser.add_argument('--auth', help='用户认证 token (JWT)')
    parser.add_argument('--movecard', type=int, default=7, help='移动卡标识（默认：7）')
    parser.add_argument('--enable', type=lambda x: x.lower() == 'true', help='true=开启，false=关闭（仅 change 操作需要）')
    
    args = parser.parse_args()
    
    # 从环境变量获取默认值
    env_uuid = os.environ.get('JF_UUID')
    env_appkey = os.environ.get('JF_APP_KEY')
    env_secret = os.environ.get('JF_APP_SECRET')
    env_movecard = os.environ.get('JF_MOVE_CARD', '7')
    env_sn = os.environ.get('JF_DEVICE_SN')
    env_auth = os.environ.get('JF_AUTHORIZATION')
    env_user = os.environ.get('JF_USER')
    
    # 命令行参数优先于环境变量
    uuid = args.uuid or env_uuid
    appkey = args.appkey or env_appkey
    secret = args.secret or env_secret
    movecard = args.movecard or int(env_movecard)
    sn = args.sn or env_sn
    auth = args.auth or env_auth
    user = args.user or env_user
    
    # 检查必需参数
    if args.action == 'get':
        if not all([sn, user, uuid, appkey, secret, auth]):
            print('❌ 缺少必需参数:')
            if not sn: print('   - sn (设备序列号)')
            if not user: print('   - user (用户 ID)')
            if not uuid: print('   - uuid (开放平台用户 uuid)')
            if not appkey: print('   - appkey (开放平台应用 appKey)')
            if not secret: print('   - secret (开放平台应用密钥)')
            if not auth: print('   - auth (用户认证 token)')
            sys.exit(1)
    elif args.action == 'change':
        if not all([sn, user, uuid, appkey, secret, auth, args.enable]):
            print('❌ 缺少必需参数:')
            if not sn: print('   - sn (设备序列号)')
            if not user: print('   - user (用户 ID)')
            if not uuid: print('   - uuid (开放平台用户 uuid)')
            if not appkey: print('   - appkey (开放平台应用 appKey)')
            if not secret: print('   - secret (开放平台应用密钥)')
            if not auth: print('   - auth (用户认证 token)')
            if args.enable is None: print('   - enable (true=开启，false=关闭)')
            sys.exit(1)
    
    print('🔧 杰峰室外安防服务开关管理')
    print('=' * 50)
    print(f'环境：{CONFIG["base_url"]}')
    print(f'设备序列号 (sn): {sn}')
    print(f'用户 ID (user): {user}')
    print(f'操作类型：{args.action}')
    print('=' * 50)
    
    try:
        if args.action == 'get':
            result = query_switch(sn, user, uuid, appkey, secret, movecard, auth)
        else:
            result = change_switch(sn, user, uuid, appkey, secret, movecard, auth, args.enable)
        
        if result.get('code') == 2000:
            print('\n✅ 操作成功')
            if args.action == 'get':
                status = '已开启' if result.get('data', {}).get('aiAnalysisSwitch') else '已关闭'
                print(f'室外安防服务状态：{status}')
            else:
                status = '开启' if args.enable else '关闭'
                print(f'服务已{status}')
            print(f'\n完整响应:')
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            error_code = result.get('code', 'Unknown')
            error_msg = result.get('msg', 'Unknown error')
            print(f'\n❌ 操作失败')
            print(f'错误码：{error_code}')
            print(f'错误信息：{error_msg}')
            
            # 常见错误码处理
            if error_code == 12504:
                print('\n💡 处理建议：设备未开通室外安防套餐，请登录开放平台为设备绑定套餐卡')
            elif error_code == 28007:
                print('\n💡 处理建议：Header 参数错误，请检查 uuid、appKey、timeMillis、signature')
            elif error_code == 40103:
                print('\n💡 处理建议：Token 已过期，请重新获取 authorization')
            
            sys.exit(1)
            
    except Exception as e:
        print(f'\n❌ 请求异常：{str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()
