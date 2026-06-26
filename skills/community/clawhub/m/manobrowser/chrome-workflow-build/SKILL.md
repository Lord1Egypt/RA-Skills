---
name: chrome-workflow-build
description: 支持双模式生成浏览器自动化Skill：模式1-使用chrome-server MCP工具执行浏览器操作并从成功执行中生成可复用Skill；模式2-将DATASAVER录制工作流.json文件转换为可复用Skill。适用场景：1.自动化重复的浏览器任务（社交媒体发帖、网页抓取、表单填写）2.从浏览器自动化中创建可复用的工作流 3.为特定网站平台操作构建自定义Skill 4.将DATASAVER录制的浏览器操作转换为Claude Skill。
---

# Chrome工作流构建器

## 概述

这是一个元技能（Meta-skill），支持**双模式**将浏览器自动化操作转换为可复用的Claude Skills：

- **模式1（执行并记录）**：通过智能记录、分析和生成，将实时执行的浏览器操作链路转换为Skill
- **模式2（DATASAVER录制转换）**：将DATASAVER录制工作流.json文件分析、验证并转换为Skill

<mandatory-rules>

### 规则1：严格按阶段顺序执行
- **模式1**：阶段1(LOG.md) → 阶段2(WORKFLOW.md) → 阶段3(CREATOR.md)
- **模式2**：阶段1(DATASAVER录制工作流转换模块) → 阶段2(CREATOR.md)
- **禁止跳过任何阶段**，每个阶段必须完整执行后才能进入下一阶段
- **禁止偷懒**：不能只做部分工作就声称完成

### 规则2：中间产物必须生成
每个阶段必须生成对应的输出文件，缺少任何一个都视为阶段未完成：

| 阶段 | 必须生成的文件 |
|------|---------------|
| 模式1-阶段1 | `workflow-logs/[skill-name]-log.json` |
| 模式1-阶段2 | `workflow-workflows/[skill-name]-workflow.json` |
| 模式2-阶段1 | `workflow-workflows/[skill-name]-workflow.json` |
| 最终阶段 | `workflow-skills/[skill-name]/SKILL.md` |

</mandatory-rules>

## 快速开始

本Skill支持**双输入模式**：

### 模式1：执行并记录（适用于新需求）
1. 立即使用chrome-server MCP 提供的工具执行任务
2. 将执行步骤记录到结构化日志并抽取的Workflow
3. 基于Workflow生成可供未来使用的可复用Skill

### 模式2：DATASAVER录制工作流转换（适用于已有DATASAVER录制文件）
1. 提供DATASAVER录制工作流.json文件
2. 分析并验证转换为workflow.json
3. 基于Workflow生成可供未来使用的可复用Skill

## 工作流程

### 模式1：执行并记录流程

#### 阶段1：执行并记录
执行浏览器任务，同时记录每个工具调用和决策。
加载 [LOG.md](LOG.md) 并严格遵循它的指令工作

#### 阶段2：提取工作流（仅在阶段1完成后）
分析执行日志以提取可复用的工作流模式。
加载 [WORKFLOW.md](WORKFLOW.md) 并严格遵循它的指令工作

#### 阶段3：生成Skill（仅在阶段2完成后）
从提取的工作流创建、验证并生成新的Skill。
加载 [CREATOR.md](CREATOR.md) 并严格遵循它的指令工作

### 模式2：DATASAVER录制工作流转换流程

#### 阶段1：DATASAVER录制工作流分析提取workflow
读取DATASAVER录制工作流.json文件，分析、验证并提取为workflow.json。
加载 [DATASAVER.md](DATASAVER.md) 并严格遵循它的指令工作

#### 阶段2：生成Skill
从生成的工作流创建、验证并生成新的Skill。
加载 [CREATOR.md](CREATOR.md) 并严格遵循它的指令工作

## 决策树

```
 用户请求分析
  ├─ 1. 判断输入类型
  │  ├─ 提供DATASAVER录制工作流.json文件? → 模式2: DATASAVER录制工作流转换流程
  │  ├─ 描述浏览器操作需求? → 模式1: 执行并记录流程
  │  └─ 其他 → 不使用此Skill
  │
  ├─ 2. 模式1: 执行并记录流程
  │  │
  │  阶段1：执行并记录（LOG.md）
  │     ↓
  │  【确认点】展示最终执行结果，询问用户是否正确
  │     ├─ 正确 → 进入Skill发现检查
  │     └─ 有问题 → 根据用户反馈调整后重新执行
  │     ↓
  │   Skill发现检查（LOG模式-执行后立即发现）
  │     加载 SKILL_DISCOVERY.md 执行智能发现
  │     ├─ 发现高度匹配Skill（>=90分）→ 强制询问用户 → 等待用户决策
  │     │   ├─ 用户确认"满足需求" → 停止创建流程 + 文字指导使用 → 结束（不保存日志）
  │     │   └─ 用户选择"不满足" → 保存日志 → 继续阶段2和3
  │     └─ 无匹配（<90分）→ 保存日志 → 直接继续阶段2和3（不提示）
  │     ↓
  │  阶段2：提取工作流（WORKFLOW.md）
  │     ↓（自动继续）
  │  阶段3：生成Skill（CREATOR.md）
  │     ↓
  │  完成（包括验证和发布报告，用户确认后保存文件并发布服务端(如果存在skill发布tool)）
  │
  └─ 3. 模式2: DATASAVER录制工作流转换流程
     │
     阶段1：DATASAVER录制工作流分析转换（DATASAVER录制工作流转换模块）
        - 读取DATASAVER录制工作流.json文件
        - 提取description和业务需求
        ↓
     Skill发现检查（DATASAVER模式-读取后立即发现）
        加载 SKILL_DISCOVERY.md 执行智能发现
        ├─ 发现高度匹配Skill（>=90分）→ 强制询问用户 → 等待用户决策
        │   ├─ 用户确认"满足需求" → 停止创建流程 + 文字指导使用 → 结束
        │   └─ 用户选择"不满足" → 继续转换流程
        └─ 无匹配（<90分）→ 直接继续转换流程（不提示）
        ↓
        - 分析并抽取必要步骤
        - 逐步执行验证
        - 生成workflow.json
        ↓
     阶段2：生成Skill（CREATOR.md）
        ↓
     完成（包括验证和发布报告，用户确认后保存文件并发布服务端(如果存在skill发布tool)）
```

