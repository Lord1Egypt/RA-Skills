#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度云 OCR 模块
提供 BaiduOCR 类用于百度云 OCR 识别
"""

import os
import base64
import requests
from pathlib import Path

class BaiduOCR:
    def __init__(self):
        """初始化百度云OCR"""
        self.api_key = os.getenv('BAIDU_API_KEY', '')
        self.secret_key = os.getenv('BAIDU_SECRET_KEY', '')
        
        # 尝试从配置文件读取
        self.config = self._load_config()
        if not self.api_key and 'baidu_api_key' in self.config:
            self.api_key = self.config['baidu_api_key']
        if not self.secret_key and 'baidu_secret_key' in self.config:
            self.secret_key = self.config['baidu_secret_key']
        
        # 检查是否配置
        self.available = bool(self.api_key and self.secret_key and '替换' not in self.api_key)
        
        if self.available:
            print("[BaiduOCR] 百度云 OCR 已配置")
            # 获取access_token
            self.access_token = self._get_access_token()
            if not self.access_token:
                self.available = False
                print("[BaiduOCR] 获取access_token失败，百度云OCR不可用")
        else:
            print("[BaiduOCR] 百度云 OCR 未配置（缺少密钥）")
    
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
            print("[BaiduOCR] 缺少 pyyaml，无法从YAML读取配置")
            return {}
        except Exception as e:
            print(f"[BaiduOCR] 读取配置文件失败: {e}")
            return {}
    
    def _get_access_token(self) -> str:
        """获取百度云access_token"""
        try:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get('access_token')
            else:
                # 仅记录状态码，不打印完整响应体（防止敏感信息泄露到日志）
                print(f"[BaiduOCR] 获取token失败: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"[BaiduOCR] 获取token异常: {e}")
            return None
    
    def recognize(self, image_path: str) -> dict:
        """识别图片"""
        if not self.available:
            return {"success": False, "text": "", "error": "百度云OCR未配置"}
        
        try:
            # 读取图片并base64编码
            with open(image_path, 'rb') as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # 调用百度云通用文字识别API
            url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={self.access_token}"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'image': img_base64}
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            if response.status_code != 200:
                return {"success": False, "text": "", "error": f"API调用失败: {response.text}"}
            
            result = response.json()
            if 'error_code' in result:
                return {"success": False, "text": "", "error": f"百度云OCR错误: {result.get('error_msg', '未知错误')}"}
            
            # 提取识别文本
            text_list = [item['words'] for item in result.get('words_result', [])]
            text = '\n'.join(text_list)
            
            if not text:
                return {"success": False, "text": "", "error": "识别结果为空"}
            
            return {"success": True, "text": text}
        except Exception as e:
            return {"success": False, "text": "", "error": str(e)}

if __name__ == "__main__":
    ocr = BaiduOCR()
    if len(sys.argv) > 1:
        result = ocr.recognize(sys.argv[1])
        print(result)
