# CSS失效处理执行指南

## 概述

本文档专注于 **DATASAVER录制工作流模式中CSS失效后的实际执行处理逻辑**。

### DATASAVER录制文件结构

DATASAVER录制的工作流文件(.datasaver.json)具有以下结构：

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

**关键字段说明**：
- `name`：工作流名称
- `description`：业务需求描述（顶级description，是意图推断的重要依据）
- `drawflow.nodes`：节点数组，每个节点包含：
  - `id`：节点唯一标识
  - `label`：节点类型（trigger、new-tab、forms、event-click、trigger-event、mark-element等）
  - `data`：节点配置数据（selector、value、url、purpose、textPreview等）
  - `position`：画布位置信息
- `drawflow.edges`：连接关系数组，定义节点执行顺序

### 核心理念

DATASAVER录制工作流.json 是用户录制的**成功执行链路**，应该：
1. **优先直接执行**：按录制的selector执行操作
2. **失效时动态恢复**：CSS失效时触发意图推断 + 动态查找
3. **精确封装**：将失效步骤封装为"查找selector获取动态参数 + 根据动态参数执行操作"2步

### 本文档适用场景

- 执行DATASAVER录制步骤时发现CSS失效
- 需要推断用户操作意图
- 需要动态查找新selector并封装到workflow

---

## 1. CSS失效检测机制

### 1.1 何时判定CSS失效

执行DATASAVER录制步骤时，以下情况判定为CSS失效：

**失效表现**：
```
chrome_click_element(selector="div[data-v-abc123]")
→ 返回错误："Element not found" 或超时

chrome_fill_or_select(selector="input.YEhxqQNi", value="xxx")
→ 返回错误："No such element" 或 "Element is not visible"
```

**常见失效原因**：
- **UUID选择器**：`#common-menu-item-936e0b4e-xxx`（每次生成不同）
- **CSS Modules哈希**：`.searchBtn-Pe9pEs`、`.addReportBtn-FOIiZ8`（打包后变化）
- **Vue/React动态属性**：`[data-v-abc123]`（构建时生成）
- **位置选择器**：`div:nth-child(3)`（DOM结构变化失效）

### 1.2 失效后的处理流程

```
执行DATASAVER录制步骤（chrome_click_element等）
   ↓
判断执行结果
   ├─ 成功 → 记录原selector到workflow，继续下一步
   └─ 失败 → 触发CSS失效处理流程：
           1. 意图推断（本文档第2章）
           2. 动态查找新selector（本文档第3章）
```

---

## 2. 意图推断原则

CSS失效后，第一步是推断用户的操作意图。意图推断只回答"用户想做什么"，不生成workflow步骤。

### 2.1 策略1：有 node data.description → 直接使用

**来源**：description是DATASAVER录制时自动捕获的元素文本内容

**推断方法**：
```
data.description: "人群"
→ 操作意图："点击包含'人群'文本的菜单项"
→ 查找方式：chrome_get_interactive_elements(textQuery="人群")
```

**关键点**：
- 准确反映用户点击的元素（按钮文本、菜单项等）
- 简单直接，优先使用此策略

---

### 2.2 策略2：无 node data.description → 综合推断

**推断线索**（多线索互相印证）：
1. **顶级description**：整个流程的业务目标（北极星）
2. **selector语义**：类名/ID中的关键词（search、submit、cancel、addReportBtn等）
3. **前后步骤**：上下文操作流程（填写 → 提交、点击展开 → 选择）
4. **节点特征**：label类型、data.value值、元素类型

**推断方法**：
```
示例1 - forms节点：
  顶级description: "巨量云图下创建人群报告"
  + label: "forms", data.value: "lyl-test5-dm"
  + 前一步: 点击新建报告按钮
  → 操作意图："在报告名称输入框填写名称"
  → 查找方式：Task Tool（复杂推断 + 填写）

示例2 - event-click节点：
  selector: ".addReportBtn-FOIiZ8"（包含addReportBtn关键词）
  + 顶级description: "创建人群报告"
  → 操作意图："点击新建报告按钮"
  → 查找方式：chrome_get_interactive_elements(textQuery="新建") 或 Task Tool
```

