# 上下文隔离策略

使用 Task Tool 隔离大数据处理，保持主 agent 上下文清洁。

## 核心原则
1. **主 agent 提供意图**: 说明当前页面状态以及需要执行的工具操作和需要获取的信息
2. **Subagent 处理细节**: 调用工具、分析数据、返回主 agent 需要的精简信息
3. **明确purpose用途**: 标记Task Tool是获取页面信息还是辅助分析

## Task Tool 参数说明
- `description`: 描述调用工具的目的需求
- `subagent_type`: general-purpose
- `model`: sonnet
- `prompt`: 必须包含:
  - 任务背景
  - 具体tool调用方式
  - 返回格式(使用"只返回"明确限制)
- `purpose`: **必填** - 标记用途
  - `"get_html_info"` - 获取页面信息型，如果收集数据用，必须保留到workflow
  - `"selector_finding"` - 选择器查找型，根据 output 是否被后续步骤引用决定保留或过滤
  - `"verification"` - 辅助分析型 (验证)，过滤不保留

## Task Tool 的两种用途

根据用途,Task Tool 分为两类,处理方式不同:

### 1. 获取页面信息型 (`purpose: "get_html_info"`)
- **用途**: 获取整个网页html数据用于获取页面信息分析或数据收集
- **特征**: 是workflow的核心功能步骤
- **处理**:  **保留到workflow中**
- **示例**: 采集商品列表、获取用户信息、提取文章内容

### 2. 选择器查找型 (`purpose: "selector_finding"`)
- **用途**: 动态查找页面元素的uid或selector
- **特征**: 返回的uid/selector供后续步骤使用
- **处理**: 根据 output 是否被后续步骤引用决定
  - **output 被引用**（如 `{step_N.uid}`）→ **保留**（执行性，动态参数必需）
  - **output 未被引用** → **过滤**（探索性，仅用于分析）
- **示例**: 查找搜索框uid供后续填写使用

### 3. 验证型 (`purpose: "verification"`)
- **用途**: 验证页面状态
- **特征**: 仅用于辅助主agent决策
- **处理**: **过滤不保留到workflow**
- **示例**: 确认页面加载状态、检查元素是否存在

## 选择器查找型示例 (`purpose: "selector_finding"`)

### 示例1：使用chrome_accessibility_snapshot查找页面元素

**场景**: 需要找到发布按钮但不知道选择器

**用途**: 查找元素uid，供后续步骤使用（如 output 被后续引用则保留到workflow）

**Task Tool 调用**:
```json
{
  "reasoning": "当前状态分析：\n- 已成功进入小红书发布页面\n- 页面已完全加载\n- 需要找到发布按钮但不知道确切的选择器\n\n为什么选择这个行动 [应用TU-005]：\n页面元素未知，需要分析页面元素树找到发布按钮。使用Task Tool隔离chrome_accessibility_snapshot 避免污染主上下文。\n\n期望获得什么结果：\n获取发布按钮的uid、role、name等信息，用于后续的chrome_click_element操作。",
  "tool_name": "task_tool",
  "tool_params": {
    "description": "查找发布按钮",
    "subagent_type": "general-purpose",
    "model": "sonnet",
    "prompt": "当前页面：小红书发布页，页面已加载完成。\n\n执行任务：\n1. 调用 chrome_accessibility_snapshot() 获取页面元素树\n2. 分析元素树找到\"发布\"按钮（通常是button role，文本包含\"发布\"）\n3. 返回JSON格式：{\"uid\": \"元素uid\", \"role\": \"button\", \"name\": \"发布\"}\n\n严格限制：只能调用chrome_accessibility_snapshot一次，禁止调用其他工具。\n\n返回格式：\n- 只返回目标元素信息，不要返回完整元素树\n- 必须包含uid字段，用于后续chrome_click_element(uid=\"...\")"
  },
  "purpose": "selector_finding"
}
```

**返回结果**:
```json
{
  "uid": "1_42",
  "role": "button",
  "name": "发布笔记"
}
```
**处理方式**: 过滤不保留到workflow (最终workflow会直接使用uid或硬编码选择器)

**优势**:
- 元素覆盖率高
- 返回的uid可直接用于chrome_click_element(uid="1_42")
- Token消耗严格可控

### 示例2：验证页面状态 (`purpose: "verification"`)

**场景**: 需要确认页面是否正确加载

**用途**: 临时验证状态,辅助主agent决策下一步操作

**Task Tool 调用**:
```json
{
  "reasoning": "当前状态分析：\n- 已导航到发布页面\n- 需要确认页面是否正确加载\n- 关键元素（上传按钮、标题输入框）可见性未知\n\n为什么选择这个行动 [应用EH-001]：\n需要截图并分析页面状态。使用Task Tool处理图片分析，避免base64数据污染上下文。\n\n期望获得什么结果：\n获取页面加载状态（loaded、error、ready三个字段），用于决定下一步操作。",
  "tool_name": "task_tool",
  "tool_params": {
    "description": "验证页面加载状态",
    "subagent_type": "general-purpose",
    "model": "sonnet",
    "prompt": "当前tab已导航到发布页面。需要验证页面是否正确加载。\n\n执行：chrome_screenshot() 对当前tab截图，分析截图检查是否有错误提示，确认关键元素（上传按钮、标题输入框）是否可见。\n\n严格限制：只能调用chrome_screenshot一次，禁止调用chrome_navigate、chrome_get_web_content、chrome_click等任何其他工具。\n\n返回格式：{\"loaded\": true/false, \"error\": \"错误信息\", \"ready\": true/false}"
  },
  "purpose": "verification"
}
```

**返回结果**:
```json
{
  "loaded": true,
  "error": null,
  "ready": true
}
```

**处理方式**:  过滤不保留到workflow (这是临时验证,最终workflow假设页面正常加载)

## 数据收集场景（必须保留到workflow）

### 数据收集场景：必须使用 web-data-extractor Skill

**所有数据收集场景**（purpose="get_html_info"）必须使用 `web-data-extractor` skill。

**调用方式**：
```json
{
  "reasoning": "需要收集页面数据作为最终结果",
  "tool_name": "Skill",
  "tool_params": {
    "skill": "web-data-extractor",
    "args": "提取当前页面的[数据需求描述]"
  },
  "purpose": "get_html_info"
}
```

## 工具使用决策流程图

```
需要获取页面信息
    ↓
这个信息是用户最终需要的数据吗？
    ├─ YES → 数据收集场景
    │        ↓
    │        【必须】使用 web-data-extractor skill
    │        - purpose: "get_html_info"
    │        - 保留到workflow
    │
    └─ NO → 页面分析/元素查找场景
            ↓
            使用 chrome_accessibility_snapshot + Task Tool
            - purpose: "selector_finding"
            - 过滤不保留到workflow
            - Subagent内部：
              1. chrome_accessibility_snapshot() → 获取元素树
              2. 分析元素树 → 找到目标元素
              3. 返回精简结果（uid、role、name等）

特殊场景：
- 需要截图分析 → chrome_screenshot + Task Tool (purpose: "verification")
```

