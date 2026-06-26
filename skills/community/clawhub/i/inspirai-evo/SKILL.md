---
name: inspirai-evo
description: "技能自我进化 - 检测流程问题信号（重复试错、流程中断、代码翻动），生成分析报告，引导改进。Triggers: '流程优化', '技能进化', 'skill evolution', '自我改进', '流程问题', 'workflow analysis'."
version: 1.0.0
license: MIT
---

# /evo - 技能进化分析

检测工作流中的问题信号（重复试错、流程中断、代码翻动），生成分析报告，并引导在独立 session 中处理改进，不阻塞当前工作。

## 使用方式

```
/evo              # 执行完整分析流程
/evo --status     # 查看当前信号状态
/evo --report     # 仅生成报告，不进入交互
/evo --continue   # 继续处理 pending 改进项（独立 session 使用）
```

## 核心原则

1. **非阻塞** - 分析快速完成，改进在独立 session 处理
2. **阈值触发** - 单类信号达到 3 次才建议分析
3. **双重存储** - 项目内详细报告 + 全局跨项目统计

## 执行步骤

### Step 1: 收集数据

#### 1.1 读取状态文件

```bash
STATE_FILE=".evo-state.json"
if [ -f "$STATE_FILE" ]; then
    echo "[INFO] 读取状态文件..."
    cat "$STATE_FILE" | jq '.'
else
    echo "[INFO] 状态文件不存在，将仅分析 git 历史"
fi
```

#### 1.2 分析 Git 历史

```bash
# 最近 20 个 commit
git log --oneline -20

# 检测高频修改文件
git log --name-only --pretty=format: -20 | sort | uniq -c | sort -rn | head -10

# 检测 revert commits
git log --oneline -50 | grep -i "revert"

# 检测连续 fix commits
git log --oneline -20 | grep -E "^[a-f0-9]+ fix"
```

#### 1.3 汇总数据

收集以下信息：
- 状态文件中的信号计数和实例
- Git 历史中的高频修改文件
- Revert 和连续 fix 的 commit
- 当前 session 中观察到的模式（如果有）

### Step 2: 生成分析报告

#### 2.1 创建报告目录

```bash
REPORT_DIR="docs/evo-reports"
mkdir -p "$REPORT_DIR"
```

#### 2.2 报告文件命名

```bash
REPORT_FILE="$REPORT_DIR/$(date +%Y-%m-%d)-report.md"
```

#### 2.3 报告模板

生成报告包含以下结构：

```markdown
# Evo 分析报告

生成时间：{YYYY-MM-DD HH:mm}
项目：{project-name}

## 发现的问题

### 1. [{signal_type}] {问题标题}
- **出现次数**：{count}
- **时间跨度**：{first_timestamp} - {last_timestamp}
- **上下文**：{context 汇总}
- **模式**：{检测到的模式}
- **关联 Skill**：{相关 skill 名称，如果能识别}
- **建议**：{具体改进建议}

## 改进建议汇总

| 优先级 | 类型 | 建议 | 影响范围 |
|--------|------|------|----------|
| 高/中/低 | 新增/优化/修复 | {建议内容} | {影响的 skill 或配置} |

## 待处理项

- [ ] {改进项 1}
- [ ] {改进项 2}
```

#### 2.4 写入报告

使用收集的数据填充模板，写入报告文件。

### Step 3: 交互确认

展示发现的问题摘要（不超过 5 条），使用 AskUserQuestion 逐条确认：

```
发现 {N} 个流程问题：

1. [retry_loops] TypeScript 编译错误循环 (3次)
2. [interrupted_flows] Debugging 中断未恢复 (2次)

请选择要处理的问题：
- [ ] 问题 1
- [ ] 问题 2
- [ ] 全部处理
- [ ] 暂不处理
```

用户确认后，将选中的问题加入 `pending_improvements`。

### Step 4: 引导独立 Session

若用户确认了需要处理的问题：

```
已记录 {N} 个待处理改进项。

要在独立 session 中处理这些改进，请运行：

    claude "继续处理 evo 改进项"

或稍后运行 /evo --continue

当前 session 可继续其他工作。
```

### Step 5: 更新状态

#### 5.1 更新项目状态文件

