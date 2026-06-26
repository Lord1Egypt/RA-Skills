#!/usr/bin/env python3
"""
杰峰室外安防车辆管理脚本

功能：
- 查询车辆列表
- 查询车辆数量
- 添加车辆
- 编辑车辆
- 删除车辆
- 车牌识别

API:
- LIST: POST /aisvr/v3/gateway/api/outdoorSecurity/car/list
- COUNT: POST /aisvr/v3/gateway/api/outdoorSecurity/car/count
- ADD: POST /aisvr/v3/gateway/api/outdoorSecurity/car/add
- EDIT: POST /aisvr/v3/gateway/api/outdoorSecurity/car/edit
- DEL: POST /aisvr/v3/gateway/api/outdoorSecurity/car/del
- PREVIEW: POST /aisvr/v3/gateway/api/outdoorSecurity/car/preview
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
    'api_list': '/aisvr/v3/gateway/api/outdoorSecurity/car/list',
    'api_count': '/aisvr/v3/gateway/api/outdoorSecurity/car/count',
    'api_add': '/aisvr/v3/gateway/api/outdoorSecurity/car/add',
    'api_edit': '/aisvr/v3/gateway/api/outdoorSecurity/car/edit',
    'api_del': '/aisvr/v3/gateway/api/outdoorSecurity/car/del',
    'api_preview': '/aisvr/v3/gateway/api/outdoorSecurity/car/preview'
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


def list_cars(user, uuid, appkey, secret, movecard, auth):
    """查询车辆列表"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {'user': user}
    url = CONFIG['base_url'] + CONFIG['api_list']
    return make_request(url, data, headers)


def count_cars(user, uuid, appkey, secret, movecard, auth):
    """查询车辆数量"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {'user': user}
    url = CONFIG['base_url'] + CONFIG['api_count']
    return make_request(url, data, headers)


def add_car(user, uuid, appkey, secret, movecard, auth, plate_number, color=None, car_type=None):
    """添加车辆"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {
        'user': user,
        'plateNumber': plate_number
    }
    
    if color:
        data['color'] = color
    if car_type:
        data['type'] = car_type
    
    url = CONFIG['base_url'] + CONFIG['api_add']
    return make_request(url, data, headers)


def edit_car(car_id, user, uuid, appkey, secret, movecard, auth, plate_number=None, color=None, car_type=None):
    """编辑车辆"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {
        'id': car_id,
        'user': user
    }
    
    if plate_number:
        data['plateNumber'] = plate_number
    if color:
        data['color'] = color
    if car_type:
        data['type'] = car_type
    
    url = CONFIG['base_url'] + CONFIG['api_edit']
    return make_request(url, data, headers)


def delete_car(car_id, user, uuid, appkey, secret, movecard, auth):
    """删除车辆"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {
        'id': car_id,
        'user': user
    }
    
    url = CONFIG['base_url'] + CONFIG['api_del']
    return make_request(url, data, headers)