**关键原则**：
- 不依赖单一线索，综合判断
- 顶级description是北极星
- 前后步骤提供上下文（理解操作流程）
- selector语义辅助（即使失效，命名仍有价值）
- 不确定时可用chrome工具辅助验证

**推断输出**：
- 操作意图（文本描述）
- 推荐的查找方式（chrome_get_interactive_elements 或 Task Tool 调用 chrome_accessibility_snapshot 或 chrome_get_web_content 全面分析）

---

## 3. CSS失效处理完整流程示例

根据DATASAVER节点特征，分为3种场景。每个场景包含完整流程：DATASAVER节点 → 执行 → 失效 → 推断意图 → 生成workflow。

### 3.1 场景1：有data.description → chrome_get_interactive_elements（生成2步）

#### 完整示例：点击"人群"菜单

**DATASAVER节点配置**：

```json
{
  "id": "abc123",
  "label": "event-click",
  "type": "BlockBasic",
  "data": {
    "selector": "span#common-menu-item-936e0b4e-xxx",
    "description": "人群",
    "findBy": "cssSelector",
    "waitForSelector": true
  },
  "position": { "x": 600, "y": 300 }
}
```

---

**流程1：尝试执行原selector**
```
chrome_click_element(selector="span#common-menu-item-936e0b4e-xxx")
→ 失败："Element not found"（UUID selector失效）
```

---

**流程2：推断意图**（应用策略1）
```
data.description: "人群"
→ 操作意图："点击包含'人群'文本的菜单项"
→ 查找方式：chrome_get_interactive_elements(textQuery="人群")
```

---

**流程3：生成workflow步骤（2步）**

**步骤N：查找selector**
```json
{
  "step": 2,
  "tool_name": "mcp__chrome-server__chrome_get_interactive_elements",
  "tool_params": {
    "textQuery": "人群"
  },
  "output": {
    "selector": "动态查找到的selector"
  },
  "description": "查找'人群'菜单项",
  "datasaver_note": {
    "original_selector": "span#common-menu-item-936e0b4e-xxx",
    "original_description": "人群",
    "css_failed": true,
    "recovery_method": "使用textQuery动态查找"
  }
}
```

**步骤N+1：使用动态selector执行操作**
```json
{
  "step": 3,
  "tool_name": "mcp__chrome-server__chrome_click_element",
  "tool_params": {
    "selector": "{step_2.selector}"
  },
  "description": "点击'人群'菜单",
  "datasaver_note": {
    "uses_dynamic_selector": true,
    "selector_from_step": 2
  }
}
```

**关键点**：
- 步骤N返回output: {selector: "..."}
- 步骤N+1使用 `{step_N.selector}` 引用
- datasaver_note记录失效原因和恢复方法

### 3.2 场景2：无data.description → Task Tool深度推断（生成2步）

#### 完整示例：填写搜索框

**DATASAVER节点配置**：
```json
// 顶级description
"description": "获取douyin用户合集标签页下的内容"

// 当前节点
{
  "id": "a35a63bfe975",
  "label": "forms",
  "type": "BlockBasic",
  "data": {
    "disableBlock": false,
    "description": "",  // 缺失
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
}
```

---

**流程1：尝试执行原selector**
```
chrome_fill_or_select(selector="input.YEhxqQNi.jUqDCyab", value="甄会说")
→ 失败："No such element"（CSS Modules selector失效）
```

---

**流程2：推断意图**（应用策略2综合推断）
```
线索1 - 顶级description: "获取douyin用户合集标签页下的内容" → 需要搜索用户
线索2 - 节点特征: label="forms" + data.value="甄会说" → 填写用户名
线索3 - 前后步骤: 上一步打开抖音页面 → 第一个填写操作
线索4 - selector语义: "input.YEhxqQNi.jUqDCyab" → CSS Modules，无语义

综合推断：
  → 操作意图："在搜索框填写用户名"
  → 查找方式：Task Tool（需要综合推断 + 填写操作）
```

---

**流程3：生成workflow步骤（2步）**

