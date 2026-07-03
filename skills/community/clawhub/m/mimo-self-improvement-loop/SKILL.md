---
name: self-improvement-loop
version: 2.0.0
description: |
  三层自我改进循环升级版。融入Self-Harness三阶段循环（Weakness Mining → Harness Proposal → Proposal Validation）。
  让Agent从每次执行中提取经验，自动发现弱点模式，生成改进方案，验证改进效果。
  触发场景：完成重要任务后、遇到执行失败后、发现重复犯错后、评估技能升级效果后、
  每小时进化巡航触发时、深度复盘时。
---

# Self-Improvement Loop v2.0（自我改进循环）

## Overview

基于 Hexo Labs SIA 三层架构 + Self-Harness (arXiv 2026.06.08) 三阶段循环，实现 Agent 从执行中持续学习的核心能力。

**v2.0 升级要点：**
- 新增 Phase 0: Weakness Mining（从执行trace中自动挖掘弱点模式）
- 新增 Phase 5: Proposal Validation（回归测试验证改进效果）
- 量化指标追踪（ Self-Harness 实测：弱点→改进→验证 循环提升 33-60%）
- 跨会话记忆沉淀（改进记录持久化，防止重复犯错）

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Meta-Agent (编排层)                                      │
│  - 读取进化目标 + 历史改进记录 + 弱点模式库                  │
│  - 决定本轮改进焦点                                        │
│  - 分发任务给 Target / Feedback / Validator Agent          │
└──────────┬──────────────┬───────────────┬──────────────┘
           │              │               │
    ┌──────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
    │ Target Agent │ │ Feedback   │ │ Validator  │
    │ (执行层)     │ │ Agent      │ │ Agent      │
    │              │ │ (审查层)    │ │ (验证层)    │
    │ 执行具体任务  │ │ 挖掘弱点    │ │ 回归测试    │
    │ 记录执行trace │ │ 分析trace  │ │ 验证改进    │
    │              │ │ 生成改进方案 │ │ 量化效果    │
    └──────────────┘ └────────────┘ └────────────┘
```

## When to Use

- 每小时进化巡航触发时
- 完成一批任务后需要复盘时
- 发现重复犯错时
- 需要评估技能升级效果时
- 用户给出显式或隐式反馈后
- 自审发现执行力下降时

## The Process

### Phase 0: Weakness Mining（弱点挖掘）

> 来源：Self-Harness 论文的核心创新

从执行 trace 中自动发现弱点模式。

```
执行 trace 收集
  ↓
模式分析：
  - 重复出现的错误类型
  - 缺失的错误处理
  - 低效的工具使用模式
  - 上下文管理失败
  - 规划错误
  - 卡住循环或无限重试
  ↓
弱点分类：
  | 类别 | 描述 | 示例 |
  |------|------|------|
  | 工具选择错误 | 为任务选了错误的工具 | 用search_web代替fetch_web |
  | 上下文错误 | 丢失或误解信息 | 子Agent上下文不足导致返工 |
  | 规划错误 | 任务分解不当 | 一次性做太多导致遗漏 |
  | 错误处理 | 未能从失败中恢复 | 工具报错后重试同样操作 |
  | 验证缺失 | 未验证假设 | 声称"完成"但未运行测试 |
  | 过度自信 | 跳过审查/测试 | 不经过doubt-driven就提交 |
  ↓
