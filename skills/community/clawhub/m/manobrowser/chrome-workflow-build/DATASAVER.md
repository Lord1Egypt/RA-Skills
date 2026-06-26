# DATASAVER录制工作流转换模块

## 执行触发

**本模块在用户提供DATASAVER录制工作流.json文件时触发（模式2-阶段1）。**

<mandatory-rule>
本模块是模式2（DATASAVER录制工作流转换流程）的第一阶段，负责将DATASAVER录制工作流.json转换为workflow.json。
必须严格遵守我们定义的执行流程：逐一执行待执行链路中的每个步骤，全部成功后才能生成workflow.json。
完成转换并生成workflow.json后，会展示转换分析报告供用户确认。
用户确认后，将自动执行CREATOR.md（阶段2）生成Skill。
</mandatory-rule>

## 步骤进度初始化（强制要求）

<mandatory-rule>
在执行本阶段任何操作前，必须先使用 TodoWrite 工具初始化以下步骤列表。
这是强制要求，不可跳过。
</mandatory-rule>

**初始化内容**：

使用 TodoWrite 工具创建以下 todos（全部设为 pending 状态）：

| 步骤 | content             | activeForm |
|-----|---------------------|------------|
| 1 | 读取DATASAVER录制工作流.json文件完整信息 | 读取DATASAVER录制工作流.json中 |
| 2 | 执行Skill发现检查         | 执行Skill发现检查中 |
| 3 | 构建执行顺序              | 构建执行顺序中 |
| 4 | 过滤无用步骤并生成待执行链路      | 生成待执行链路中 |
| 5 | 逐一执行待执行链路中的每个步骤     | 逐一执行验证中 |
| 6 | 生成workflow.json     | 生成workflow.json中 |
| 7 | 输出转换和验证摘要           | 输出转换和验证摘要中 |

**状态管理规则**：

1. **开始步骤前**：将该步骤标记为 `in_progress`
2. **完成步骤后**：立即将该步骤标记为 `completed`
3. **同一时间**：只能有一个步骤处于 `in_progress` 状态
4. **顺序执行**：必须按步骤顺序执行，不可跳过

## 概述

本模块负责将 DATASAVER录制工作流.json 录制文件转换为可复用的 workflow.json，通过**先分析、过滤再执行、验证**的策略，生成经过实际执行验证的高质量工作流文件。

## 核心原则

### 1. 顶级description为用户需求核心指导

DATASAVER录制工作流.json的顶级description字段是整个转换过程的核心参考：

- **业务需求描述**：清楚说明用户要做什么（如"获取douyin用户合集标签页下的内容"）
- **执行逻辑路径**：详细说明操作步骤（如"打开抖音首页→搜索用户→进入用户主页→点击合集标签→获取数据"）
- **关键节点提示**：指出重要交互点（如"搜索用户"、"合集标签"、"合集列表数据"）
- **意图推断依据**：当node级别description缺失时，从顶级description推断操作意图（如搜索框填写步骤虽无description，但可从"获取用户合集"推断出需要搜索特定用户）

**真实案例**（来自`获取douyin合集.DATASAVER录制工作流.json`）：

```
顶级description: "获取douyin用户合集标签页下的内容"
↓ 可以推断出：
- 需要访问抖音网站
- 需要搜索特定用户（"甄会说"）
- 需要进入用户主页
- 需要点击"合集"标签
- 最终目标是获取合集列表数据
```

### 2. 过滤无用步骤 → 生成待执行链路 → 逐一执行

**不是**完全重放DATASAVER录制的全部步骤，而是：

1. **过滤无用步骤**：移除trigger、trigger-event等DATASAVER内部机制步骤
2. **生成待执行链路**：保留所有业务操作步骤，形成完整的待执行链路
3. **逐一执行每个步骤**：对待执行链路中的**每个步骤**依次执行，**不得跳过任何一个**

**强制要求**：

