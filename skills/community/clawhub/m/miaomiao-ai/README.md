# 秒秒AI助理 多能力智能体技能

## 概述
秒秒AI助理是一个集成了多种实用功能的AI智能体技能，通过统一的API接口调用，自动识别用户意图并提供对应的服务。

## 功能清单
| 功能 | 描述 | 触发关键词 |
|------|------|-----------|
| 智能聊天 | 日常对话、问题解答 | 任意问题、聊天 |
| 天气查询 | 查询全球各地实时天气 | 天气、气温、降水 |
| 新闻早报 | 获取每日最新资讯 | 新闻、早报、资讯 |
| 快递查询 | 追踪快递物流进度 | 快递、物流、包裹 |
| 图像生成 | 根据描述生成AI图片 | 生成图片、画图、AI绘图 |
| 网页搜索 | 搜索互联网最新信息 | 搜索、查找、百度一下 |
| 内容总结 | 总结长文本/文章/文档 | 总结、概括、摘要 |
| 图表生成 | 生成各类可视化数据图表 | 图表、柱状图、折线图、饼图 |
| 地图查询 | 地点搜索、路线规划 | 地图、位置、路线、导航 |
| 车票查询 | 12306火车票余票查询 | 火车票、车票、12306 |

## 快速开始

### 1. 安装依赖
```bash
pip install python-dotenv
```

### 2. 配置环境变量
在项目根目录创建`.env`文件，填入你的Link-AI凭证：
```env
LINKAI_APP_CODE=你的应用编码
LINKAI_API_KEY=你的API密钥
```

### 3. 调用示例
```python
from linkai_client import LinkAIClient

# 初始化客户端
client = LinkAIClient()

# 发送请求
response = client.chat("查询上海明天天气")
print(response)
```

## API文档
### 接口地址
`POST https://api.link-ai.tech/v1/chat/completions`

### 请求参数
| 参数 | 类型 | 必选 | 描述 |
|------|------|------|------|
| app_code | string | 是 | 应用编码 |
| messages | array | 是 | 对话消息列表 |
| stream | boolean | 否 | 是否启用流式响应，默认false |

### 响应格式
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1710000000,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "上海明天晴，气温15-22℃，微风。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 23,
    "total_tokens": 35
  }
}
```

## 目录结构
```
秒秒AI助理/
├── SKILL.md          # 技能定义文件
├── README.md         # 本说明文档
├── .env.example      # 环境变量示例
├── tools/            # 工具代码目录
│   ├── miaomiao_client.py  # 客户端SDK
│   └── examples.py       # 更多示例代码
└── docs/             # 额外文档（可选）
```

## 常见问题
### Q: 如何获取APP_CODE和API_KEY？
A: 登录Link-AI平台(https://link-ai.tech)，在应用管理中创建应用即可获取。

### Q: 支持流式响应吗？
A: 支持，设置`stream: true`即可接收SSE格式的流式响应。

### Q: 有请求频率限制吗？
A: 免费版限制为100次/天，付费版可提升配额。

## 更新日志
### v1.0.0 (2026-03-12)
- 初始版本发布
- 支持10项核心功能
- 提供Python SDK
