---
name: multi-agent-orchestrator
description: 多代理编排引擎 - 目标驱动的深度研究与项目协作系统。支持任务分解、分支执行、验证审核、返工迭代、智能决策。遵循第一性原理，实现主代理与分支代理的双向通信。触发词：多代理、multi-agent、代理编排、深度研究、目标分解、任务委派、工作流、agent orchestrate、multi agent
user-invocable: true
---

# 多代理编排引擎 v8.0 (Multi-Agent Orchestrator)

> **v8.0 核心变更**: Tokens消耗优化（节省25-30%）+ 强约束JSON输出 + 失败边界机制

## v8.0 新增功能

### 🎯 Tokens优化（第一阶段完成）
- **提示词精简**: 从 ~800行 → ~80行（减少90%）
- **JSON强约束输出**: 提升流程遵循性，降低输出不确定性
- **失败边界机制**: skip/fallback/partial/retry 四种策略
- **精简版执行引擎**: `executorLite.js` 可选使用

### 使用方式
```bash
# 精简版（默认JSON输出，节省25-30% tokens）
多代理 run_lite --goal "研究主题"

# 完整版（Markdown输出，向后兼容）
多代理 run --goal "研究主题"
```

### Tokens节省估算
| 输出模式 | 提示词行数 | 预计节省 | 适用场景 |
|---------|-----------|----------|----------|
| JSON | ~80行 | 25-30% | 结构化研究、数据提取 |
| Markdown | ~400行 | 10-15% | 深度报告、叙事分析 |

## 环境依赖

| 依赖 | 最低版本 | 说明 |
|------|----------|------|
| OpenClaw | **2026.3.x+** | 需要 `sessions_spawn`、`subagents`、`sessions_send` API |
| Node.js | 20.x+ | ES Module 支持 |
| 操作系统 | Windows / macOS / Linux | 路径自动适配（`USERPROFILE` / `HOME`） |

**启动前检查**：`多代理 check_env` — 验证 OpenClaw 版本和工具可用性

## 第三方部署说明

### 兼容性保证
- ✅ **路径无关**：所有路径通过 `process.env.USERPROFILE || process.env.HOME` 动态计算
- ✅ **配置驱动**：模型池、代理配置、角色映射均从外部 JSON 读取，无硬编码
- ✅ **跨平台**：纯 Node.js + `path` 模块，Windows/macOS/Linux 兼容
- ✅ **模型自适应**：自动扫描 `openclaw.json` 中的 providers + fallbacks

### 自定义规则（可选）

在 workspace 根目录创建 `.model-selector-rules.json` 覆盖启发式推断：

```json
{
  "traits": {
    "your-provider/special-model": ["analysis", "research"],
    "another-provider/code-model": ["coding"]
  },
  "tiers": {
    "your-provider/paid-model": "standard",
    "your-provider/free-model": "free"
  },
  "boost": {
    "your-provider/premium-model": 20
  }
}
```

### 不降级策略

本系统**不提供降级方案**。如果环境检查失败（`check_env` 返回错误），说明 OpenClaw 版本过低或缺少必需 API，必须升级 OpenClaw 到 2026.3.x+ 才能使用。

## 🎯 命令使用

### 如何调用命令

本技能支持通过以下方式调用命令：

**方式 1：通过触发词**
```
用户: 多代理 check_env
用户: 多代理 help
用户: 多代理 plan --goal "研究固态电池"
```

**方式 2：通过技能命令**（推荐）
```
用户: /skill multi-agent-orchestrator check_env
用户: /skill multi-agent-orchestrator help
```

### 可用命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `help` | 显示帮助信息 | `多代理 help` |
| `check_env` | 检查环境配置 | `多代理 check_env` |
| `list_profiles` | 列出代理配置 | `多代理 list_profiles` |
| `list_workflows` | 列出工作流 | `多代理 list_workflows` |
| `validate_config` | 验证配置完整性 | `多代理 validate_config` |
| `show_profile` | 显示代理详情 | `多代理 show_profile Research_Analyst` |
| `show_workflow` | 显示工作流详情 | `多代理 show_workflow default` |
| `archive` | 归档工作流产出物 | `多代理 archive` |
| `clean` | 清理临时文件 | `多代理 clean` |
| `run` | 一键启动工作流 | `多代理 run --goal "研究主题"` |
| `plan` | 获取执行计划(JSON) | `多代理 plan --goal "研究主题"` |
| `run_demo` | 快速演示 | `多代理 run_demo` |

