#!/usr/bin/env python3
"""
JF 杰峰云台 PTZ 控制工具 - Python 版本

仅支持环境变量配置凭据，避免命令行泄露风险。

用法:
    export JF_UUID="your-uuid"
    export JF_APPKEY="your-appkey"
    export JF_APPSECRET="your-appsecret"
    export JF_MOVECARD=5
    export JF_SN="your-device-sn"
    export JF_USERNAME="admin"
    export JF_PASSWORD="your-password"
    
    python jf_open_pro_ptz_control.py status
    python jf_open_pro_ptz_control.py ptz --direction up --action start
    python jf_open_pro_ptz_control.py mask --enable true
    python jf_open_pro_ptz_control.py zoom --zoom-command ZoomTile --action start
    python jf_open_pro_ptz_control.py preset --preset-command set --id 1 --name "门口"
    python jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 1
"""

import argparse
import hashlib
import json
import os
import time
import urllib.request
import urllib.error


# ==================== 工具函数 ====================

def str2byte(s):
    """字符串转字节数组（UTF-8 编码）"""
    return list(s.encode('utf-8'))


def change(encrypt_str, move_card):
    """移位算法"""
    encrypt_byte = str2byte(encrypt_str)
    length = len(encrypt_byte)
    for idx in range(length):
        tmp = encrypt_byte[idx] if (idx % move_card) > ((length - idx) % move_card) else encrypt_byte[length - (idx + 1)]
        encrypt_byte[idx], encrypt_byte[length - (idx + 1)] = encrypt_byte[length - (idx + 1)], tmp
    return encrypt_byte


def merge_byte(encrypt_byte, change_byte):
    """合并字节数组"""
    length = len(encrypt_byte)
    temp = [0] * (length * 2)
    for idx in range(length):
        temp[idx] = encrypt_byte[idx]
        temp[length * 2 - 1 - idx] = change_byte[idx]
    return temp


def get_signature(uuid, app_key, app_secret, time_millis, move_card=5):
    """获取签名"""
    encrypt_str = uuid + app_key + app_secret + time_millis
    encrypt_byte = str2byte(encrypt_str)
    change_byte = change(encrypt_str, move_card)
    merged_byte = merge_byte(encrypt_byte, change_byte)
    return hashlib.md5(bytes(merged_byte)).hexdigest()


def get_time_millis():
    """获取 20 位时间戳"""
    return str(int(time.time() * 1000)).zfill(20)


def generate_request_id():
    """生成 32 位请求 ID"""
    import random
    return ''.join(random.choice('0123456789abcdef') for _ in range(32))


# ==================== HTTP 请求 ====================

def https_post(url, data, headers):
    """发送 HTTPS POST 请求"""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raise Exception(f'HTTP 错误：{e.code} - {e.reason}')
    except urllib.error.URLError as e:
        raise Exception(f'请求失败：{e.reason}')


# ==================== 认证相关 ====================

def get_device_token(config):
    """获取设备 Token"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/token"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    data = {'sns': [config['deviceSn']], 'accessToken': ''}
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"获取 Token 失败：{response.get('msg')} (code: {response.get('code')})")
    
    if not response.get('data') or len(response['data']) == 0:
        raise Exception('获取 Token 失败：返回数据为空')
    
    return response['data'][0]['token']


def device_login(config, device_token, keepalive_time=300):
    """设备登录"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/login/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    data = {
        'UserName': config['userName'],
        'PassWord': config['passWord'] or '',
        'KeepaliveTime': keepalive_time
    }
    
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"设备登录失败：{response.get('msg')} (code: {response.get('code')})")
    
    if response.get('data', {}).get('Ret') != 100:
        raise Exception(f"设备登录失败：设备返回码 {response['data']['Ret']}")
    
    return response['data']


# ==================== 设备状态查询 ====================

def get_device_status(config):
    """获取设备状态"""
    print('>>> 获取设备 Token...')
    device_token = get_device_token(config)
    
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/status"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    data = {'deviceTokenList': [device_token], 'region': 'Local'}
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"查询状态失败：{response.get('msg')} (code: {response.get('code')})")
    
    return response['data'][0]


# ==================== PTZ 方向控制 ====================

DIRECTION_MAP = {
    'up': 'DirectionUp',
    'down': 'DirectionDown',
    'left': 'DirectionLeft',
    'right': 'DirectionRight',
    'leftup': 'DirectionLeftUp',
    'leftdown': 'DirectionLeftDown',
    'rightup': 'DirectionRightUp',
    'rightdown': 'DirectionRightDown'
}