def preview_plate(image_data, user, uuid, appkey, secret, movecard, auth):
    """车牌识别"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        'uuid': uuid,
        'appKey': appkey,
        'timeMillis': time_millis,
        'signature': signature,
        'Authorization': auth.strip() if auth else user
    }
    
    data = {
        'user': user,
        'imageData': image_data
    }
    
    url = CONFIG['base_url'] + CONFIG['api_preview']
    return make_request(url, data, headers)


def main():
    parser = argparse.ArgumentParser(description='杰峰室外安防车辆管理')
    parser.add_argument('--action', required=True, choices=['list', 'count', 'add', 'edit', 'del', 'preview'], help='操作类型')
    parser.add_argument('--user', help='用户 ID')
    parser.add_argument('--uuid', help='开放平台用户 uuid')
    parser.add_argument('--appkey', help='开放平台应用 appKey')
    parser.add_argument('--secret', help='开放平台应用密钥')
    parser.add_argument('--auth', help='用户认证 token (JWT)')
    parser.add_argument('--movecard', type=int, default=7, help='移动卡标识（默认：7）')
    parser.add_argument('--id', type=int, help='车辆 ID（edit/del 操作需要）')
    parser.add_argument('--plate-number', help='车牌号码')
    parser.add_argument('--color', help='车辆颜色')
    parser.add_argument('--type', help='车辆类型')
    parser.add_argument('--image-data', help='图片 Base64 数据（preview 操作需要）')
    
    args = parser.parse_args()
    
    # 从环境变量获取默认值
    env_uuid = os.environ.get('JF_UUID')
    env_appkey = os.environ.get('JF_APP_KEY')
    env_secret = os.environ.get('JF_APP_SECRET')
    env_movecard = os.environ.get('JF_MOVE_CARD', '7')
    env_auth = os.environ.get('JF_AUTHORIZATION')
    env_user = os.environ.get('JF_USER')
    
    uuid = args.uuid or env_uuid
    appkey = args.appkey or env_appkey
    secret = args.secret or env_secret
    movecard = args.movecard or int(env_movecard)
    auth = args.auth or env_auth
    user = args.user or env_user
    
    # 检查必需参数
    if not all([uuid, appkey, secret, auth, user]):
        print('❌ 缺少必需参数:')
        if not uuid: print('   - uuid (开放平台用户 uuid)')
        if not appkey: print('   - appkey (开放平台应用 appKey)')
        if not secret: print('   - secret (开放平台应用密钥)')
        if not auth: print('   - auth (用户认证 token)')
        if not user: print('   - user (用户 ID)')
        sys.exit(1)
    
    if args.action == 'add' and not args.plate_number:
        print('❌ add 操作需要 --plate-number 参数')
        sys.exit(1)
    
    if args.action in ['edit', 'del'] and not args.id:
        print(f'❌ {args.action} 操作需要 --id 参数')
        sys.exit(1)
    
    if args.action == 'preview' and not args.image_data:
        print('❌ preview 操作需要 --image-data 参数')
        sys.exit(1)
    
    print('🚗 杰峰室外安防车辆管理')
    print('=' * 50)
    print(f'环境：{CONFIG["base_url"]}')
    print(f'用户 ID (user): {user}')
    print(f'操作类型：{args.action}')
    print('=' * 50)
    
    try:
        if args.action == 'list':
            result = list_cars(user, uuid, appkey, secret, movecard, auth)
        elif args.action == 'count':
            result = count_cars(user, uuid, appkey, secret, movecard, auth)
        elif args.action == 'add':
            result = add_car(user, uuid, appkey, secret, movecard, auth, args.plate_number, args.color, args.type)
        elif args.action == 'edit':
            result = edit_car(args.id, user, uuid, appkey, secret, movecard, auth, args.plate_number, args.color, args.type)
        elif args.action == 'del':
            result = delete_car(args.id, user, uuid, appkey, secret, movecard, auth)
        else:  # preview
            result = preview_plate(args.image_data, user, uuid, appkey, secret, movecard, auth)
        
        if result.get('code') == 2000:
            print('\n✅ 操作成功')
            if args.action == 'list':
                data = result.get('data', [])
                print(f'共查询到 {len(data)} 辆车')
                for car in data:
                    car_id = car.get('id', 'N/A')
                    plate = car.get('plateNumber', 'N/A')
                    color = car.get('color', 'N/A')
                    car_type = car.get('type', 'N/A')
                    print(f'  - ID: {car_id}, 车牌：{plate}, 颜色：{color}, 类型：{car_type}')
            elif args.action == 'count':
                count = result.get('data', {}).get('count', 0)
                print(f'车辆总数：{count}')
            elif args.action == 'add':
                print(f'车辆已添加：{args.plate_number}')
            elif args.action == 'edit':
                print(f'车辆已更新：ID={args.id}')
            elif args.action == 'del':
                print(f'车辆已删除：ID={args.id}')
            elif args.action == 'preview':
                plate_result = result.get('data', {})
                plate_number = plate_result.get('plateNumber', 'N/A')
                confidence = plate_result.get('confidence', 'N/A')
                print(f'识别结果：{plate_number} (置信度：{confidence})')
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
