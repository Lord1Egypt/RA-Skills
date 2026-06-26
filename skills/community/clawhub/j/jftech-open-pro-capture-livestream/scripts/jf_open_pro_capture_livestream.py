#!/usr/bin/env python3
"""
JF 杰峰设备认证与状态查询 Python SDK

功能:
- 获取设备 Token
- 设备登录
- 查询设备状态
- 设备云抓图
- 获取直播地址

用法:
    # 设置环境变量
    export JF_UUID="xxx" JF_APPKEY="xxx" JF_APPSECRET="xxx" JF_MOVECARD=5 JF_SN="xxx"
    python jf_open_pro_capture_livestream.py status

安全说明:
    ✅ 仅支持环境变量，避免凭据泄露风险
    🔒 不支持命令行参数或配置文件
"""

import hashlib
import os
import sys
import time

try:
    import requests
except ImportError:
    print("❌ 错误：需要安装 requests 库")
    print("请运行：pip install -r requirements.txt")
    sys.exit(1)


# ==================== 配置 ====================

DEFAULT_ENDPOINT = 'api.jftechws.com'
DEFAULT_MOVECARD = 5


def get_config():
    """
    从环境变量获取配置
    
    必需环境变量:
        JF_UUID - 开放平台用户唯一标识
        JF_APPKEY - 开放平台应用 Key
        JF_APPSECRET - 开放平台应用密钥
        JF_MOVECARD - 签名算法偏移量 (0-9)
        JF_SN - 设备序列号
    
    可选环境变量:
        JF_USERNAME - 设备用户名 (默认 admin)
        JF_PASSWORD - 设备密码
        JF_ENDPOINT - API 端点 (默认 api.jftechws.com)
        JF_KEEPALIVE - 保活时长 (默认 300)
    """
    config = {
        'uuid': os.environ.get('JF_UUID', ''),
        'appKey': os.environ.get('JF_APPKEY', ''),
        'appSecret': os.environ.get('JF_APPSECRET', ''),
        'moveCard': int(os.environ.get('JF_MOVECARD', DEFAULT_MOVECARD)),
        'endpoint': os.environ.get('JF_ENDPOINT', DEFAULT_ENDPOINT),
        'deviceSn': os.environ.get('JF_SN', ''),
        'userName': os.environ.get('JF_USERNAME', 'admin'),
        'passWord': os.environ.get('JF_PASSWORD', ''),
        'keepaliveTime': int(os.environ.get('JF_KEEPALIVE', 300)),
    }
    return config


# ==================== JF 杰峰认证 SDK ====================

