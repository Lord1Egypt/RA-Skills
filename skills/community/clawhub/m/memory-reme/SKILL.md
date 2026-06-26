---
name: memory-reme
description: Memory management system powered by ReMe. Enables cross-session memory persistence, automatic user preference application, and intelligent context compression. Use when user asks to remember information, retrieve past context, apply user preferences, or manage long-term memory. Essential for preventing repeated mistakes and maintaining continuity across sessions.
---

# Memory-reme - ReMe Memory Management

A memory management system powered by ReMe that provides persistent cross-session memory, automatic user preference application, and intelligent context compression.

## When to Use This Skill

Activate this skill when:
- User asks you to remember something ("记住这个", "别忘了", "下次注意")
- User provides feedback on your behavior ("你总是忘记", "为什么又这样")
- User refers to past information ("之前说过", "上次怎么做的")
- User asks about your preferences or settings
- User wants to prevent repeated mistakes
- Long conversations where context might overflow

## Core Concepts

### Three-Level Memory

**1. Long-term Memory (MEMORY.md)**
- User preferences and rules
- Persistent across all sessions
- Updated manually or through learning

**2. Daily Memory (memory/YYYY-MM-DD.md)**
- Session summaries
- Important events and decisions
- Auto-generated at session end

**3. In-Memory Context**
- Current conversation state
- Compressed when approaching limits
- Temporary, session-bound

### Memory Types

| Type | Purpose | Example |
|-------|---------|----------|
| **Personal** | User preferences, habits | "Prefer concise code", "Always send files" |
| **Task** | Execution experience, patterns | "Python scripts should include error handling" |
| **Tool** | Tool usage experience | "web_fetch needs timeout 30s for this site" |

---

## Quick Start

### Installation (One-time setup)

```bash
pip install reme-ai
```

### Session Initialization

**At the start of EVERY session:**

1. Initialize ReMe
2. Retrieve user preferences
3. Apply to current context

```python
# Initialize
from reme.reme_light import ReMeLight
reme = ReMeLight(working_dir=".reme", language="zh")
await reme.start()

# Retrieve preferences
prefs = await reme.memory_search(
    query="用户偏好 文件发送",
    max_results=5
)

# Apply
if prefs and "必须发送" in prefs[0]['content']:
    auto_send_files = True
```

---

## Workflow

### Phase 1: Session Start (0-5s)

```
┌─────────────────────────────────┐
│  1. Initialize ReMe            │
│  2. Load MEMORY.md            │
│  3. Search for user prefs     │
│  4. Apply to current context   │
└─────────────────────────────────┘
```

**Action:**
```bash
python3 C:\path\to\memory-reme\scripts\init_reme.py
```

**Expected Output:**
```
✓ ReMe initialized
📖 Retrieved 3 preferences
  - User prefers concise code
  - Files must be sent automatically
  - Prefer markdown over plain text
✓ Preferences applied
```

---

### Phase 2: During Session

**Check before actions:**

1. **Before generating files:**
   - Search for file handling preferences
   - Apply formatting preferences

2. **Before using tools:**
   - Search for tool-specific preferences
   - Apply timeout/retry settings

3. **User feedback:**
   - Extract new rules
   - Add to MEMORY.md

**Example:**

User: "你怎么总是忘记发送文件？记住，生成文件后必须直接发送！"

**Action:**
```python
# Learn from feedback
await reme.add_memory(
    memory_content="用户偏好：生成文件后必须使用message工具直接发送文件，不接受链接地址。原因：用户需要直观可见的内容。",
    user_name="阿伟",
    memory_type="personal"
)
```

---

### Phase 3: Session End

```
┌─────────────────────────────────┐
│  1. Extract key events        │
│  2. Generate summary          │
│  3. Write to memory/          │
│  4. Update MEMORY.md         │
│  5. Cleanup tool results       │
│  6. Close ReMe               │
└─────────────────────────────────┘
```

**Action:**
```bash
python3 C:\path\to\memory-reme\scripts\save_summary.py
```

**Output:**
```
💾 Summary saved to memory/2026-03-06.md
✓ MEMORY.md updated
✓ Tool results cleaned
✓ ReMe closed
```

---

## Common Use Cases

### Use Case 1: File Generation

**Trigger:** User requests a file to be created

**Workflow:**
1. Check for file preferences
2. Generate file with correct format
3. Send automatically if required
4. Learn if user corrects

