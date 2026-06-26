# 步骤过滤指南

## 概述

本指南用于帮助WORKFLOW模块正确识别和过滤日志中的步骤。通过分析reasoning内容和工具类型，区分探索性步骤（需要过滤）和执行性步骤（需要保留）。

## 核心原则

**关键决策点**：分析每个步骤的reasoning字段，这是判断步骤类型的主要依据。

## 快速判断表

### ✅ 保留这些步骤

| 步骤类型      | 判断依据 | 示例 |
|-----------|---------|------|
| **页面导航**  | chrome_navigate | 访问网站、跳转页面 |
| **用户交互**  | chrome_click_element, chrome_fill_or_select, chrome_input_upload_file | 点击按钮、填写表单、上传文件 |
| **中间触发**  | reasoning含"打开面板"、"展开选项"、"切换标签" | 打开筛选面板、切换到短剧tab |
| **收集数据类** | 调用 web-data-extractor skill 且 purpose=get_html_info | 获取网页数据作为最终结果（必须使用 web-data-extractor） |
| **最终验证**  | 最后的chrome_get_web_content 且 reasoning含"获取结果" | 获取完成后的数据 |

### ✅ 保留 - 执行性选择器查找

| 步骤类型 | 判断依据 | 示例 |
|---------|---------|------|
| **执行性选择器查找** | task_tool 且 purpose=selector_finding，**output 被后续步骤引用** | 查找搜索框uid，后续步骤用 `{step_N.uid}` 填写内容 |

**判断方法**：检查该步骤的 output 字段是否被后续步骤作为动态参数 `{step_N.xxx}` 引用。

### ❌ 过滤这些步骤

| 步骤类型 | 判断依据 | 示例 |
|---------|---------|------|
| **探索性选择器查找** | task_tool 且 purpose=selector_finding，**output 未被后续步骤引用** | 了解页面有哪些按钮（仅用于分析，不用于后续操作） |
| **验证状态** | task_tool 且 purpose=verification | 检查页面是否加载完成 |
| **探索页面** | chrome_get_web_content 且 reasoning含"了解"、"查看" | 获取页面结构用于分析 |
| **查找元素** | chrome_get_interactive_elements（未被后续引用） | 定位可交互元素用于分析 |
| **非必要截图** | chrome_screenshot 且 reasoning含"查看" | 查看页面状态（非必要） |
| **试错重试** | 重复的操作 | 多次尝试点击 |

## Task Tool 的特殊判断 ⭐

Task Tool 需要根据 **purpose** 字段和 **output 是否被引用** 判断：

```
task_tool 步骤
    ↓
检查 purpose 字段
    ↓
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│ get_html_info           │ selector_finding        │ verification            │
│ (数据收集类)            │ (查找选择器)             │ (验证状态)               │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ ✅ 保留                  │ ⚠️ 需进一步判断          │ ❌ 过滤                  │
│ 使用web-data-extractor  │                         │ 临时验证,假设正常         │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
                                    ↓
                          output 被后续步骤引用？
                          ({step_N.uid} 等动态参数)
                                    ↓
                    ┌───────────────┴───────────────┐
                    │ 是                            │ 否
                    │ ✅ 保留（执行性）              │ ❌ 过滤（探索性）
                    │ 动态参数必需                  │ 仅用于分析决策
                    └───────────────────────────────┘
```

### 三种 purpose 对比示例

#### ✅ 保留 - get_html_info 用于收集数据时

```json
{
  "step": "8",
  "type": "task_tool",
  "content": {
    "reasoning": "收集短剧列表数据作为最终结果返回",
    "tool_params": {
      "description": "收集短剧列表",
      "prompt": "用chrome_get_web_content获取页面,提取短剧信息,返回JSON数组"
    },
    "purpose": "get_html_info"
  }
}
```

**保留理由**：是workflow核心功能，无法用简单chrome工具替代