class JFAuth:
    """JF 杰峰设备认证 SDK"""
    
    def __init__(self, uuid, app_key, app_secret, move_card, endpoint=DEFAULT_ENDPOINT):
        """
        初始化 JF 认证
        
        Args:
            uuid: 开放平台用户 uuid（必需）
            app_key: 开放平台应用 appKey（必需）
            app_secret: 应用密钥（必需）
            move_card: 签名算法参数（必需，int 类型 0-9）
            endpoint: API 端点域名
        """
        if not all([uuid, app_key, app_secret, move_card]):
            raise ValueError("缺少必需的配置参数：uuid, app_key, app_secret, move_card")
        
        self.uuid = uuid
        self.app_key = app_key
        self.app_secret = app_secret
        self.endpoint = endpoint
        self.move_card = move_card
    
    def _str2byte(self, s):
        """字符串转字节数组（ISO-8859-1 编码）"""
        return list(s.encode('iso-8859-1'))
    
    def _change(self, encrypt_str, move_card):
        """简单移位算法"""
        encrypt_byte = self._str2byte(encrypt_str)
        length = len(encrypt_byte)
        for idx in range(length):
            tmp = encrypt_byte[idx] if (idx % move_card) > ((length - idx) % move_card) else encrypt_byte[length - (idx + 1)]
            encrypt_byte[idx], encrypt_byte[length - (idx + 1)] = encrypt_byte[length - (idx + 1)], tmp
        return encrypt_byte
    
    def _merge_byte(self, encrypt_byte, change_byte):
        """合并字节数组"""
        length = len(encrypt_byte)
        temp = [0] * (length * 2)
        for i in range(length):
            temp[i] = encrypt_byte[i]
            temp[length * 2 - 1 - i] = change_byte[i]
        return temp
    
    def _get_signature(self, time_millis):
        """生成签名"""
        encrypt_str = self.uuid + self.app_key + self.app_secret + time_millis
        encrypt_byte = self._str2byte(encrypt_str)
        change_byte = self._change(encrypt_str, self.move_card)
        merged_byte = self._merge_byte(encrypt_byte, change_byte)
        return hashlib.md5(bytes(merged_byte)).hexdigest()
    
    def _get_time_millis(self):
        """生成 20 位时间戳"""
        return str(int(time.time() * 1000)).zfill(20)
    
    def _generate_request_id(self):
        """生成请求 ID"""
        import uuid
        return uuid.uuid4().hex
    
    def _request(self, url, body, headers=None):
        """发送 HTTP 请求"""
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json'
        
        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)
            return response.json()
        except Exception as e:
            return {'code': 0, 'msg': str(e)}
    
    def get_device_token(self, device_sn):
        """
        获取设备 Token（24 小时有效）
        """
        time_millis = self._get_time_millis()
        signature = self._get_signature(time_millis)
        url = f"https://{self.endpoint}/gwp/v3/rtc/device/token"
        headers = {
            'uuid': self.uuid,
            'appKey': self.app_key,
            'timeMillis': time_millis,
            'signature': signature,
            'X-Request-Id': self._generate_request_id()
        }
        body = {'sns': [device_sn], 'accessToken': ''}
        
        result = self._request(url, body, headers)
        if result.get('code') == 2000 and result.get('data') and len(result['data']) > 0:
            return {'success': True, 'token': result['data'][0]['token'], 'sn': result['data'][0]['sn']}
        return {'success': False, 'error': result.get('msg', 'Unknown error'), 'code': result.get('code')}
    
    def device_login(self, device_token, username, password='', keepalive_time=300):
        """设备登录认证"""
        time_millis = self._get_time_millis()
        signature = self._get_signature(time_millis)
        url = f"https://{self.endpoint}/gwp/v3/rtc/device/login/{device_token}"
        headers = {
            'uuid': self.uuid,
            'appKey': self.app_key,
            'timeMillis': time_millis,
            'signature': signature,
            'X-Request-Id': self._generate_request_id()
        }
        body = {
            'UserName': username,
            'PassWord': password,
            'KeepaliveTime': keepalive_time
        }
        
        result = self._request(url, body, headers)
        if result.get('code') == 2000 and result.get('data') and result['data'].get('Ret') == 100:
            return {
                'success': True,
                'sessionId': result['data'].get('SessionID'),
                'deviceType': result['data'].get('DeviceType'),
                'aliveInterval': result['data'].get('AliveInterval'),
                'channelNum': result['data'].get('ChannelNum')
            }
        return {'success': False, 'error': result.get('msg', 'Unknown error'), 'code': result.get('code')}
    
    def get_device_status(self, device_token):
        """查询设备状态"""
        time_millis = self._get_time_millis()
        signature = self._get_signature(time_millis)
        url = f"https://{self.endpoint}/gwp/v3/rtc/device/status"
        headers = {
            'uuid': self.uuid,
            'appKey': self.app_key,
            'timeMillis': time_millis,
            'signature': signature,
            'X-Request-Id': self._generate_request_id()
        }
        body = {'deviceTokenList': [device_token], 'region': 'Local'}
        
        result = self._request(url, body, headers)
        if result.get('code') == 2000 and result.get('data') and len(result['data']) > 0:
            device = result['data'][0]
            status = device.get('status', 'unknown')
            
            status_desc = '未知'
            if status == 'online':
                wake_status = device.get('wakeUpStatus')
                if wake_status is None:
                    status_desc = '常电设备，在线'
                elif wake_status == '0':
                    status_desc = '低功耗设备，已休眠'
                elif wake_status == '1':
                    status_desc = '低功耗设备，已唤醒'
                elif wake_status == '2':
                    status_desc = '低功耗设备，准备休眠中'
            elif status == 'notfound':
                status_desc = '设备不在线'
            
            auth_status = device.get('authStatus')
            auth_desc = '未知'
            if auth_status is not None:
                if auth_status == 1:
                    auth_desc = '认证成功'
                elif auth_status == 0:
                    auth_desc = '正在认证'
                elif auth_status == -1:
                    auth_desc = '认证未通过'
            
            return {
                'success': True,
                'uuid': device.get('uuid'),
                'status': status,
                'statusDesc': status_desc,
                'authStatus': auth_status,
                'authDesc': auth_desc,
                'wakeUpStatus': device.get('wakeUpStatus'),
                'wakeUpEnable': device.get('wakeUpEnable'),
                'wanIp': device.get('wanIp'),
                'channel': device.get('channel')
            }
        return {'success': False, 'error': result.get('msg', 'Unknown error'), 'code': result.get('code')}
    
    def device_capture(self, device_token, channel=0, pic_type=0):
        """设备云抓图"""
        time_millis = self._get_time_millis()
        signature = self._get_signature(time_millis)
        url = f"https://{self.endpoint}/gwp/v3/rtc/device/capture/{device_token}"
        headers = {
            'uuid': self.uuid,
            'appKey': self.app_key,
            'timeMillis': time_millis,
            'signature': signature,
            'X-Request-Id': self._generate_request_id()
        }
        body = {
            'Name': 'OPSNAP',
            'OPSNAP': {'Channel': channel, 'PicType': pic_type}
        }
        
        result = self._request(url, body, headers)
        if result.get('code') == 2000 and result.get('data') and result['data'].get('Ret') == 100:
            return {'success': True, 'imageUrl': result['data'].get('image'), 'ret': result['data'].get('Ret')}
        return {'success': False, 'error': result.get('msg', 'Unknown error'), 'code': result.get('code'), 'ret': result.get('data', {}).get('Ret')}
    
    def get_live_stream(self, device_token, channel='0', stream='1', protocol='flv', username='admin', password='', expire_time=None):
        """获取直播地址"""
        time_millis = self._get_time_millis()
        signature = self._get_signature(time_millis)
        url = f"https://{self.endpoint}/gwp/v3/rtc/device/livestream/{device_token}"
        headers = {
            'uuid': self.uuid,
            'appKey': self.app_key,
            'timeMillis': time_millis,
            'signature': signature,
            'X-Request-Id': self._generate_request_id()
        }
        body = {
            'channel': channel,
            'stream': stream,
            'protocol': protocol,
            'username': username,
            'password': password
        }
        if expire_time:
            body['expireTime'] = expire_time
        
        result = self._request(url, body, headers)
        if result.get('code') == 2000 and result.get('data') and result['data'].get('Ret') == 100:
            return {'success': True, 'url': result['data'].get('url'), 'ret': result['data'].get('Ret')}
        return {'success': False, 'error': result.get('msg', 'Unknown error'), 'code': result.get('code'), 'ret': result.get('data', {}).get('Ret'), 'retMsg': result.get('data', {}).get('retMsg')}


