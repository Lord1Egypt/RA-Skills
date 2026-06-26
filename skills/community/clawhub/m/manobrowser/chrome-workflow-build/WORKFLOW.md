# 工作流提取模块

## 执行触发

**本模块在模式1-阶段1（LOG.md）完成且用户确认后自动执行（模式1-阶段2）。**

<mandatory-rule>
本模块是模式1（执行并记录流程）的第二阶段，负责从LOG.md生成的日志提取workflow.json。
用户已在阶段1后确认执行结果正确，阶段2和3将自动连续执行。
不需要再次询问用户是否继续。
完成后将自动执行CREATOR.md（阶段3）生成Skill。
</mandatory-rule>

## 步骤进度初始化（强制要求）

<mandatory-rule>
在执行本阶段任何操作前，必须先使用 TodoWrite 工具初始化以下步骤列表。
这是强制要求，不可跳过。
</mandatory-rule>

**初始化内容**：

使用 TodoWrite 工具创建以下 todos（全部设为 pending 状态）：

| 步骤 | content | activeForm |
|-----|---------|------------|
| 1 | 读取并解析日志文件 | 读取并解析日志文件中 |
| 2 | 分析日志内容 | 分析日志内容中 |
| 3 | 参数提取和分类 | 参数提取和分类中 |
| 4 | 生成工作流定义 | 生成工作流定义中 |
| 5 | 工作流质量保障 | 工作流质量保障中 |
| 6 | 保存工作流文件 | 保存工作流文件中 |
| 7 | 输出提取摘要 | 输出提取摘要中 |

**状态管理规则**：

1. **开始步骤前**：将该步骤标记为 `in_progress`
2. **完成步骤后**：立即将该步骤标记为 `completed`
3. **同一时间**：只能有一个步骤处于 `in_progress` 状态
4. **顺序执行**：必须按步骤顺序执行，不可跳过

## 概述

本模块负责从LOG.md生成的执行日志中提取可复用的工作流定义。通过深度分析reasoning信息、智能识别参数类型、过滤探索性步骤，使用 Write 工具生成标准化的工作流JSON文件。

## 核心原则

### 1. 深度利用Reasoning信息
每个步骤的reasoning字段包含宝贵信息：
- **状态分析** → 判断是否为探索性步骤
- **行动理由** → 判断是否为执行性步骤
- **期望结果** → 判断是否为最终结果

### 2. 参数分类体系
- **用户参数**：每次执行可变的值，使用 `{param_name}` 占位符
- **静态参数**：固定不变的值，直接硬编码
- **动态参数**：运行时获取的值，使用 `{step_N.param_name}` 引用

### 3. 工具使用严格性
- 只能使用日志中出现的MCP工具
- 提取的workflow是执行步骤的子集
- 不添加日志中没有的新步骤

## 执行步骤

<mandatory-rule>
必须严格按以下步骤执行
</mandatory-rule>

### 1. 读取并解析日志文件

从当前工作目录读取LOG模块生成的日志：
```
[当前工作目录]/workflow-logs/[skill-name]-log.json
```

解析JSON结构，提取以下关键字段：
- `user_query`：用户原始需求
- `steps`：执行步骤数组
- `final_result`：最终结果
- `session_stats`：执行统计

### 2. 分析日志内容

#### 2.1 识别平台和任务类型
从user_query和steps中识别：
- 目标平台（小红书、抖音、TikTok等）
- 任务类型（发布、搜索、收集等）
- 核心功能描述

#### 2.2 深度分析Reasoning

如何正确识别和过滤LOG中的步骤必须先参考文档：[references/FILTER_STEP.md](references/FILTER_STEP.md)

对每个 tool_call 和 task_tool 步骤，分析reasoning内容：