def ptz_control(config, device_token, direction, action, step=5, channel=0):
    """云台方向控制"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/opdev/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    command = DIRECTION_MAP.get(direction.lower())
    if not command:
        raise Exception(f'无效的方向：{direction}')
    
    preset = 0 if action.lower() == 'start' else -1
    
    data = {
        'Name': 'OPPTZControl',
        'OPPTZControl': {
            'Command': command,
            'Parameter': {
                'Preset': preset,
                'Channel': channel,
                'Step': step
            }
        }
    }
    
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"PTZ 控制失败：{response.get('msg')} (code: {response.get('code')})")
    
    return response['data']


# ==================== 一键遮蔽 ====================

def set_mask(config, device_token, enable):
    """一键遮蔽"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/setconfig/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    data = {
        'Name': 'General.OneKeyMaskVideo',
        'General.OneKeyMaskVideo': [{'Enable': enable}]
    }
    
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"一键遮蔽设置失败：{response.get('msg')} (code: {response.get('code')})")
    
    return response['data']


# ==================== 变倍聚焦控制 ====================

def zoom_focus_control(config, device_token, command, action, step=8, channel=0):
    """变倍聚焦控制"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/opdev/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    preset = 0 if action.lower() == 'start' else -1
    
    data = {
        'Name': 'OPPTZControl',
        'OPPTZControl': {
            'Command': command,
            'Parameter': {
                'Channel': channel,
                'Step': step,
                'Preset': preset
            }
        }
    }
    
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"变倍聚焦控制失败：{response.get('msg')} (code: {response.get('code')})")
    
    return response['data']


# ==================== 预置点管理 ====================

def preset_control(config, device_token, command, preset_id, preset_name='', channel=0):
    """预置点控制"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/opdev/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    command_map = {
        'set': 'SetPreset',
        'clear': 'ClearPreset',
        'goto': 'GotoPreset',
        'name': 'SetPresetName'
    }
    
    op_command = command_map.get(command.lower())
    if not op_command:
        raise Exception(f'无效的预置点命令：{command}')
    
    data = {
        'Name': 'OPPTZControl',
        'OPPTZControl': {
            'Command': op_command,
            'Parameter': {
                'Preset': preset_id,
                'Channel': channel
            }
        }
    }
    
    if command in ['set', 'name']:
        data['OPPTZControl']['Parameter']['PresetName'] = preset_name or f'预置点{preset_id}'
    
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"预置点操作失败：{response.get('msg')} (code: {response.get('code')})")
    
    return response['data']


def get_preset_list(config, device_token):
    """获取预置点列表"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/getconfig/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    data = {'Name': 'Uart.PTZPreset'}
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"获取预置点列表失败：{response.get('msg')} (code: {response.get('code')})")
    
    # API 返回的是二维数组，需要扁平化
    presets = response['data'].get('Uart.PTZPreset', [])
    return [item for sublist in presets for item in sublist] if presets else []


# ==================== 巡航管理 ====================

def tour_control(config, device_token, command, tour_id=0, preset_id=0, step=5, channel=0):
    """巡航控制"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/opdev/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    command_map = {
        'add': 'AddTour',
        'delete': 'DeleteTour',
        'start': 'StartTour',
        'stop': 'StopTour',
        'clear': 'ClearTour'
    }
    
    op_command = command_map.get(command.lower())
    if not op_command:
        raise Exception(f'无效的巡航命令：{command}')
    
    data = {
        'Name': 'OPPTZControl',
        'OPPTZControl': {
            'Command': op_command,
            'Parameter': {
                'Tour': tour_id,
                'Channel': channel
            }
        }
    }
    
    if command in ['add', 'delete']:
        data['OPPTZControl']['Parameter']['Preset'] = preset_id
        data['OPPTZControl']['Parameter']['Step'] = step
    
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"巡航操作失败：{response.get('msg')} (code: {response.get('code')})")
    
    return response['data']


def get_tour_list(config, device_token):
    """获取巡航列表"""
    time_millis = get_time_millis()
    signature = get_signature(config['uuid'], config['appKey'], config['appSecret'], time_millis, config['moveCard'])
    
    url = f"https://{config['endpoint']}/gwp/v3/rtc/device/getconfig/{device_token}"
    headers = {
        'uuid': config['uuid'],
        'appKey': config['appKey'],
        'timeMillis': time_millis,
        'signature': signature,
        'X-Request-Id': generate_request_id()
    }
    
    data = {'Name': 'Uart.PTZTour'}
    response = https_post(url, data, headers)
    
    if response.get('code') != 2000:
        raise Exception(f"获取巡航列表失败：{response.get('msg')} (code: {response.get('code')})")
    
    return response['data'].get('Uart.PTZTour', [])


# ==================== 命令行参数解析 ====================

