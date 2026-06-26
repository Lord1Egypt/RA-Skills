# MiMo 联网搜索技能使用指南

## 快速开始

### 1. 配置 API Key
在 OpenClaw 配置文件中添加：
```
MIMO_API_KEY=sk-your-api-key-here
```

### 2. 基本使用
```javascript
// 搜索 MiMo 基准测试
const result = await mimoWebSearch("MiMo-V2-Flash 的基准测试结果是什么？");
console.log(result);
```

### 3. 高级用法
```javascript
// 自定义搜索参数
const result = await mimoWebSearch({
  query: "你的搜索内容",
  model: "mimo-v2-flash",
  maxTokens: 2048,
  temperature: 0.7
});
```

## API 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | string | 必填 | 搜索查询内容 |
| model | string | "mimo-v2-flash" | 使用的模型 |
| maxTokens | number | 1024 | 最大生成 token 数 |
| temperature | number | 1.0 | 温度参数 |
| topP | number | 0.95 | 核采样参数 |
| maxKeyword | number | 3 | 最大关键词数 |
| forceSearch | boolean | true | 强制搜索 |
| limit | number | 1 | 搜索结果数量 |

## 计费信息
- **联网搜索调用**: ¥25 / 1K 次请求
- **模型 Token 费用**: 按标准价格计费

## 支持模型
- mimo-v2-pro
- mimo-v2-omni
- mimo-v2-flash

## 示例场景

### 1. 搜索技术文档
```javascript
const result = await mimoWebSearch("Python async/await 最佳实践");
```

### 2. 查找最新新闻
```javascript
const result = await mimoWebSearch("2026 年 AI 行业最新动态");
```

### 3. 学术研究
```javascript
const result = await mimoWebSearch("深度学习注意力机制最新研究");
```

## 故障排除

### API Key 错误
```
错误: 401 Invalid API Key
解决: 检查 MIMO_API_KEY 环境变量是否正确配置
```

### 模型不支持
```
错误: 400 Not supported model
解决: 确保使用支持联网搜索的模型（mimo-v2-flash 等）
```

### 网络错误
```
错误: 网络连接失败
解决: 检查网络连接和 API 端点 (https://api.xiaomimimo.com)
```

## 最佳实践
1. **合理使用**: 联网搜索功能需要付费，避免不必要的调用
2. **缓存结果**: 对于重复查询，考虑缓存搜索结果
3. **错误处理**: 始终处理 API 调用失败的情况
4. **日志记录**: 记录搜索查询和结果，便于调试和分析