**探索性步骤识别**（需要过滤）：
- 包含关键词："查看"、"检查"、"获取信息用于分析"、"确认页面状态"
- 工具类型：
  - chrome_get_web_content（非最终结果，仅用于分析）
  - chrome_get_interactive_elements
  - Task Tool（purpose为verification）
  - Task Tool（purpose为selector_finding 且 **output未被后续步骤引用**）

**执行性步骤识别**（需要保留）：
- 包含关键词："执行"、"触发"、"点击提交"、"完成任务"
- 工具类型：
  - chrome_navigate
  - chrome_click_element
  - chrome_fill_or_select
  - Task Tool（purpose为get_html_info且意图为收集数据用）
  - Task Tool（purpose为selector_finding 且 **output被后续步骤引用**，如 `{step_N.uid}`）

**中间触发步骤**（必须保留）：
- 包含关键词："打开面板"、"展开选项"、"切换标签"
- 这些步骤虽不直接完成任务，但是必要的交互

**页面跳转步骤**（需要识别并保留）：
- 工具类型：get_windows_and_tabs
- 目的：检查并切换新打开的标签页，防止后续操作位于错误的标签页
- 特征：通常出现在点击链接或导航操作之后
- 处理：保留到workflow，标记output字段记录tabId供后续使用

#### 2.3 处理用户反馈步骤 

user_feedback步骤记录了用户在执行过程中的干预和指导，需要特殊处理：

**原则**：user_feedback步骤本身不出现在最终workflow中，但反馈的影响会体现在：

1. **更新parameters**
   - 参数修改型反馈 → 更新example值
   - 使用反馈后的最终值作为参数示例
   ```json
   // 原始需求：标题为"欧莱雅"
   // 用户反馈：标题改成"欧莱雅小棕瓶"
   // parameters应该使用：
   {
     "name": "note_title",
     "type": "string",
     "example": "欧莱雅小棕瓶",  // 使用反馈后的值
     "description": "笔记标题内容"
   }
   ```

2. **调整steps**
   - 工具纠正型反馈 → 使用正确的工具
   - 策略指导型反馈 → 采用用户建议的方法
   - 流程优化型反馈 → 调整步骤顺序
   ```json
   // 用户反馈：用chrome_fill_or_select工具填写正文
   // steps应该使用：
   {
     "step": 4,
     "tool_name": "mcp__chrome-server__chrome_fill_or_select",  // 使用反馈建议的工具
     "tool_params": {
       "selector": ".tiptap.ProseMirror",
       "value": "{note_content}"
     }
   }
   ```

3. **优化description**
   - 策略指导型反馈 → 在描述中体现最佳实践
   - 添加"建议直接..."、"推荐使用..."等说明
   ```json
   {
     "description": "在小红书创作者平台发布图文笔记。建议直接访问发布页面URL，使用chrome_fill_or_select工具填写内容。",
     ...
   }
   ```

**核心理念**：提取的workflow应该是"经过用户反馈优化后的最佳实践版本"，而不是包含错误尝试的原始版本。

#### 2.4 识别必须使用Task Tool的步骤（上下文保护策略）

**重要**：如果log中的步骤调用了以下工具，应该识别为task_tool类型（或应该使用Task Tool但没有使用）：

1. **chrome_get_web_content()** - 获取页面信息
   - 返回OSS URL，必须配合WebFetch取回HTML
   - 必须标记 `purpose: "get_html_info"`
   - 用于获取页面HTML信息或收集数据

2. **chrome_accessibility_snapshot()** - 页面元素分析
   - 返回~4k tokens的元素树（包含树状结构+base64图片）
   - 必须标记 `purpose: "selector_finding"`
   - 用于查找按钮、输入框、分析页面结构等
   - 返回uid等精简结果供后续步骤使用

3. **chrome_screenshot()** - 截图分析
   - 返回base64图片，需要隔离大数据
   - 必须标记 `purpose: "verification"`
   - 用于验证页面状态、检查UI显示等

#### 2.4.1 识别 web-data-extractor 数据收集步骤

