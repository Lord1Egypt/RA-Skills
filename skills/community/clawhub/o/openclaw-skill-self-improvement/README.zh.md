# OpenClaw Skill Self Improvement

OpenClaw 技能的自动化健康检查、路由评估和回归测试系统。

## 这是什么？

OpenClaw Skill Self Improvement 是一套脚本和评估用例，帮助你维护一个干净、健康、无回归的 OpenClaw agent 技能库。

它回答三个核心问题：

1. **我的技能库干净吗？** — 检测重复、废弃和僵尸技能
2. **路由是否正确？** — 验证正确的输入能否触发正确的技能
3. **是否在持续变好？** — 通过每日心跳追踪变化趋势

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/X-RayLuan/openclaw-skill-self-improvement.git
cd openclaw-skill-self-improvement

# 运行健康检查
node scripts/skill-health-check.mjs /path/to/your/openclaw/workspace

# 运行路由评估
node scripts/routing-eval-runner.mjs /path/to/your/openclaw/workspace

# 运行每日心跳
node scripts/daily-health-heartbeat.mjs /path/to/your/openclaw/workspace
```

## 系统要求

- Node.js 18+
- 带有 `skills/` 目录的 OpenClaw 工作区

## 工作原理

### 技能健康检查 (`scripts/skill-health-check.mjs`)

扫描工作区和系统技能目录中的所有 `SKILL.md` 文件：

- **重复检测**：使用 token 相似度比较技能名称和描述，≥72% 重叠的配对会被标记
- **僵尸技能检测**：标记 30+ 天无使用信号且未更新的技能
- **过期技能检测**：标记有使用信号但 60+ 天无活动的技能

带有 `status: deprecated` frontmatter 标记的技能会自动从重复检测中排除。

### 路由评估 (`scripts/routing-eval-runner.mjs`)

读取 `references/routing-evals.json`，使用关键词加权路由器模拟路由决策。每个评估用例定义：

- `input`：用户提示
- `shouldTrigger`：期望触发的技能 ID
- `shouldNotTrigger`：绝对不能触发的技能

评分机制包括：
- 名称词匹配
- 触发短语重叠（要求 ≥50% 词匹配）
- 描述关键词重叠
- 已知冲突对的动作专属加分

### 每日心跳 (`scripts/daily-health-heartbeat.mjs`)

自动运行上述两个脚本，与上次结果对比，生成人类可读摘要。追踪：

- 总技能数
- 重复配对数
- 僵尸技能数
- 评估通过率
- 自上次运行以来的变化

## 评估用例（8 个）

| # | 输入 | 期望触发 | 禁止触发 |
|---|------|----------|----------|
| 1 | debug this production failure | investigate | office-hours |
| 2 | brainstorm startup idea | office-hours | investigate |
| 3 | create a new skill | skill-creator | seo-content-writer |
| 4 | update the docs after PR | document-release | content-quality-auditor |
| 5 | audit my content quality | content-quality-auditor | content-writer |
| 6 | write a blog post for ClawLite | content-writer | seo-content-writer |
| 7 | run daily marketing pipeline | daily-marketing-operating-system | openclaw-mark |
| 8 | do a retro for this week | retro | openclaw-retro |

## 输出文件

| 文件 | 说明 |
|------|------|
| `.learnings/skill-health-report.json` | 完整健康检查结果 |
| `.learnings/routing-eval-report.json` | 评估通过/失败详情 |
| `.learnings/daily-skill-health-summary.txt` | 人类可读的每日摘要 |
| `.learnings/skill-health-history.json` | 用于增量追踪的历史快照 |

## 实际效果

在 [ClawLite](https://clawlite.ai) 工作区（共 122 个技能）：

- **清理前**：7 对重复，37 个僵尸技能
- **清理后**：1 个误报重复，0 个僵尸技能，评估通过率 100%

三对重复技能已通过废弃标记解决：
- `openclaw-investigate` → 废弃（使用 `/investigate`）
- `openclaw-office-hours` → 废弃（使用 `/office-hours`）
- `openclaw-daily-backup` → 废弃（使用 `/openclaw-backup-restore`）

## 架构

```
skill-health-check.mjs
  ├── walkSkills()           → 扫描所有 SKILL.md
  ├── parseFrontmatter()     → 读取名称、描述、状态
  ├── similarity()           → 基于 token 的文本比较
  ├── collectSessionFiles()  → 扫描 agent 会话记录获取使用信号
  └── 生成报告

routing-eval-runner.mjs
  ├── scoreSkill()           → 关键词 + 短语 + 加分评分
  ├── routeInput()           → 选择最高分技能
  └── 与期望值对比

daily-health-heartbeat.mjs
  ├── 运行两个脚本
  ├── 加载历史记录
  ├── 计算增量
  └── 写入摘要
```

## 路线图

### Phase 2A
- 为高风险冲突对添加更多评估用例
- 用语义匹配器替换关键词路由器

### Phase 2B
- 从真实会话记录推导 `last_used_at`
- 从观察到的路由追踪 `useCount`

### Phase 3
- 为基于 CLI/API 的技能添加依赖漂移检查
- 添加健康状态标签：`healthy`、`duplicate`、`dark`、`broken`、`degraded`
- 添加 cron/heartbeat 自动化，实现无人值守的每日运行

## 参与贡献

欢迎提交 Issue 和 PR。重点方向：
- 更好的语义路由评估
- 真实会话记录的使用追踪
- 额外的健康维度（依赖漂移、技能性能）

## 许可证

MIT © Ray Luan
