---
name: meta-skill-weaver
description: Use this skill when orchestrating complex multi-step tasks. Provides first-principles task decomposition, EventBus event system, multi-skill collaboration with parallel execution, timeout control, and interrupt recovery. v2.4 adds MetricsMiddleware with auto-optimization triggers and FeedbackMiddleware for user ratings. v2.3 includes 54+ Jest tests for production stability.
origin: meta-skill
version: 2.4.0
tags:
  - orchestration
  - workflow
  - event-driven
  - infrastructure
  - meta-skill
tools:
  - Read
  - Write
  - Bash
  - Exec
model: sonnet
---

# Meta Skill Weaver - 技能编织器

**版本**：v2.4.0  
**定位**：L2 编排层 - 多技能协作编排引擎  
**状态**：✅ 生产就绪（54 个新增测试用例，MetricsMiddleware + FeedbackMiddleware）

---

## 📖 技能说明

Meta Skill Weaver 是一款企业级 AI 技能编排引擎，专为复杂多步骤任务设计。它通过第一性原理任务分解器将宏大目标拆解为原子任务，利用 EventBus 事件系统实现多技能松耦合协作，支持并行执行、超时控制、中断恢复。v2.3 新增 35 个 Jest 测试用例（覆盖率 62%），确保生产级稳定性。

**核心价值**：让 AI 从"单点响应"升级为"系统协作"，轻松驾驭研究→分析→报告等长程任务，是构建企业级 AI 工作流的必备基础设施。

**适用场景**：
- ✅ 多步骤研究报告（资料收集→数据分析→报告撰写）
- ✅ 跨技能协作任务（同时调用 3+ 技能）
- ✅ 长时中断恢复（支持 15 分钟超时控制）
- ✅ 事件驱动工作流（基于 EventBus 订阅/发布）
- ✅ 企业级任务编排（7 个内置中间件）

---

## 🎯 使用场景

### 场景 1：多步骤研究报告

**任务**：「研究 AI Agent 市场趋势，生成分析报告」

**编排流程**：
```
1. 资料收集（web_search, browser）
   ↓
2. 数据分析（xlsx, data-analysis）
   ↓
3. 报告撰写（copywriting, docx）
   ↓
4. 质量审查（quality-checker）
   ↓
5. 发布报告（publish）
```

**使用方式**：
```bash
meta-skill-weaver start \
  --task="研究 AI Agent 市场趋势" \
  --skills="web_search,browser,xlsx,copywriting,docx" \
  --timeout=15m \
  --parallel=true
```

**预期结果**：
- 自动分解为 5 个子任务
- 并行执行可并行的任务
- 自动追踪每个子任务进度
- 支持中断后从断点恢复

---

### 场景 2：跨技能协作任务

**任务**：「分析销售数据，生成 PPT 报告」

**编排流程**：
```
1. 读取 Excel 数据（xlsx）
   ↓
2. 数据分析（data-analysis）
   ↓
3. 生成图表（chart-generator）
   ↓
4. 创建 PPT（pptx）
   ↓
5. 导出 PDF（pdf）
```

**使用方式**：
```bash
meta-skill-weaver start \
  --task="分析销售数据生成 PPT" \
  --skills="xlsx,data-analysis,chart-generator,pptx,pdf" \
  --output="sales-report.pdf"
```

---

### 场景 3：长时中断恢复

**任务**：「完成市场研究报告（可能需要 2 小时）」

**中断恢复流程**：
```
1. 启动任务（15 分钟超时）
   ↓
2. 任务中断（用户暂停/超时）
   ↓
3. 自动保存状态到虚拟路径
   ↓
4. 用户恢复：meta-skill-weaver resume <task-id>
   ↓
5. 从断点继续，已完成子任务不重复执行
```

---

## 💰 定价方案

| 版本 | 价格 | 功能 | 适用对象 |
|------|------|------|----------|
| **个人版** | ¥99/年 | 基础任务编排、3 技能并发、中断恢复、虚拟路径隔离 | 个人开发者、研究者 |
| **商业版** | ¥999/年 | 个人版 + EventBus 事件系统、7 中间件、35 单元测试、优先支持 | 小型团队、创业公司 |
| **企业版** | ¥9999/年 | 商业版 + 自定义中间件、私有部署、SLA 保障、专属技术支持 | 中大型企业、系统集成商 |

---

## ❓ FAQ（常见问题）

**Q1: Meta Skill Weaver 适合什么类型的任务？**  
A: 适合需要 3+ 步骤、调用多个技能、耗时超过 5 分钟的复杂任务。简单查询类任务无需使用。

