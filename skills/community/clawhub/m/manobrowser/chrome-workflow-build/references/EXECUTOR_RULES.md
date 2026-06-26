# 工具执行规则

## 概述
本文档定义了使用chrome-server MCP工具执行浏览器自动化任务的规则和最佳实践。这些规则从实际执行经验中提取，用于指导AI助手高效、准确地完成任务。

## 规则分类

### CS - 核心策略 (Core Strategy)
执行任务的整体策略和方法。

#### CS-001: 任务分析优先
- **规则**: 分析用户需求，选择合适的MCP tool工具
- **应用**: 在执行前充分理解任务目标，避免盲目尝试
- **示例**: 发帖任务需要先分析是创建新内容还是编辑现有内容

#### CS-002: 失败重试机制
- **规则**: 如果某个步骤失败，尝试其他方案
- **应用**: 准备备选方案，不要在一种方法上反复失败
- **示例**: 搜索按钮点击失败时，尝试使用Enter键提交

### RR - 推理要求 (Reasoning Requirements)
每次工具调用前的思考和说明要求。

#### RR-001: 目的明确性
- **规则**: 每次调用工具前，详细说明目的和预期结果
- **应用**: reasoning字段必须包含当前操作的具体目标
- **格式**: "为了[目标]，需要[操作]，预期[结果]"

#### RR-002: 上下文关联
- **规则**: 描述当前步骤与整体任务和前后步骤的关系
- **应用**: 说明这一步在整个流程中的位置和作用，尤其涉及到前后步骤需要依赖传递参数情况
- **示例**: "这是发布流程的第3步，在第2步获取的文本框内容填写标题后才能继续填写正文"

### TU - 工具使用 (Tool Usage)
具体工具的使用规范和注意事项。

#### TU-001: 参数完整性
- **规则**: 每个工具的参数和返回值都有详细的说明，请仔细阅读选择合适的工具
- **应用**: 使用工具前检查所有必需参数是否提供
- **示例**: chrome_keyboard必须指定keys参数，selector可选（如果需要焦点元素则必须添加不能忽略）

#### TU-002: 搜索执行策略
- **规则**: 搜索可以使用chrome_click_element点击搜索按钮，也可以使用chrome_keyboard输入Enter键
- **应用**: 如果一种方式不行，尝试另一种方式
- **示例**: 点击搜索按钮失败时，在搜索框按Enter键


#### TU-003: 元素查找策略
- **规则**: 查找页面元素时，**优先使用chrome_accessibility_snapshot**获取元素树和uid
- **应用**:
  - 必须通过Task Tool调用chrome_accessibility_snapshot
  - 返回元素的uid可直接用于chrome_click_element、chrome_fill_or_select等工具
  - 元素覆盖率高：页面全量元素
- **流程**: Task Tool → chrome_accessibility_snapshot → 分析元素树 → 返回精简信息（uid、role、name）
- **备选方案**: 仅当chrome_accessibility_snapshot不可用时，使用chrome_get_interactive_elements或chrome_get_web_content

#### TU-004: 数据收集使用规范
- **规则**:
  - **所有数据收集场景必须使用 `web-data-extractor` skill**
  - 调用方式：使用 Skill 工具，参数 `skill: "web-data-extractor"`
  - 必须标记 `purpose: "get_html_info"`
- **应用**:
  - 收集商品列表、用户信息、文章内容等页面数据
  - 提取点赞数、评论数、统计数据等
  - 获取表格、列表等内容
- **示例**:
```json
{
  "tool_name": "Skill",
  "tool_params": {
    "skill": "web-data-extractor",
    "args": "提取当前页面的商品信息"
  },
  "purpose": "get_html_info",
  "reasoning": "收集商品数据，使用web-data-extractor skill[应用TU-004]"
}
```

#### TU-005: chrome_accessibility_snapshot页面分析规范
- **规则**:
  - chrome_accessibility_snapshot **用于页面元素分析和交互**（不限于点击）
  - **必须**通过Task Tool调用（禁止主agent直接调用）
  - Subagent调用chrome_accessibility_snapshot()获取元素树
  - Subagent分析元素树完成任务（查找元素、分析结构、提取信息等）
  - 只返回精简结果
- **应用场景**:
  - 查找按钮并点击（返回uid用于chrome_click_element）
  - 查找输入框并填写（返回uid/selector用于chrome_fill_or_select）
  - 整体分析页面结构（返回表单元素列表）
  - 查找搜索框并输入（返回selector用于chrome_keyboard）
  - 查找链接并提取信息（返回href等属性）
  - 验证页面状态（检查错误提示、加载状态等）
- **标记规范**:
  - 根据实际用途选择purpose值：
    - 查找元素（按钮、输入框、链接等）→ `purpose: "selector_finding"`
    - 验证页面状态（检查错误提示、加载状态）→ `purpose: "verification"`
    - 分析页面结构（为后续操作查找元素）→ `purpose: "selector_finding"`
  - 返回格式必须精简：只包含必要的字段（uid、role、name、selector等）
