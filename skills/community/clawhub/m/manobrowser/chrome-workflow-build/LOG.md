# 执行与记录模块

## 执行触发

**本模块在用户描述浏览器操作需求时触发（模式1-阶段1）。**

<mandatory-rule>
本模块是模式1（执行并记录流程）的第一阶段，负责执行任务并生成详细日志。
完成执行并保存日志后，会展示最终执行结果供用户确认。
用户确认后，将自动执行WORKFLOW.md（阶段2）和CREATOR.md（阶段3）。
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
| 1 | 初始化日志结构 | 初始化日志结构中 |
| 2 | 执行浏览器自动化操作 | 执行浏览器自动化操作中 |
| 3 | 展示执行摘要并等待用户确认 | 展示执行摘要并等待用户确认中 |
| 4 | 执行Skill发现检查 | 执行Skill发现检查中 |
| 5 | 保存日志文件并验证 | 保存日志文件并验证中 |

**状态管理规则**：

1. **开始步骤前**：将该步骤标记为 `in_progress`
2. **完成步骤后**：立即将该步骤标记为 `completed`
3. **同一时间**：只能有一个步骤处于 `in_progress` 状态
4. **顺序执行**：必须按步骤顺序执行，不可跳过

## 概述

使用chrome-server MCP工具执行浏览器自动化任务，同时记录每个操作的详细日志。本模块负责捕获完整的执行过程，包括用户输入、工具调用、推理过程和最终结果。

## 依赖资源
<mandatory-rule>
- [执行规则](references/EXECUTOR_RULES.md) - 工具执行的详细规则和最佳实践。使用工具执行浏览器操作时必须遵循。

- [日志模板](assets/log_template.json) - 标准日志格式示例。在开始执行任务前，必须先读取 log_template.json 了解完整的日志格式。

</mandatory-rule>

## 日志结构

### 顶层结构
```json
{
  "user_query": "string",           // 用户原始请求
  "created_at": "ISO 8601",         // 创建时间
  "completed_at": "ISO 8601",       // 完成时间
  "steps": [],                      // 执行步骤数组
  "final_result": "string",         // 最终执行结果
  "session_stats": {                // 会话统计
    "total_steps": "number",        // 总步骤数（包含所有类型）
    "user_feedback_count": "number", // 用户反馈次数
    "tool_call_count": "number",    // 工具调用次数
    "task_tool_count": "number"    // task_tool 调用次数
  }
}
```

### 步骤类型 (Step Types)

#### 1. 用户需求输入 (user_input)
```json
{
  "step": "string",
  "type": "user_input",
  "timestamp": "ISO 8601",
  "content": {
    "message": "string"
  }
}
```

#### 2. 工具调用 (tool_call)
```json
{
  "step": "string",
  "type": "tool_call",
  "timestamp": "ISO 8601",
  "content": {
    "reasoning": "string",
    "tool_name": "string",
    "tool_params": {},
    "output": "string",
    "success": "boolean"
  }
}
```

#### 3. 系统响应 (system_response)
```json
{
  "step": "string",
  "type": "system_response",
  "timestamp": "ISO 8601",
  "content": {
    "message": "string",
    "error": "boolean",         // 可选
    "final_result_preview": "string"  // 可选
  }
}
```

#### 4. 使用 Subagent (task_tool)

**说明**: 通过Task Tool隔离调用会返回大量数据的工具，在启用Task Tool前必须阅读[CONTEXT_ISOLATION.md](references/CONTEXT_ISOLATION.md)手册严格按要求执行

**何时使用**（必须满足其中之一）：
1. 需要调用 `chrome_get_web_content()`（获取页面信息）
2. 需要调用 `chrome_accessibility_snapshot()`（页面元素分析）
3. 需要调用 `chrome_screenshot()`（截图分析）

**上下文保护策略**：

- **绝对禁止**在主 Agent 中直接调用上述工具
- **必须**使用 Task Tool 隔离大数据处理（~4k-84k tokens）
- 每次 Task Tool 仅允许调用三个 tool 其中一个，**严禁**在 Task Tool 中调用多个 tool 操作

**数据结构**:
```json
{
  "step": "string",
  "type": "task_tool",
  "timestamp": "ISO 8601",
  "content": {
    "reasoning": "当前状态分析 + 为什么使用Task Tool + 期望获得什么结果",
    "tool_name": "task_tool",
    "tool_params": {
      "description": "简短描述（3-5字）",
      "prompt": "当前页面 + 执行任务 + 返回格式要求",
      "subagent_type": "general-purpose",
      "model": "sonnet"
    },
    "output": "subagent返回的精简结果",
    "purpose": "get_html_info | selector_finding | verification"
  }
}
```

**prompt 编写要点**：