弱点模式库更新（recent_memory/evolution/weaknesses.json）
```

**弱点记录格式：**
```json
{
  "weakness_id": "W-043",
  "pattern": "子Agent指令不够精确，导致返工",
  "frequency": 5,
  "last_occurrence": "2026-06-17T10:30:00+08:00",
  "category": "上下文错误",
  "impact": "每次返工增加10-15分钟",
  "root_cause": "未使用subagent-driven-development技能的标准指令模板",
  "proposed_fix": "强制执行指令模板检查清单"
}
```

### Phase 1: Execution Logging（执行记录）

每次任务执行后，自动生成执行 trace：

```json
{
  "task_id": "xxx",
  "task_type": "技术开发|咨询顾问|营销推广|内容创作",
  "skills_used": ["skill-a", "skill-b"],
  "execution_steps": [
    {"step": 1, "action": "...", "tool": "...", "result": "...", "duration_ms": 123}
  ],
  "outcome": "success|partial|failed",
  "time_spent_minutes": 0,
  "issues_encountered": [],
  "quality_score": 0,
  "self_observation": "",
  "anti_rationalization_check": {
    "steps_skipped": [],
    "rationalizations_caught": []
  }
}
```

### Phase 2: Feedback Analysis（反馈分析）

Feedback Agent 审查执行 trace + 弱点模式库，输出：

```
1. 做得好的方面（保留并强化）
2. 做得差的方面（需要改进）
3. 跳过的步骤（反借口检查）
4. 新发现的弱点模式（更新弱点库）
5. 与历史弱点对比（是否重复犯错）
6. 具体改进建议（可操作、可验证）
```

**改进建议分类：**

| 类型 | 描述 | 风险 | 应用方式 |
|------|------|------|---------|
| 技能级改进 | 修改 SKILL.md 的某个段落 | 中 | 更新技能文件 |
| 流程级改进 | 调整执行步骤顺序 | 低 | 更新 MEMORY.md |
| 知识级改进 | 新增参考文档 | 低 | 创建 references/ |
| 行为级改进 | 更新反借口表 | 低 | 修改技能 Anti-rationalization |
| 决策级改进 | 更新决策规则 | 中 | 更新 MEMORY.md 规则段 |
| 弱点缓解 | 针对特定弱点的防护 | 低 | 更新弱点模式库 |

### Phase 3: Improvement Generation（改进生成）

基于反馈分析，生成**最小化、可测试**的改进方案。

> 关键原则（来源 Self-Harness）：改进方案必须是 targeted（针对特定弱点）+ minimal（小聚焦变更）+ testable（可通过基准任务验证）

```markdown
## Improvement Proposal

### 目标弱点
W-043: 子Agent指令不够精确

### 改进方案
在 subagent-driven-development 技能的 Step 2a 增加指令检查清单：
- [ ] 包含任务完整描述
- [ ] 包含相关规格/约束
- [ ] 包含必要的上下文文件内容
- [ ] 明确禁止事项

### 预期效果
子Agent返工率从 40% 降到 <15%

### 验证方法
下一个使用子Agent的任务中，跟踪返工次数

### 回滚方案
如果改进导致执行时间增加>30%，回退到原版
```

### Phase 4: Application（应用改进）

按风险级别应用改进：

| 风险 | 行为 | 示例 |
|------|------|------|
| **低风险** | 直接应用 | 更新反借口表、添加检查清单 |
| **中风险** | 记录为待验证假设，下个任务试用 | 修改技能流程步骤 |
| **高风险** | 向用户确认后应用 | 修改核心决策规则 |

**应用后：**
1. 更新技能的 SKILL.md
2. 更新 MEMORY.md / TOOLS.md
3. 更新 recent_memory/ 中的决策记录
4. 记录本轮改进到 evolution-log.md

### Phase 5: Proposal Validation（改进验证）

> 来源 Self-Harness 的核心创新 — 防止"改进"实际是退化

```
改进应用后
  ↓
设计验证任务：
  - 选取能触发原弱点的任务类型
  - 执行任务
  - 对比改进前后的表现
  ↓
量化评估：
  | 指标 | 改进前 | 改进后 | 变化 |
  |------|--------|--------|------|
  | 返工次数 | N | M | -X% |
  | 执行时间 | Xmin | Ymin | -Z% |
  | 质量评分 | A | B | +C |
  ↓
决策：
  - 改善 → 接受改进，更新基线
  - 持平 → 保留改进，标记待观察
  - 退化 → 回滚改进，记录失败原因