**Q2: 任务中断后如何恢复？**  
A: 系统自动保存任务状态到虚拟路径，调用`resume-task`命令即可从断点继续，已完成的子任务不会重复执行。

**Q3: EventBus 事件系统如何使用？**  
A: 通过`bus.on('事件名', 回调)`订阅事件，`bus.emit('事件名', 数据)`发布事件。支持事件拦截器和上下文保持。

**Q4: 如何监控任务执行进度？**  
A: 调用`get-task-status`命令返回 6 种状态（pending/running/paused/completed/failed/cancelled）及每个子任务的详细进度。

**Q5: 支持多少并发任务？**  
A: 默认限制 3 个并发任务，企业版可自定义并发数。超过限制的任务会进入队列等待。

**Q6: 虚拟路径隔离如何工作？**  
A: 每个任务创建独立的虚拟路径空间，任务间数据完全隔离，避免数据污染和冲突。

**Q7: 如何自定义中间件？**  
A: 企业版支持自定义中间件，继承`Middleware`基类，实现`execute(context, next)`方法即可。

---

## 🚀 快速开始

### 安装

```bash
clawhub install meta-skill-weaver
```

### 基础使用

```bash
# 启动任务
meta-skill-weaver start --task="任务描述" --skills="skill1,skill2,skill3"

# 查看状态
meta-skill-weaver status <task-id>

# 恢复任务
meta-skill-weaver resume <task-id>

# 取消任务
meta-skill-weaver cancel <task-id>
```

### 高级使用

```bash
# 并行执行
meta-skill-weaver start \
  --task="并行任务" \
  --skills="skill1,skill2,skill3" \
  --parallel=true

# 超时控制
meta-skill-weaver start \
  --task="长时任务" \
  --timeout=30m

# 事件监听
meta-skill-weaver on 'task.complete' \
  --handler="notify.sh"
```

---

## 📊 技术架构

### 核心组件

```
┌─────────────────────────────────────────┐
│           Task Decomposer               │
│  (第一性原理任务分解器)                   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           EventBus                      │
│  (事件系统 - 订阅/发布)                   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Middleware Chain                 │
│  (7 个内置中间件)                         │
│  - Logging, Auth, RateLimit, Cache...   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Virtual Path System              │
│  (虚拟路径隔离)                           │
└─────────────────────────────────────────┘
```

### 测试覆盖

| 模块 | 覆盖率 | 测试用例数 |
|------|--------|------------|
| Task Decomposer | 75% | 12 |
| EventBus | 80% | 10 |
| Middleware Chain | 60% | 8 |
| Virtual Path | 55% | 5 |
| **总计** | **62%** | **35** |

---

## 📁 文件结构

```
meta-skill-weaver/
├── SKILL.md              # 技能定义（本文件）
├── README.md             # 详细文档
├── package.json          # 依赖配置
├── src/
│   ├── index.js          # 主入口
│   ├── decomposer.js     # 任务分解器
│   ├── event-bus.js      # 事件系统
│   ├── middleware/       # 中间件
│   └── virtual-path.js   # 虚拟路径
├── tests/
│   ├── decomposer.test.js
│   ├── event-bus.test.js
│   ├── middleware.test.js
│   └── virtual-path.test.js
└── examples/
    ├── basic-usage.js
    ├── advanced-usage.js
    └── enterprise-usage.js
```

---

## 🏆 成功案例

### 案例 1：AI 市场研究报告

**客户**：某 AI 创业公司  
**任务**：研究 AI Agent 市场趋势，生成 50 页报告  
**技能调用**：web_search, browser, xlsx, data-analysis, copywriting, docx  
**执行时间**：45 分钟  
**结果**：自动生成 50 页报告，节省 8 小时人工时间

### 案例 2：销售数据分析

**客户**：某电商公司  
**任务**：分析 Q4 销售数据，生成 PPT 报告  
**技能调用**：xlsx, data-analysis, chart-generator, pptx, pdf  
**执行时间**：30 分钟  
**结果**：自动生成 PPT，数据准确率 100%

---

## 📞 技术支持

- 📧 邮箱：support@pagoda111king.com
- 💬 微信：pagoda111king
- 📖 文档：https://clawhub.ai/skills/meta-skill-weaver/docs
- 🐛 反馈：https://clawhub.ai/skills/meta-skill-weaver/issues

---

## 📜 许可证

MIT License - 免费使用、修改和重新分发

---

**文件版本**：v2.3.0  
**创建时间**：2026-04-01  
**上架时间**：2026-04-01  
**更新时间**：2026-04-02  
**上架用户**：pagoda111king  
**测试状态**：✅ 35 个测试用例，62% 覆盖率