- **明确当前状态**：告诉subagent当前在哪个页面、页面是否已加载
- **直接指定工具**：
  - chrome_get_web_content：`执行任务：\n1. 调用 chrome_get_web_content() 获取OSS URL\n2. 调用 WebFetch 获取URL对应的HTML内容\n3. 分析HTML提取...`
  - chrome_accessibility_snapshot：`执行任务：\n1. 调用 chrome_accessibility_snapshot() 获取页面元素树\n2. 分析元素树找到...\n3. 返回JSON格式：{...}`
  - chrome_screenshot：`执行：chrome_screenshot() 分析截图...`
- **精简返回格式**：要求subagent只返回关键信息，不要返回原始HTML/base64图片
- **禁止项说明**：
  - chrome_get_web_content：`严格要求：\n- 只返回精简的JSON结果，不要返回完整HTML`
  - chrome_accessibility_snapshot：`严格要求：\n- 只返回目标元素信息，不要返回完整元素树`

**字段说明**：
- `purpose`: 标记用途，决定是否保留到workflow
  - `get_html_info`: 获取页面信息 → **如果是收集数据作用，需要保留到workflow**
  - `selector_finding`: 查找元素 → **如果是必要步骤，需要保留到workflow**
  - `verification`: 验证状态 → **大概率过滤不保留**

#### 5. 数据收集场景必须使用 web-data-extractor

**说明**: 当需要收集页面数据作为最终结果时（purpose="get_html_info"），**必须**使用 `web-data-extractor` skill

**调用方式**：
```json
{
  "step": "string",
  "type": "tool_call",
  "timestamp": "ISO 8601",
  "content": {
    "reasoning": "需要收集页面数据作为最终结果",
    "tool_name": "Skill",
    "tool_params": {
      "skill": "web-data-extractor",
      "args": "提取当前页面的[具体数据需求]"
    },
    "output": "skill返回的数据",
    "purpose": "get_html_info"
  }
}
```

**注意**：`purpose` 字段仍需标记为 `"get_html_info"`，确保该步骤被保留到workflow

#### 6. 用户反馈 (user_feedback)

**说明**：用户在执行过程中提供的指导、纠正或建议

**记录时机**：
- 执行过程中用户发送新消息（中断当前流程）
- 用户纠正执行错误或提供更优策略
- 任务完成后用户提供改进建议

**数据结构**：
```json
{
  "step": "string",
  "type": "user_feedback",
  "timestamp": "ISO 8601",
  "content": {
    "message": "string"  // 用户反馈的具体内容
  }
}
```

**典型场景示例**：
1. **策略指导**：`"直接使用 https://creator.xiaohongshu.com/... 网页就可以上传图片发布笔记"`
2. **工具纠正**：`"用chrome_fill_or_select工具填写正文就可以"`
3. **参数修改**：`"标题改成'欧莱雅小棕瓶'"`
4. **流程优化**：`"应该先预览再发布"`

**后续处理要求**：
- 下一个tool_call步骤的reasoning必须明确引用反馈内容
- 使用 "根据用户的反馈..." 或 "用户明确指出..." 等表述
- 调整执行策略以响应用户指导

## 推理记录要求

### Reasoning字段规范
每个tool_call步骤的reasoning字段必须包含：

1. **当前状态分析** - 描述当前页面/系统状态
2. **决策依据** - 解释为什么选择这个工具和参数
3. **预期结果** - 说明这个操作预期达到的效果

### 示例格式
```
当前状态分析：
- 已成功访问小红书创作者发布页面
- 页面已完全加载，显示图文发布界面
- 找到了文件上传的input元素

为什么选择这个行动：
需要使用chrome_input_upload_file工具上传指定的图片文件。
根据用户提供的参数，需要上传指定URL的图片。

期望获得什么结果：
成功将指定的图片文件上传到小红书发布页面，
为后续填写标题和正文内容做准备。
```

### 页面跳转场景的 Reasoning 示例

**参考**：[EXECUTOR_RULES.md - TU-006](references/EXECUTOR_RULES.md) 中包含完整的页面跳转场景 reasoning 示例，包括：
- 点击链接可能打开新标签页的场景
- 检查新打开标签页的场景
- 在新标签页继续操作的场景

## 执行流程

### 阶段1：初始化
1. 接收用户请求 (user_query)
2. 记录创建时间 (created_at)
3. 添加user_input步骤

### 阶段2：执行循环
对于每个操作：
1. **推理阶段**
   - 分析当前状态 [应用CS-001]
   - 选择合适的工具 [应用RR-001]
   - 构造工具参数 [应用TU-001]

2. **执行阶段**
   - 调用chrome-server MCP工具
   - 记录tool_call步骤
   - 捕获输出和状态

3. **页面跳转检测**
   - 检查是否执行了可能触发跳转的操作
   - 如需要，调用 get_windows_and_tabs 检查标签页状态 [应用TU-006]
   - 记录新标签页的 tabId 供后续步骤引用