#### ✅ 保留 - 使用 web-data-extractor 收集数据

```json
{
  "step": "8",
  "type": "tool_call",
  "content": {
    "reasoning": "收集短剧列表数据作为最终结果返回",
    "tool_name": "Skill",
    "tool_params": {
      "skill": "web-data-extractor",
      "args": "提取当前页面的短剧信息"
    },
    "purpose": "get_html_info"
  }
}
```

**保留理由**：是workflow核心功能，数据收集场景必须使用 web-data-extractor

#### ✅ 保留 - 执行性 selector_finding（output 被后续步骤引用）

```json
// 步骤2：查找搜索框
{
  "step": "2",
  "type": "task_tool",
  "content": {
    "reasoning": "使用chrome_accessibility_snapshot查找搜索框元素",
    "tool_params": {
      "description": "查找搜索框",
      "prompt": "调用chrome_accessibility_snapshot()获取页面元素树,找到搜索框,返回{uid, role, name}"
    },
    "output": {"search_input_uid": "1_268"},
    "purpose": "selector_finding"
  }
}

// 步骤3：使用步骤2的output
{
  "step": "3",
  "type": "tool_call",
  "content": {
    "tool_name": "mcp__chrome-server__chrome_fill_or_select",
    "tool_params": {
      "uid": "{step_2.search_input_uid}",  // ← 引用了步骤2的output
      "value": "搜索内容"
    }
  }
}
```

**保留理由**：步骤2的output被步骤3作为动态参数引用，删除步骤2会导致步骤3无法执行

#### ❌ 过滤 - 探索性 selector_finding（output 未被后续引用）

```json
{
  "step": "5",
  "type": "task_tool",
  "content": {
    "reasoning": "了解页面有哪些可点击的按钮",
    "tool_params": {
      "description": "分析页面按钮",
      "prompt": "用chrome_accessibility_snapshot获取元素树,列出所有按钮"
    },
    "output": {"buttons": ["登录", "注册", "帮助"]},
    "purpose": "selector_finding"
  }
}
// 后续步骤未使用 {step_5.buttons}
```

**过滤理由**：仅用于探索分析，output未被后续步骤引用，可安全删除

#### ❌ 过滤 - verification

```json
{
  "step": "7",
  "type": "task_tool",
  "content": {
    "reasoning": "验证页面是否已完全加载",
    "tool_params": {
      "description": "验证页面状态",
      "prompt": "检查页面元素是否可见,返回验证结果"
    },
    "purpose": "verification"
  }
}
```

**过滤理由**：仅临时验证，最终workflow假设页面正常加载

## 过滤决策流程

``` mermaid
graph TD
    A[分析步骤] --> B{步骤类型?}

    B -->|task_tool| C{检查purpose}
    C -->|get_html_info| D[保留]
    C -->|selector_finding| SF{output被后续引用?}
    SF -->|是| D[保留-执行性]
    SF -->|否| E[过滤-探索性]
    C -->|verification| E

    B -->|tool_call| F{工具名称?}
    F -->|chrome_navigate| D
    F -->|chrome_click_element| D
    F -->|chrome_fill_or_select| D
    F -->|chrome_input_upload_file| D
    F -->|Skill| D
    F -->|其他| G{分析reasoning}

    G -->|中间触发关键词| D
    G -->|探索性关键词| H{是最终结果?}
    H -->|是| D
    H -->|否| E
    G -->|执行性关键词| D
    G -->|其他| E
```

## 实际应用示例

### 示例1：动态选择器场景（selector_finding 需保留）

使用动态选择器策略时，selector_finding 步骤的 output 被后续步骤引用，必须保留：

