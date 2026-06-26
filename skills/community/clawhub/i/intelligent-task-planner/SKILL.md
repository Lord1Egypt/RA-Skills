---
name: intelligent-task-planner
version: 6.0.0-final
description: |
  智能任务规划器 - 高度自主的AI任务自动化引擎
  Auto-Skill Orchestrator with 152 task types
author: ethvs
license: MIT
repository: https://github.com/ethvs/Intelligent-Task-Planner
homepage: https://github.com/ethvs/Intelligent-Task-Planner#readme
bugs: https://github.com/ethvs/Intelligent-Task-Planner/issues

# ClawHub 发布信息
clawhub:
  namespace: ethvs
  name: intelligent-task-planner
  display_name: "Intelligent Task Planner"
  short_description: "智能任务规划器 - 自动识别意图并调度技能执行"
  icon: 🤖
  color: "#4A90D9"
  pricing: free
  visibility: public

# 技能分类
category: automation
tags:
  - task-planner
  - intent-recognition
  - skill-orchestrator
  - automation
  - ai-assistant
  - openclaw-compatible

# 入口配置
entry:
  file: index.js
  function: analyze

# 导出接口
exports:
  - name: analyze
    description: 完整分析并执行用户任务
    params:
      - name: userInput
        type: string
        required: true
      - name: context
        type: object
        required: false
    returns: object
  - name: recognize
    description: 快速意图识别
    params:
      - name: userInput
        type: string
        required: true
    returns: object
  - name: getSupportedTasks
    description: 获取所有支持的任务类型
    returns: array
  - name: getTaskDetails
    description: 获取任务详情
    params:
      - name: taskType
        type: string
        required: true
    returns: object
  - name: validateConfig
    description: 验证系统配置
    returns: object
  - name: batchAnalyze
    description: 批量分析多个任务
    params:
      - name: inputs
        type: array
        required: true
    returns: array

# 技能依赖
dependencies:
  - node: ">=14.0"

# 可选技能集成
# ITP 会自动识别任务所需技能，并从以下渠道查找和调用：
# 1. 优先使用全局已安装的技能
# 2. 从 ClawHub 搜索并安装匹配的技能
# 3. 使用内置通用技能作为兜底
optionalSkills: []
# 动态发现 - 无需预配置，ITP 会按需自动匹配

# 配置参数
config:
  autoInstall:
    type: boolean
    default: true
    description: 自动安装缺失技能
  sources:
    type: array
    default: ["clawhub", "github", "openclaw"]
    description: 技能查找来源
  qualityThreshold:
    type: number
    default: 0.85
    description: 质量门控阈值
  maxSteps:
    type: number
    default: 20
    description: 最大执行步骤
  timeoutMinutes:
    type: number
    default: 30
    description: 任务超时时间

# 触发条件
triggers:
  - type: intent
    patterns:
      - ".*"
    description: 所有自然语言输入

# 性能指标
metrics:
  taskTypes: 152
  keywords: 1325
  avgConfidence: 99.1
  responseTime: "0.27ms"

# 支持的语言
languages:
  - zh-CN
  - en-US

# 文档
documentation:
  readme: README.md
  skill: SKILL.md
  api: docs/API.md
  changelog: docs/CHANGELOG.md

# 测试
test:
  command: "node test/comprehensive-test.js"

# 强制模式配置 (解决不触发/不执行问题)
force_mode:
  enabled: true
  priority: 1000                    # 最高优先级
  exclusive: true                   # 独占模式，匹配后阻止其他技能
  intercept_all: true               # 拦截所有输入
  min_confidence: 0.85              # 最低置信度阈值
  fallback_action: "reject"         # 不达标时拒绝执行
  agent_override:                   # Agent级别覆盖
    override_system_prompt: true    # 覆盖系统提示词
    require_planning: true          # 强制要求规划
    enforce_skill_chain: true       # 强制执行技能链
  hook_config:
    pre_processing: true            # 预处理钩子
    post_processing: true           # 后处理钩子
    on_plan_fail: "stop"            # 规划失败时停止
---