### 用户请求识别规则

**模式2（DATASAVER录制工作流转换）触发条件**：
- 用户明确提到"DATASAVER录制文件"或"DATASAVER工作流文件"
- 用户上传DATASAVER录制工作流.json文件（文件名包含.datasaver.json）
- 用户说"我有一个DATASAVER浏览器录制文件"
- 用户提供包含DATASAVER录制数据的文件路径

**模式1（执行并记录）触发条件**：
- 用户描述具体的浏览器操作需求
- 用户说"帮我做..."、"自动化..." 并封装为一个skill
- 用户要求在某个网站执行操作

## 资源结构

此Skill包含以下支持资源：
- **assets/**: 模板文件
  - `log_template.json` - 日志格式模板（模式1）
  - `workflow_template.json` - 工作流格式模板（模式1）
  - `datasaver_workflow_template.json` - DATASAVER录制工作流格式模板（模式2）
- **references/**: 参考文档
  - `EXECUTOR_RULES.md` - 执行规则指导（模式1）
  - `CONTEXT_ISOLATION.md` - 上下文隔离策略（模式1）
  - `FILTER_STEP.md` - 步骤过滤指南（模式1和2共用）
  - `CSS_SELECTOR.md` - CSS选择器判断（模式1和2共用）
  - `DATASAVER_CONVERSION.md` - DATASAVER录制工作流转换规则详细说明（模式2）
- **scripts/**: Python工具脚本
  - `validate_log.py` - 验证执行日志格式（模式1）
  - `init_skill.py` - 创建Skill目录结构
  - `validate_skill.py` - 验证Skill结构和功能

## 使用示例

### 示例1：小红书发帖自动化

用户请求："帮我在小红书发一篇笔记，标题是'美食推荐'，内容是'今天发现一家超棒的餐厅'，上传图片xxx"

执行流程（模式1）：
1. **阶段1** - 使用chrome-server工具完成发帖，同时记录执行log
2. **阶段2** - 分析日志，提取有效操作 workflow
3. **阶段3** - 生成`xiaohongshu-post` Skill

### 示例2：批量数据抓取

用户请求："从某网站抓取产品列表信息"

执行流程（模式1）：
1. **阶段1** - 执行抓取并记录步骤log
2. **阶段2** - 分析日志，提取有效操作 workflow
3. **阶段3** - 生成可复用的抓取Skill

### 示例3：DATASAVER录制工作流文件转Skill 

用户请求："我有一个DATASAVER录制工作流.json 文件，帮我转成Skill"

输入文件：`获取douyin合集.DATASAVER录制工作流.json`

执行流程（模式2）：
1. **阶段1** - 分析DATASAVER录制工作流.json并提取有效操作 workflow
2. **阶段2** - 生成可复用的获取douyin用户合集信息的Skill

## 核心功能特性

### 日志记录能力(模式1)
- 记录每个chrome-server工具调用
- 保存执行推理过程
- 捕获错误和恢复策略
- 生成结构化JSON日志

### LOG文件提取工作流能力(模式1)
- 智能识别用户参数
- 区分静态值和动态内容
- 评估CSS选择器稳定性
- 过滤非必要的探索步骤

### DATASAVER录制工作流文件提取工作流能力(模式2)
- 解析DATASAVER录制工作流.json录制文件结构（drawflow.nodes、edges）
- 提取顶级description作为业务需求核心指导
- **先分析抽取**：应用FILTER_STEP.md规则，从原始步骤抽取必要步骤清单
- **再执行验证**：**必须逐一实际调用**chrome工具验证抽取后的全部步骤，不能跳过验证直接生成workflow
- 选择器稳定性评估（1-5分制）和动态查找优化
- mark-element节点特殊处理（利用data.purpose和textPreview字段指导AI提取数据）
- 记录完整的转换统计和验证结果到datasaver_conversion_report

### Skill生成能力(模式1和模式2)
- 自动创建标准Skill结构
- 生成清晰的执行指令
- 包含错误处理机制
- 支持参数化和复用

## 执行流程详解

### 模式1完整工作流执行路径

1. **用户输入分析**
   - 解析用户意图
   - 识别目标平台
   - 确定是否需要生成Skill
   - 根据用户需求，生成规范的 [skill-name]
     - 格式：[skill-name]
     - 规则：小写英文字母、连字符（^[a-z-]+$）
     - 示例：
       - "在小红书发布笔记" → skill-name = "xiaohongshu-post"
       - "收集抖音短剧信息" → skill-name = "douyin-drama-collection"
        **<mandatory-rule>生成后，将 skill-name 作为全局变量，在后续所有步骤中使用。</mandatory-rule>**
2. **执行阶段** - **必须读取并使用 [LOG.md](LOG.md)**
   - 调用chrome-server MCP工具
   - 实时记录执行步骤
   - 处理错误和异常情况
   - 保存结构化日志
3. **分析阶段** - **必须读取并使用 [WORKFLOW.md](WORKFLOW.md)**
   - 加载执行日志
   - 分析工具调用序列
   - 提取参数模式
   - 生成工作流定义
4. **生成阶段** - **必须读取并使用 [CREATOR.md](CREATOR.md)**
   - 创建Skill目录结构
   - 生成SKILL.md文件
   - 验证Skill结构和功能
   - 发布完成报告
   - 如果存在skill发布tool则直接调用发布到服务端

 ### 模式2完整工作流执行路径 

  1. **DATASAVER录制工作流文件读取**
     - 用户提供DATASAVER录制工作流.json文件路径
     - 验证文件格式
     - 提取顶级description用户需求作为核心指导要义
     - 提取name字段生成 [skill-name]
       - 格式：[skill-name]
       - 规则：小写英文字母、连字符（^[a-z-]+$）
       - 示例：
         - "在小红书发布笔记" → skill-name = "xiaohongshu-post"
         - "收集抖音短剧信息" → skill-name = "douyin-drama-collection"
          **<mandatory-rule>生成后，将 skill-name 作为全局变量，在后续所有步骤中使用。</mandatory-rule>**
  2. **分析转换阶段** - **必须读取 [DATASAVER.md](DATASAVER.md)**
     - **步骤1-2**：读取DATASAVER录制工作流.json，构建执行顺序（如7个节点）
     - **步骤3**：分析并抽取必要步骤
       - 应用FILTER_STEP.md规则过滤（trigger、trigger-event等）
       - 从7步抽取到5步必要步骤清单
       - 记录过滤原因到datasaver_note
     - **步骤4**：**必须逐步执行验证**（核心，不能跳过）
       - **必须**对所有必要步骤**逐一实际调用chrome工具执行**，不能仅分析
       - 验证选择器有效性
       - 失效则动态查找新selector并重新执行
       - 记录验证结果
     - **步骤5**：生成workflow.json（必须等步骤4全部验证完成后）
       - 包含验证通过的步骤
       - datasaver_note记录original/new selector
       - datasaver_conversion_report记录转换统计
     - **步骤6**：输出转换摘要（等待用户确认）
  3. **生成阶段** - **必须读取并使用 [CREATOR.md](CREATOR.md)**
     - 创建Skill目录结构
     - 生成SKILL.md文件
     - 验证Skill结构和功能
     - 发布完成报告
     - 如果存在skill发布tool则直接调用发布到服务端

## 输出文件说明

### 日志文件(模式1)
- 位置：`[当前工作目录]/workflow-logs/`
- 格式：`[skill-name]-log.json`
- 内容：完整的执行记录

### 工作流文件(模式1和模式2)
- 位置：`[当前工作目录]/workflow-workflows/`
- 格式：`[skill-name]-workflow.json`
- 内容：提取的工作流定义

### 生成的Skill(模式1和模式2)
- 位置：`[当前工作目录]/workflow-skills/[skill-name]/`
- 结构：标准Skill目录结构
- 发布：如果环境中有用于发布 Skill 的 create_workflow tool，则会调用自动发布到服务端

## 错误处理

### 模式1阶段1失败（执行错误）
- **症状**：chrome工具调用失败
- **处理**：记录错误，询问用户是否重试或调整策略
- **不继续**后续阶段

### 模式1阶段2失败（提取失败）
- **症状**：无法识别可复用模式
- **处理**：说明原因（如步骤太少、太多用户干预）
- **输出**：日志文件仍可用于参考

### 模式2阶段1失败（转换失败）
- **症状**：DATASAVER录制工作流.json格式错误、关键步骤验证失败、无法推断操作意图、验证通过率过低
- **处理**：根据具体失败原因停止转换，说明原因（如文件格式问题、页面结构变化、选择器全部失效、缺少description）
- **建议**：检查DATASAVER录制工作流文件格式、确认页面可访问、为关键步骤添加description、重新录制DATASAVER工作流
- **输出**：部分转换结果和详细错误信息供参考

### 阶段3失败（生成失败）
- **症状**：验证不通过
- **处理**：最多重试3次，每次修复后重新验证
