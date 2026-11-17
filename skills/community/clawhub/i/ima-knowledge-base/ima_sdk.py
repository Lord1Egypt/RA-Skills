#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA 知识库 OpenAPI SDK
腾讯 IMA 智能知识库 API 封装
"""

import requests
import json
from typing import Optional, Dict, List, Any

class IMAKnowledgeBase:
    """IMA 知识库客户端"""
    
    BASE_URL = "https://ima.qq.com/openapi"
    
    def __init__(self, client_id: str, api_key: str):
        self.client_id = client_id
        self.api_key = api_key
        self.session = requests.Session()
    
    def _headers(self) -> Dict[str, str]:
        return {
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def _request(self, endpoint: str, payload: Dict) -> Dict:
        """发送请求"""
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.post(url, headers=self._headers(), json=payload)
        try:
            return response.json()
        except:
            return {"code": -1, "msg": response.text, "data": {}}
    
    def create_note(self, content: str, title: str = "", content_format: int = 1) -> Dict:
        """
        创建笔记
        
        Args:
            content: 笔记内容
            title: 笔记标题
            content_format: 1-Markdown, 2-HTML, 3-纯文本
        
        Returns:
            {"code":0, "msg":"success", "data":{"note_id":"..."}}
        """
        payload = {
            "content": content,
            "content_format": content_format
        }
        if title:
            payload["title"] = title
        return self._request("/note/v1/import_doc", payload)
    
    def get_note(self, note_id: str) -> Dict:
        """
        获取笔记内容
        
        Args:
            note_id: 笔记ID
        
        Returns:
            {"code":0, "msg":"success", "data":{"content":"..."}}
        """
        return self._request("/note/v1/get_doc_content", {"doc_id": note_id})
    
    def append_note(self, note_id: str, content: str, content_format: int = 1) -> Dict:
        """
        追加内容到笔记
        
        Args:
            note_id: 笔记ID
            content: 要追加的内容
            content_format: 1-Markdown, 2-HTML, 3-纯文本
        """
        payload = {
            "doc_id": note_id,
            "content": content,
            "content_format": content_format
        }
        return self._request("/note/v1/append_doc", payload)
    
    def save_to_knowledge_base(self, title: str, content: str, tags: List[str] = None) -> str:
        """
        保存内容到知识库，自动添加元数据
        
        Args:
            title: 标题
            content: 内容
            tags: 标签列表
        
        Returns:
            note_id: 创建的笔记ID
        """
        # 添加元数据
        full_content = f"# {title}\n\n"
        if tags:
            full_content += f"**标签**: {', '.join(tags)}\n\n"
        full_content += content
        
        result = self.create_note(full_content, title=title)
        if result.get("code") == 0:
            return result["data"].get("note_id", "")
        return ""
    
    def create_summary_note(self, topic: str, summary: str, details: str = "") -> str:
        """
        创建摘要笔记
        
        Args:
            topic: 主题
            summary: 摘要
            details: 详细内容
        
        Returns:
            note_id
        """
        content = f"# {topic}\n\n"
        content += "## 摘要\n\n"
        content += f"{summary}\n\n"
        if details:
            content += "## 详情\n\n"
            content += f"{details}\n\n"
        
        result = self.create_note(content, title=f"[摘要] {topic}")
        return result["data"].get("note_id", "") if result.get("code") == 0 else ""


if __name__ == "__main__":
    # 测试代码
    import os
    
    client_id = os.getenv("IMA_CLIENT_ID", "")
    api_key = os.getenv("IMA_API_KEY", "")
    
    if not client_id or not api_key:
        print("请设置环境变量 IMA_CLIENT_ID 和 IMA_API_KEY")
        exit(1)
    
    ima = IMAKnowledgeBase(client_id, api_key)
    
    # 测试创建
    print("创建测试笔记...")
    result = ima.create_note("# SDK测试\n\n这是SDK测试内容。", title="SDK测试笔记")
    print(f"结果: {result}")
    
    if result.get("code") == 0:
        note_id = result["data"]["note_id"]
        print(f"创建成功: {note_id}")
        
        # 测试读取
        print("\n读取笔记...")
        note = ima.get_note(note_id)
        print(f"内容: {note}")
        
        # 测试追加
        print("\n追加内容...")
        append_result = ima.append_note(note_id, "\n\n---\n*追加的内容*")
        print(f"结果: {append_result}")
