# Common User Preferences Reference

This document contains common preference patterns that can be used as templates when adding user preferences to memory.

---

## File Handling Preferences

### Preference: Auto-send Files

**When**: User wants files sent immediately after generation

**Memory Entry:**
```markdown
### File Auto-Send
- **Rule**: 生成文件后必须使用message工具的path参数直接发送文件
- **Reason**: 用户需要直观可见的内容，不接受链接地址
- **Status**: Active
- **Learned**: 2026-03-06
- **Source**: 用户反复提醒
```

**Search Query**: `文件发送 偏好 自动发送`

**Application:**
```python
if file_generated:
    prefs = await reme.memory_search("文件发送 偏好")
    if prefs and "必须发送" in str(prefs):
        await message.send(path=file_path)
```

---

### Preference: File Format

**When**: User wants specific file formats

**Examples:**

**Markdown:**
```markdown
### File Format
- **Rule**: 文本文件使用Markdown格式
- **Reason**: 便于阅读和代码高亮
- **Status**: Active
- **Learned**: 2026-03-06
```

**Plain Text:**
```markdown
### File Format
- **Rule**: 文本文件使用纯文本格式（.txt）
- **Reason**: 兼容性和简洁性
- **Status**: Active
- **Learned**: 2026-03-06
```

**HTML:**
```markdown
### File Format
- **Rule**: 富文本文件使用HTML格式
- **Reason**: 需要样式和格式
- **Status**: Active
- **Learned**: 2026-03-06
```

---

## Code Style Preferences

### Preference: Concise Python Code

**When**: User wants brief, efficient Python code

**Memory Entry:**
```markdown
### Python Code Style
- **Rule**: Python代码要简洁，有注释，使用docstrings
- **Details**:
  - 使用docstrings描述函数
  - 最大3层嵌套
  - 优先使用列表推导式
  - 复杂逻辑添加中文注释
- **Reason**: 便于维护和理解
- **Status**: Active
- **Learned**: 2026-03-05
```

**Search Query**: `Python 代码风格 简洁 注释`

**Application:**
```python
# Before writing code
prefs = await reme.memory_search("Python 代码风格")
if prefs and "简洁" in str(prefs):
    # Apply concise style
    use_docstrings()
    limit_nesting(3)
    prefer_list_comprehensions()
```

---

### Preference: Verbose Documentation

**When**: User wants detailed comments

**Memory Entry:**
```markdown
### Code Documentation
- **Rule**: 代码必须有详细注释，解释每一步
- **Details**:
  - 函数用途
  - 参数说明
  - 返回值说明
  - 复杂逻辑逐行注释
- **Reason**: 便于学习和理解
- **Status**: Active
- **Learned**: 2026-03-05
```

---

### Preference: Type Hints

**When**: User wants Python type hints

**Memory Entry:**
```markdown
### Python Type Hints
- **Rule**: Python代码必须包含类型提示（type hints）
- **Reason**: 提高代码可读性和IDE支持
- **Status**: Active
- **Learned**: 2026-03-06
```

**Application:**
```python
def process_data(data: List[str]) -> Dict[str, int]:
    """
    处理数据并返回统计

    Args:
        data: 输入字符串列表

    Returns:
        统计结果字典
    """
    # ...
```

---

## Communication Preferences

### Preference: Markdown Responses

**When**: User prefers markdown-formatted responses

**Memory Entry:**
```markdown
### Response Format
- **Rule**: 除非生成文件，否则用markdown格式回复
- **Reason**: 阿伟喜欢markdown，便于阅读和复制
- **Status**: Active
- **Learned**: 2026-03-04
```

**Search Query**: `回复格式 markdown`

---

### Preference: Plain Text Responses

**When**: User wants simple plain text

**Memory Entry:**
```markdown
### Response Format
- **Rule**: 使用纯文本回复，不使用markdown格式
- **Reason**: 简洁直接
- **Status**: Active
- **Learned**: 2026-03-06
```

---

### Preference: Concise Responses

**When**: User wants brief answers

