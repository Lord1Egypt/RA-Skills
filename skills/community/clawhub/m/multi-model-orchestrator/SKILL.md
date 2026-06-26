---
name: multi-model-orchestrator
description: 多模型编排系统，基于 oh-my-codex 框架。支持 deep-interview、ralplan、team、ralph、debug、frontend 等工作流模式。
triggers: ["编排", "orchestrate", "多模型", "multi-model", "团队协作", "team", "并行", "parallel", "$deep-interview", "$ralplan", "$ralph", "$team", "$code-review", "$debug", "$frontend", "$autopilot"]
---

# Multi-Model Orchestrator

基于 oh-my-codex 的多模型编排系统。集成 **superpowers-systematic-debugging**（调试纪律）和 **frontend-design**（UI 品质）。

## 工作流模式

### 模式选择指南

| 场景 | 模式 | 说明 |
|---|---|---|
| 需求不明确 | `$deep-interview` | 先澄清再行动 |
| 需要规划 | `$ralplan` | Planner/Architect/Critic 共识 |
| 大任务并行 | `$team N` | N 个 Agent 并行执行 |
| 小任务持续 | `$ralph` | 单 Agent 持久完成 |
| 遇到 bug/测试失败 | `$debug` | 四阶段系统化调试（多模型交叉验证） |
| 做前端/UI | `$frontend` | 多模型协作，UI 品质把关 |
| 全自动 | `$autopilot` | ralplan → ralph → code-review 循环 |
| 代码审查 | `$code-review` | 多模型交叉审查（含 UI 审查） |

### 触发词映射

- "帮我编排" / "多模型并行" → 自动选择 `$team` 或 `$ralph`
- "澄清需求" / "我不确定" → `$deep-interview`
- "规划一下" / "制定计划" → `$ralplan`
- "并行执行" / "同时做" → `$team`
- "做完它" / "持续执行" → `$ralph`
- "有 bug" / "测试失败" / "报错了" / "调试" → `$debug`
- "做个页面" / "前端" / "UI" / "组件" / "landing page" → `$frontend`
- "审查代码" / "code review" → `$code-review`
- "全自动" / "autopilot" → `$autopilot`

---

## 执行流程

### $deep-interview（需求澄清）

```
1. 收集用户初始需求
2. 识别模糊点和边界条件
3. 生成澄清问题列表
4. 等待用户确认
5. 输出明确的需求文档
```

### $ralplan（共识规划）

```
1. Planner: 制定实现计划
2. Architect: 从架构角度审查
3. Critic: 识别风险和改进点
4. 达成共识，输出最终计划
```

### $team（并行执行）

```
1. 将计划拆分为独立子任务
2. 分配给不同模型的 Agent
3. 并行执行（sessions_spawn）
4. 收集结果并汇总
5. 验证质量
```

### $ralph（持久完成）

```
1. 单 Agent 接收任务
2. 持续执行直到完成
3. 遇到问题自动修复（遵循 $debug 纪律）
4. 输出最终结果
```

### $debug（系统化调试）🆕

集成自 **superpowers-systematic-debugging**。多模型交叉验证，杜绝"猜-试"循环。

```
阶段 1: 根本原因调查（Agent A - mimo/mimo-v2.5-pro）
├── 读错误信息、堆栈跟踪、行号、错误码
├── 稳定复现：步骤、频率、环境
├── 检查最近变更：git diff、配置、依赖
├── 追踪数据流：坏值从哪来？谁传入的？
└── 输出: 根本原因报告

阶段 2: 模式分析（Agent B - sub2api-openai/gpt-5.5）
├── 找代码库中类似正常工作的例子
├── 对比参考实现，逐行阅读
├── 识别差异，列出每个不同点
├── 理解依赖和假设
└── 输出: 差异分析

阶段 3: 假设与测试（Agent A + B 交叉验证）
├── 形成假设："X 是根本原因，因为 Y"
├── 最小化测试：一次只改一个变量
├── 验证：有效→阶段4，无效→新假设
└── 输出: 验证结果

阶段 4: 实现修复
├── 创建失败的测试用例（先写后修）
├── 实现单一修复，不捆绑重构
├── 验证：测试通过？其他测试坏了吗？
├── 如果 3+ 修复失败 → 停止，质疑架构
└── 输出: 修复代码 + 测试
```

**铁律：**
- 未经根本原因调查，不许修复
- 3+ 修复失败 → 停止并质疑架构，不要继续猜
- "快速修复" + "以后再调查" = 违反流程

**红旗（立即停止，回到阶段 1）：**
- "先试试改 X 看看行不行"
- "大概是 X，让我修那个"
- "我没有完全理解但这可能行"
- 每个修复在不同地方揭示新问题

### $frontend（前端/UI 品质）🆕

集成自 **frontend-design**。多模型协作，UI 品质把关。