### 命令参数

- `--goal "描述"` — 任务目标描述
- `--workflow <名称>` — 指定工作流（可选，默认使用 default）
- `--dry_run` — 干运行模式（仅 clean 命令）

### 完整工作流示例

```bash
# 1. 检查环境
多代理 check_env

# 2. 查看可用代理
多代理 list_profiles

# 3. 查看工作流
多代理 list_workflows

# 4. 执行任务
多代理 run --goal "2026年中国固态电池产业发展现状研究"

# 5. 归档清理
多代理 archive_and_clean
```

## 概述

目标驱动的深度研究与项目协作系统，通过 `sessions_spawn` 实现多代理并行执行。

```
提纲确认 → 复杂度评估 → 路由 → plan → 并行执行 → 收集验证 → 重试/降级 → Critic审核 → 聚合 → 完成
```

## 📋 配置检查（首次使用必做）

### 配置检查流程

**多代理引擎在启动前会自动检查以下配置项**：

1. **OpenClaw 版本** ≥ 2026.3.x
2. **Node.js 版本** ≥ 20.5
3. **工作区目录结构**（详细检查以下目录）
4. **代理配置**（至少 1 个代理配置）
5. **工作流配置**（默认工作流）
6. **模型配置**（可用的模型池）

### 📁 工作区目录检查

系统会详细检查以下目录及其作用：

| 目录 | 必需 | 作用说明 | 缺失影响 |
|------|------|----------|----------|
| **工作区根目录** | ✅ | OpenClaw 工作区根目录，存放所有配置和输出文件 | 系统无法运行 |
| **agents/ 代理工作区** | ✅ | 各代理的独立工作区，每个代理有自己的历史研究子目录 | 子代理无法存放过程文件，任务失败 |
| **shared/ 共享输出目录** | ✅ | 共享输出根目录，存放所有研究的共享文件 | 研究成果无法共享和保存 |
| **shared/researches/ 研究目录** | ✅ | 研究任务目录，按任务名称和时间戳组织研究目录 | 不同研究任务无法隔离 |
| **shared/final/ 最终输出目录** | ✅ | 最终报告目录，存放所有研究的最终报告 | 最终报告无法保存和查看 |
| **.cache/ 缓存目录** | ⚠️ | 缓存目录，用于存储临时文件和缓存数据 | 性能可能受影响 |
| **logs/ 日志目录** | ⚠️ | 日志目录，用于存储系统运行日志 | 调试信息无法保存 |

### 配置检查结果

- **✅ 全部通过**：直接开始执行任务
- **⚠️ 有警告**：提示可选配置项，但继续执行
- **❌ 有错误**：生成详细配置指南，等待用户确认后自动配置

### 自动配置说明

如果检测到必需配置缺失，系统会：

1. **生成详细配置指南**：列出每个缺失目录的路径、作用、缺失影响
2. **等待用户确认**：用户清楚了解每个目录的作用后同意自动配置
3. **自动完成配置**：创建所有必需目录和配置文件
4. **继续执行**：配置完成后自动开始多代理任务

### 配置检查示例

