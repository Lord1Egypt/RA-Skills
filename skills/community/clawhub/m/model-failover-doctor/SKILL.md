# model-failover-doctor

诊断和修复 OpenClaw "All models failed" 错误的专用工具。

## 触发条件

遇到以下任何一种情况时，调用此工具：

1. **日志或用户报告** `All models failed (N)`，且 N 个 provider 的错误信息中 model ID 全部相同
   - 例：`kimi-coding/k2p5: No available channel for model openai/gpt-5.3-codex` ← provider 和 model 对不上
2. **agent 重启后第一条消息必然失败**，但后续消息正常（冷启动 session 无 fallbackChain）
3. **pools.json 或 session_model_state.json 手动编辑后** agent 开始报 503 model_not_found

## 诊断命令

```bash
# 仅诊断，不修改任何文件
python3 ~/.openclaw/workspace/skills/model-failover-doctor/model_failover_doctor.py

# 诊断 + 自动修复 + 重启 gateway
python3 ~/.openclaw/workspace/skills/model-failover-doctor/model_failover_doctor.py --fix --restart

# 预览将要修改的内容（不实际写入）
python3 ~/.openclaw/workspace/skills/model-failover-doctor/model_failover_doctor.py --dry-run
```

## 根因速查表

| 症状 | 代码 | 严重 | 自动修复 |
|------|------|------|----------|
| 所有 fallback 的 model ID 相同（provider 已切换但 model 没变） | MI-1 | 🔴 | ✅ |
| 同一死亡模型被不同 session/子代理反复踩坑 | MI-2 | 🟡 | ❌ 需手动 |
| pools.json 中引用了不存在的 provider | P-1 | 🔴 | ✅ |
| session 无 fallbackChain，runtime fallback 永远无法推进 | S-1 | 🔴 | ✅ |
| session fallbackChain 含无效 provider 前缀 | S-2 | 🔴 | ✅ |

## 根因 MI-1 详解（最常见）

**问题**：`message-injector` 的 `before_agent_start` 无条件返回：
```typescript
return { modelOverride, providerOverride, ... }
```

**后果**：Gateway 尝试每个 fallback 时都携带相同的 `modelOverride`，
导致 `kimi-coding`、`zai`、`minimax` 等收到了错误的 model ID。

**修复**：包装在 `lockModel` 条件中，正常路由只依赖 `sessions.patch`：
```typescript
return { ...(lockModel ? { modelOverride, providerOverride } : {}), ... }
```

## 备份说明

所有自动修复操作会在 `~/.openclaw/workspace/.lib/.mfd_backups/` 创建时间戳备份，
可随时手动恢复。
