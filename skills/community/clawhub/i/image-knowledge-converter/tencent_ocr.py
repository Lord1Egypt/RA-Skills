#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云 OCR 模块
提供 TencentOCR 类用于腾讯云 OCR 识别
"""

import os
import base64
import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

class TencentOCR:
    def __init__(self):
        """初始化腾讯云OCR"""
        self.secret_id = os.getenv('TENCENT_SECRET_ID', '')
        self.secret_key = os.getenv('TENCENT_SECRET_KEY', '')
        
        # 尝试从配置文件读取
        self.config = self._load_config()
        if not self.secret_id and 'tencent_secret_id' in self.config:
            self.secret_id = self.config['tencent_secret_id']
        if not self.secret_key and 'tencent_secret_key' in self.config:
            self.secret_key = self.config['tencent_secret_key']
        
        # 检查是否配置
        self.available = bool(self.secret_id and self.secret_key and '替换' not in self.secret_id)
        
        if self.available:
            print("[TencentOCR] 腾讯云 OCR 已配置")
        else:
            print("[TencentOCR] 腾讯云 OCR 未配置（缺少密钥）")
    
    def _load_config(self) -> dict:
        """从配置文件加载配置"""
        config_file = Path('config/api_keys.yaml')
        if not config_file.exists():
            return {}
        
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                # 支持嵌套格式
                if config and 'api_keys' in config:
                    return config['api_keys']
                return config or {}
        except ImportError:
            print("[TencentOCR] 缺少 pyyaml，无法从YAML读取配置")
            return {}
        except Exception as e:
            print(f"[TencentOCR] 读取配置文件失败: {e}")
            return {}
    
    def recognize(self, image_path: str) -> dict:
        """识别图片"""
        if not self.available:
            return {"success": False, "text": "", "error": "腾讯云OCR未配置"}
        
        # 优先尝试使用SDK
        try:
            result = self._recognize_with_sdk(image_path)
            if result.get('success'):
                return result
            print(f"[TencentOCR] SDK识别失败，尝试HTTP API: {result.get('error', '未知错误')}")
        except Exception as e:
            print(f"[TencentOCR] SDK不可用，尝试HTTP API: {e}")
        
        # SDK失败，尝试HTTP API
        try:
            return self._recognize_with_http_api(image_path)
        except Exception as e:
            return {"success": False, "text": "", "error": f"腾讯云OCR识别失败: {str(e)}"}
    
    def _recognize_with_sdk(self, image_path: str) -> dict:
        """使用SDK识别（需要正确安装tencentcloud-sdk-python）"""
        try:
            from tencentcloud.common import credential
            from tencentcloud.ocr.v20181119 import ocr_client, models
            
            cred = credential.Credential(self.secret_id, self.secret_key)
            client = ocr_client.OcrClient(cred, "ap-guangzhou")
            
            req = models.GeneralBasicOCRRequest()
            with open(image_path, 'rb') as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')
            req.ImageBase64 = img_base64
            
            resp = client.GeneralBasicOCR(req)
            text = '\n'.join([item.DetectedText for item in resp.TextDetections])
            return {"success": True, "text": text}
        except ImportError:
            raise Exception("腾讯云SDK未安装（pip install tencentcloud-sdk-python）")
        except Exception as e:
            raise e
    
    def _recognize_with_http_api(self, image_path: str) -> dict:
        """使用HTTP API直接调用（TC3签名）"""
        # 读取图片并base64编码
        with open(image_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # 构建请求体
        payload = {
            "ImageBase64": img_base64
        }
        
        # 腾讯云OCR API端点
        host = "ocr.tencentcloudapi.com"
        service = "ocr"
        region = "ap-guangzhou"
        action = "GeneralBasicOCR"
        version = "2018-11-19"
        
        # 获取当前时间戳
        timestamp = int(time.time())
        
        # 构建规范请求
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        canonical_headers = f"content-type:application/json\nhost:{host}\nx-tc-action:{action.lower()}\n"
        signed_headers = "content-type;host;x-tc-action"
        
        # 请求体哈希
        payload_str = json.dumps(payload)
        hashed_request_payload = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        canonical_request = (f"{http_request_method}\n{canonical_uri}\n{canonical_querystring}\n"
                          f"{canonical_headers}\n{signed_headers}\n{hashed_request_payload}")
        
        # 构建待签名字符串
        algorithm = "TC3-HMAC-SHA256"
        request_timestamp = str(timestamp)
        credential_scope = f"{datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d')}/{service}/tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        
        string_to_sign = f"{algorithm}\n{request_timestamp}\n{credential_scope}\n{hashed_canonical_request}"
        
        # 计算签名
        def sign(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
        
        secret_date = sign(("TC3" + self.secret_key).encode('utf-8'), 
                         datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d'))
        secret_service = sign(secret_date, service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # 构建Authorization
        authorization = (f"{algorithm} "
                         f"Credential={self.secret_id}/{credential_scope}, "
                         f"SignedHeaders={signed_headers}, "
                         f"Signature={signature}")
        
        # 发送请求
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json",
            "Host": host,
            "X-TC-Action": action,
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Version": version,
            "X-TC-Region": region
        }
        
        url = f"https://{host}"
        response = requests.post(url, headers=headers, data=payload_str, timeout=30)
        
        if response.status_code != 200:
            return {"success": False, "text": "", "error": f"API调用失败: {response.text}"}
        
        result = response.json()
        if 'Response' in result and 'Error' in result['Response']:
            error = result['Response']['Error']
            return {"success": False, "text": "", "error": f"腾讯云OCR错误: {error.get('Message', '未知错误')}"}
        
        # 提取识别文本
        if 'Response' in result and 'TextDetections' in result['Response']:
            text_list = [item['DetectedText'] for item in result['Response']['TextDetections']]
            text = '\n'.join(text_list)
            return {"success": True, "text": text}
        
        return {"success": False, "text": "", "error": "无法解析OCR结果"}

if __name__ == "__main__":
    ocr = TencentOCR()
    if len(sys.argv) > 1:
        result = ocr.recognize(sys.argv[1])
        print(result)