- **设计理由**:
  - Token消耗可控：隔离在subagent中
  - 策略简单：无需判断页面复杂度
  - 避免预判：模型无法提前知道元素数量
  - 支持多种操作：不限于点击，涵盖所有页面交互
- **示例**:
```json
// 场景1：查找按钮并点击
{
  "tool_name": "task_tool",
  "tool_params": {
    "description": "查找发布按钮",
    "subagent_type": "general-purpose",
    "model": "sonnet",
    "prompt": "当前页面：小红书发布页，页面已加载完成。\n\n执行任务：\n1. 调用 chrome_accessibility_snapshot() 获取页面元素树\n2. 分析元素树找到\"发布\"按钮（通常是button role，文本包含\"发布\"）\n3. 返回JSON格式：{\"uid\": \"元素uid\", \"role\": \"button\", \"name\": \"发布\"}\n\n严格要求：\n- 只返回目标元素信息，不要返回完整元素树\n- 必须包含uid字段，用于后续chrome_click_element(uid=\"...\")"
  },
  "purpose": "selector_finding",
  "reasoning": "查找发布按钮，使用Task Tool隔离[应用TU-005]"
}

// 场景2：分析页面结构
{
  "tool_name": "task_tool",
  "tool_params": {
    "description": "分析表单结构",
    "subagent_type": "general-purpose",
    "model": "sonnet",
    "prompt": "当前页面：注册页面，页面已加载完成。\n\n执行任务：\n1. 调用 chrome_accessibility_snapshot() 获取页面元素树\n2. 分析页面结构，找到所有表单元素（输入框、按钮、下拉框）\n3. 返回JSON数组格式：[{\"type\": \"textbox\", \"name\": \"用户名\", \"uid\": \"...\"}, {\"type\": \"button\", \"name\": \"注册\", \"uid\": \"...\"}]\n\n严格要求：\n- 只返回表单元素列表，不要返回完整元素树"
  },
  "purpose": "selector_finding",
  "reasoning": "分析页面表单结构，使用Task Tool隔离[应用TU-005]"
}
```

#### TU-006: 页面跳转后的标签页管理
- **规则**:
  - 点击元素可能触发新标签页打开或页面跳转
  - 跳转后必须调用 get_windows_and_tabs 检查标签页状态
  - 根据返回结果识别新标签页并在后续步骤中使用正确的 tabId
- **应用场景**:
  - 点击链接打开新标签页（target="_blank"）
  - 点击按钮触发页面跳转
  - 访问用户主页、详情页等通常会打开新标签页的操作
  - 需要在新页面继续执行后续操作
- **检测方法**:
  - 点击操作后立即调用 get_windows_and_tabs
  - 对比操作前后的标签页数量和 URL
  - 如果有新标签页，记录新标签页的 tabId
  - 后续操作使用该 tabId 参数指定操作的标签页
- **示例**:
```json
// 步骤1：点击用户主页链接（可能打开新标签页）
{
  "reasoning": "当前状态分析：\n- 已在搜索结果页找到用户'甄会说'的主页链接\n- 链接元素uid为'1_42'\n- 点击该链接通常会打开新标签页\n\n为什么选择这个行动 [应用TU-006]：\n点击用户主页链接访问详情页。由于可能打开新标签页，点击后需要立即调用 get_windows_and_tabs 检查标签页状态，确保后续操作在正确的页面执行。\n\n期望获得什么结果：\n成功打开用户主页，并通过 get_windows_and_tabs 获取新标签页的 tabId。",
  "tool_name": "mcp__chrome-server__chrome_click_element",
  "tool_params": {
    "uid": "1_42"
  }
}

// 步骤2：检查并记录新打开的标签页
{
  "reasoning": "当前状态分析：\n- 已执行点击用户主页链接操作\n- 需要确认是否打开了新标签页\n- 后续需要在用户主页继续操作（点击'合集'标签）\n\n为什么选择这个行动 [应用TU-006]：\n调用 get_windows_and_tabs 检查当前所有打开的标签页。对比操作前的标签页数量，识别新打开的标签页及其 tabId。后续在该页面的操作需要使用这个 tabId 参数。\n\n期望获得什么结果：\n获取所有标签页信息，识别新打开的用户主页标签页的 tabId 和 URL，为后续操作提供正确的 tabId 参数。",
  "tool_name": "mcp__chrome-server__get_windows_and_tabs",
  "tool_params": {}
}

// 步骤3：在新标签页继续操作
{
  "reasoning": "当前状态分析：\n- 已确认新标签页 ID 为 123\n- 用户主页已加载完成\n- 需要点击'合集'标签\n\n为什么选择这个行动：\n使用上一步获取的 tabId=123，在新标签页中点击'合集'标签。\n\n期望获得什么结果：\n成功切换到合集标签页，显示用户的合集列表。",
  "tool_name": "mcp__chrome-server__chrome_click_element",
  "tool_params": {
    "selector": "#semiTabcompilation span",
    "tabId": 123
  }
}
```
- **关键点**:
  - 不是所有点击都需要检查，只在可能跳转的场景使用（点击链接、访问主页等）
  - 在 reasoning 中明确说明为什么需要检查标签页
  - get_windows_and_tabs 返回的标签页信息包括 tabId、url、active 等字段
  - 后续操作的 chrome 工具可以使用 tabId 参数指定操作的标签页
  - 如果没有打开新标签页，后续操作仍在当前标签页执行（不需要 tabId 参数）

