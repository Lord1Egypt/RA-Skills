# MiMo 联网搜索技能使用说明

## 同事使用指南

### 1. 安装技能
```bash
# 将技能文件夹复制到 OpenClaw 技能目录
cp -r mimo-web-search ~/.openclaw/skills/
```

### 2. 配置 API Key
在 OpenClaw 配置文件中添加：
```bash
# 编辑 ~/.openclaw/config.env
MIMO_API_KEY=sk-your-api-key-here
```

### 3. 在代码中使用
```javascript
// 引入技能
const { mimoWebSearch, searchAndFormat } = require('mimo-web-search');

// 基本搜索
const result = await mimoWebSearch('MiMo-V2-Flash 的基准测试结果是什么？');

// 格式化搜索
const formatted = await searchAndFormat('2026 年 AI 大模型最新进展');
```

### 4. 在 OpenClaw 中使用
```javascript
// 在 OpenClaw 会话中调用
const command = `curl -X POST "https://api.xiaomimimo.com/v1/chat/completions" \
  -H "api-key: $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '${JSON.stringify({
    model: "mimo-v2-flash",
    messages: [{ role: "user", content: "你的搜索查询" }],
    tools: [{ type: "web_search", max_keyword: 3, force_search: true, limit: 1 }],
    max_completion_tokens: 1024,
    temperature: 1.0,
    top_p: 0.95,
    stream: false,
    thinking: { type: "disabled" }
  })}'`;

exec(command);
```

## 常见问题

### Q: 如何获取 API Key？
A: 访问小米 MiMo 开放平台，注册并获取 API Key。

### Q: 联网搜索功能收费吗？
A: 是的，中国区 ¥25 / 1K 次请求。

### Q: 支持哪些模型？
A: mimo-v2-pro, mimo-v2-omni, mimo-v2-flash。

### Q: 搜索结果包含来源吗？
A: 是的，搜索结果会包含来源链接（citation）。

## 最佳实践
1. **合理使用**: 联网搜索功能需要付费，避免不必要的调用
2. **缓存结果**: 对于重复查询，考虑缓存搜索结果
3. **错误处理**: 始终处理 API 调用失败的情况
4. **日志记录**: 记录搜索查询和结果，便于调试和分析