- 待执行链路中的每个步骤都必须实际执行
- 任何一个步骤失败 = 整体失败，停止转换

### 3. 步骤执行失败时的处理

当某个步骤执行失败时：
- **CSS失效处理**：尝试动态查找新CSS，找到后继续执行该步骤
- **动态查找失败**：停止转换，告知用户该步骤无法执行

## 执行流程（7步）

### 步骤1: 读取DATASAVER录制工作流.json并提取关键信息

使用Read工具读取用户提供的DATASAVER录制工作流.json文件路径。

**DATASAVER录制文件结构**：

```json
{
  "name": "抖音合集信息获取",
  "description": "获取douyin用户合集标签页下的内容",
  "drawflow": {
    "nodes": [
      {
        "id": "b79a7b391260",
        "label": "trigger",
        "type": "BlockBasic",
        "data": {
          "type": "manual",
          "disableBlock": false
        },
        "position": { "x": 50, "y": 300 }
      },
      {
        "id": "392848525615",
        "label": "new-tab",
        "type": "BlockBasic",
        "data": {
          "disableBlock": false,
          "description": "",
          "url": "https://www.douyin.com/jingxuan",
          "active": true,
          "waitTabLoaded": false,
          "updatePrevTab": true
        },
        "position": { "x": 600, "y": 300 }
      },
      {
        "id": "a35a63bfe975",
        "label": "forms",
        "type": "BlockBasic",
        "data": {
          "disableBlock": false,
          "description": "",
          "findBy": "cssSelector",
          "waitForSelector": true,
          "waitSelectorTimeout": 5000,
          "selector": "input.YEhxqQNi.jUqDCyab",
          "markEl": false,
          "multiple": false,
          "selected": true,
          "clearValue": true,
          "getValue": false,
          "saveData": false,
          "dataColumn": "",
          "type": "text-field",
          "value": "甄会说",
          "delay": 100
        },
        "position": { "x": 880, "y": 300 }
      },
      {
        "id": "c3c79039ee54",
        "label": "event-click",
        "type": "BlockBasic",
        "data": {
          "disableBlock": false,
          "description": "",
          "findBy": "cssSelector",
          "waitForSelector": true,
          "waitSelectorTimeout": 5000,
          "selector": "div.semi-tabs-tab.semi-tabs-tab-button:nth-child(2) > div.KTylVXFk > span",
          "markEl": false,
          "multiple": false
        },
        "position": { "x": 50, "y": 300 }
      },
      {
        "id": "54b32587f35d",
        "label": "mark-element",
        "type": "BlockBasic",
        "data": {
          "attributes": { "class": "ek9O6CWD" },
          "purpose": "抖音甄会说用户下合集信息",
          "selector": "div.ek9O6CWD",
          "tagName": "div",
          "textPreview": "深度解说\n\n18.2万 播放\n\n更新至 2 集..."
        },
        "position": { "x": 330, "y": 300 }
      }
    ],
    "edges": [
      {
        "id": "fb0ba195c484",
        "source": "b79a7b391260",
        "target": "e6e63ecb6989",
        "sourceHandle": "b79a7b391260-output-1",
        "targetHandle": "e6e63ecb6989-input-1"
      },
      {
        "id": "3a0adb0e56d1",
        "source": "392848525615",
        "target": "a35a63bfe975",
        "sourceHandle": "392848525615-output-1",
        "targetHandle": "a35a63bfe975-input-1"
      }
    ]
  }
}
```

**验证格式**：
- `name` - 工作流名称
- `description` - 业务需求描述（顶级description，是意图推断的重要依据）
- `drawflow.nodes` - 节点数组，每个节点包含：
  - `id`：节点唯一标识
  - `label`：节点类型（trigger、new-tab、forms、event-click、trigger-event、mark-element等）
  - `type`：块类型（通常为BlockBasic）
  - `data`：节点配置数据（selector、value、url、purpose、textPreview等）
  - `position`：画布位置信息
