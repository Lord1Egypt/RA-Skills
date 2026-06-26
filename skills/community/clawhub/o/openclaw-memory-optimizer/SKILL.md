---
name: openclaw-memory-optimizer
description: 自动优化 OpenClaw 4.2 记忆搜索参数。当用户提到记忆不准确、搜索结果太少、MMR 关闭、时间衰减未启用、session 同步阈值过高，或者要求优化 OpenClaw 记忆系统时触发。也用于定期检查和调整 memory-search 配置。
---

# OpenClaw Memory Optimizer

优化 OpenClaw 4.2 内置记忆搜索系统的参数配置，提升记忆检索精度。

## 快速诊断

运行以下命令检查当前配置：

```bash
openclaw config get agents.defaults.memorySearch 2>/dev/null || echo "未设置"
cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; c=json.load(sys.stdin); print(json.dumps(c.get('agents',{}).get('defaults',{}).get('memorySearch',{}), indent=2))"
```

## 核心参数（OpenClaw 当前保守默认值）

| 参数 | 默认值 | 问题 | 推荐值 |
|------|--------|------|--------|
| `maxResults` | 6 | 结果太少 | 10–15 |
| `minScore` | 0.35 | 过于宽松 | 0.25 |
| `mmr.enabled` | false | MMR 可提升多样性 | true |
| `mmr.lambda` | 0.7 | — | 0.6 |
| `temporalDecay.enabled` | false | 旧记忆权重过高 | true |
| `temporalDecay.halfLifeDays` | 30 | — | 14 |
| `sessionDeltaMessages` | 50 | 同步太慢 | 15 |
| `sessionDeltaBytes` | 100KB | 阈值过高 | 20KB |

详见 [references/defaults.md](references/defaults.md)

## 优化流程

### 1. 扫描当前配置

读取 `~/.openclaw/openclaw.json`，找到 `agents.defaults.memorySearch` 节。

### 2. 选择优化级别

**轻度优化**（保守，推荐首次使用）：
```json
{
  "memorySearch": {
    "maxResults": 10,
    "minScore": 0.30,
    "sessionDeltaMessages": 25,
    "sessionDeltaBytes": 50000
  }
}
```

**中度优化**（平衡精度与召回）：
```json
{
  "memorySearch": {
    "maxResults": 12,
    "minScore": 0.25,
    "mmr": { "enabled": true, "lambda": 0.65 },
    "temporalDecay": { "enabled": true, "halfLifeDays": 14 },
    "sessionDeltaMessages": 15,
    "sessionDeltaBytes": 30000
  }
}
```

**深度优化**（高精度）：
```json
{
  "memorySearch": {
    "maxResults": 15,
    "minScore": 0.20,
    "mmr": { "enabled": true, "lambda": 0.60 },
    "temporalDecay": { "enabled": true, "halfLifeDays": 7 },
    "sessionDeltaMessages": 10,
    "sessionDeltaBytes": 20000,
    "experimental": { "sessionMemory": true }
  }
}
```

### 3. 应用配置

```bash
openclaw config set agents.defaults.memorySearch.maxResults 12
openclaw config set agents.defaults.memorySearch.mmr.enabled true
# ... 逐条设置
```

或直接编辑 `~/.openclaw/openclaw.json` 的 `agents.defaults.memorySearch` 节。

### 4. 验证

```bash
openclaw memory status --deep
openclaw doctor --memory-search
```

## Feature Flag 快速开关

通过环境变量快速切换（无需重启 Gateway）：

```bash
# 启用 MMR
OPENCLAW_MEMORY_MMR=true openclaw gateway restart

# 启用时间衰减
OPENCLAW_MEMORY_TEMPORAL_DECAY=true openclaw gateway restart
```

## 何时使用轻度 vs 深度

- **轻度**：个人项目、短期任务、上下文简单
- **中度**：多模块项目、有多位协作者
- **深度**：大型代码库、长期维护、需要高精度记忆