```
多代理 run --goal "研究人工智能在医疗领域的应用前景"

📋 多代理编排引擎 - 配置检查报告
══════════════════════════════════════════════════════════════

## 📊 配置概览
- 总检查项: 6
- ✅ 通过: 3
- ⚠️  警告: 0
- ❌ 错误: 3

## ❌ 需要修复的配置 (3 项)

### 代理配置
- 当前状态: 未配置
- 要求: 必需
- 说明: 配置文件不存在
  📋 目录作用: 代理配置文件，定义每个代理的角色、职责和能力
  ⚠️  影响说明: 没有配置文件，多代理系统无法识别和启动任何子代理
  🔧 需要自动创建此配置文件才能运行多代理系统

### agents/ 代理工作区
- 当前状态: 未配置
- 要求: 必需
- 说明: 目录不存在
  📋 目录作用: 各代理的独立工作区，每个代理有自己的历史研究子目录
  ⚠️  影响说明: 没有代理工作区，子代理无法存放过程文件，会导致任务失败
  🔧 需要自动创建代理工作区才能运行多代理系统

### shared/final/ 最终输出目录
- 当前状态: 未配置
- 要求: 必需
- 说明: 目录不存在
  📋 目录作用: 最终报告目录，存放所有研究的最终报告
  ⚠️  影响说明: 没有最终输出目录，研究成果无法保存和查看
  🔧 需要自动创建最终输出目录才能运行多代理系统

## 🔧 自动配置选项

如果同意自动配置，系统将执行以下操作：

### 1. 创建 代理配置
**路径**: .multi-agent-profiles.json
**作用**: 代理配置文件，定义每个代理的角色、职责和能力
**影响**: 必需文件，用于配置多代理系统中的各个子代理
**操作**: 创建包含 4 个默认代理的配置文件

### 2. 创建 agents/ 代理工作区
**路径**: agents/
**作用**: 各代理的独立工作区，每个代理有自己的历史研究子目录
**影响**: 必需目录，为每个代理创建独立的工作空间
**操作**: 创建 agents/ 目录以及各个代理的子目录

### 3. 创建 shared/final/ 最终输出目录
**路径**: shared/final/
**作用**: 最终报告目录，存放所有研究的最终报告
**影响**: 必需目录，用于存放最终研究成果
**操作**: 创建最终输出目录结构

[等待用户确认...]

🔧 开始自动配置...
  → 代理配置: 创建配置文件
     ✅ 已完成
  → agents/ 代理工作区: 创建目录结构
     ✅ 已完成
  → shared/final/ 最终输出目录: 创建目录
     ✅ 已完成

✅ 配置完成！

✅ 配置完成，开始执行多代理任务...
```

### 🤔 用户疑虑解答

**Q**: 为什么需要这么多目录？
**A**: 这是多代理系统的架构设计，确保：
1. **代理隔离** - 每个代理独立工作，不互相影响
2. **文件组织** - 按研究、代理、输出类型分类存储
3. **可追溯性** - 历史研究记录可随时查看

**Q**: 目录创建后会影响现有文件吗？
**A**: 不会，系统只会创建缺失的目录，不会修改或删除现有文件

**Q**: 可以手动创建这些目录吗？
**A**: 可以，但建议使用自动配置功能，确保目录结构完全正确

## 🔴 铁律（不可违反）

1. **质量优先**：质量 > 速度。未经用户明确确认，不得以任何理由降低标准、裁剪流程、省略审核
2. **流程不可跳跃**：6 个 Phase 必须按顺序执行，Critic 审核为强制门禁，不可跳过
3. **看板强制输出**：每个阶段完成后必须调用看板函数并展示给用户
4. **聚合不可省略**：即使 100% 成功也必须执行聚合

## 核心能力

- **📋 提纲确认门**（v6 新增）——用户提交目标后，主代理先生成研究提纲，用户确认后才启动协同流程
- **复杂度路由**：简单任务直接完成，中等任务主代理+验证，复杂任务完整多代理并行
- **异构模型分配**：按角色+复杂度自动选择最优模型，同批次不重复
- **增强重试**：区分 6 种错误类型（超时/API错误/空输出/文件缺失/质量不合格/崩溃），针对性重试
- **双看板系统**（v6 新增）——计划看板（Plan）+ 执行看板（Execution），含调用模型/Tokens/文件验证
- **降级协议**：60%成功→主代理补做，30%→重试，<30%→全接管
- **返工机制**：Critic 审核不通过时，自动触发子代理返工循环
- **输出分层**（v6 新增）——按「研究任务/版本/交付物」三级目录隔离，不同任务互不干扰
- **归档清理**：工作流完成后一键归档产出物 + 清理临时文件

## 🛡️ 子代理状态监控（v8.1 新增）

### 子代理完成检查函数

```javascript
/**
 * 检查子代理状态，检测交互消息
 * @param {string} childSessionKey - 子代理会话 Key
 * @param {number} recentMinutes - 最近多少分钟内的会话
 * @returns {Promise<{hasInteraction: boolean, message?: string}>}
 */
async function checkSubagentStatus(childSessionKey, recentMinutes = 120) {
  const result = await subagents({
    action: "list",
    recentMinutes: recentMinutes
  });
  
  const childSession = result.recent.find(s => s.sessionKey === childSessionKey);
  
  if (!childSession) {
    return { hasInteraction: false };
  }
  
  // 检查是否有交互消息
  const interactionKeywords = [
    "是否需要",
    "请确认",
    "是否继续",
    "是否完成",
    "是否承担",
    "Do you need",
    "Please confirm",
    "Should I continue"
  ];
  
  const messages = childSession.messages || [];
  const interactionMessage = messages.find(msg => 
    interactionKeywords.some(keyword => msg.body.includes(keyword))
  );
  
  if (interactionMessage) {
    return { 
      hasInteraction: true, 
      message: interactionMessage.body 
    };
  }
  
  return { hasInteraction: false };
}
```