- `drawflow.edges` - 连接关系数组，定义节点执行顺序
  - `source`：源节点id
  - `target`：目标节点id

**提取关键信息**：
1. **name**：生成workflow和skill的name（如"抖音合集信息获取"）
2. **description**：业务需求描述（如"获取douyin用户合集标签页下的内容"）
3. **业务线索**：从description提取关键动作、目标、执行顺序、最终目标

---

### 步骤2: Skill发现检查

**触发条件**：已阅读 DATASAVER录制工作流.json 了解了详细业务需求

**执行说明**：必须读取 [SKILL_DISCOVERY.md](SKILL_DISCOVERY.md) 并严格按照其中的指导执行智能Skill发现。

**核心流程**：

1. **提取用户意图**：从DATASAVER录制工作流.json整个文件分析业务需求（重点是description字段）
2. **扫描已有skills**：扫描当前环境可以使用的全部 Skills
3. **智能匹配分析**：平台必须一致、业务需求必须一致
4. **用户交互决策**：根据匹配度决定是否向用户推荐

**执行结果**：

- **发现高度匹配Skill（>=90分）**：
  - 向用户展示匹配 Skill 的信息
  - 等待用户决策：
    - 用户确认"满足需求" → 停止创建流程 + 展示匹配Skill的使用指导→ 结束整个流程
    - 用户选择"不满足" → 继续执行步骤3-7（转换DATASAVER录制工作流）

- **无匹配或低匹配（<90分）**：
  - 不提示用户，直接继续执行步骤3（转换DATASAVER录制工作流）

**输出**：用户决策（使用已有Skill / 继续转换DATASAVER录制工作流）

---

### 步骤3: 构建执行顺序

从nodes和edges构建执行顺序：

```python
1. 找到 label="trigger" 的节点作为起点
2. 按照 edges 的 source→target 关系遍历
3. 生成 ordered_steps 数组（按执行顺序）
```

**真实示例**（抖音合集信息获取）：
```
trigger → new-tab(hao123) → new-tab(抖音) → forms(搜索) → trigger-event → new-tab(用户主页) → event-click(合集标签) → mark-element(合集数据)
(共8个节点)
```

---

### 步骤4: 过滤无用步骤，生成待执行链路

从DATASAVER录制的所有步骤中，过滤掉无用步骤，保留所有业务操作步骤，形成**待执行链路**。

#### 4.1 必须过滤的步骤（仅以下类型）

只过滤以下明确的DATASAVER内部机制步骤：

- **trigger节点**（label="trigger"）：DATASAVER启动触发器，不是用户操作
- **trigger-event节点**（label="trigger-event"）：DATASAVER内部事件机制，不是用户操作
- **element-scroll节点**（label="element-scroll"）：滚动操作通常不影响业务流程
- **重复的new-tab**：只保留第一个用于导航的

#### 4.2 必须保留的步骤（除上述类型外的所有步骤）

以下类型的步骤**全部保留**，不得过滤：

- **new-tab**（label="new-tab"）：导航步骤 → 转换为 chrome_navigate
- **forms**（label="forms"）：表单填写 → 转换为 chrome_fill_or_select
- **event-click**（label="event-click"）：点击操作 → 转换为 chrome_click_element
- **mark-element**（label="mark-element"）：数据收集 → 转换为 web-data-extractor skill
- **其他所有业务操作步骤**

**节点类型到chrome工具的映射**：

| DATASAVER节点label | 转换为chrome工具 |
|-------------------|-----------------|
| new-tab | chrome_navigate |
| event-click | chrome_click_element |
| forms | chrome_fill_or_select |
| mark-element | web-data-extractor skill（根据data.purpose和textPreview提取数据） |

#### 4.3 待执行链路 = 过滤后保留的所有步骤

过滤完成后，剩余的步骤组成**待执行链路**。这个链路中的**每个步骤**都必须在步骤5中逐一执行。

#### 4.3 日期选择器场景的发现和处理方式