**Memory Entry:**
```markdown
### Response Length
- **Rule**: 回复要简洁明了，直击要害，不说废话
- **Details**:
  - 一句话能说清就一句话
  - 不分两条消息
  - 不啰嗦
- **Reason**: 提高效率，避免冗长
- **Status**: Active
- **Learned**: 2026-03-06
```

---

### Preference: Detailed Explanations

**When**: User wants thorough explanations

**Memory Entry:**
```markdown
### Response Length
- **Rule**: 回复要详细，包含步骤和原因
- **Details**:
  - 说明操作步骤
  - 解释为什么这样做
  - 提供注意事项
- **Reason**: 便于学习和理解
- **Status**: Active
- **Learned**: 2026-03-06
```

---

## Tool Usage Preferences

### Preference: web_fetch Timeout

**When**: User needs specific timeout for web_fetch

**Memory Entry:**
```markdown
### web_fetch Tool Settings
- **Tool**: web_fetch
- **Timeout**: 30秒
- **Retry**: 3次
- **Reason**: 某些网站（如theverge.com）响应慢
- **Status**: Active
- **Learned**: 2026-03-05
```

**Search Query**: `web_fetch 超时 设置`

---

### Preference: browser Wait Time

**When**: User needs specific wait time for browser tool

**Memory Entry:**
```markdown
### browser Tool Settings
- **Tool**: browser
- **Timeout**: 60秒
- **Wait Time**: 3秒（页面加载后）
- **Screenshot**: 是
- **Reason**: 确保页面完全加载和渲染
- **Status**: Active
- **Learned**: 2026-03-06
```

---

### Preference: exec Background Mode

**When**: User wants commands to run in background

**Memory Entry:**
```markdown
### exec Tool Settings
- **Tool**: exec
- **Background**: 是（默认）
- **PTY**: 否（除非需要交互式终端）
- **Reason**: 不阻塞对话，允许并行操作
- **Status**: Active
- **Learned**: 2026-03-06
```

---

## Research Preferences

### Preference: Preferred Sources

**When**: User wants specific sources prioritized

**Memory Entry:**
```markdown
### Information Sources
- **Preferred Sources**:
  1. 官方文档
  2. GitHub官方仓库
  3. 知名技术博客
- **Avoided Sources**:
  - 非官方教程
  - 过时内容
- **Reason**: 提高准确性和可靠性
- **Status**: Active
- **Learned**: 2026-03-06
```

**Search Query**: `信息来源 偏好 优先`

---

### Preference: Search Strategy

**When**: User wants specific search approach

**Memory Entry:**
```markdown
### Research Strategy
- **Rule**: 先搜索官方文档，再搜索社区资源
- **Details**:
  1. 官方文档优先
  2. GitHub issues/PRs次之
  3. Stack Overflow/SO次之
  4. 博客/教程最后
- **Reason**: 官方信息更准确
- **Status**: Active
- **Learned**: 2026-03-05
```

---

## Format Preferences

### Preference: Code Blocks

**When**: User wants code in specific format

**Memory Entry:**
```markdown
### Code Formatting
- **Rule**: 代码必须使用markdown代码块
- **Details**:
  - 指定语言：```python 或 ```javascript
  - 长代码使用折叠
  - 添加行号引用
- **Reason**: 便于阅读和复制
- **Status**: Active
- **Learned**: 2026-03-06
```

---

### Preference: Table Format

**When**: User prefers tables over lists

**Memory Entry:**
```markdown
### Table Formatting
- **Rule**: 多个条目使用表格而非列表
- **Example**:
  | 项目 | 数量 | 日期 |
  |------|------|------|
  | 文章 | 14  | 今日 |
- **Reason**: 便于对比和查看
- **Status**: Active
- **Learned**: 2026-03-06
```

---

## Error Prevention Preferences

### Preference: File Send Reminder

**When**: User was repeatedly forgotten about file sending

**Memory Entry:**
```markdown
### Error Pattern: Forget to Send Files
- **Pattern**: 生成文件后忘记发送给用户
- **Solution**: 每次生成文件后立即调用message.send(path=xxx)
- **Occurrences**: 3次
- **Last Occurrence**: 2026-03-06
- **Prevention**: 添加自动检查逻辑
```