### 使用示例

```javascript
// 在等待完成事件时，定期检查子代理状态
async function waitForCompletionWithInteraction(childSessionKey, timeoutMs = 3600000) {
  const startTime = Date.now();
  const pollInterval = 30000; // 每 30 秒检查一次
  
  while (Date.now() - startTime < timeoutMs) {
    // 检查是否有交互消息
    const status = await checkSubagentStatus(childSessionKey, 120);
    
    if (status.hasInteraction) {
      // 收到交互消息，立即处理
      console.log("收到子代理交互消息：", status.message);
      // 立即回复，不要等待完成事件
      return { type: "interaction", message: status.message };
    }
    
    // 等待 30 秒后再次检查
    await new Promise(resolve => setTimeout(resolve, pollInterval));
  }
  
  // 超时，返回完成事件
  return { type: "completion" };
}
```

### 交互消息关键词库

**中文关键词**：
- "是否需要"
- "请确认"
- "是否继续"
- "是否完成"
- "是否承担"
- "需要我..."
- "我已完成..."

**英文关键词**：
- "Do you need"
- "Please confirm"
- "Should I continue"
- "Should I complete"
- "Do you want me to"
- "I have completed"
- "Can I continue"

### 监控规则

1. **定期检查**：在等待完成事件时，每 30 秒检查一次子代理状态
2. **立即处理**：如果检测到交互消息，立即回复，不要等待完成事件
3. **超时保护**：如果 1 小时内未收到完成事件也未收到交互消息，触发超时保护
4. **记录日志**：记录交互消息内容，便于后续分析

## 快速开始

### 一键启动

```
多代理 run --goal "研究人工智能在医疗领域的应用前景"
```

### 模型配置（首次使用必做）

```
多代理 setup                   # 查看当前配置
多代理 setup_recommended       # 查看基于模型库的推荐配置
多代理 setup_confirm           # 确认并保存推荐配置
```

### 高级命令
```
多代理 check_env               # 检查 OpenClaw 版本和工具可用性（首次启动必做）
多代理 thinking_capabilities   # 查看模型 Thinking 支持矩阵
多代理 check_changes           # 检测模型池变更
```

### 分步执行

```
多代理 plan --goal "目标"       # 生成 JSON 执行计划
多代理 dashboard                # 查看任务看板
多代理 model_pool               # 查看可用模型池
多代理 archive --workflow_id X  # 归档产出物
```

## 执行流程

```
用户提交目标
  ↓
Phase 0: 提纲确认 ← 展示研究提纲 → 用户确认/修改/取消
  ↓
Phase 1: plan → 生成执行计划 + 计划看板
  ↓
Phase 2: spawn → 并行启动子代理 → 等待完成事件 + 监听交互消息
  ↓
Phase 3: collect → 检查文件 → 评估 → 降级/继续
  ↓
Phase 4: critic → Critic 审核 → 通过/返工
  ↓
Phase 5: aggregate → 融合为 FINAL_REPORT.md
  ↓
Phase 6: finalize → 输出执行摘要
```

### Phase 2 子代理监控规则（v8.1 修复）

**等待完成事件时，必须同时监听交互消息**：

1. **等待完成事件**：子代理任务完成后会推送完成通知
2. **监听交互消息**：子代理可能发送需要主代理决策的消息
3. **立即处理交互消息**：如果收到交互消息，立即回复，不要等待完成事件

**错误示例（v8.0）**：
```
# 等待完成事件到达...
# 忽略子代理发送的交互消息
# 结果：子代理等待回复，主代理不知道
```

**正确示例（v8.1）**：
```
# 等待完成事件到达，同时监听交互消息
if (收到交互消息) {
  # 立即回复
  replyToSubagent("收到，继续完成...");
}
# 所有任务完成后，输出最终答案
```

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    主代理 (Coordinator)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ 提纲确认  │  │ 结果验证  │  │ 降级补做  │  │ 聚合  │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
└────────┬────────────────────────────────────────────────┘
         │ sessions_spawn
  ┌──────▼──────┐ ┌───────────┐ ┌───────────┐ ┌─────────┐
  │  Research   │ │ Technical │ │ Strategy  │ │ Critic  │
  │  _Analyst   │ │ Specialist│ │ _Analyst  │ │ (独立)  │
  └─────────────┘ └───────────┘ └───────────┘ └─────────┘
         │              │              │              │
         └──────────────┴──────────────┴──────────────┘
         shared/researches/{slug}_{date}/v{n}/
