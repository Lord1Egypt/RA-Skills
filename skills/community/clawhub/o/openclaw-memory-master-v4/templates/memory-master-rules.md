# 记忆系统规则 - memory-master v2.6.0

> ⚠️ v2.6.0 架构变更：规则已优化整合到 AGENTS.md

## v2.6.0 架构变更

**核心文件重新组织：**

| 文件 | 变更 | 新用途 |
|------|------|--------|
| **AGENTS.md** | 优化整合 | 行为准则 + 记忆系统规则（已去重、精简） |
| **MEMORY.md** | 功能转换 | 纯重要教训/经验记录（非操作规则） |
| **HEARTBEAT.md** | 独立迁移 | 心跳检测任务和指南（从AGENTS.md分离） |

## 完整文件位置

| 文件 | 用途 |
|---|---|
| AGENTS.md | 行为准则 + 记忆系统规则（优化整合版） |
| MEMORY.md | 重要教训/经验记录（纯教训库） |
| HEARTBEAT.md | 心跳任务和指南（可空） |
| memory/daily/ | 每日记录（YYYY-MM-DD.md格式） |
| memory/daily-index.md | 记忆索引（主题→日期映射） |
| memory/knowledge/ | 知识库（*.md文件） |
| memory/knowledge-index.md | 知识索引（关键字列表） |

## 格式规范

### 记忆格式（每日记录）
```
## [日期] 主题
- 因：原因/背景
- 改：做了什么
- 待：待办/后续
```

### 索引格式
- **记忆索引**：`- 主题 → daily/日期.md,日期.md`
- **知识库索引**：关键字列表（一行一个）

## 初始化流程

使用 `clawdhub init memory-master` 自动完成：

1. **备份** → 原始文件保存到 `.memory-master-backup/`
2. **心跳迁移** → AGENTS.md心跳内容移到HEARTBEAT.md
3. **AGENTS优化** → 去重、精简、重构
4. **MEMORY转换** → 转为纯教训库
5. **结构创建** → 创建memory目录和索引文件

## 兼容性说明

- **v2.5.x → v2.6.0**：自动迁移，无需手动修改
- **新安装**：直接获得优化整合的完整系统
- **回滚**：使用备份目录 `.memory-master-backup/` 恢复