# ==================== 输出函数 ====================

def print_device_status(status):
    """打印设备状态"""
    print("\n=== 设备状态 ===")
    print(f"设备序列号：{status['uuid']}")
    print(f"状态：{status['status']} ({status['statusDesc']})")
    if status.get('authDesc'):
        print(f"认证状态：{status['authDesc']} ({status['authStatus']})")
    if status.get('wakeUpStatus') is not None:
        print(f"休眠状态：{status['wakeUpStatus']}")
    if status.get('wakeUpEnable') is not None:
        print(f"远程唤醒：{'支持' if status['wakeUpEnable'] == '1' else '不支持'}")
    if status.get('wanIp'):
        print(f"外网 IP: {status['wanIp']}")


# ==================== 主函数 ====================

def main():
    if len(sys.argv) < 2:
        print("用法：python jf_open_pro_capture_livestream.py <command>")
        print("")
        print("可用命令:")
        print("  status      查询设备状态")
        print("  login       设备登录")
        print("  capture     设备云抓图")
        print("  livestream  获取直播地址")
        print("  token       仅获取设备 Token")
        print("")
        print("环境变量:")
        print("  JF_UUID       - 开放平台用户唯一标识（必需）")
        print("  JF_APPKEY     - 开放平台应用 Key（必需）")
        print("  JF_APPSECRET  - 开放平台应用密钥（必需）")
        print("  JF_MOVECARD   - 签名算法偏移量 (0-9)（必需）")
        print("  JF_SN         - 设备序列号（必需）")
        print("  JF_USERNAME   - 设备用户名（可选，默认 admin）")
        print("  JF_PASSWORD   - 设备密码（可选）")
        print("  JF_ENDPOINT   - API 端点（可选，默认 api.jftechws.com）")
        sys.exit(1)
    
    command = sys.argv[1]
    
    # 从环境变量获取配置
    config = get_config()
    
    # 验证必需参数
    if not config['uuid']:
        print("❌ 错误：缺少必需环境变量 JF_UUID")
        sys.exit(1)
    if not config['appKey']:
        print("❌ 错误：缺少必需环境变量 JF_APPKEY")
        sys.exit(1)
    if not config['appSecret']:
        print("❌ 错误：缺少必需环境变量 JF_APPSECRET")
        sys.exit(1)
    if not config['deviceSn']:
        print("❌ 错误：缺少必需环境变量 JF_SN")
        sys.exit(1)
    
    print("============================================================")
    print("JF 杰峰设备认证工具 (Python)")
    print("============================================================")
    print(f"设备 SN: {config['deviceSn']}")
    print(f"命令：{command}")
    
    # 初始化 SDK
    sdk = JFAuth(
        uuid=config['uuid'],
        app_key=config['appKey'],
        app_secret=config['appSecret'],
        move_card=config['moveCard'],
        endpoint=config['endpoint']
    )
    
    device_token = None
    
    try:
        if command == 'token':
            print("\n>>> 获取设备 Token...")
            result = sdk.get_device_token(config['deviceSn'])
            if result['success']:
                print(f"✅ Token: {result['token']}")
            else:
                print(f"❌ 失败：{result['error']}")
        
        elif command == 'status':
            print("\n>>> 获取设备 Token...")
            token_result = sdk.get_device_token(config['deviceSn'])
            if not token_result['success']:
                print(f"❌ 获取 Token 失败：{token_result['error']}")
                return
            device_token = token_result['token']
            print("✅ Token 获取成功\n>>> 查询设备状态...")
            status_result = sdk.get_device_status(device_token)
            if status_result['success']:
                print_device_status(status_result)
            else:
                print(f"❌ 查询失败：{status_result['error']}")
        
        elif command == 'login':
            print("\n>>> 获取设备 Token...")
            token_result = sdk.get_device_token(config['deviceSn'])
            if not token_result['success']:
                print(f"❌ 获取 Token 失败：{token_result['error']}")
                return
            device_token = token_result['token']
            print("✅ Token 获取成功\n>>> 设备登录...")
            print(f"用户名：{config['userName']}, 保活时长：{config['keepaliveTime']}秒")
            login_result = sdk.device_login(device_token, config['userName'], config['passWord'], config['keepaliveTime'])
            if login_result['success']:
                print("\n=== 登录成功 ===")
                print(f"SessionID: {login_result['sessionId']}")
                print(f"设备类型：{login_result['deviceType']}")
                print(f"保活间隔：{login_result['aliveInterval']}秒")
                print(f"通道数：{login_result['channelNum']}")
            else:
                print(f"❌ 登录失败：{login_result['error']}")
        
        elif command == 'capture':
            print("\n>>> 获取设备 Token...")
            token_result = sdk.get_device_token(config['deviceSn'])
            if not token_result['success']:
                print(f"❌ 获取 Token 失败：{token_result['error']}")
                return
            device_token = token_result['token']
            print("✅ Token 获取成功")
            print("\n>>> 执行云抓图...")
            print("通道号：0, 图片类型：实时图片（辅码流）")
            print("⚠️  注意：云抓图按调用次数计费")
            capture_result = sdk.device_capture(device_token, 0, 0)
            if capture_result['success']:
                print("\n=== 抓图成功 ===")
                print(f"图片地址：{capture_result['imageUrl']}")
                print("⚠️  图片有效期 24 小时，请及时下载！")
                print(f"\n下载命令：curl -o snapshot.png \"{capture_result['imageUrl']}\"")
            else:
                print(f"❌ 抓图失败：{capture_result['error']}")
                if capture_result.get('ret'):
                    print(f"设备返回码：{capture_result['ret']}")
        
        elif command == 'livestream':
            print("\n>>> 获取设备 Token...")
            token_result = sdk.get_device_token(config['deviceSn'])
            if not token_result['success']:
                print(f"❌ 获取 Token 失败：{token_result['error']}")
                return
            device_token = token_result['token']
            print("✅ Token 获取成功")
            print("\n>>> 获取直播地址...")
            print("通道号：0, 码流：标清（辅码流）, 协议：flv")
            print("⚠️  注意：直播地址默认有效期 10 小时")
            print("⚠️  低功耗设备：获取后 3 秒内必须播放")
            stream_result = sdk.get_live_stream(
                device_token, 
                '0', 
                '1', 
                'flv', 
                config['userName'], 
                config['passWord']
            )
            if stream_result['success']:
                print("\n=== 直播地址获取成功 ===")
                print(f"播放地址：{stream_result['url']}")
                print("\n使用方式:")
                print("  - H5 播放：<video src=\"URL\" controls></video>")
                print("  - VLC 播放：vlc \"URL\"")
                print("  - ffmpeg: ffmpeg -i \"URL\" output.mp4")
                print("\n⚠️  地址有效期 10 小时，可重复使用")
            else:
                print(f"❌ 获取失败：{stream_result['error']}")
                if stream_result.get('retMsg'):
                    print(f"设备信息：{stream_result['retMsg']}")
                if stream_result.get('ret'):
                    print(f"设备返回码：{stream_result['ret']}")
        
        else:
            print(f"❌ 未知命令：{command}")
            print("可用命令：status, login, capture, livestream, token")
    
    except Exception as e:
        print(f"❌ 执行出错：{e}")
        import traceback
        traceback.print_exc()
    
    print("\n============================================================")


if __name__ == '__main__':
    main()