4. **用户反馈检测**
   - 检测用户是否发送了新消息
   - 如果有反馈，记录user_feedback步骤
   - 在后续reasoning中引用反馈内容

5. **后续决策**
   - 根据工具返回结果决定下一步
   - 处理错误情况 [应用EH-001]
   - 必要时尝试备选方案 [应用CS-002]

### 用户反馈处理机制

#### 检测用户反馈
在执行过程中，如果用户发送了新消息：

1. **立即记录为user_feedback步骤**
   ```json
   {
     "step": "4",
     "type": "user_feedback",
     "timestamp": "2025-11-18T18:59:45.477178",
     "content": {
       "message": "直接使用 https://creator.xiaohongshu.com/... 网页就可以"
     }
   }
   ```

2. **分析反馈类型**
   - **策略指导**：用户提供更直接的方法（如直接给出URL）
   - **工具纠正**：用户指出应该用哪个工具
   - **参数修改**：用户修改输入参数值
   - **流程调整**：用户建议改变执行顺序

3. **在后续reasoning中引用反馈**
   后续tool_call步骤必须明确引用反馈：
   ```json
   {
     "step": "5",
     "type": "tool_call",
     "content": {
       "reasoning": "根据用户的反馈，我需要直接导航到小红书创作者发布页面 https://creator.xiaohongshu.com/...\n\n分析当前状态：\n1. 用户已经明确指出了正确的发布页面URL\n2. 需要上传图片...\n\n执行策略：\n1. 首先导航到小红书创作者发布页面\n2. ...",
       "tool_name": "chrome_navigate",
       ...
     }
   }
   ```

#### 引用反馈的规范
- ✅ "根据用户的反馈，..."
- ✅ "用户明确指出了..."
- ✅ "用户建议使用..."
- ✅ "采纳用户建议，..."
- ✅ "根据用户纠正，..."

### 阶段3：完成与确认

<mandatory-rule>
⚠️ 关键要求：在保存日志文件之前，必须先向用户展示执行结果并等待确认！
</mandatory-rule>

#### 步骤3.1：展示执行摘要并等待用户确认

**在内存中准备好日志数据后（不要写入文件），先向用户展示执行摘要：**

```
✅ 阶段1：执行并记录 - 已完成

📊 执行摘要：
- 任务结果：[简述最终结果，例如：成功收集到抖音用户'甄会说'的8个合集信息]
- 执行步骤：{total_steps}个
- 工具调用：{tool_call_count}次
- Task Tool使用：{task_tool_count}次

请确认上述执行结果是否正确？

如果正确，我将：
1. 检查是否有已有的Skill可以满足您的需求
2. 如果没有匹配的Skill，则保存日志文件，然后继续自动执行阶段2（提取工作流）和阶段3（生成可复用的Skill）

如果有问题，请告诉我需要如何调整。
```

**等待用户响应**：
- **用户确认正确/继续**：执行步骤3.2 Skill发现检查
- **用户指出问题**：根据用户反馈调整，重新执行或修正

#### 步骤3.2：Skill发现检查

**触发条件**：用户确认log执行结果正确

**执行说明**：必须读取 [SKILL_DISCOVERY.md](SKILL_DISCOVERY.md) 并严格按照其中的指导执行智能Skill发现。

**核心流程**：

1. **提取用户意图**：从当前上下文中的user_query、整个执行链路和最终步骤综合分析业务需求
2. **扫描已有skills**：扫描当前环境可以使用的全部 Skills
3. **智能匹配分析**：平台必须一致、业务需求必须一致
4. **用户交互决策**：根据匹配度决定是否向用户推荐

**执行结果**：

- **发现高度匹配Skill（>=90分）**：
  - 向用户展示匹配 Skill 的信息
  - 等待用户决策：
    - 用户确认"满足需求" → 停止创建流程 + 展示匹配Skill的使用指导 → 结束整个流程（不保存日志）
    - 用户选择"不满足" → 继续执行步骤3.3保存日志

- **无匹配或低匹配（<90分）**：
  - 不提示用户，直接继续执行步骤3.3保存日志

**输出**：用户决策（使用已有Skill / 继续创建新Skill）

#### 步骤3.3：保存日志文件

**触发条件**：Skill发现无匹配或用户选择继续创建

<mandatory-rule>
⚠️ JSON生成要求：必须确保生成有效的JSON格式！
</mandatory-rule>

**生成日志时的强制要求**：

1. **字段处理**：
   - 如果字段值包含特殊字符（emoji、换行、引号等），必须正确转义以符合标准的JSON格式