```bash
# 重置已分析的信号计数
# 更新 last_analysis 时间戳
# 保留 pending_improvements

jq '.last_analysis = now | .signals.retry_loops.count = 0 | .signals.interrupted_flows.count = 0 | .signals.git_churn.count = 0' .evo-state.json > .evo-state.json.tmp && mv .evo-state.json.tmp .evo-state.json
```

#### 5.2 同步全局统计

```bash
GLOBAL_DIR="$HOME/.claude/evo-stats"
mkdir -p "$GLOBAL_DIR/projects"

# 更新项目统计
PROJECT_NAME=$(basename $(pwd))
cp .evo-state.json "$GLOBAL_DIR/projects/$PROJECT_NAME.json"

# 更新汇总统计
# 累加 pattern_frequency
# 更新 skills_needing_attention
```

## --status 模式

仅显示当前信号状态，不执行分析：

```
Evo 状态检查:

信号状态:
  retry_loops:       2/3 (未达阈值)
  interrupted_flows: 1/3 (未达阈值)
  git_churn:         0/3 (无记录)

上次分析: 2026-01-25 18:00
待处理改进: 0 项

提示: 任一信号达到 3 次将自动建议执行 /evo
```

## --continue 模式

用于独立 session 处理 pending 改进项：

1. 读取 `.evo-state.json` 中的 `pending_improvements`
2. 若无待处理项，提示并退出
3. 逐个展示待处理项：
   - 显示问题详情和建议
   - 分析需要修改的文件
   - 提出具体修改方案
   - 用户确认后执行修改
4. 完成后从 `pending_improvements` 中移除
5. 更新全局统计

```
继续处理 Evo 改进项...

待处理项 1/2:
[retry_loops] TypeScript 编译错误循环

建议: 添加 pre-commit hook 进行类型检查

要执行此改进吗？
- 是，开始修改
- 跳过，处理下一个
- 退出，稍后继续
```

## --report 模式

仅生成报告，不进入交互确认流程。适用于快速检查或自动化场景。

## 注意事项

1. **状态文件位置**: `.evo-state.json` 在项目根目录，建议加入 `.gitignore`
2. **报告位置**: `docs/evo-reports/` 可选择是否提交到版本控制
3. **全局统计**: `~/.claude/evo-stats/` 跨项目累积，用于发现通用模式
4. **阈值调整**: 可手动编辑 `.evo-state.json` 中的 `threshold` 值

## 自动监控

将以下内容添加到项目的 CLAUDE.md 以启用自动信号检测。

### 信号检测规则

**1. retry_loops（重复试错）**
检测条件（满足任一即记录）：
- 同一个错误/问题连续尝试 2+ 次未解决
- 同一段代码在 10 分钟内修改 3+ 次
- 测试失败后的修复尝试超过 3 轮

**2. interrupted_flows（流程中断）**
检测条件（满足任一即记录）：
- 用户明确说"先不管这个"、"等会再说"、"跳过"
- 任务切换时前一个任务未完成且未说明原因
- debugging/实现过程被打断超过 30 分钟未恢复

**3. git_churn（代码翻动）**
检测条件（满足任一即记录）：
- 同一文件在最近 5 个 commit 中出现 3+ 次修改
- 出现 revert commit
- fix: 类型 commit 针对同一功能连续 2+ 次

### 检测到信号时的行为

1. 读取项目根目录的 `.evo-state.json`（不存在则创建初始结构）
2. 更新对应信号类型的 `count` 和 `instances` 数组
3. 检查是否有任一信号的 `count >= threshold`（默认阈值为 3）
4. 若达到阈值，在当前回复末尾提示：

   > **[Evo]** 检测到流程问题信号（{信号类型} 已达 {count} 次），建议执行 `/evo` 进行分析。

### .evo-state.json 初始结构

首次检测到信号时，若文件不存在，创建以下结构：

```json
{
  "version": "1.0",
  "project": "{当前项目名}",
  "signals": {
    "retry_loops": { "count": 0, "threshold": 3, "instances": [] },
    "interrupted_flows": { "count": 0, "threshold": 3, "instances": [] },
    "git_churn": { "count": 0, "threshold": 3, "instances": [] }
  },
  "last_analysis": null,
  "pending_improvements": []
}
```

### 记录实例的格式

```json
{
  "timestamp": "ISO8601 时间戳",
  "context": "简短描述发生了什么",
  "pattern": "匹配的检测规则"
}
```