LOG阶段数据收集场景必须使用 web-data-extractor，WORKFLOW阶段需要识别并保留：

LOG中的步骤格式：
```json
{
  "type": "tool_call",
  "content": {
    "reasoning": "收集商品列表数据作为最终结果",
    "tool_name": "Skill",
    "tool_params": {
      "skill": "web-data-extractor",
      "args": "提取当前页面的商品信息"
    },
    "purpose": "get_html_info"
  }
}
```

转换为workflow步骤（直接保留）：
```json
{
  "step": 8,
  "tool_name": "Skill",
  "tool_params": {
    "skill": "web-data-extractor",
    "args": "提取当前页面的商品信息"
  },
  "purpose": "get_html_info",
  "is_final_result": true,
  "description": "收集商品列表数据"
}
```

**关键原则**：
- 数据收集场景必须使用 web-data-extractor
- WORKFLOW阶段只负责识别并保留
- 标记 `purpose: "get_html_info"` 的步骤会被保留到workflow

**判断规则**：

查看log中的步骤类型：
- 如果 `type="task_tool"` → 已经使用了Task Tool，必须保留
- ⚠️ **不应该出现**：`type="tool_call"` 但调用了上述三个工具
  - LOG.md已明确禁止主agent直接调用这些工具
  - 如果出现此情况，说明日志生成阶段违反了规则，应该报错而非继续处理

#### 2.5 日期选择器场景识别

**识别条件**（满足任一）：
- tool_call的selector包含：date, calendar, picker, month, year, time
- reasoning中提到"日期"、"时间"、"选择日期"
- 连续多个chrome_click_element点击数字1-31
- 页面文本包含"开始时间"、"结束时间"、"~"、"-"

**识别后处理**：
1. 标记这组步骤为日期选择器场景
2. 确保workflow中保留完整的日期选择步骤链路
3. 参数化日期值为 `{start_date}` 和 `{end_date}`
4. 在步骤的description中说明原始日期值（供调试参考）

**参考文档**：[DATE_PICKER_HANDLING.md](references/DATE_PICKER_HANDLING.md),生成的workflow中相关步骤参考文档中"完整的Workflow步骤示例"章节模板

### 3. 参数提取和分类

#### 3.1 识别用户参数
从user_query中提取可变值：
- 用户名、ID、搜索关键词
- 标题、内容、描述文本
- 数量、日期、其他可配置值

**参数命名规范**：
- 使用描述性名称：`douyin_user_id` 而非 `user_id`
- 使用下划线命名：`search_keyword` 而非 `searchKeyword`
- 避免通用名称：`drama_name` 而非 `name`

#### 3.2 评估选择器稳定性
对每个CSS选择器进行稳定性评分，必须参考文档：[references/CSS_SELECTOR.md](references/CSS_SELECTOR.md)

**稳定选择器**（4-5分，作为静态参数）：
- 标准ID：`#search-input`
- 语义化类：`.submit-button`
- 标准属性：`input[type="text"]`

**不稳定选择器**（1-2分，作为动态参数）：
- Vue/React hash：`[data-v-abc123]`
- 动态ID：`#item-timestamp`
- 复杂路径：`div:nth-child(7) > span`

#### 3.3 处理动态参数

**动态参数使用的5大原则**：

1. **优先考虑选择器稳定性** - 不稳定的必须使用动态参数
2. **参数名称必须完全一致** - 大小写也要匹配
3. **参数类型必须匹配工具需求** - 不同工具需要不同类型
4. **先定义output，后引用** - 不能引用未定义的参数
5. **支持单值和数组模式** - `{step_N.param}` 或 `{step_N.param[0]}`