def parse_args():
    parser = argparse.ArgumentParser(
        description='JLink 杰峰云台 PTZ 控制工具 - Python 版本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
环境变量:
  JF_UUID       开放平台用户唯一标识 (必需)
  JF_APPKEY     开放平台应用 Key (必需)
  JF_APPSECRET  开放平台应用密钥 (必需)
  JF_MOVECARD   签名算法偏移量，通常设为 5 (必需)
  JF_SN         设备序列号 (必需)
  JF_USERNAME   设备用户名，默认 admin (可选)
  JF_PASSWORD   设备密码 (可选)
  JF_ENDPOINT   API 端点，默认 api.jftechws.com (可选)

示例:
  # 设置环境变量
  export JF_UUID="your-uuid"
  export JF_APPKEY="your-appkey"
  export JF_APPSECRET="your-appsecret"
  export JF_MOVECARD=5
  export JF_SN="your-device-sn"
  
  # 查询设备状态
  python jf_open_pro_ptz_control.py status
  
  # 云台方向控制（向上转动）
  python jf_open_pro_ptz_control.py ptz --direction up --action start
  python jf_open_pro_ptz_control.py ptz --direction up --action stop
  
  # 一键遮蔽
  python jf_open_pro_ptz_control.py mask --enable true
  
  # 变倍控制（放大）
  python jf_open_pro_ptz_control.py zoom --zoom-command ZoomTile --action start
  python jf_open_pro_ptz_control.py zoom --zoom-command ZoomTile --action stop
  
  # 设置预置点
  python jf_open_pro_ptz_control.py preset --preset-command set --id 1 --name "门口"
  
  # 转到预置点
  python jf_open_pro_ptz_control.py preset --preset-command goto --id 1
  
  # 添加巡航点
  python jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 1
  
  # 启动巡航
  python jf_open_pro_ptz_control.py tour --tour-command start --tour-id 0
        ''')
    
    parser.add_argument('command', choices=['status', 'ptz', 'mask', 'zoom', 'preset', 'tour'], help='命令')
    
    # PTZ 参数
    parser.add_argument('--direction', choices=['up', 'down', 'left', 'right', 'leftup', 'leftdown', 'rightup', 'rightdown'], help='方向')
    parser.add_argument('--action', choices=['start', 'stop'], help='动作')
    parser.add_argument('--step', type=int, default=5, help='速度 1-8（默认：5）')
    
    # Mask 参数
    parser.add_argument('--enable', type=str, help='开启/关闭遮蔽 (true/false)')
    
    # Zoom 参数
    parser.add_argument('--zoom-command', dest='zoom_command', help='变倍/聚焦命令')
    
    # Preset 参数
    parser.add_argument('--preset-command', dest='preset_command', help='预置点操作 (set/clear/goto/name/list)')
    parser.add_argument('--id', type=int, help='预置点 ID')
    parser.add_argument('--name', help='预置点名称')
    
    # Tour 参数
    parser.add_argument('--tour-command', dest='tour_command', help='巡航操作 (add/delete/start/stop/clear/list)')
    parser.add_argument('--tour-id', dest='tour_id', type=int, default=0, help='巡航线路 ID（默认：0）')
    parser.add_argument('--preset-id', dest='preset_id', type=int, help='预置点 ID')
    
    return parser.parse_args()


def get_config_from_env():
    """从环境变量读取配置"""
    required_vars = ['JF_UUID', 'JF_APPKEY', 'JF_APPSECRET', 'JF_MOVECARD', 'JF_SN']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        raise Exception(f"缺少必需的环境变量：{', '.join(missing_vars)}\n"
                       f"请设置：export JF_UUID='...' JF_APPKEY='...' JF_APPSECRET='...' JF_MOVECARD=5 JF_SN='...'")
    
    return {
        'uuid': os.environ.get('JF_UUID'),
        'appKey': os.environ.get('JF_APPKEY'),
        'appSecret': os.environ.get('JF_APPSECRET'),
        'moveCard': int(os.environ.get('JF_MOVECARD', 5)),
        'endpoint': os.environ.get('JF_ENDPOINT', 'api.jftechws.com'),
        'deviceSn': os.environ.get('JF_SN'),
        'userName': os.environ.get('JF_USERNAME', 'admin'),
        'passWord': os.environ.get('JF_PASSWORD', '')
    }


def main():
    args = parse_args()
    
    try:
        config = get_config_from_env()
    except Exception as e:
        print(f'❌ 配置错误：{e}')
        return 1
    
    try:
        if args.command == 'status':
            print('========================================')
            print('JLink 设备状态查询')
            print('========================================')
            print(f"设备 SN: {config['deviceSn']}")
            print()
            
            status = get_device_status(config)
            
            print('=== 设备状态 ===')
            print(f"设备序列号：{status.get('uuid')}")
            print(f"状态：{status.get('status')}")
            print(f"认证状态：{status.get('authStatus')}")
            if status.get('wakeUpStatus') is not None:
                print(f"唤醒状态：{status.get('wakeUpStatus')}")
            if status.get('wakeUpEnable') is not None:
                print(f"支持唤醒：{status.get('wakeUpEnable')}")
            if status.get('wanIp'):
                print(f"WAN IP: {status.get('wanIp')}")
        
        elif args.command == 'ptz':
            if not args.direction or not args.action:
                print('❌ PTZ 命令需要 --direction 和 --action 参数')
                return 1
            
            print('========================================')
            print('JLink 云台方向控制')
            print('========================================')
            print(f"设备 SN: {config['deviceSn']}")
            print(f"方向：{args.direction}")
            print(f"动作：{args.action}")
            print(f"速度：{args.step}")
            print()
            
            device_token = get_device_token(config)
            result = ptz_control(config, device_token, args.direction, args.action, args.step)
            
            print('✅ PTZ 控制成功')
            print(f"返回码：{result.get('Ret')}")
        
        elif args.command == 'mask':
            if args.enable is None:
                print('❌ Mask 命令需要 --enable 参数')
                return 1
            
            enable = args.enable.lower() == 'true'
            print('========================================')
            print('JLink 一键遮蔽')
            print('========================================')
            print(f"设备 SN: {config['deviceSn']}")
            print(f"开启遮蔽：{enable}")
            print()
            
            device_token = get_device_token(config)
            result = set_mask(config, device_token, enable)
            
            print(f"✅ 一键遮蔽{'开启' if enable else '关闭'}成功")
            print(f"返回码：{result.get('Ret')}")
        
        elif args.command == 'zoom':
            if not args.zoom_command or not args.action:
                print('❌ Zoom 命令需要 --zoom-command 和 --action 参数')
                return 1
            
            print('========================================')
            print('JLink 变倍聚焦控制')
            print('========================================')
            print(f"设备 SN: {config['deviceSn']}")
            print(f"命令：{args.zoom_command}")
            print(f"动作：{args.action}")
            print(f"速度：{args.step}")
            print()
            
            device_token = get_device_token(config)
            result = zoom_focus_control(config, device_token, args.zoom_command, args.action, args.step)
            
            print('✅ 变倍聚焦控制成功')
            print(f"返回码：{result.get('Ret')}")
        
        elif args.command == 'preset':
            if not args.preset_command:
                print('❌ Preset 命令需要 --preset-command 参数')
                return 1
            
            print('========================================')
            print('JLink 预置点管理')
            print('========================================')
            print(f"设备 SN: {config['deviceSn']}")
            print(f"操作：{args.preset_command}")
            if args.id is not None:
                print(f"预置点 ID: {args.id}")
            if args.name:
                print(f"名称：{args.name}")
            print()
            
            device_token = get_device_token(config)
            
            if args.preset_command == 'list':
                presets = get_preset_list(config, device_token)
                print('=== 预置点列表 ===')
                if not presets:
                    print('暂无预置点')
                else:
                    for p in presets:
                        print(f"  ID {p.get('Id')}: {p.get('PresetName')}")
            else:
                if args.id is None:
                    print('❌ 需要指定 --id 参数')
                    return 1
                
                result = preset_control(config, device_token, args.preset_command, args.id, args.name or '')
                print(f'✅ 预置点{args.preset_command}成功')
                print(f"返回码：{result.get('Ret')}")
        
        elif args.command == 'tour':
            if not args.tour_command:
                print('❌ Tour 命令需要 --tour-command 参数')
                return 1
            
            print('========================================')
            print('JLink 巡航管理')
            print('========================================')
            print(f"设备 SN: {config['deviceSn']}")
            print(f"操作：{args.tour_command}")
            print(f"巡航线路 ID: {args.tour_id}")
            if args.preset_id is not None:
                print(f"预置点 ID: {args.preset_id}")
            print()
            
            device_token = get_device_token(config)
            
            if args.tour_command == 'list':
                tours = get_tour_list(config, device_token)
                print('=== 巡航线路列表 ===')
                print(json.dumps(tours, indent=2, ensure_ascii=False))
            else:
                result = tour_control(config, device_token, args.tour_command, args.tour_id, args.preset_id or 0, args.step)
                print(f'✅ 巡航{args.tour_command}成功')
                print(f"返回码：{result.get('Ret')}")
        
        print('========================================')
        return 0
    
    except Exception as e:
        print(f'❌ 错误：{e}')
        return 1


if __name__ == '__main__':
    exit(main())