**步骤N：Task Tool查找selector**
```json
{
  "step": 2,
  "tool_name": "task_tool",
  "tool_params": {
    "description": "查找搜索框selector",
    "prompt": "当前页面：抖音页面，页面已加载完成。\n\n执行任务：\n1. 调用 chrome_accessibility_snapshot() 获取页面元素树\n2. 分析元素树找到搜索框（通常是input或textbox role，可能包含'搜索'的label或placeholder）\n3. 返回JSON格式：{\"selector\": \"找到的CSS选择器\", \"uid\": \"元素uid\"}\n\n严格要求：\n- 只返回目标元素信息，不要返回完整元素树\n- 必须包含uid字段，用于后续chrome_fill_or_select",
    "subagent_type": "general-purpose",
    "model": "sonnet"
  },
  "purpose": "selector_finding",
  "output": {
    "selector": "找到的selector",
    "uid": "找到的元素uid"
  },
  "description": "使用chrome_accessibility_snapshot动态查找搜索框",
  "datasaver_note": {
    "original_selector": "input.YEhxqQNi.jUqDCyab",
    "css_failed": true,
    "recovery_method": "Task Tool调用chrome_accessibility_snapshot分析元素树查找",
    "inference_source": "topLevelDescription + forms节点特征"
  }
}
```

**步骤N+1：使用动态selector填写**
```json
{
  "step": 3,
  "tool_name": "mcp__chrome-server__chrome_fill_or_select",
  "tool_params": {
    "selector": "{step_2.selector}",
    "value": "{douyin_username}"
  },
  "description": "填写搜索框",
  "datasaver_note": {
    "uses_dynamic_selector": true,
    "selector_from_step": 2
  }
}
```

**关键点**：
- Task Tool只负责查找selector，返回output: {selector: "..."}
- 下一步使用 `{step_N.selector}` 引用动态selector
- 与场景1保持一致的2步模式
- datasaver_note记录推断来源和动态引用关系

## 4. 关键决策点

### 4.1 何时使用chrome_get_interactive_elements（不需要Task Tool）

**条件**：
- 有明确的 node 级别的description字段
- 或从顶级description/selector语义推断出明确文本内容
- 操作简单（单步点击、填写）

**优势**：
- 快速、简洁
- 返回精确selector
- 不需要Task Tool包装

**示例**：
```
description="人群" → chrome_get_interactive_elements(textQuery="人群")
description="搜索按钮" → chrome_get_interactive_elements(textQuery="搜索")
```

### 4.2 何时使用Task Tool

**条件1：无description，需深度推断**
```
DATASAVER节点：
- selector: "input.YEhxqQNi"
- description: ""（缺失）
- value: "甄会说"

需要推断：
- 从顶级description: "获取用户合集"
- 结合forms节点特征
- 综合推断："填写搜索框"

→ 生成2步：Task Tool查找selector + chrome_fill_or_select使用selector
```

**条件2：需要调用大数据工具时必须使用Task Tool封装**

以下工具返回大量数据，必须通过Task Tool隔离：

1. **chrome_accessibility_snapshot()** - 页面元素分析
   - 返回~4k tokens元素树数据
   - 用于查找元素uid和详细页面结构
   - 通常标记为 `purpose: "selector_finding"`
   - **优先用于元素查找**（元素覆盖率高：151 vs 35）

2. **chrome_get_web_content()** - 获取页面信息
   - 返回OSS URL然后WebFetch 获取URL对应的HTML内容
   - 用于提取结构化数据
   - 通常标记为 `purpose: "get_html_info"`
   - **用于获取完整HTML并分析的场景**
   - **说明**：这是一种页面分析、获取页面信息、收集数据的方式

3. **chrome_screenshot()** - 截图分析
   - 返回~84k tokens base64图片
   - 用于视觉验证和分析或者收集页面信息

风险：污染主agent上下文

→ 必须使用Task Tool隔离大数据处理

**条件3：复杂操作（多步骤组合）**
```
场景：
- 连续点击canvas 5次触发数据展示然后分别收集
- 查找元素 + 滚动 + 再查找

→ 使用Task Tool封装完整逻辑
```