**示例1：使用chrome_accessibility_snapshot获取uid作为动态参数**
```json
{
  "step": 3,
  "tool_name": "task_tool",
  "tool_params": {
    "description": "查找发布按钮",
    "prompt": "当前页面：小红书发布页，页面已加载完成。\n\n执行任务：\n1. 调用 chrome_accessibility_snapshot() 获取页面元素树\n2. 分析元素树找到\"发布\"按钮\n3. 返回JSON格式：{\"uid\": \"元素uid\", \"role\": \"button\", \"name\": \"发布\"}\n\n严格要求：\n- 只返回目标元素信息，不要返回完整元素树",
    "subagent_type": "general-purpose",
    "model": "sonnet"
  },
  "purpose": "selector_finding",
  "output": {
    "publish_button_uid": "发布按钮的uid，由chrome_accessibility_snapshot返回"
  }
},
{
  "step": 4,
  "tool_name": "mcp__chrome-server__chrome_click_element",
  "tool_params": {
    "uid": "{step_3.publish_button_uid}"
  },
  "description": "点击发布按钮"
}
```

**示例2：使用Task Tool获取不稳定选择器作为动态参数**
```json
{
  "step": 3,
  "tool_name": "task_tool",
  "tool_params": {
    "description": "查找搜索按钮",
    "prompt": "当前页面：抖音首页。\n\n执行任务：\n1. 调用 chrome_get_web_content() 获取OSS URL\n2. 调用 WebFetch 获取HTML\n3. 分析HTML找到搜索按钮的selector\n4. 返回JSON格式：{\"selector\": \"按钮选择器\"}\n\n严格要求：\n- 只返回精简的JSON结果",
    "subagent_type": "general-purpose",
    "model": "sonnet"
  },
  "purpose": "selector_finding",
  "output": {
    "search_button": "搜索按钮选择器，需要AI分析获取"
  }
},
{
  "step": 4,
  "tool_name": "mcp__chrome-server__chrome_click_element",
  "tool_params": {
    "selector": "{step_3.search_button}"
  },
  "description": "点击搜索按钮"
}
```

**动态参数的主要来源**：
- **chrome_accessibility_snapshot返回的uid**：优先推荐，元素覆盖率高（151 vs 35），可直接用于chrome_click_element
- **不稳定的CSS选择器**：包含hash值（data-v-*）、动态ID、复杂路径的选择器
- **数据收集结果**：从页面提取的URL、文本等信息

### 4. 生成工作流定义

在生成Workflow之前必须示例参考：[assets/workflow_template.json](assets/workflow_template.json)

#### 4.1 构建基本信息
```json
{
  "name": "[skill-name]",
  "description": "基于执行结果的功能描述",
  "platform": "标准平台名称",
  "created_from": "原始日志文件名",
  "created_at": "生成时间"
}
```

#### 4.2 构建参数列表
```json
"parameters": [
  {
    "name": "username",
    "type": "string",
    "required": true,
    "description": "目标用户名",
    "example": "磁力短剧"
  }
]
```

#### 4.3 构建步骤列表
过滤探索性步骤后，组织执行步骤：
```json
"steps": [
  {
    "step": 1,
    "tool_name": "mcp__chrome-server__chrome_navigate",
    "tool_params": {
      "url": "https://www.douyin.com"
    },
    "description": "打开抖音网站",
    "is_final_result": false
  }
]
```

#### 4.3.1 保留Task Tool的purpose字段

**重要**：对于日志中的task_tool步骤，必须保留purpose字段到workflow.json。

**日志中的task_tool步骤示例**：
```json
{
  "step": "3",
  "type": "task_tool",
  "content": {
    "reasoning": "需要动态查找发布按钮的选择器",
    "tool_params": {
      "description": "查找发布按钮",
      "prompt": "...",
      "subagent_type": "general-purpose"
    },
    "output": "{\"selector\": \".publish-button\"}",
    "purpose": "selector_finding"  // ✅ 关键字段
  }
}
```

**转换为workflow步骤时保留purpose**：
```json
{
  "step": 8,
  "tool_name": "task_tool",
  "tool_params": {
    "description": "查找发布按钮",
    "prompt": "...",
    "subagent_type": "general-purpose"
  },
  "purpose": "selector_finding",  // ✅ 必须保留
  "is_final_result": false
}
```