2. **完整的日志结构**：
   ```json
   {
     "user_query": "用户原始请求",
     "created_at": "ISO 8601时间戳",
     "completed_at": "ISO 8601时间戳",
     "steps": [...],  // 所有执行步骤
     "final_result": "最终结果（必须正确转义）",
     "session_stats": {
       "total_steps": 数字,
       "user_feedback_count": 数字,
       "tool_call_count": 数字,
       "task_tool_count": 数字
     }
   }
   ```

3. **保存位置**：
   ```
   [当前工作目录]/workflow-logs/[skill-name]-log.json
   ```

4. **保存后验证**（必须执行）：
   ```bash
   python .claude/skills/chrome-workflow-build/scripts/validate_log.py workflow-logs/[skill-name]-log.json
   ```

5. **如验证失败**：
   - 分析错误信息
   - 修复JSON格式问题（通常是转义问题）
   - 重新保存并再次验证
   - 确保验证通过后再继续

**保存后流程**：
- 继续自动继续执行WORKFLOW.md（阶段2）和CREATOR.md（阶段3）

## 错误处理

### 工具调用失败
当工具调用失败时：
1. 记录错误信息到output字段
2. 设置success为false
3. [应用EH-002] 降级策略
4. 在下一步的reasoning中说明调整方案

### 用户中断
当用户在执行过程中发送新消息时：
1. **记录user_feedback步骤**
   - 捕获用户消息内容
   - 记录当前时间戳
   - 步骤号连续递增

2. **分析反馈内容** [应用RS-002]
   - 识别反馈类型（策略指导/工具纠正/参数修改/流程调整）
   - 理解用户意图
   - 确定需要调整的部分

3. **调整执行策略**
   - 更新后续步骤的reasoning
   - 采用用户建议的方法或工具
   - 修改参数或选择器

4. **继续执行**
   - 在reasoning中明确引用反馈
   - 说明如何响应用户指导
   - 保持执行连贯性

## 工具调用规则

### 导航策略

**在执行浏览器导航前，必须遵循以下原则：**

**❌ 禁止行为**：
1. **猜测和构造 URL**：不要自己拼接用户主页URL、不要假设URL格式
2. **跳过自然流程**：不要直接跳到目标页面，应从首页逐步导航
3. **假设页面结构**：不要假设tab的URL、不要假设参数格式

**✅ 正确行为**：
1. **使用搜索功能**：不知道URL时，从平台首页开始 → 使用搜索框 → 点击搜索结果
2. **逐步点击导航**：通过点击链接、切换tab等真实用户操作到达目标
3. **验证到达**：导航后检查是否到达正确页面

**推荐流程**：
```
首页 → 搜索框 → 输入关键词 → 回车 → 点击结果 → 到达目标页面
```

**记忆口诀**：
```
能搜索，就别猜
从首页，一步步路由
```

### 页面跳转和标签页管理

**点击可能触发页面跳转的元素后，必须检查并切换标签页 [应用TU-006]**

**触发场景**：
- 点击链接元素可能打开新标签页（target="_blank"）
- 点击按钮触发页面跳转
- 访问用户主页、详情页等操作

**处理要求**：
- 执行点击操作后立即调用 `get_windows_and_tabs` 检查标签页状态
- 记录新标签页的 tabId 供后续步骤使用
- 在 reasoning 中明确说明检查标签页的目的

**详细规则请参考**：[EXECUTOR_RULES.md - TU-006](references/EXECUTOR_RULES.md)

### 日期选择器处理

遇到日期选择器场景时，参考 [DATE_PICKER_HANDLING.md](references/DATE_PICKER_HANDLING.md) 执行操作。

## 日志验证

### 使用验证脚本
使用 `scripts/validate_log.py` 脚本对生成的日志进行验证：

```bash
# 验证日志文件
python scripts/validate_log.py workflow-logs/[skill-name]-log.json
```

### 验证结果格式
脚本将输出JSON格式的验证结果：
```json
{
  "is_valid": true,           // 是否通过验证
  "error_count": 0,            // 错误数量
  "warning_count": 3,          // 警告数量
  "errors": [],                // 错误列表
  "warnings": [                // 警告列表
    "步骤编号不连续: 期望'3'，实际'4'"
  ],
  "rule_usage": {              // 规则使用统计
    "CS-001": 2,
    "RR-002": 5,
    "TU-003": 1
  }
}
```

### 验证要点
- [验证脚本](scripts/validate_log.py) - 验证脚本会检查以下方面：
#### 1. 结构完整性
- 顶层结构必需的字段
- session_stats内部必需的字段

#### 2. 步骤验证
- 步骤类型正确性（user_input, tool_call, user_feedback, system_response）
- 每种类型的必需字段完整
- tool_call步骤必须包含reasoning字段
- user_feedback步骤后的tool_call应引用反馈内容

#### 3. 数据一致性
- 步骤编号连续性（从"1"开始递增）
- 时间戳格式正确（ISO 8601）
- 时间戳递增顺序
- 统计数据与实际步骤匹配