```
步骤 1: 需求收集
├── Purpose: 界面做什么？
├── Audience: 开发者？终端用户？内部工具？
├── Constraint: 框架已选定？静态？SSR？
└── Aesthetic: 技术风？内容风？交易风？

步骤 2: 架构规划（$ralplan）
├── Planner: 页面结构 + 组件拆分
├── Architect: 框架选型 + 性能预算
└── Critic: 可访问性 + 移动端风险

步骤 3: 并行实现（$team）
├── Agent 1: 结构/布局（HTML/模板）
├── Agent 2: 样式/主题（CSS/Tailwind）
├── Agent 3: 交互/状态（JS/TS）
└── Agent 4: 动效/细节（微交互）

步骤 4: UI 审查（$code-review + frontend-design）
├── 检查 AI 通用美学红线（见下）
├── 移动端 + 触控 + 键盘导航
├── 深色 + 浅色双主题
├── Core Web Vitals + 包大小
└── 输出: UI 审查报告（P0-P3 分级）
```

**AI 通用美学红线（禁止出货）：**
- Card-grid-of-nothing（圆角卡片网格泛滥）
- 紫粉渐变 CTA / hero
- 无空间理由的毛玻璃
- Lucide/Heroicons 图标撒满每个列表项
- 三栏"Features"：图标 + 标题 + 12 字描述
- 居中 hero + "Build [noun] [adverb]" + 两个按钮
- 渐变文字 h1（`from-indigo-500 to-pink-500`）
- "Trusted by" 灰色 logo 行
- 默认 indigo 强调色
- 非 AI 功能的 "AI shimmer" 加载态
- 常规操作的彩纸/气球动效
- 应内联的 toast 通知
- 首次加载的 newsletter/Cookie 弹窗

**硬性默认值（直接出货，用户可覆盖）：**
- Mobile-first 布局
- 深色 + 浅色双主题同时设计
- 触控目标 >= 44x44px
- `prefers-reduced-motion` 降级
- Focus-visible 样式（禁止 `outline: none`）
- WCAG AA 对比度
- 真实框架（Astro 6 / SvelteKit 2 / Vite 8 / Next 16 / Tailwind v4）

### $code-review（代码审查，增强版）

```
1. 模型 A（gpt-5.5）: 逻辑正确性 + 架构
2. 模型 B（gpt-5.3-codex）: 性能 + 安全
3. 模型 C（mimo-v2.5-pro）: 可维护性 + 测试覆盖
4. 如果涉及 UI → 自动附加 frontend-design 审查
5. 汇总交叉审查结果
```

### $autopilot（全自动，增强版）

```
ralplan（共识规划）
  → ralph（持久执行，遇 bug 自动 $debug）
    → code-review（交叉审查，含 UI 审查）
      → 修复反馈循环
```

---

## 模型路由

根据任务类型自动选择最优模型：

- **架构/推理** → `sub2api-openai/gpt-5.5`
- **代码生成** → `sub2api-openai/gpt-5.3-codex`
- **快速执行** → `mimo/mimo-v2.5-pro`
- **代码审查** → `sub2api-openai/gpt-5.5`
- **简单任务** → `sub2api-openai/gpt-5.4-mini`
- **中文任务** → `local-qwen/gpt-4o`
- **图像生成** → `sub2api-openai/gpt-image-2`
- **调试根因分析** → `sub2api-openai/gpt-5.5`（推理能力强）
- **调试修复实现** → `sub2api-openai/gpt-5.3-codex`（代码生成强）
- **UI 结构/布局** → `sub2api-openai/gpt-5.5`
- **UI 样式/主题** → `sub2api-openai/gpt-5.3-codex`
- **UI 交互/动效** → `mimo/mimo-v2.5-pro`

## 子任务模板

### 通用模板

```
你是一个专注于 [角色] 的 AI 助手。

## 任务
[具体任务描述]

## 上下文
[相关代码/文件/背景信息]

## 约束
- [具体约束条件]

## 预期输出
[明确的交付物描述]
```

### 调试子任务模板

```
你是 [根因分析师 / 修复实现者]。

## Bug 描述
[症状、错误信息、复现步骤]

## 已知信息
[堆栈跟踪、相关代码、最近变更]

## 任务
阶段 [1/2/3/4]: [具体阶段任务]

## 约束
- 未经根因调查不许提修复方案
- 一次只改一个变量
- 3+ 修复失败必须停止并质疑架构

## 预期输出
- 根因分析报告 / 差异分析 / 假设验证结果 / 修复代码+测试
```

### 前端子任务模板

```
你是前端 [结构工程师 / 样式工程师 / 交互工程师 / UI 审查员]。

## 任务
[具体前端任务]

## 设计约束
- Mobile-first，触控目标 >= 44px
- 深色 + 浅色双主题
- WCAG AA 对比度
- prefers-reduced-motion 降级
- 禁止 AI 通用美学红线（card-grid-of-nothing、紫粉渐变等）
- 真实框架，当前版本

## 预期输出
[组件代码 / 样式文件 / 审查报告]
```

---

## 集成说明

本技能集成两个专项技能的核心方法论：

| 来源 | 集成内容 | 应用模式 |
|------|---------|---------|
| **superpowers-systematic-debugging** | 四阶段调试流程、铁律、红旗识别 | `$debug` 模式 + `$ralph`/$autopilot` 中的自动调试 |
| **frontend-design** | UI 品质标准、AI 美学红线、双主题、移动优先 | `$frontend` 模式 + `$code-review` 中的 UI 审查 |

详细参考：
- 调试完整流程: `~/.openclaw/skills/superpowers-systematic-debugging/SKILL.md`
- UI 品质标准: `~/.openclaw/skills/frontend-design/SKILL.md`