**识别条件**（满足任一）：
- selector包含关键词：`date`, `calendar`, `picker`, `month`, `year`, `time`
- description是1-31的纯数字
- 连续多个event-click点击不同数字
- 页面文本包含"开始时间"、"结束时间"、"~"、"-"

**处理流程**：
一旦识别到日期选择器场景：
1. **阅读操作指南**：[DATE_PICKER_HANDLING.md](references/DATE_PICKER_HANDLING.md)
2. **在步骤5中按指南操作**：使用chrome_accessibility_snapshot识别日历结构、判断月份、选择日期
3. **生成workflow中相关步骤**：参考 DATE_PICKER_HANDLING.md 中的"完整的Workflow步骤示例"章节生成日期选择器相关步骤

**关键点**：
- 参数化起止日期为{start_date}、{end_date}（日期值必须作为用户参数，不能硬编码）
- 打开日期选择器的控件（如日期输入框）：如果selector没失效可以固定，失效则动态查找
- 日历面板中的日期数字选择：必须动态处理（使用chrome_accessibility_snapshot识别当前月份和日期位置）

#### 4.4 记录过滤原因

对每个被过滤的步骤，记录到datasaver_note供回溯检查。

**输出**：待执行链路（如：原始7个节点 → 过滤后5个步骤需要执行）

---

### 步骤5: 逐一执行待执行链路中的每个步骤

<mandatory-rule>
必须对待执行链路中的每个步骤依次实际调用chrome工具执行。

**每个步骤的执行策略**：
1. 优先使用DATASAVER录制的CSS selector执行
2. **成功** → 继续执行下一个步骤
3. **失败** → 尝试动态查找新元素（参考 [DATASAVER_CONVERSION.md](references/DATASAVER_CONVERSION.md)）
4. **动态查找成功** → 用新selector执行该步骤，成功后继续下一个步骤
5. **动态查找失败** → **整体失败，停止转换**

**任何一个步骤失败 = 整体失败**：
- 停止转换，不生成workflow.json
- 告知用户：DATASAVER录制的链路无法回放，建议重新录制

**禁止事项**：
- 禁止跳过任何待执行步骤直接生成workflow

</mandatory-rule>

#### 5.1 上下文保护策略

**重要**：当DATASAVER节点转换后需要调用以下工具时，使用Task Tool封装，不能直接调用：

1. `chrome_get_web_content()` - 获取页面信息（返回OSS URL，需配合WebFetch）
2. `chrome_accessibility_snapshot()` - 页面元素分析（返回~4k tokens元素树）
3. `chrome_screenshot()` - 截图分析（返回base64图片）

**原因**：这些工具返回大量数据（chrome_get_web_content ~84k tokens, chrome_accessibility_snapshot ~4k tokens, chrome_screenshot ~84k tokens），会迅速填满主agent上下文

**Task Tool 使用要点**：
- **明确当前状态**：告诉subagent当前在哪个页面、页面已加载
- **直接指定工具**：用"执行：工具名(参数)"格式
- **精简返回格式**：要求subagent只返回关键信息，不要原始数据
- 使用 `subagent_type="general-purpose"` 和 `model="sonnet"`
- Task Tool 内部只允许针对当前需求调用一次目标工具

**必须阅读**：[references/CONTEXT_ISOLATION.md](references/CONTEXT_ISOLATION.md)

- 该文档提供了详细的Task Tool使用指南、核心原则和参数说明
- **重要提醒**：DATASAVER模式中，标记为`purpose: "selector_finding"`的Task Tool需要**保留到workflow**
  - 原因：DATASAVER录制的CSS selector可能在运行时失效，需要动态查找机制
  - 这确保了workflow在CSS变化时仍能正常执行

**DATASAVER模式中Task Tool的用途分类**：

- `purpose: "selector_finding"`：CSS失效时动态查找selector（通常使用chrome_accessibility_snapshot） → **保留到workflow**
- `purpose: "get_html_info"`：mark-element节点必须使用 web-data-extractor skill → **保留到workflow**

