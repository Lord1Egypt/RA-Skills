# MiMo 联网搜索技能

## 描述
使用小米 MiMo 模型的联网搜索功能进行实时信息搜索。

## 触发条件
- 用户要求搜索实时信息、最新动态或资料核对
- 用户提到 "搜索"、"查找"、"查询" 等关键词
- 需要获取最新网络信息时

## 工具
- `exec`: 调用 MiMo 联网搜索 API

## 配置要求
1. **API Key**: 需要配置 `MIMO_API_KEY` 环境变量
2. **模型支持**: mimo-v2-pro, mimo-v2-omni, mimo-v2-flash
3. **计费**: 中国区 ¥25 / 1K 次请求

## 使用方法

### 1. 配置 API Key
```bash
# 在 OpenClaw 配置文件中添加
MIMO_API_KEY=sk-your-api-key-here
```

### 2. 调用联网搜索 API
```bash
curl -X POST "https://api.xiaomimimo.com/v1/chat/completions" \
  -H "api-key: $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2-flash",
    "messages": [
      {
        "role": "user",
        "content": "你的搜索查询内容"
      }
    ],
    "tools": [
      {
        "type": "web_search",
        "max_keyword": 3,
        "force_search": true,
        "limit": 1
      }
    ],
    "max_completion_tokens": 1024,
    "temperature": 1.0,
    "top_p": 0.95,
    "stream": false,
    "thinking": {
      "type": "disabled"
    }
  }'
```

### 3. 在 OpenClaw 中使用
```javascript
// 使用 exec 工具调用 MiMo 联网搜索
const command = `curl -X POST "https://api.xiaomimimo.com/v1/chat/completions" \
  -H "api-key: $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '${JSON.stringify({
    model: "mimo-v2-flash",
    messages: [{ role: "user", content: query }],
    tools: [{ type: "web_search", max_keyword: 3, force_search: true, limit: 1 }],
    max_completion_tokens: 1024,
    temperature: 1.0,
    top_p: 0.95,
    stream: false,
    thinking: { type: "disabled" }
  })}'`;

exec(command);
```

## 示例

### 搜索 MiMo 基准测试
```javascript
const query = "MiMo-V2-Flash 的基准测试结果是什么？";
// 调用 API 获取搜索结果
```

### 搜索最新技术动态
```javascript
const query = "2026 年 AI 大模型最新进展";
// 调用 API 获取搜索结果
```

## 注意事项
1. **API Key 安全**: 不要在代码中硬编码 API Key，使用环境变量
2. **计费控制**: 联网搜索功能需要付费，注意控制调用频率
3. **模型选择**: 确保使用支持联网搜索的模型（mimo-v2-flash 等）
4. **错误处理**: 处理 API 调用失败的情况

## 故障排除
- **401 错误**: API Key 无效或未配置
- **400 错误**: 模型名称错误或参数不正确
- **网络错误**: 检查网络连接和 API 端点