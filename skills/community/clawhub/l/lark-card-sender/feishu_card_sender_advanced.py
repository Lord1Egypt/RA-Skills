#!/usr/bin/env python3
"""
高级飞书卡片发送器
专业级interactive卡片发送解决方案
"""

import json
import requests
import os
import time
from typing import Dict, Any, Optional, List
from feishu_card_templates import (
    build_news_card, build_flight_deal_card, build_simple_info_card
)

class AdvancedFeishuCardSender:
    """高级飞书卡片发送器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化发送器
        
        Args:
            app_id: 飞书应用ID，如果不提供则从环境变量获取
            app_secret: 飞书应用密钥，如果不提供则从环境变量获取
        """
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        
        if not self.app_id or not self.app_secret:
            raise ValueError("必须提供app_id和app_secret，或设置环境变量FEISHU_APP_ID和FEISHU_APP_SECRET")
        
        self.base_url = "https://open.feishu.cn/open-apis"
        self.tenant_access_token = None
        self.token_expires_at = 0
        
    def get_tenant_access_token(self) -> str:
        """获取tenant_access_token，带缓存机制"""
        current_time = int(time.time())
        
        # 如果token还有效，直接返回
        if self.tenant_access_token and current_time < self.token_expires_at:
            return self.tenant_access_token
            
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取token失败: {result.get('msg')} (错误码: {result.get('code')})")
                
            self.tenant_access_token = result["tenant_access_token"]
            # 提前5分钟过期，避免边界情况
            self.token_expires_at = current_time + result.get("expire", 7200) - 300
            return self.tenant_access_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def validate_card_size(self, card: Dict[str, Any]) -> bool:
        """验证卡片大小是否在限制内（30KB）"""
        card_json = json.dumps(card, ensure_ascii=False)
        size_bytes = len(card_json.encode('utf-8'))
        size_kb = size_bytes / 1024
        
        if size_kb > 30:
            print(f"⚠️ 警告：卡片大小为 {size_kb:.1f}KB，超过30KB限制")
            return False
        else:
            print(f"✅ 卡片大小验证通过：{size_kb:.1f}KB")
            return True
    
    def send_interactive_card(self, receive_id: str, receive_id_type: str, 
                            card: Dict[str, Any], uuid: Optional[str] = None) -> Dict[str, Any]:
        """发送interactive卡片"""
        if not self.validate_card_size(card):
            raise ValueError("卡片大小超过30KB限制")
            
        access_token = self.get_tenant_access_token()
            
        url = f"{self.base_url}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 构建请求体
        payload = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(card, ensure_ascii=False)
        }
        
        # 添加UUID用于去重
        if uuid:
            payload["uuid"] = uuid
            
        params = {
            "receive_id_type": receive_id_type
        }
        
        try:
            response = requests.post(url, headers=headers, params=params, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 0:
                error_code = result.get('code')
                error_msg = result.get('msg', 'Unknown error')
                
                # 特殊错误处理
                error_handlers = {
                    230013: "用户不在应用可用范围内",
                    230002: "机器人不在群组中",
                    230006: "应用未开启机器人能力",
                    230020: "触发频率限制",
                    230025: "消息内容超出长度限制",
                    99992361: "open_id跨应用问题"
                }
                
                error_desc = error_handlers.get(error_code, "未知错误")
                raise Exception(f"发送失败: {error_desc} - {error_msg} (错误码: {error_code})")
                
            return {
                "success": True,
                "message_id": result.get("data", {}).get("message_id"),
                "chat_id": result.get("data", {}).get("chat_id"),
                "response": result
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def send_simple_card(self, receive_id: str, receive_id_type: str, 
                        title: str, content: str, template: str = "blue",
                        uuid: Optional[str] = None) -> Dict[str, Any]:
        """发送简单卡片"""
        card = build_simple_info_card(title, content, template)
        return self.send_interactive_card(receive_id, receive_id_type, card, uuid)
    
    def send_news_card(self, receive_id: str, receive_id_type: str,
                      news_items: List[Dict[str, str]], 
                      title: str = "📰 今日新闻简报",
                      uuid: Optional[str] = None) -> Dict[str, Any]:
        """发送新闻简报卡片"""
        card = build_news_card(news_items, title)
        return self.send_interactive_card(receive_id, receive_id_type, card, uuid)
    
    def send_flight_deal_card(self, receive_id: str, receive_id_type: str,
                             flight_info: Dict[str, Any],
                             title: str = "✈️ 特价机票发现",
                             uuid: Optional[str] = None) -> Dict[str, Any]:
        """发送机票特价卡片"""
        card = build_flight_deal_card(flight_info, title)
        return self.send_interactive_card(receive_id, receive_id_type, card, uuid)
    
    def send_system_status_card(self, receive_id: str, receive_id_type: str,
                               status: str, details: Dict[str, str],
                               title: str = "🖥️ 系统状态",
                               uuid: Optional[str] = None) -> Dict[str, Any]:
        """发送系统状态卡片"""
        from feishu_card_templates import build_system_status_card
        card = build_system_status_card(status, details, title)
        return self.send_interactive_card(receive_id, receive_id_type, card, uuid)
    
    def send_task_management_card(self, receive_id: str, receive_id_type: str,
                                tasks: List[Dict[str, Any]],
                                title: str = "📋 任务管理",
                                uuid: Optional[str] = None) -> Dict[str, Any]:
        """发送任务管理卡片"""
        from feishu_card_templates import build_task_management_card
        card = build_task_management_card(tasks, title)
        return self.send_interactive_card(receive_id, receive_id_type, card, uuid)
    
    def send_interactive_card_with_buttons(self, receive_id: str, receive_id_type: str,
                                         title: str, content: str,
                                         buttons: List[Dict[str, str]],
                                         template: str = "blue",
                                         uuid: Optional[str] = None) -> Dict[str, Any]:
        """发送带按钮的交互式卡片"""
        from feishu_card_templates import build_interactive_card
        card = build_interactive_card(title, content, buttons, template)
        return self.send_interactive_card(receive_id, receive_id_type, card, uuid)

def main():
    """测试函数"""
    # 从环境变量获取配置
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        print("请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量")
        return
    
    sender = AdvancedFeishuCardSender(app_id, app_secret)
    
    # 测试不同类型的卡片
    test_cases = [
        {
            "name": "简单卡片",
            "func": lambda: sender.send_simple_card(
                receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",
                receive_id_type="open_id",
                title="🎯 测试卡片",
                content="这是一个**测试卡片**，用于验证飞书interactive卡片发送功能！"
            )
        },
        {
            "name": "新闻简报",
            "func": lambda: sender.send_news_card(
                receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",
                receive_id_type="open_id",
                news_items=[
                    {
                        "category": "国际新闻",
                        "title": "重大科技突破",
                        "source": "路透社",
                        "time": "2024-02-28 15:30"
                    },
                    {
                        "category": "财经动态",
                        "title": "市场分析报告",
                        "source": "财经网",
                        "time": "2024-02-28 14:20"
                    }
                ]
            )
        },
        {
            "name": "机票特价",
            "func": lambda: sender.send_flight_deal_card(
                receive_id="ou_7a6d94f4f20cf166aa429d75fe09cc95",
                receive_id_type="open_id",
                flight_info={
                    "route": "上海 → 东京",
                    "price": 899,
                    "original_price": 2500,
                    "date": "2024-03-15",
                    "discount": "3.6折",
                    "valid_until": "2024-03-01",
                    "book_advance": 30,
                    "refund_policy": "可免费改期一次",
                    "booking_url": "https://example.com/book",
                    "detail_url": "https://example.com/detail"
                }
            )
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"正在测试 {test_case['name']}...")
            result = test_case["func"]()
            print(f"✅ {test_case['name']} 发送成功！消息ID: {result['message_id']}")
            
        except Exception as e:
            print(f"❌ {test_case['name']} 发送失败: {e}")
            
        print("-" * 50)

if __name__ == "__main__":
    main()