#### 5.2 mark-element 节点必须使用 web-data-extractor

当 DATASAVER 的 `mark-element` 节点需要收集页面数据时，**必须**使用 `web-data-extractor` skill：

**识别条件**（满足以下条件即判定为收集数据步骤）：
- 节点类型为 `mark-element`
- 有 `data.purpose` 字段描述要收集的数据
- 有 `data.textPreview` 字段展示数据预览

**转换规则**：

识别为收集数据步骤后，**必须**转换为 `web-data-extractor` skill 调用：

```json
// DATASAVER 原始节点
{
  "id": "54b32587f35d",
  "label": "mark-element",
  "type": "BlockBasic",
  "data": {
    "attributes": { "class": "ek9O6CWD" },
    "purpose": "抖音甄会说用户下合集信息",
    "selector": "div.ek9O6CWD",
    "tagName": "div",
    "textPreview": "深度解说\n\n18.2万 播放\n\n更新至 2 集..."
  }
}

// 必须转换为 workflow 步骤
{
  "step": 8,
  "tool_name": "Skill",
  "tool_params": {
    "skill": "web-data-extractor",
    "args": "提取当前页面的合集列表数据，包括合集名称、播放量、更新集数等信息"
  },
  "purpose": "get_html_info",
  "is_final_result": true,
  "description": "收集合集列表数据",
  "datasaver_note": {
    "original_label": "mark-element",
    "original_purpose": "抖音甄会说用户下合集信息",
    "original_selector": "div.ek9O6CWD",
    "original_textPreview": "深度解说\n\n18.2万 播放\n\n更新至 2 集...",
    "converted_to": "web-data-extractor"
  }
}
```

#### 5.3 操作触发新打开标签页时的特殊处理

**场景识别**：

当DATASAVER节点类型为 `new-tab` 或者操作触发了打开了新的页面时，表示用户录制了打开新页面的操作，需要特殊处理以确保后续步骤在正确的标签页执行。

**处理流程**：

1. **识别new-tab节点，或者操作触发了打开新的页面**
   
   ```json
   {
     "label": "new-tab",
     "data": {
       "url": "https://example.com/page",
       "active": true,
       "description": "打开目标页面"
     }
   }
   ```
   
2. **转换为workflow步骤（自动添加标签页管理）**

   生成3个步骤：

   **步骤N：执行导航或点击**
   - 如果 new-tab 有明确 URL → 生成 `chrome_navigate` 步骤
   - 如果 URL 需要动态获取 → 生成 `chrome_click_element` 步骤（使用前面步骤的链接）

   **步骤N+1：检查新标签页（自动添加）**
   ```json
   {
     "step": N+1,
     "tool_name": "get_windows_and_tabs",
     "tool_params": {},
     "description": "检查新打开的标签页并记录tabId",
     "output": {
       "new_tab_id": "新标签页ID",
       "new_tab_url": "新标签页URL"
     },
     "datasaver_note": {
       "added_for": "new-tab节点自动添加标签页管理",
       "auto_generated": true
     }
   }
   ```

   **步骤N+2及后续：使用tabId参数**
   - 所有后续在新页面的操作都需要添加 `tabId` 参数
   - 引用前面步骤的输出：`"tabId": "{step_N+1.new_tab_id}"`

**示例**：

```json
// 原始DATASAVER录制: new-tab节点
{
  "label": "new-tab",
  "data": {
    "url": "https://www.douyin.com/user/xxx"
  }
}

// 转换为workflow步骤:
[
  {
    "step": 3,
    "tool_name": "chrome_navigate",
    "tool_params": {
      "url": "https://www.douyin.com/user/xxx"
    },
    "description": "导航到用户主页"
  },
  {
    "step": 4,
    "tool_name": "get_windows_and_tabs",
    "tool_params": {},
    "description": "检查新打开的标签页",
    "output": {
      "new_tab_id": "新标签页ID"
    },
    "datasaver_note": {
      "auto_generated": true
    }
  },
  {
    "step": 5,
    "tool_name": "chrome_click_element",
    "tool_params": {
      "selector": "#semiTabcompilation span",
      "tabId": "{step_4.new_tab_id}"
    },
    "description": "在新标签页点击合集标签"
  }
]
```