**条件4：mark-element节点（数据收集场景）**

```
场景：
- DATASAVER的mark-element节点
- data.purpose描述要收集的数据
- data.textPreview展示数据预览

 → 必须使用 web-data-extractor skill (purpose="get_html_info")
 → 使用purpose和textPreview指导数据提取
```

### 4.3 决策流程图

```
DATASAVER录制步骤执行失败（CSS失效）
   ↓
有明确description？
   ├─ 是 → chrome_get_interactive_elements(textQuery)
   │        生成2步：查找selector + 执行操作
   │
   └─ 否 → 检查节点类型
           ├─ mark-element → 数据收集场景
           │                必须使用 web-data-extractor skill (purpose="get_html_info")
           │                使用data.purpose和textPreview指导数据提取
           │
           └─ 其他交互节点 → Task Tool + chrome_accessibility_snapshot (selector_finding)
                          从顶级description/selector语义/前后步骤推断
                          生成2步：Task Tool查找selector+uid + 执行操作
                          标记 purpose: "selector_finding"
```

---

## 5. datasaver_note字段说明

### 5.1 CSS失效记录

**用于chrome_get_interactive_elements恢复的情况**：
```json
"datasaver_note": {
  "original_selector": "span#common-menu-item-936e0b4e-xxx",
  "original_description": "人群",
  "css_failed": true,
  "recovery_method": "使用textQuery动态查找"
}
```

**用于Task Tool恢复的情况**：
```json
"datasaver_note": {
  "original_selector": "input.YEhxqQNi",
  "css_failed": true,
  "recovery_method": "Task Tool推断意图并动态查找",
  "inference_source": "topLevelDescription + forms节点特征"
}
```

### 5.2 动态selector引用记录

```json
"datasaver_note": {
  "uses_dynamic_selector": true,
  "selector_from_step": 2
}
```

### 5.3 mark-element节点记录

```json
"datasaver_note": {
  "original_label": "mark-element",
  "original_selector": "div.ek9O6CWD",
  "original_purpose": "抖音甄会说用户下合集信息",
  "original_textPreview": "深度解说\n\n18.2万 播放\n\n更新至 2 集...",
  "data_extraction_strategy": "使用purpose和textPreview指导AI提取目标数据"
}
```

### 5.4 成功执行记录

```json
"datasaver_note": {
  "original_selector": "#semiTabcompilation span",
  "original_description": "合集",
  "css_verified": true
}
```

---

## 总结

### 核心原则

1. **信任录制**：优先直接执行DATASAVER录制的selector
2. **按需转换**：只在CSS失效时才动态查找
3. **精确恢复**：意图推断 → 动态查找 → 封装为workflow步骤
4. **特殊处理**：mark-element统一转web-data-extractor skill，以purpose和textPreview为核心

### 决策矩阵

| 情况 | description | selector状态 | 处理策略 | 工具选择                                             |
|-----|------------|------------|---------|--------------------------------------------------|
| 1 | 有 | 失效 | 动态查找 | chrome_get_interactive_elements                  |
| 2 | 无 | 失效（交互节点） | 深度推断 | Task Tool + chrome_accessibility_snapshot        |
| 3 | - | mark-element节点 | 获取页面信息 | web-data-extractor skill                         |
| 4 | 任意 | 成功 | 直接使用 | 原chrome工具                                        |

### 关键记忆点

- ✅ 有description → chrome_get_interactive_elements(textQuery)
- ✅ 无description（交互节点） → Task Tool + chrome_accessibility_snapshot（优先用于元素查找）
- ✅ mark-element节点 → 数据收集场景，必须使用 web-data-extractor skill
- ✅ data.purpose和data.textPreview是mark-element节点的核心指导
- ✅ 封装为2步时：步骤N查找selector/uid → 步骤N+1使用{step_N.selector}或{step_N.uid}
- ✅ datasaver_note记录失效原因和恢复方法
- ✅ chrome_accessibility_snapshot元素覆盖率高（151 vs 35），优先用于元素查找
- ✅ chrome_get_web_content主要用于获取页面信息，不是查找元素的首选