<!-- CLAWHUB-BADGES-START -->
[![Version](https://img.shields.io/badge/version-6.0.0--final-blue.svg)](https://github.com/ethvs/Intelligent-Task-Planner)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ethvs/Intelligent-Task-Planner/blob/main/LICENSE)
[![Tasks](https://img.shields.io/badge/任务类型-152种-orange.svg)](https://github.com/ethvs/Intelligent-Task-Planner)
[![Confidence](https://img.shields.io/badge/识别率-99.1%25-brightgreen.svg)](https://github.com/ethvs/Intelligent-Task-Planner)
<!-- CLAWHUB-BADGES-END -->

# Intelligent Task Planner v6.0.0-final

> **ClawHub 技能 ID**: `ethvs/intelligent-task-planner`

**智能任务规划器** - 高度自主的AI任务自动化引擎

---

## 技能描述

自动分析用户任务意图，智能匹配并调度所需技能，自主规划执行路径，全程质量把控，无需用户指定具体工具或方法。

用户只需用自然语言描述需求，系统自动完成：意图识别 → 技能匹配 → 路径规划 → 质量验证 → 结果交付的全流程闭环。

---

## 版本信息

- **版本**: 6.0.0-final
- **任务类型**: 152种
- **关键词覆盖**: 1325+
- **平均识别率**: 99.1%
- **响应时间**: 0.27ms

---

## 触发条件

当用户提出任务但未指定具体工具/方法时自动激活：

### 创作类任务
- 写小说、写文章、生成内容、创作故事
- 设计角色、构建世界观、润色内容

### 查询分析类
- 查天气、查新闻、搜索信息
- 数据分析、图表生成、趋势预测

### 技术开发类
- Python/JavaScript/Java/C++代码
- 网站开发、APP开发、脚本生成
- 图片生成、视频处理

### 商业规划类
- 商业计划书、营销策划、财务规划
- 数据分析、市场调研、学术研究

### 生活服务类
- 旅行计划、学习规划、健身计划
- 菜谱烹饪、穿搭建议、情感咨询

### 其他任务
- 文件处理、文档编辑、任务管理
- PPT生成、思维导图、翻译等

---

## 核心能力

### 1. 三层关键词意图识别
- **第一层**: 动词意图识别 (写/分析/查/设计)
- **第二层**: 目标对象识别 (小说/代码/数据/图片)
- **第三层**: 修饰词精细化 (玄幻/Python/学术)

### 2. 多维度置信度评分
- 位置权重、长度权重、组合加成
- 短语权重、多关键词奖励
- 默认识别准确率: 99.1%

### 3. 四层技能链执行
```
TIER 1: 需求分析与资料收集
TIER 2: 核心内容创建
TIER 3: 质量提升 (去AI感、润色、审阅)
TIER 4: 输出交付 (格式化、导出)
```

### 4. 质量门控验证
```
完整性检查 ≥85%
逻辑一致性验证
AI感检测 ≤15%
流畅度评估
风格一致性检查
格式规范审查
```

### 5. OpenClaw/ClawHub技能生态
- 自动匹配OpenClaw官方技能
- 集成ClawHub社区技能
- 支持技能下载与安装
- 相似技能替代推荐

### 6. 透明度执行报告
执行前完整告知用户：
```
📋 任务执行计划
━━━━━━━━━━━━━━━━━━━━━━━
任务类型: creative_writing_novel
置信度: 100%
识别技能: 6个
执行顺序:
  1. outline_creation (大纲创建)
  2. character_design (角色设计)
  3. world_building (世界观构建)
  4. chapter_writing (章节撰写)
  5. content_polishing (内容润色)
  6. final_review (最终审阅)
质量门控: 3个检查点
━━━━━━━━━━━━━━━━━━━━━━━
```

### 7. 多轮对话记忆
- 会话上下文保持
- 模糊请求追问
- 超大型任务分阶段执行

---

## 使用方式

### 方式1: ClawHub安装
```bash
clawhub install ethvs/intelligent-task-planner
```

### 方式2: NPM安装
```bash
npm install ethvs/intelligent-task-planner
```

### 方式3: 直接使用
```javascript
const { analyze, recognize } = require('intelligent-task-planner');

// 完整分析并执行
const result = await analyze('帮我写一部玄幻小说');

// 快速意图识别
const intent = recognize('分析一下销售数据');
```

---

## 配置参数详解

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| autoInstall | boolean | true | 自动安装缺失技能 |
| sources | array | ["clawhub", "github", "openclaw"] | 技能查找来源 |
| qualityThreshold | number | 0.85 | 质量门控阈值(0-1) |
| maxSteps | number | 20 | 最大执行步骤数 |
| timeoutMinutes | number | 30 | 任务超时时间(分钟) |
| requireConfirmation | boolean | false | 是否需要用户确认 |
| enableSkillChain | boolean | true | 是否启用技能链 |
| qualityGate | boolean | true | 是否启用质量门控 |
| maxIterations | number | 3 | 最大迭代优化次数 |

---

## 导出接口

| 接口名 | 说明 |
|--------|------|
| `analyze(userInput, context)` | 完整分析并执行用户任务 |
| `recognize(userInput)` | 快速意图识别 |
| `getSupportedTasks()` | 获取所有支持的任务类型 |
| `getTaskDetails(taskType)` | 获取任务详情 |
| `validateConfig()` | 验证系统配置 |
| `batchAnalyze(inputs)` | 批量分析多个任务 |

---

## 依赖

- Node.js ≥ 14.0
- 可选: clawhub CLI (技能安装)
- 可选: openclaw CLI (官方技能)

---

## 示例

### 示例1: 小说创作
```
用户: 帮我写一部玄幻小说，主角废材逆袭
系统:
  → 识别: creative_writing_novel (100%)
  → 匹配: 从已安装技能/ClawHub 动态查找写作类技能
  → 规划: 6个技能节点，4阶段执行
  → 执行: 大纲→角色→世界观→章节→润色→审阅
  → 交付: 完整小说文档
```

### 示例2: 数据分析
```
用户: 分析一下这个季度的销售数据
系统:
  → 识别: data_analysis (100%)
  → 匹配: data-analyzer, chart-generator
  → 规划: 4个技能节点
  → 执行: 数据加载→清洗→分析→可视化→报告
  → 交付: 数据分析报告 + 图表
```

### 示例3: Python脚本
```
用户: 生成一个Python脚本来处理JSON数据
系统:
  → 识别: code_python (100%)
  → 匹配: python-coder, code-generator
  → 规划: 5个技能节点
  → 执行: 需求分析→代码设计→编写→测试→交付
  → 交付: 可运行Python脚本
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `index.js` | 统一入口，导出analyze/recognize等接口 |
| `src/planner.js` | 主规划器，负责任务解析与编排 |
| `src/intent-analyzer.js` | 意图识别引擎 |
| `src/mega-analyzer.js` | 百任务分析器，152种任务识别 |
| `src/skill-matcher.js` | OpenClaw/ClawHub技能匹配器 |
| `src/executor.js` | 任务执行与质量验证引擎 |
| `config/ultimate-mappings.json` | 终极任务-技能映射配置 |

---

## ClawHub 安装与配置

### 安装

```bash
# 通过 ClawHub CLI 安装
clawhub install ethvs/intelligent-task-planner

# 或通过 OpenClaw CLI 安装
openclaw skill install ethvs/intelligent-task-planner
```

### Agent 配置（强制触发模式）

在 Agent 的 `agents.md` 文件中添加以下配置，确保 ITP 技能被强制触发：

```yaml
# agent.yaml 或 agents.md
name: your-agent-name

skills:
  - ethvs/intelligent-task-planner  # 必须放在第一个，确保最高优先级
  # 执行技能由 ITP 动态发现，无需手动列出

system_prompt: |
  你是由 Intelligent Task Planner (ITP) 驱动的智能 Agent。
  
  ## 核心规则 (必须遵守):
  1. 所有用户输入必须先通过 ITP 进行意图分析和任务规划
  2. 未经 ITP 规划的任务不得直接执行
  3. 严格按照 ITP 返回的 skill_chain 顺序调用技能

# 触发配置（强制 ITP 优先）
intent:
  default_skill: ethvs/intelligent-task-planner
  priority:
    ethvs/intelligent-task-planner: 1000  # 最高优先级
  exclusive_mode: true                      # 独占模式
  intercept_all: true                      # 拦截所有输入

triggers:
  - skill: ethvs/intelligent-task-planner
    patterns: [".*"]
    min_confidence: 0.85

execution:
  follow_plan: true
  allow_skip_planning: false
  enforce_skill_chain: true
```

### 验证安装

```bash
# 验证配置
openclaw agent validate

# 测试触发
openclaw agent test --agent your-agent-name --input "帮我写一部玄幻小说"
# 预期输出: 显示 ITP 分析和技能调用流程
```

---

## License

MIT License © 2026