**关键点**：

- new-tab节点或者其他打开新的tab页面的节点需要触发添加 `get_windows_and_tabs` 步骤
- `output` 字段必须定义 `new_tab_id` 供后续步骤引用
- 所有后续步骤必须添加 `tabId` 参数指向新标签页
- 标记 `datasaver_note.auto_generated: true` 表示自动添加的步骤

### 步骤6: 生成workflow.json

使用Write工具生成workflow.json，格式基于 [assets/datasaver_workflow_template.json](assets/datasaver_workflow_template.json)。

**包含内容**：
1. **基本信息**：name, description, platform, created_from, created_at
2. **参数列表**：用户参数、静态参数、动态参数
3. **步骤列表**：chrome工具 + Task Tool步骤
4. **datasaver_note**：记录验证结果、CSS更新、优化说明
5. **datasaver_conversion_report**：统计转换数据

**关键字段生成逻辑**：

#### Task Tool步骤的purpose字段（智能分析）

每个Task Tool步骤必须包含purpose字段，**通过智能分析DATASAVER原始节点、前后步骤上下文、顶级description来推断**，而非僵化的规则匹配。

**分析维度**：
1. **DATASAVER原始节点类型和数据字段**
   - `mark-element` + `data.purpose` + `data.textPreview` → 明确指示数据收集
   - `forms` + CSS失效 → 需要动态查找
   - `event-click` + CSS失效 → 需要动态查找

2. **前后步骤上下文**
   - 前一步：填写搜索框 → 当前步：点击搜索按钮 → 推断为selector_finding
   - 前一步：导航到页面 → 当前步：mark-element → 推断为get_html_info

3. **顶级description业务意图**
   - description提到"获取合集列表数据" + 当前步骤是mark-element → get_html_info
   - description提到"填写用户名" + 当前步骤CSS失效 → selector_finding

4. **is_final_result标记**
   - 如果步骤被标记为`is_final_result: true`且使用Task Tool → 大概率是get_html_info
   - 如果是中间步骤 → 可能是selector_finding

**示例1 - get_html_info（mark-element节点，必须使用 web-data-extractor）**：
```json
// 分析：mark-element节点 + purpose="抖音甄会说用户下合集信息"
// → 判定为数据收集步骤，必须使用 web-data-extractor
{
  "step": 8,
  "tool_name": "Skill",
  "tool_params": {
    "skill": "web-data-extractor",
    "args": "提取当前页面的合集列表数据，包括合集名称、播放量、更新集数等信息"
  },
  "purpose": "get_html_info",
  "is_final_result": true,
  "datasaver_note": {
    "original_label": "mark-element",
    "original_purpose": "抖音甄会说用户下合集信息",
    "converted_to": "web-data-extractor"
  }
}
```

**示例2 - selector_finding（forms节点CSS失效）**：
```json
// 分析：forms节点 + CSS失效 + 中间步骤
//      + 顶级description提到"搜索用户"
// → 智能推断为选择器查找
{
  "tool_name": "task_tool",
  "purpose": "selector_finding",  // ✅ 智能推断
  "is_final_result": false,
  "datasaver_note": {
    "original_selector": "input.YEhxqQNi",
    "css_failed": true,
    "recovery_method": "Task Tool深度推断"
  }
}
```

#### 日期选择器相关步骤

如果步骤4.3识别到日期选择器场景，生成workflow时：

