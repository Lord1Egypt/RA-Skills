---
name: "秒秒AI助理"
description: "调用秒秒AI多能力智能体，支持聊天、天气、新闻、快递、图像生成、搜索、总结、图表、地图、车票查询等功能。Invoke when user needs AI assistant with multiple practical functions or mentions related keywords."
---

# 秒秒AI助理 多能力智能体技能

## 功能说明
本技能提供丰富的AI能力集合，通过意图识别自动触发对应功能：
- 智能聊天对话
- 天气查询
- 新闻早报
- 快递查询
- 图像生成
- 网页搜索
- 内容总结
- 可视化图表生成
- 地图查询
- 12306车票查询

## 配置要求
1. 在项目根目录创建`.env`文件
2. 配置以下环境变量：

   - `LINKAI_API_KEY`: 你的Link-AI API密钥

## 使用方法
当用户需要以下服务时自动调用本技能：
- 普通聊天对话
- 查询天气
- 获取新闻资讯
- 查询快递进度
- 生成图片
- 搜索网页内容
- 总结长文本/文档
- 生成数据图表
- 查询地点/路线
- 查询火车票信息

## 调用示例
```python
import os
import http.client
import json
from dotenv import load_dotenv

load_dotenv()

conn = http.client.HTTPSConnection("api.link-ai.tech")
payload = json.dumps({
    "app_code": os.getenv("LINKAI_APP_CODE"),
    "messages": [
        {
            "role": "user",
            "content": "查询北京今天天气"
        }
    ]
})
headers = {
    'Authorization': f'Bearer {os.getenv("LINKAI_API_KEY")}',
    'Content-Type': 'application/json'
}
conn.request("POST", "/v1/chat/completions", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```
