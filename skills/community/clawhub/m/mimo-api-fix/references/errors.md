# mimo API 错误参考

## 错误码对照

| HTTP | 错误信息 | 含义 | 修复 |
|------|---------|------|------|
| 400 | `Param Incorrect` | 请求参数格式不被 API 接受 | 检查 tools 格式、model 名称、maxTokens |
| 400 | `model_not_found` | 模型名不存在 | 检查 `/models` 端点确认可用模型 |
| 401 | `Invalid token` | API key 无效 | 检查配置中的 apiKey |
| 429 | Rate limit | 请求频率过高 | 等待后重试 |

## OpenClaw 日志关键词

```
# 搜索错误
grep -i "mimo" /tmp/openclaw/openclaw-*.log | grep -i "error\|fail\|400\|schema\|format"

# 搜索 fallback 决策
grep "model_fallback_decision" /tmp/openclaw/openclaw-*.log | grep mimo

# 搜索配置变更
grep "config.*reload\|hot.*reload" /tmp/openclaw/openclaw-*.log | tail -5
```

## 已知竞态条件触发场景

**场景**：修改 `openclaw.json` 中 `agents.defaults.model.primary` 字段

**过程**：
1. 配置文件被修改
2. Gateway 检测到变更，开始热加载
3. 热加载期间有请求在处理
4. 请求使用旧配置（包含 tools）但模型路由已更新
5. API 返回 400

**预防**：修改配置后等待 2-3 秒再发消息，或使用 `openclaw gateway restart` 确保干净加载。