**必要信息**：
- 日期参数化为 `{start_date}` 和 `{end_date}`
- 需要先定位到日期选择器位置，然后分别查到到正确的开始和结束月份选择起止日期
- 使用动态查找的步骤需要保留 Task Tool
- 在 datasaver_note 中记录原始的日期值和选择器（用于调试）


---

### 步骤7: 输出转换和验证摘要

向用户展示业务化的转换摘要：

```markdown
✅ DATASAVER录制工作流转换完成

📝 工作流功能：
[基于workflow.description生成业务描述，如："在巨量云图报告市场中搜索指定报告，获取触达频次分析中各频次各触点的曝光次数数据"]

📋 需要提供的参数：
[列出parameters，用通俗语言说明]
示例：
- report_name（报告名称）：需要查询的报告名称，如"HJ-白话频道-test"
- aadvid（广告主ID）：您的广告主ID，可从URL中获取，如"1713035749117966"

🔄 已按顺序逐一执行全部 N 个步骤：
[用业务语言描述steps，避免技术术语]
示例：
1. 打开巨量云图平台 ✅
2. 点击"人群"菜单 ✅
3. 进入"报告市场" ✅
4. 搜索您指定的报告 ✅
5. 打开报告详情页 ✅
6. 滚动到触达频次分析区域 ✅
7. 选择"全部触点"选项 ✅
8. 收集各频次各触点的曝光数据 ✅

📊 最终能得到什么：
[基于is_final_result=true的步骤说明返回结果]
示例：各频次各触点的曝光次数数据，包含频次、触点名称、曝光次数等信息

✅ 转换状态：
- 转换成功，workflow已生成 ✅
- 全部 N 个步骤已逐一执行成功 ✅

📁 文件已保存：
[当前工作目录]/workflow-workflows/[workflow-name]-workflow.json

---

请确认转换结果是否符合预期？
【确认后，将自动执行阶段2(CREATOR.md)生成可复用的Skill】
```

## 质量检查清单

在生成workflow.json前，确认：

- [ ] 待执行链路中的每个步骤都已实际执行并成功
- [ ] CSS失效时已触发动态处理并记录到datasaver_note
- [ ] 用户参数正确识别并使用 `{param}` 占位符
- [ ] Task Tool步骤包含purpose字段（selector_finding或get_html_info）
- [ ] 最终结果步骤标记为is_final_result: true
- [ ] 包含完整的datasaver_conversion_report

## 常见问题处理

### 问题1：选择器验证失败

**场景**：执行DATASAVER录制步骤时，CSS selector无法找到元素，且动态查找元素也失败

**停止转换并告知用户**：
```
DATASAVER录制工作流转换失败
步骤 [N] 执行失败：[步骤描述]
- 原始选择器：[selector]
- 失败原因：元素未找到
- 尝试查找元素：失败

DATASAVER录制工作流.json录制的操作链路无法在当前环境回放。

可能原因:
1) 页面结构已变化
2) 需要登录或特定权限
3) DATASAVER录制时的页面状态与当前不同

建议:
- 检查目标页面是否可正常访问
- 确认登录状态
- 重新录制DATASAVER录制工作流.json
```

### 问题2：转换成功标准

**成功条件**：
- 待执行链路中的每个步骤都已依次执行并全部成功
- 每个步骤要么使用原始CSS成功，要么使用动态查找的CSS操作成功
- 最终步骤执行成功

## 调试提示

如果生成的workflow.json存在问题，检查：

1. **步骤过滤是否合理**
   - 查看datasaver_conversion_report的filtered_steps和优化说明
   - 确认被过滤的只有DATASAVER内部机制步骤（trigger、trigger-event、重复new-tab），没有误删业务步骤

2. **参数引用是否正确**
   - `{param}` 用户参数是否在parameters中定义
   - `{step_N.selector}` 动态selector引用是否正确

3. **Task Tool的prompt是否清晰**
   - 是否明确当前页面状态
   - 是否指定返回格式（JSON、selector字符串等）
   - 是否禁止返回完整HTML或base64图片