```

## Metrics Tracking（指标追踪）

### 进化指标看板

| 指标 | 基线 | 当前 | 目标 |
|------|------|------|------|
| 任务申请通过率 | - | 待测量 | >30% |
| 交付一次性通过率 | - | 待测量 | >80% |
| 平均交付时间(min) | - | 待测量 | <30min |
| 技能版本覆盖度 | 74% | 待测量 | 100% |
| 反借口表覆盖率 | 0% | 进行中 | 100% |
| 弱点模式库规模 | 0 | 待测量 | 持续增长 |
| 弱点重复率 | - | 待测量 | <10% |
| 改进验证通过率 | - | 待测量 | >80% |

### 指标记录格式

```json
// recent_memory/evolution/metrics.json
{
  "date": "2026-06-17",
  "tasks_completed": 0,
  "tasks_successful": 0,
  "tasks_partial": 0,
  "tasks_failed": 0,
  "avg_quality_score": 0,
  "avg_time_minutes": 0,
  "rationalizations_caught": 0,
  "weaknesses_discovered": 0,
  "improvements_applied": 0,
  "improvements_validated": 0,
  "improvements_rolled_back": 0
}
```

## Memory Integration（记忆集成）

### 跨会话记忆沉淀

```
recent_memory/evolution/
├── weaknesses.json      # 弱点模式库（Weakness Mining产出）
├── improvements.json    # 所有历史改进记录
├── patterns.json        # 识别出的可复用模式
├── mistakes.json        # 犯过的错误（防止重复）
├── metrics.json         # 进化指标时间序列
├── proposals/           # 改进提案详情
│   ├── P-001.md
│   └── P-002.md
└── validations/         # 验证结果
    ├── V-001.md
    └── V-002.md
```

### 弱点模式库的跨会话使用

每次会话开始时：
1. 读取 weaknesses.json
2. 将活跃的弱点模式加载为"注意事项"
3. 执行任务时主动避开已知弱点
4. 任务结束后检查是否有新弱点或弱点复发

## Anti-rationalization

| 借口 | 现实 |
|------|------|
| "这次任务特殊，不需要复盘" | 每个任务都要记录执行trace，特殊性正是学习机会 |
| "改进太多，下轮再说" | 每轮至少落地1个具体改进，哪怕很小 |
| "执行结果还行，不需要改进" | "还行"是最低标准，必须找到至少1个改进点 |
| "用户没反馈问题，说明做得好" | 用户不反馈≠做得好，主动自检 |
| "这个错误是意外，不会再犯" | 记录到mistakes.json，用数据验证是否再犯 |
| "改技能太麻烦，改prompt就行" | 技能是持久化的，prompt是临时的，优先改技能 |
| "弱点挖掘太耗时" | Self-Harness论文证明：自动化弱点挖掘提升33-60%性能 |
| "验证改进太麻烦" | 不验证的改进可能是退化。最小验证只需1个任务 |
| "改进方案太小不会有效果" | Self-Harness原则：minimal changes, targeted fixes。小改进累积为大提升 |
| "弱点库太大了管不过来" | 按频率和影响排序，优先处理Top 5 |

## Red Flags

- 连续3轮进化巡航没有可量化产物 → 进化系统失效
- 同类错误重复出现 → Feedback循环断裂
- 技能版本长期不更新 → 改进没有落地
- 执行trace缺失 → 没有数据支撑改进
- 弱点库中某弱点持续30天未消除 → 改进方案无效，需要新方案
- 改进应用后指标退化但未回滚 → 验证机制失效
- 弱点挖掘阶段没有发现任何弱点 → 分析不够深入

## Interaction with Other Skills

- **`doubt-driven-development`**：doubt cycle 发现的错误模式是 Weakness Mining 的输入
- **`code-review-and-quality`**：审查发现是弱点挖掘的数据源
- **`subagent-driven-development`**：子Agent执行结果包含丰富的执行trace
- **`test-driven-development`**：TDD的测试套件是 Proposal Validation 的验证工具
- **进化规则（EVOLUTION_RULES.md）**：本技能的执行受进化规则约束（小步快跑、可回滚、有验证）

## Verification

完成一轮 self-improvement loop 后：
- [ ] Phase 0: 弱点模式库已更新（新弱点或已知弱点频率更新）
- [ ] Phase 1: 执行trace已记录且完整
- [ ] Phase 2: 反馈分析已产出，包含至少1个可操作改进建议
- [ ] Phase 3: 改进方案已文档化（目标、方案、预期效果、验证方法、回滚方案）
- [ ] Phase 4: 改进已按风险级别应用
- [ ] Phase 5: 改进效果已验证（改善/持平/退化 已分类）
- [ ] metrics.json 已更新
- [ ] evolution-log.md 已记录本轮改进
