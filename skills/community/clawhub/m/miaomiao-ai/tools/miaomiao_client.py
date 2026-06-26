import os
import http.client
import json
import time
from dotenv import load_dotenv
from typing import List, Dict, Optional, Union

class MiaoMiaoClient:
    """秒秒AI 多能力智能体客户端 SDK"""
    
    def __init__(self, app_code: Optional[str] = None, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        初始化客户端
        :param app_code: 应用编码，优先使用参数，否则从环境变量读取
        :param api_key: API密钥，优先使用参数，否则从环境变量读取
        :param api_url: API接口地址，可选
        """
        load_dotenv()
        
        self.app_code = app_code or os.getenv("MIAOMIAO_APP_CODE", "ZQmQHAXf")
        self.api_key = api_key or os.getenv("MIAOMIAO_API_KEY")
        self.api_url = api_url or os.getenv("MIAOMIAO_API_URL", "api.link-ai.tech")
        self.debug = os.getenv("MIAOMIAO_DEBUG", "false").lower() == "true"
        
        if not self.app_code or not self.api_key:
            raise ValueError("请配置MIAOMIAO_APP_CODE和MIAOMIAO_API_KEY环境变量")
    
    def chat(self, content: str, messages: Optional[List[Dict]] = None, stream: bool = False) -> Union[str, Dict]:
        """
        发送聊天请求
        :param content: 用户输入内容
        :param messages: 历史消息列表，可选
        :param stream: 是否启用流式响应，默认false
        :return: 响应内容
        """
        if messages is None:
            messages = []
        
        messages.append({
            "role": "user",
            "content": content
        })
        
        payload = json.dumps({
            "app_code": self.app_code,
            "messages": messages,
            "stream": stream
        })
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        if self.debug:
            print(f"请求URL: {self.api_url}/v1/chat/completions")
            print(f"请求参数: {payload}")
        
        # 判断是否为图像相关请求，设置不同超时时间
        image_keywords = ['生成图片', '画图', 'AI绘图', '图像生成', '生成图像', '画一张']
        is_image_request = any(keyword in content for keyword in image_keywords)
        timeout = 80 if is_image_request else 40
        
        conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn.request("POST", "/v1/chat/completions", payload, headers)
                res = conn.getresponse()
                data = res.read()
                break
            except http.client.HTTPException as e:
                retry_count += 1
                error_msg = f"HTTP请求异常: {str(e)}"
                if retry_count == max_retries:
                    raise Exception(error_msg)
                if self.debug:
                    print(f"{error_msg}，正在重试...({retry_count}/{max_retries})")
                time.sleep(1)
                conn.close()
                conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
            except ConnectionError as e:
                retry_count += 1
                error_msg = f"网络连接异常: {str(e)}"
                if retry_count == max_retries:
                    raise Exception(error_msg)
                if self.debug:
                    print(f"{error_msg}，正在重试...({retry_count}/{max_retries})")
                time.sleep(1)
                conn.close()
                conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
            except Exception as e:
                retry_count += 1
                error_msg = f"未知异常: {str(e)}"
                if retry_count == max_retries:
                    raise Exception(error_msg)
                if self.debug:
                    print(f"{error_msg}，正在重试...({retry_count}/{max_retries})")
                time.sleep(1)
                conn.close()
                conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
        
        if self.debug:
            print(f"响应状态: {res.status}")
            print(f"响应内容: {data.decode('utf-8')}")
        
        if res.status != 200:
            try:
                error_data = json.loads(data.decode('utf-8'))
                error_message = error_data.get('error', {}).get('message', data.decode('utf-8'))
            except:
                error_message = data.decode('utf-8')
            raise Exception(f"请求失败: {res.status}, {error_message}")
        
        result = json.loads(data.decode("utf-8"))
        
        if stream:
            return result
        
        return result["choices"][0]["message"]["content"]
    
    def chat_with_history(self, messages: List[Dict], stream: bool = False) -> Union[str, Dict]:
        """
        带历史消息的聊天
        :param messages: 完整的消息列表
        :param stream: 是否启用流式响应
        :return: 响应内容
        """
        if not messages:
            raise ValueError("消息列表不能为空")
        
        payload = json.dumps({
            "app_code": self.app_code,
            "messages": messages,
            "stream": stream
        })
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # 判断是否为图像相关请求，设置不同超时时间
        image_keywords = ['生成图片', '画图', 'AI绘图', '图像生成', '生成图像', '画一张']
        # 获取最后一条用户消息
        last_user_message = next((msg for msg in reversed(messages) if msg['role'] == 'user'), None)
        is_image_request = False
        if last_user_message:
            is_image_request = any(keyword in last_user_message['content'] for keyword in image_keywords)
        timeout = 80 if is_image_request else 40
        
        conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn.request("POST", "/v1/chat/completions", payload, headers)
                res = conn.getresponse()
                data = res.read()
                break
            except http.client.HTTPException as e:
                retry_count += 1
                error_msg = f"HTTP请求异常: {str(e)}"
                if retry_count == max_retries:
                    raise Exception(error_msg)
                if self.debug:
                    print(f"{error_msg}，正在重试...({retry_count}/{max_retries})")
                time.sleep(1)
                conn.close()
                conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
            except ConnectionError as e:
                retry_count += 1
                error_msg = f"网络连接异常: {str(e)}"
                if retry_count == max_retries:
                    raise Exception(error_msg)
                if self.debug:
                    print(f"{error_msg}，正在重试...({retry_count}/{max_retries})")
                time.sleep(1)
                conn.close()
                conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
            except Exception as e:
                retry_count += 1
                error_msg = f"未知异常: {str(e)}"
                if retry_count == max_retries:
                    raise Exception(error_msg)
                if self.debug:
                    print(f"{error_msg}，正在重试...({retry_count}/{max_retries})")
                time.sleep(1)
                conn.close()
                conn = http.client.HTTPSConnection(self.api_url, timeout=timeout)
        
        if res.status != 200:
            try:
                error_data = json.loads(data.decode('utf-8'))
                error_message = error_data.get('error', {}).get('message', data.decode('utf-8'))
            except:
                error_message = data.decode('utf-8')
            raise Exception(f"请求失败: {res.status}, {error_message}")
        
        result = json.loads(data.decode("utf-8"))
        
        if stream:
            return result
        
        return result["choices"][0]["message"]["content"]

# 快捷调用函数
def chat(content: str, **kwargs) -> str:
    """快速发送聊天请求"""
    client = MiaoMiaoClient(**kwargs)
    return client.chat(content)