```

## 输出目录结构

```
shared/
├── boards/                          # 看板 JSON
│   ├── wf_xxx_plan.json
│   └── wf_xxx_exec.json
├── researches/                      # 按研究任务隔离
│   ├── ev-overseas_20260403/       # ← 任务A
│   │   ├── v1/                      #   第一轮
│   │   │   ├── Research_Analyst_report.md
│   │   │   ├── Technical_Specialist_report.md
│   │   │   ├── Strategy_Analyst_report.md
│   │   │   └── Critic_report.md
│   │   ├── v2/                      #   返工轮
│   │   │   ├── Research_Analyst_report_v2.md
│   │   │   └── ...
│   │   └── final/                   #   最终交付物
│   │       └── FINAL_REPORT.md
│   └── ai-healthcare_20260405/     # ← 任务B（完全隔离）
└── archive/                          # 归档目录
```

## 命令速查

| 命令 | 说明 |
|------|------|
| `plan --goal "X"` | 生成 JSON 执行计划 + 看板 |
| `run --goal "X"` | 生成执行计划 + 文本指南 |
| `dashboard [--workflow_id X]` | 查看任务看板 |
| `model_pool` | 查看可用模型池 |
| `diagnose --result "X"` | 诊断失败原因 |
| `archive --workflow_id X` | 归档产出物 |
| `clean [--dry_run true]` | 清理临时文件 |
| `archive_and_clean --workflow_id X` | 一键归档+清理 |

**代理管理：** `list` / `create` / `template --type research|technical|critical|coordinator|advocate|developer`

**工作流：** `workflow_list`

**验证/聚合/决策：** `validate` / `aggregate` / `decide` / `generate_prompt` / `generate_feedback`

## 与 OpenClaw 工具的配合

本技能提供配置、验证、聚合、决策等能力，实际的代理执行使用 OpenClaw 内置工具：

```
# 创建子代理（主代理的核心调用）
sessions_spawn --task "子任务描述" --runtime subagent --mode run

# 查看子代理状态
subagents --action list

# 向子代理发送消息（向目标会话发送）
sessions_send --sessionKey "目标会话Key" --message "指令"
```

### ⚠️ 交互消息处理机制（v8.1 修复）

**重要区别**：

| 消息类型 | 推送机制 | 处理规则 | 示例 |
|---------|---------|---------|------|
| **完成事件** | push-based | 等待所有完成事件到达后输出最终答案 | "任务完成：02_hermes_analysis_v2.md" |
| **交互消息** | push-based | **立即回复**，不要等待完成事件 | "我的部分已完成。关于 X 任务，是否需要我继续完成？" |

**交互消息特征**：
- 以询问句结尾（"是否需要..."、"请确认..."、"是否继续..."）
- 需要主代理做出决策或提供指令
- 不是任务完成通知，而是需要主代理介入

**处理规则**：
1. 等待完成事件到达 → 所有任务完成后输出最终答案
2. 如果收到交互消息 → **立即回复**，不要等待完成事件
3. 交互消息通常以询问句结尾，需明确给出决策

**交互消息示例**：
```
I'm the Research_Analyst_2 subagent and have already completed my deliverable: `02_hermes_analysis_v2.md`.

My part is done. About `03_metrics_comparison_v2.md` (评分标准重构), that was originally assigned to another subagent (Technical_Specialist). Do you need me to continue with that?
```

**响应示例**：
```
收到，继续完成 Technical_Specialist 的任务：03_metrics_comparison_v2.md

**任务要求**:
1. 读取 `shared/researches/openclaw-hermes-comparison_20260419/v1/01_openclaw_analysis.md`
2. 读取 `memory/2026-04-*.md` 提取真实统计数据
3. 重新制定 8 维度评分标准
4. 输出：`shared/researches/openclaw-hermes-comparison_20260419/v2/03_metrics_comparison_v2.md`

开始执行！
```

## 配置存储

- 代理配置: `.multi-agent-profiles.json`
- 工作流状态: `.multi-agent-workflows.json`

## 详细文档

- **运行时操作协议**：见 [references/protocols.md](references/protocols.md)（提纲确认、复杂度评估、超时预设、降级协议、看板体系、分层目录等完整规范）