**Search Query**: `错误 忘记 发送文件`

**Application:**
```python
async def generate_and_send(content, filename):
    # Generate
    await write(content, filename)

    # ALWAYS send
    await message.send(path=filename)

    # No exception - always check
```

---

### Preference: Timeout Handling

**When**: User experiences frequent timeouts

**Memory Entry:**
```markdown
### Error Pattern: Frequent Timeouts
- **Pattern**: web_fetch经常超时
- **Solution**: 增加超时到30秒，重试3次
- **Occurrences**: 多次
- **Affected Sites**: theverge.com, techcrunch.com
- **Prevention**: 配置更长的超时时间
```

---

## Language Preferences

### Preference: Chinese Responses

**When**: User wants Chinese language

**Memory Entry:**
```markdown
### Language Preference
- **Rule**: 所有回复使用中文
- **Exception**: 代码、技术术语（可保留英文）
- **Reason**: 用户的母语是中文
- **Status**: Active
- **Learned**: 2026-03-04
```

---

### Preference: English Responses

**When**: User wants English language

**Memory Entry:**
```markdown
### Language Preference
- **Rule**: All responses in English
- **Reason**: User prefers English
- **Status**: Active
- **Learned**: 2026-03-06
```

---

### Preference: Mixed Language (Code + Explanation)

**When**: User wants code in English, explanations in Chinese

**Memory Entry:**
```markdown
### Language Preference
- **Rule**: 代码用英文，解释用中文
- **Reason**: 代码规范性和可读性兼顾
- **Status**: Active
- **Learned**: 2026-03-06
```

**Example:**
```python
# Write file
async def process_data(data: List[str]) -> Dict[str, int]:
    # English variable names and comments
    result = {}
    for item in data:
        result[item] = result.get(item, 0) + 1
    return result

# Explain in Chinese
# 这个函数统计数据中每个字符串出现的次数
# 返回一个字典，键是字符串，值是计数
```

---

## Tone Preferences

### Preference: Professional Tone

**When**: User wants formal, professional tone

**Memory Entry:**
```markdown
### Communication Tone
- **Rule**: 使用专业、正式的语气
- **Avoid**:
  - 口语化表达
  - 过于随意的措辞
  - emoji（除非必要）
- **Reason**: 商业/专业场景
- **Status**: Active
- **Learned**: 2026-03-06
```

---

### Preference: Friendly/Casual Tone

**When**: User wants relaxed, conversational tone

**Memory Entry:**
```markdown
### Communication Tone
- **Rule**: 使用友好、轻松的语气
- **Include**:
  - 适当的emoji
  - 口语化表达
  - 更自然的对话
- **Reason**: 轻松的学习环境
- **Status**: Active
- **Learned**: 2026-03-06
```

---

## Template for New Preferences

Use this template when adding new preferences:

```markdown
### [Preference Category]
- **Rule**: [Clear, specific rule]
- **Details**:
  - [Specific requirement 1]
  - [Specific requirement 2]
  - [Exceptions if any]
- **Reason**: [Why this preference exists]
- **Status**: Active
- **Learned**: [YYYY-MM-DD]
- **Source**: [How/when learned - e.g., "用户明确要求", "从反馈学习"]
```

---

## Search Query Patterns

**For finding specific preference types:**

| Category | Search Query |
|----------|-------------|
| File handling | `文件发送 偏好 格式` |
| Code style | `代码风格 Python 简洁` |
| Communication | `回复格式 长度 语气` |
| Tool settings | `工具 超时 重试` |
| Research | `信息来源 优先 官方` |
| Error prevention | `错误 避免 模式` |

---

## Usage Checklist

When adding a new preference, ensure:

- [ ] Clear, specific rule
- [ ] Reason documented
- [ ] Timestamp included
- [ ] Status marked
- [ ] Source specified
- [ ] Search query noted
- [ ] Application method clear

---

**Version**: 1.0
**Last Updated**: 2026-03-06