**Example:**
```
📖 Retrieved: "Send files automatically"

User: 生成AI日报

✓ Generated: AI日报_2026-03-06.md
📤 Sending file...
✓ Sent successfully
```

---

### Use Case 2: Code Style Preferences

**Trigger:** User asks to write code

**Workflow:**
1. Search for style preferences
2. Apply conventions
3. Format accordingly

**Example:**
```
📖 Retrieved: "Prefer concise, well-commented code"

User: 写个Python函数

✓ Applied: Concise style with docstrings
```

---

### Use Case 3: Preventing Repeated Mistakes

**Trigger:** User corrects your behavior

**Workflow:**
1. Accept feedback
2. Extract rule
3. Add to memory
4. Verify next time

**Example:**
```
User: Why do you keep forgetting to send files?

🧠 Learning...
✓ Rule recorded: "Always send files automatically"
✓ Will apply next time
```

---

### Use Case 4: Context Overflow

**Trigger:** Conversation approaches 70% of token limit

**Workflow:**
1. ReMe automatically triggers
2. Compresses history to summary
3. Keeps critical information
4. Continues conversation

**Automatic - no action needed.**

---

## Search Patterns

### Common Search Queries

| Goal | Query |
|-------|--------|
| **File preferences** | "文件发送 偏好 自动发送" |
| **Code style** | "代码风格 简洁 注释" |
| **Tool settings** | "工具 超时 重试" |
| **User habits** | "用户习惯 偏好" |
| **Past errors** | "错误 避免 重复" |

### Search Results Processing

**Always:**
1. Review returned memories
2. Filter by relevance and recency
3. Apply to current context
4. Document what was applied

**Example:**
```python
results = await reme.memory_search(query="文件发送 偏好", max_results=3)

for i, result in enumerate(results, 1):
    print(f"{i}. {result['content']}")
    if "必须发送" in result['content']:
        self.auto_send_files = True

print(f"✓ Applied: auto_send_files = {self.auto_send_files}")
```

---

## Memory File Structure

### MEMORY.md

```markdown
# MEMORY.md - Long-term Memory

## User Profile
- **Name**: 阿伟
- **Role**: 90后程序员、AI博主

## Preferences

### File Handling
- **Rule**: 生成文件后必须使用message工具直接发送
- **Reason**: 用户需要直观可见的内容
- **Status**: Active
- **Learned**: 2026-03-06

### Code Style
- **Rule**: 代码要简洁，有注释
- **Reason**: 便于维护和理解
- **Status**: Active
- **Learned**: 2026-03-05

## Tool Usage

### web_fetch
- **Timeout**: 30s
- **Retry**: 3 times
- **Reason**: 某些网站响应慢

### browser
- **Timeout**: 60s
- **Wait time**: 3s for page load
- **Reason**: 确保页面完全加载
```

### memory/YYYY-MM-DD.md

```markdown
# 2026-03-06 Session Summary

## Session 1 - AI News Aggregation

### User Request
"给我今天的AI资讯"

### Processing
- Scraped 8 sources
- Filtered 20+ articles
- Selected 14 items

### Output
- File: AI日报_2026-03-06.md
- Size: 3611 bytes
- Sent: ✓

### User Feedback
"你怎么总是忘记发送文件？记住，生成文件后必须直接发送！"

### Learning
✓ New rule: Auto-send files
✓ Updated MEMORY.md

---

## Session 2 - ReMe Integration

### User Request
"接入ReMe后工作流程是怎样的"

### Processing
- Analyzed ReMe documentation
- Designed workflow
- Created integration plan

### Output
- File: ReMe工作流程设计.md
- File: ReMe存在形式与影响.md
- Sent: ✓

### No User Feedback

### Learning
No new rules
```

---

## Best Practices

### 1. Always Start Sessions with Memory Retrieval

**Bad:**
```python
# Start without memory
user_request = get_user_input()
process_request(user_request)
```

**Good:**
```python
# Start with memory
reme = await init_reme()
prefs = await reme.memory_search(query="用户偏好")
apply_preferences(prefs)
user_request = get_user_input()
process_request(user_request)
```

---

### 2. Learn from Every Correction

**When user says "You forgot X":**
1. Acknowledge immediately
2. Extract the rule
3. Add to memory
4. Verify application

**Example:**
```
User: 你总是忘记发送文件！

Me: ✓ 已记住：生成文件后必须发送文件
   正在添加到 MEMORY.md...

Next file generation:
✓ File created
📤 Auto-sending...
✓ Sent
```