### RS - 重新执行策略 (Retry Strategy)
处理失败和用户反馈的策略。

#### RS-001: 历史分析
- **规则**: 如果有执行历史，分析每一轮执行的步骤和用户的反馈
- **应用**: 从历史记录中提取已执行的步骤和反馈
- **目的**: 避免重复相同的错误

#### RS-002: 策略调整
- **规则**: 根据用户的建议调整执行策略，确保本次执行能解决用户提出的问题
- **应用**: 用户反馈优先级最高，据此修改执行计划
- **示例**: 用户提示"使用其他选择器"时，更换定位方法

#### RS-003: 状态续接
- **规则**: 分析当前任务的执行状态，选择是否复用之前轮次的执行结果继续执行
- **应用**: 不必从头开始，可以从中断点继续
- **决策**: 必要时先获取页面内容分析再决策从哪一步开始

### EH - 错误处理 (Error Handling)
处理执行过程中的错误和异常。

#### EH-001: 错误记录
- **规则**: 详细记录错误信息和上下文
- **应用**: 包含错误类型、发生位置、相关参数
- **格式**: `{"error": true, "message": "...", "context": {...}}`

#### EH-002: 降级策略
- **规则**: 主要方法失败时使用备选方案
- **应用**: 准备多种实现路径
- **示例**: 按钮点击失败时尝试键盘快捷键

#### EH-003: 用户通知
- **规则**: 遇到无法解决的问题时及时通知用户
- **应用**: 说明问题原因和可能的解决方案
- **格式**: 清晰描述问题、已尝试的方法、建议的操作

## 规则应用示例

### 示例1：基础导航和搜索
```
应用规则：
- CS-001: 分析用户需求，确定搜索目标
- RR-001: "为了找到目标用户，需要在搜索框输入关键词，预期跳转到用户主页"
- TU-002: 先尝试点击搜索按钮，如失败则使用Enter键
- EH-002: 如搜索无结果，尝试其他关键词
```

### 示例2：表单填写
```
应用规则：
- CS-001: 分析表单结构，确定必填字段
- RR-002: "这是注册流程第2步，需要依次填写用户名、邮箱和密码"
- TU-001: 确保所有必需参数都提供给chrome_fill_or_select
- TU-003: 使用chrome_accessibility_snapshot查找输入框元素
```

### 示例3：文件上传
```
应用规则：
- CS-001: 确认文件上传的目标元素
- RR-001: "为了上传图片，需要找到上传按钮并选择文件，预期显示预览"
- TU-001: chrome_input_upload_file需要提供完整的文件路径或URL
- CS-002: 上传失败时尝试其他方式（如拖拽上传）
- EH-001: 记录上传错误详情，包括文件大小、格式等
```

### 示例4：内容发布
```
应用规则：
- CS-001: 分析发布流程的必要步骤
- RR-002: "这是发布流程的最后一步，前面已填写标题和内容，现在点击发布"
- TU-003: 使用chrome_accessibility_snapshot查找发布按钮，获取uid
- RS-003: 如果页面已在发布状态，从当前状态继续
- EH-003: 发布失败时告知用户具体原因
```

### 示例5：错误处理和重试
```
应用规则：
- RS-001: 分析之前失败的原因，避免重复错误
- RS-002: 根据用户反馈"按钮位置变了"调整选择器
- CS-002: 准备多个备选方案（不同的选择器、快捷键等）
- EH-002: 主方案失败后自动尝试备选方案
- EH-003: 多次尝试失败后，清晰告知用户问题和建议
```

### 示例6：收集页面数据
```
应用规则：
- CS-001: 分析需要收集的数据类型
- TU-004: 使用 web-data-extractor skill 收集数据
- RR-001: "为了收集商品列表，需要调用 web-data-extractor skill 提取页面数据"
- EH-001: 记录数据提取过程中的错误（字段缺失、格式错误等）
```

### 示例7：页面元素分析
```f
应用规则：
- CS-001: 分析需要查找的元素特征
- TU-005: 使用Task Tool封装chrome_accessibility_snapshot
- RR-001: "为了查找发布按钮，需要分析页面元素树，预期返回按钮的uid和基本信息"
- TU-001: 确保返回的uid用于后续chrome_click_element操作
- EH-002: 如果找不到目标元素，尝试使用其他特征（role、name等）
```
