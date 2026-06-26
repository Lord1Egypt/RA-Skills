"""
知识库连接示例 - Python 版本
Knowledge Chat v1.1

支持：
- 文本对话
- 图片理解（多模态）
- 文档解析
"""

import requests
import base64
import json
from pathlib import Path

class KnowledgeChatConnector:
    """知识库对话连接器"""
    
    def __init__(self, api_key: str, endpoint: str = "https://dashscope.aliyuncs.com/api/v1"):
        self.api_key = api_key
        self.endpoint = endpoint
    
    def chat(self, query: str, knowledge_context: str = None) -> str:
        """文本对话"""
        messages = [
            {"role": "system", "content": f"你是一个专业的学习助手，名叫小新。\n\n【知识库内容】\n{knowledge_context}" if knowledge_context else "你是小新，专业的学习助手。"},
            {"role": "user", "content": query}
        ]
        
        response = requests.post(
            f"{self.endpoint}/services/aigc/text-generation/generation",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "model": "qwen-plus",
                "input": {"messages": messages},
                "parameters": {
                    "temperature": 0.3,
                    "max_tokens": 4000,
                    "result_format": "message"
                }
            }
        )
        
        data = response.json()
        return data["output"]["choices"][0]["message"]["content"]
    
    def chat_with_image(self, query: str, image_path: str) -> str:
        """图片理解（多模态）"""
        # 读取图片转 base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        
        # 判断图片类型
        ext = Path(image_path).suffix.lower()
        mime_type = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif"
        }.get(ext, "image/jpeg")
        
        messages = [
            {"role": "user", "content": [
                {"image": f"data:{mime_type};base64,{image_data}"},
                {"text": query}
            ]}
        ]
        
        response = requests.post(
            f"{self.endpoint}/services/aigc/multimodal-generation/generation",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "X-DashScope-Synchronous": "true"
            },
            json={
                "model": "qwen-vl-max",
                "input": {"messages": messages},
                "parameters": {
                    "top_k": 50,
                    "top_p": 0.9,
                    "temperature": 0.3,
                    "max_length": 4000
                }
            }
        )
        
        data = response.json()
        content = data["output"]["choices"][0]["message"]["content"]
        
        # 解析多模态返回
        if isinstance(content, list):
            return content[0].get("text", "")
        return content
    
    def search_knowledge(self, query: str, knowledge_files: list) -> str:
        """知识库搜索（简单关键词匹配）"""
        results = []
        for file_path in knowledge_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append({
                        "file": Path(file_path).name,
                        "snippet": content[:500]
                    })
        
        if results:
            return "\n\n".join([f"📚 {r['file']}:\n{r['snippet']}" for r in results])
        return "未找到相关信息"


# 使用示例
if __name__ == "__main__":
    connector = KnowledgeChatConnector(api_key="your-api-key")
    
    # 文本对话
    answer = connector.chat("什么是 CRM？", knowledge_context="CRM是客户关系管理...")
    print(answer)
    
    # 图片理解
    answer = connector.chat_with_image("分析这张图表", "chart.png")
    print(answer)