---

### 3. Be Specific in Memory Records

**Bad:**
```markdown
- User prefers good code
```

**Good:**
```markdown
- User prefers concise, well-commented Python code
  - Use docstrings for functions
  - Maximum 3 levels of nesting
  - Prefer list comprehensions over loops
```

---

### 4. Update Memory Regularly

**Daily tasks:**
- Review memory/ files
- Merge duplicate entries
- Remove outdated info
- Organize by category

**Weekly tasks:**
- Check for stale preferences
- Verify accuracy of tool settings
- Clean up old memory files

---

### 5. Use Semantic Search Effectively

**Bad queries:**
- "files"
- "code"
- "preferences"

**Good queries:**
- "文件发送 偏好 阿伟"
- "Python代码风格 简洁 注释"
- "工具设置 超时 重试"

**Why:** Specific queries return more relevant results.

---

## Troubleshooting

### Problem: Memory Not Retrieved

**Symptoms:**
- Preferences not applied
- Repeated mistakes
- Empty search results

**Solutions:**
1. Check if ReMe is initialized
2. Verify search query matches stored content
3. Check MEMORY.md exists and is not empty
4. Try broader search terms

```python
# Debug search
results = await reme.memory_search(query="文件")
print(f"Found {len(results)} results")
for r in results:
    print(f"  - {r['content'][:50]}...")
```

---

### Problem: Old Information Used

**Symptoms:**
- Outdated preferences applied
- Deprecated tool settings used

**Solutions:**
1. Add timestamp to memory entries
2. Sort results by time_created (reverse)
3. Manually update outdated entries in MEMORY.md
4. Consider expiration for time-sensitive rules

---

### Problem: Memory File Too Large

**Symptoms:**
- MEMORY.md > 10KB
- Search slow
- Context bloat

**Solutions:**
1. Archive old entries to memory/archive/
2. Merge similar preferences
3. Remove redundant info
4. Use categories to organize

---

## Integration with Existing Skills

### Combining with docx skill

**Workflow:**
```
1. Search memory for docx preferences
2. Apply formatting rules
3. Generate document with docx skill
4. Check if auto-send required
5. Send if needed
```

---

### Combining with coding-agent skill

**Workflow:**
```
1. Search memory for coding preferences
2. Apply style conventions
3. Generate code with coding-agent
4. Check for auto-review rules
5. Review if needed
```

---

## Performance Considerations

### Time Overhead

| Operation | Time | Impact |
|-----------|-------|---------|
| Session start | ~500ms | Negligible |
| Memory search | ~200ms | Negligible |
| File operations | ~100ms | Negligible |
| Summary generation | ~300ms | Negligible |
| **Total per session** | **~1s** | **Minimal** |

### Space Usage

```
.reme/
├── MEMORY.md          ~10KB
├── memory/           ~150KB (30 days)
├── tool_result/       ~5MB (auto-cleanup)
└── .embeddings/       ~1MB

Total: ~6MB (1 month)
```

---

## Advanced Features

### Conditional Application

**Only apply when relevant:**

```python
prefs = await reme.memory_search(query="文件发送")

if file_generated and prefs:
    # Apply file preferences
    if "必须发送" in prefs[0]['content']:
        await send_file(file_path)
```

---

### Context-Aware Retrieval

**Consider current task:**

```python
if task_type == "coding":
    query = "代码风格 Python"
elif task_type == "writing":
    query = "写作风格 简洁"
elif task_type == "file_generation":
    query = "文件发送 偏好"
```

---

### Memory Cleanup

**Automatic cleanup:**
- Tool results expire after 7 days
- Embedding cache refreshed weekly
- Memory files archived monthly

**Manual cleanup:**
```bash
# Archive old sessions
mv memory/2026-01-*.md memory/archive/

# Compress large files
gzip MEMORY.md
```

---

## See Also

- [memory-structure.md](references/memory-structure.md) - Detailed memory architecture
- [best-practices.md](references/best-practices.md) - Advanced patterns
- [common-prefs.md](references/common-prefs.md) - Common preference examples

---

## Summary

This skill enables persistent memory, automatic preference application, and intelligent context management. Use it to:

- ✓ Prevent repeated mistakes
- ✓ Remember user preferences
- ✓ Maintain context across sessions
- ✓ Learn from feedback
- ✓ Provide consistent behavior

**Key principle:** Memory is only useful when it's retrieved and applied. Always start sessions with memory retrieval, and verify application throughout the conversation.