**purpose字段说明**：
- `get_html_info`：获取页面信息型，用于收集数据时→ CREATOR.md会特殊处理，在生成的SKILL.md中保留说明
- `selector_finding`：查找选择器 → 已在执行中使用，不需要在SKILL.md中体现
- `verification`：验证状态 → 已在执行中使用，不需要在SKILL.md中体现

**为什么必须保留purpose字段**：
- CREATOR.md（阶段3）依赖purpose字段判断Task Tool的类型
- purpose="get_html_info"的Task Tool步骤需要在生成的SKILL.md中特别说明
- 缺少purpose字段会导致CREATOR.md无法正确处理Task Tool步骤

#### 4.4 标记最终结果
- 最后一个chrome_get_web_content步骤
- 获取目标数据的步骤
- 设置 `is_final_result: true`

### 5. 工作流质量保障

#### 5.1 参数引用检查
- 所有 `{param}` 在parameters中定义
- 所有 `{step_N.param}` 在对应output中定义
- 参数名称大小写完全一致

#### 5.2 步骤依赖检查
- 引用的步骤在前面已定义
- 数组访问的参数确实是数组类型
- input/output配对正确

#### 5.3 工具名称检查
- 使用完整的MCP工具名（如 `mcp__chrome-server__chrome_navigate`）
- 工具名与日志中一致

### 6. 保存工作流文件

将生成的工作流保存到当前工作目录：
```
[当前工作目录]/workflow-workflows/[skill-name]-workflow.json
```

命名示例：
- `douyin-drama-collection-workflow.json`
- `xiaohongshu-post-workflow.json`

### 7. 输出提取摘要

向用户报告提取结果：
```
✅ 阶段2：提取工作流 - 已完成

📊 提取统计：
- 原始步骤：42个
- 过滤后步骤：9个
- 识别用户参数：2个
- 动态选择器：1个

📁 文件已保存：
[当前工作目录]/workflow-workflows/[skill-name]-workflow.json

---

继续执行阶段3：生成可复用的Skill...
```

<mandatory-rule>
阶段2完成后，自动继续执行阶段3（CREATOR.md）。
不要等待用户确认。
</mandatory-rule>

## 质量检查清单

在完成工作流提取前，确认以下事项：

### 步骤过滤
- 所有探索性步骤已过滤（分析性的tool调用，例如chrome_get_web_content查看页面等）
- 所有执行性步骤已保留（导航、点击、填写）
- 中间触发步骤已保留（展开、切换）

### 参数处理
- 用户参数正确识别并使用 `{param}` 占位符
- 选择器稳定性正确评估
- 动态参数引用格式正确 `{step_N.param}`
- 参数命名符合规范（描述性、下划线）

### 工作流结构
- 步骤顺序逻辑正确
- 工具名称使用完整MCP格式
- 最终结果步骤正确标记
- 包含足够的错误处理信息

## 常见问题处理

### 问题1：某个步骤既有探索性质又有执行性质
**解决**：分析reasoning的主要目的，如果主要是为了获取临时信息则过滤，如果是为了改变状态则保留

### 问题2：无法确定选择器是否稳定
**解决**：当评分为3分（中等稳定性）时，优先标记为动态参数，在生成的Skill中说明可能需要调整

### 问题3：用户参数与静态参数难以区分
**解决**：参考原始user_query，判断该值是否每次执行都可能变化

### 问题4：动态参数引用复杂
**解决**：确保先定义output再引用，参数名完全一致，必要时在description中详细说明获取方式

## 调试提示

如果提取的工作流无法正常执行，检查：
1. 是否过滤了必要的中间步骤
2. 动态参数引用是否正确
3. 选择器是否因页面更新而失效
4. 参数占位符是否正确替换