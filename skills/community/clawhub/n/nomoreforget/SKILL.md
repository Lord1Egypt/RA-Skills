---
name: no-more-forget
description: 让 OpenClaw 不再失忆！一键解决记忆问题：失忆、Token 消耗高、搜不到。自动启用 Memory Flush、优化记忆配置、提供诊断备份工具。触发词：龙虾失忆、记忆问题、Token 消耗高、记忆配置、memory 问题、记不住。
---

# No More Forget - 让 OpenClaw 不再失忆

一键解决 OpenClaw 原生记忆层的三大痛点：**失忆**、**Token 烧钱**、**搜不到**。

## 快速开始

```bash
# 一键安装所有优化
bash scripts/install.sh

# 验证安装
bash scripts/verify.sh
```

安装完成后自动获得：
- ✅ Memory Flush 自动开启，压缩前自动保存关键记忆
- ✅ 优化的 MEMORY.md 模板
- ✅ 记忆维护自动化脚本
- ✅ Token 消耗降低策略

---

## 核心问题与解决方案

### 问题 1：龙虾失忆

**原因**：Compaction 压缩时丢失关键约束

**解决方案**：启用 Memory Flush

```bash
# 自动配置
bash scripts/install.sh
```

**手动配置**（~/.openclaw/openclaw.json）：
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 40000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```

### 问题 2：Token 消耗过高

**原因**：全量加载 today+yesterday+长期记忆

**解决方案**：
1. 精简 MEMORY.md（保持在 500 行以内）
2. 定期清理 daily logs
3. 关键信息放在文件开头/结尾

```bash
# 一键优化记忆文件
bash scripts/optimize_memory.sh
```

### 问题 3：记忆搜不到

**原因**：原生 SQLite 搜索无语义理解

**解决方案**：
- **方案 A**：安装 qmd 插件（推荐）
- **方案 B**：优化原生搜索配置

```bash
# 安装 qmd 搜索增强
clawhub install qmd
```

---

## 记忆文件最佳实践

### MEMORY.md 结构

```markdown
# MEMORY.md — 长期记忆

## 用户信息
- Name: xxx
- Preferences: xxx

## 活跃项目
- 项目名: 状态 + 关键决策

## 关键决策
| Date | Decision | Reason |
|------|----------|--------|
| YYYY-MM-DD | 决策内容 | 原因 |

## 经验教训
| Date | Lesson | Source |
|------|--------|--------|

## 安全规则
**永不存储**：API keys, passwords, 私密信息
```

> ⚠️ **重要**：MEMORY.md 开头和结尾最重要，中间部分在压缩时容易丢失！

### Daily Logs 规范

- 自动追加，无需手动维护
- 每周精炼一次，提取关键规则到 MEMORY.md
- 超过 30 天的日志可归档

---

## 自动维护脚本

### 记忆诊断

```bash
# 一键诊断记忆问题
bash scripts/diagnose.sh
```

### 记忆备份

```bash
# 备份记忆
bash scripts/backup_memory.sh

# 恢复记忆
bash scripts/restore_memory.sh
```

---

## 诊断清单

龙虾失忆时，依次检查：

- [ ] `memoryFlush.enabled: true` 是否开启
- [ ] MEMORY.md 开头是否包含最关键信息
- [ ] daily log 是否过于臃肿
- [ ] 上下文是否超出限制

```bash
# 一键诊断
bash scripts/diagnose.sh
```

---

## 插件生态（可选增强）

| 插件 | 解决问题 | 安装命令 |
|------|---------|---------|
| **qmd** | 搜不到 | `clawhub install qmd` |
| **lossless-claw** | 压缩丢失 | `clawhub install lossless-claw` |

**推荐组合**：qmd + lossless-claw（作者推荐）

---

## 参考文档

- [记忆架构详解](references/architecture.md) - 双源记忆系统原理
- [插件生态对比](references/plugins.md) - 7 大记忆插件详细对比
- [问题排查指南](references/troubleshooting.md) - 常见问题诊断流程

---

## 模板文件

- `assets/MEMORY.md.template` - 优化的记忆模板
- `assets/daily-log.template.md` - 日志模板