```json
// ✅ 步骤1 - 保留（页面导航）
{
  "type": "tool_call",
  "tool_name": "mcp__chrome-server__chrome_navigate"
}

// ✅ 步骤2 - 保留（执行性selector_finding，output被步骤3引用）
{
  "type": "task_tool",
  "reasoning": "查找搜索框元素获取uid",
  "output": {"search_input_uid": "1_268"},
  "purpose": "selector_finding"
}

// ✅ 步骤3 - 保留（使用步骤2的output）
{
  "type": "tool_call",
  "tool_name": "mcp__chrome-server__chrome_fill_or_select",
  "tool_params": {"uid": "{step_2.search_input_uid}", "value": "搜索内容"}
}

// ✅ 步骤4 - 保留（执行性selector_finding，output被步骤5引用）
{
  "type": "task_tool",
  "reasoning": "查找搜索按钮获取uid",
  "output": {"search_button_uid": "1_269"},
  "purpose": "selector_finding"
}

// ✅ 步骤5 - 保留（使用步骤4的output）
{
  "type": "tool_call",
  "tool_name": "mcp__chrome-server__chrome_click_element",
  "tool_params": {"uid": "{step_4.search_button_uid}"}
}

// ✅ 步骤6 - 保留（数据收集类）
{
  "type": "tool_call",
  "tool_name": "Skill",
  "tool_params": {"skill": "web-data-extractor", "args": "..."},
  "purpose": "get_html_info"
}
```

**结果**：全部6个步骤保留（selector_finding 的 output 被后续引用）

---

### 示例2：静态选择器场景（selector_finding 可过滤）

使用稳定的静态选择器时，selector_finding 仅用于执行时决策，可过滤：

```json
// ✅ 步骤1 - 保留（页面导航）
{
  "type": "tool_call",
  "tool_name": "mcp__chrome-server__chrome_navigate"
}

// ❌ 步骤2 - 过滤（探索性selector_finding，output未被引用）
{
  "type": "task_tool",
  "reasoning": "获取页面内容找到搜索框选择器",
  "output": {"selector": "#search-input"},  // 被硬编码到步骤3，非动态引用
  "purpose": "selector_finding"
}

// ✅ 步骤3 - 保留（使用硬编码选择器）
{
  "type": "tool_call",
  "tool_name": "mcp__chrome-server__chrome_fill_or_select",
  "tool_params": {"selector": "#search-input", "value": "搜索内容"}  // 硬编码
}

// ✅ 步骤4 - 保留（使用硬编码选择器）
{
  "type": "tool_call",
  "tool_name": "mcp__chrome-server__chrome_click_element",
  "tool_params": {"selector": "#search-button"}  // 硬编码
}

// ✅ 步骤5 - 保留（数据收集类）
{
  "type": "tool_call",
  "tool_name": "Skill",
  "tool_params": {"skill": "web-data-extractor", "args": "..."},
  "purpose": "get_html_info"
}
```

**结果**：5个步骤中过滤1个（步骤2），保留4个

## 边界情况处理

### 情况1：chrome_get_web_content 的判断

- **开始/中间** + reasoning含"分析"、"了解" → ❌ 过滤
- **最后** + reasoning含"获取结果"、"收集数据" → ✅ 保留
- 用于验证操作成功 → 根据具体情况判断

### 情况2：多次点击同一类型元素

- 为了找到正确的元素（试错） → ❌ 过滤重复的
- 批量操作（如勾选多个选项） → ✅ 全部保留

### 情况3：页面滚动操作

- 为了查看更多内容进行分析 → ❌ 过滤
- 为了加载更多数据或到达特定位置 → ✅ 保留

## 注意事项

1. **不要过度过滤**：宁可多保留一些步骤，也不要错过关键操作
2. **关注上下文**：同样的工具在不同上下文可能有不同用途
3. **保留依赖关系**：如果后续步骤依赖某个步骤的结果（`{step_N.xxx}`），要保留
4. **中间步骤很重要**：不要因为步骤"看起来不重要"就过滤掉必要的交互
5. **动态参数场景**：使用动态选择器策略时，selector_finding 步骤通常需要保留，因为其 output 被后续步骤引用
