# Sprint 流水线编排器

> **本文件是 gstack-dev 的"指挥中心"**。
> 它定义了如何根据任务类型选择合适的阶段组合、
> 如何在阶段间传递数据、以及如何处理异常。

## 任务分类 → 阶段映射

| 任务类型 | 建议流程 | 可跳过 |
|----------|----------|--------|
| **新功能开发** | 全部7个阶段 | 无 |
| **Bug修复（简单）** | Think → Build → Review → Test | Plan/Ship/Reflect |
| **Bug修复（复杂/生产事故）** | 全部7个阶段 | 无 |
| **代码重构** | Plan → Build → Review → Test | Think/Ship/Reflect |
| **技术方案评审** | Think → Plan | Build之后全部跳过 |
| **部署上线** | Ship + Reflect | Think~Test |
| **Sprint回顾** | 仅 Reflect | 其余全部跳过 |
| **紧急Hotfix** | Build → Review → Test → Ship | Think/Plan/Reflect |

## 阶段间数据传递

每个阶段的**输出物自动成为下一阶段的输入**：

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  THINK ──→ 需求定义.md ──→ PLAN                     │
│                              │                       │
│                              ↓                       │
│                         技术方案.md ──→ BUILD        │
│                                              │       │
│                                              ↓       │
│                                         代码+测试 ──→ REVIEW
│                                                        │
│                                           ↓            │
│                                      审查报告+修复 ──→ TEST
│                                                            │
│                                               ↓             │
│                                          测试报告 ──→ SHIP  │
│                                                          │   │
│                                            ↓               │
│                                       发布报告 ──→ REFLECT │
│                                                              │
│                                         ↓                    │
│                                    改进报告+经验库 ←─────────┘
│
└──────────────────────────────────────────────────────┘
```

### 数据格式约定

每个阶段输出一个结构化 Markdown 文件：

```markdown
# [Phase] Report — [项目名]

## 元信息
- 阶段: [THINK/PLAN/BUILD/REVIEW/TEST/SHIP/REFLECT]
- 时间: YYYY-MM-DD HH:MM
- 执行者: [角色名]
- 输入: [上一阶段的文件引用]

## 核心内容
[阶段特定的内容，见各角色的md文件]

## 传递给下一阶段
[明确列出下一阶段需要关注的要点]
```

## 异常处理

### 情况1：某个阶段发现严重问题

```
例：PLAN 阶段 CEO Review 给了 3 星
     ↓
方案A: 返回 THINK 阶段重新定义需求
方案B: 在 PLAN 内部迭代直到通过（默认）
     ↓
如果连续2次不通过 → 升级到用户决策
```

### 情况2：REVIEW 发现 P0 bug

```
例：Review 发现安全漏洞
     ↓
自动返回 BUILD 修复
     ↓
修复后重新 REVIEW
     ↓
如果同一bug出现3次 → 升级到用户决策
```

### 情况3：TEST 不通过

```
例：E2E 测试发现功能不可用
     ↓
记录Bug → 自动修复 → 写回归测试 → 重新TEST
     ↓
循环最多3次 → 超过则升级到用户
```

### 情况4：用户中断

```
任何阶段都可以被用户中断：
  - "停一下" / "先到这里" / "这个方向不对"
     ↓
保存当前进度（所有已完成的阶段产出保留）
记录中断点（下次可以从这里继续）
```

## 并行执行规则

### 可以并行的阶段
- **Plan 的三个子审查**: CEO / Eng / Design 理论上可以并行
- **Test 的多个用例**: Happy Path / 异常路径 / 边界可以并行
- **Ship 的监控和验证**: 可以并行跑多个检查

### 必须串行的阶段
- Think → Plan（必须先有需求定义才能规划）
- Plan → Build（必须有方案才能编码）
- Build → Review（必须写完才能审查）
- Review → Test（必须修完bug才能测）
- Test → Ship（必须测试通过才能发布）

## 快速模式 vs 完整模式

### 快速模式（`gstack quick` 或 `快速分析`）

适用于：原型验证、小改动、内部工具

```
Think(简化) → Build → Review(简化) → Test(关键路径)
```

- Think 只问 2 个问题（核心问题 + MVP 范围）
- Review 只查 P0/P1 问题
- Test 只跑 happy path
- 跳过 Ship/Reflect

### 完整模式（`gstack full` 或 默认）

适用于：面向用户的正式功能、生产环境变更

```
完整 7 个阶段，一步不少
```

## 与 WorkBuddy Agent 体系的集成

### 单 Agent 模式（默认）
- 所有角色由同一个 AI 扮演（切换 system prompt）
- 适合小任务或单会话内完成的工作流

### 多 Agent 团队模式（`gstack team`）
- 使用 Task tool 启动独立的 subagent 扮演每个角色
- 各 agent 可以并行工作（Plan 三连审、Test 用例等）
- 通过 send_message 传递阶段间数据
- 适合大型项目或需要深度审查的场景

#### Team 模式 Agent 分配
```python
TEAM = {
    "think_agent":      {"role": "产品顾问",      "prompt": "roles/think.md"},
    "ceo_reviewer":     {"role": "CEO",            "prompt": "roles/plan-ceo.md"},
    "eng_reviewer":     {"role": "工程经理",       "prompt": "roles/plan-eng.md"},
    "design_reviewer":  {"role": "设计师",         "prompt": "roles/plan-design.md"},
    "builder":          {"role": "Staff Engineer", "prompt": "roles/build.md"},
    "reviewer":         {"role": "资深工程师",     "prompt": "roles/review.md"},
    "qa_lead":          {"role": "QA负责人",       "prompt": "roles/test.md"},
    "release_eng":      {"role": "发布工程师",     "prompt": "roles/ship.md"},
    "retro_lead":       {"role": "工程经理",       "prompt": "roles/reflect.md"},
}
```

## 配置项

### gstack.config.yaml （项目根目录可选配置）

```yaml
# gstack 项目配置
mode: full           # full | quick | custom
parallel: true       # 是否启用并行执行
xcheck: true         # 是否启用多模型交叉验证
careful: true        # 是否开启危险操作警告
freeze: null         # 编辑锁定路径，null=不锁定

# 自定义阶段（custom 模式下）
phases:
  - think
  - plan
  - build
  - review
  - test
  # ship 和 reflect 被注释掉了 = 跳过

# 模型分配
models:
  primary: "deepseek-v4"
  xcheck: "qwen-max"
  embed: "qwen-text-embedding-v3"

# 覆盖率要求
coverage:
  minimum: 80
  core_paths: 95
```
