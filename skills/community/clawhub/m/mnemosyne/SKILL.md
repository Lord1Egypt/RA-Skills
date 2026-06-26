---
name: auto-memory
description: >
  智能记忆系统：支持用户自定义记忆类别、AI自动分析触发、记忆冲突解决。
  当用户需要持久记忆跨会话信息、设定记忆规则、自动记忆重要内容、或解决记忆冲突时使用此技能。
  支持L1/L2/L3三层记忆分层、JSON快速索引搜索、用户自定义记忆类别、自动分析触发、冲突时以用户为准。
  详细文档见 README.md
version: 1.0.0
readme: README.md
---

# Auto Memory - 智能记忆系统 v2.0

**全自动记忆：不需要用户说任何触发词，安装即自动运行**

---

## 一句话说明

> 安装后全自动运行：每次会话结束自动记忆，boss 不需要说任何触发词。

---

## 自动触发机制（核心）

### 会话级自动记忆（完全自动）

**不需要 boss 说任何话**，系统在以下时机自动触发：

1. **每次会话结束前** → 自动调用 `auto_session` 分析整段对话并记忆
2. **新会话开始时** → 自动加载已有记忆到上下文
3. **HEARTBEAT 定时** → 每日自动整理记忆

### 自动捕捉的内容（无需触发词）

| 内容类型 | 自动触发条件 | 类别 |
|---------|------------|------|
| boss 决策 | 任何决定性表述 | `boss_decision` |
| boss 偏好 | 任何喜欢/不喜欢表达 | `boss_preference` |
| 偏好变化 | 发现"之前A现在B" | `boss_preference_change` |
| boss 情绪 | 任何情绪/心情表达 | `boss_emotion` |
| boss 评价 | 任何看法/评价 | `boss_evaluation` |
| 任务进展 | 任务完成/变化 | `work_context` |
| 数字/日期 | 重要数字出现3次+ | `work_context` |
| 偏好冲突 | 与旧记忆矛盾 | **自动更新** |

---

## 接入 AGENTS.md（自动触发）

**安装此 skill 后，在 AGENTS.md 中加入以下规则：**

```markdown
## 记忆加载（每次会话开始）
每次会话开始：
1. 读 MEMORY.md（核心长期记忆）
2. 读 ~/.openclaw/workspace/skills/auto-memory/memory/index.json（记忆索引）
3. 搜索最近相关记忆：memory_cli.sh recent 10

## 记忆自动触发（每次会话结束）
每次会话结束：
1. 整理本会话 boss 说过的所有内容
2. 调用 auto_session 整段分析：
   cd ~/.openclaw/workspace/skills/auto-memory/scripts && bash memory_cli.sh auto_session "本会话所有对话内容"
3. 检查冲突：如有新内容与旧记忆矛盾，以 boss 最新说的为准
4. 更新 memory/index.json 索引

## 冲突解决
如果 boss 说的和记忆矛盾：
→ 以 boss 最新说的为准
→ 自动更新记忆
→ 旧记忆备份到 conflict/
```

---

## 在 HEARTBEAT 中集成

在 HEARTBEAT.md 中加入：

```markdown
## 记忆维护（每天）
- 运行：memory_cli.sh auto_session 整理今日对话
- 检查：memory_cli.sh stats 查看记忆统计
- 清理：删除 temporary/ 中7天前的文件

## 每周记忆整理（周一）
- 读过去7天 memory/current/*.md
- 更新 MEMORY.md 重要内容
- 运行：memory_cli.sh dedup 去重
```

---

## CLI 命令

```bash
cd ~/.openclaw/workspace/skills/auto-memory/scripts

# 会话级自动记忆（推荐，会自动分析并记忆所有重要内容）
bash memory_cli.sh auto_session "本会话所有对话内容"

# 手动记忆
bash memory_cli.sh capture "内容" --type boss_preference --importance 8

# 搜索
bash memory_cli.sh search "关键词"

# 统计
bash memory_cli.sh stats

# 最近记忆
bash memory_cli.sh recent 10

# AI 分析（查看分析结果，不自动记忆）
bash memory_cli.sh auto_analyze "对话内容"
```

---

## 记忆类别

| 类别 | 层级 | 说明 |
|------|------|------|
| `boss_info` | permanent | boss 基本信息 |
| `boss_decision` | permanent | 重要决策 |
| `boss_preference` | permanent | 个人偏好 |
| `boss_preference_change` | permanent | 偏好变化 |
| `boss_emotion` | current | 情绪状态 |
| `boss_negative` | current | 负面情绪 |
| `work_context` | current | 工作上下文 |
| `learning` | current | 学到的新知识 |
| `boss_evaluation` | current | 对某事的评价 |
| `error_recovery` | permanent | 错误与恢复 |

---

## 用户自定义类别

```bash
# 添加自定义类别
bash memory_cli.sh config add_type "投资记录" "boss 的投资持仓"

# 调整默认层级
bash memory_cli.sh config set_tier 投资记录 permanent
```

---

## 完整文档

见 `README.md`
