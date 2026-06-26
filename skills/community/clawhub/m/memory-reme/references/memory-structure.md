# Memory File Structure Guide

This document describes the complete structure of ReMe memory files used by the memory-reme skill.

---

## Directory Structure

```
.reme/
├── MEMORY.md                 # Long-term preferences and rules
├── memory/                    # Daily session summaries
│   ├── 2026-03-05.md
│   ├── 2026-03-06.md
│   └── ...
├── tool_result/               # Cached tool outputs
│   ├── uuid-001.txt
│   └── ...
└── .embeddings/               # Embedding cache
    └── embeddings.json
```

---

## MEMORY.md - Long-term Memory

### Purpose
Store persistent user preferences, rules, and configurations that should apply across all sessions.

### Structure

```markdown
# MEMORY.md - 长期记忆

## User Profile
- **Name**: [User name]
- **Role**: [User role/occupation]
- **Timezone**: [User timezone]
- **Notes**: [Additional notes]

---

## Preferences

### File Handling
- **Rule**: [Rule description]
- **Reason**: [Why this rule exists]
- **Status**: [Active/Inactive]
- **Learned**: [Date learned]
- **Source**: [How/when learned]

### Code Style
- **Language**: [Python/JavaScript/etc.]
- **Style**: [Concise/Verbose/Documentation-heavy]
- **Formatting**: [Specific formatting requirements]
- **Status**: Active
- **Learned**: [Date]

### Communication
- **Format**: [Markdown/Plain text/HTML]
- **Tone**: [Professional/Friendly/Casual]
- **Length**: [Concise/Detailed]
- **Status**: Active
- **Learned**: [Date]

### Tool Usage
#### web_fetch
- **Timeout**: [Seconds]
- **Retry**: [Number of retries]
- **Max Chars**: [Character limit]
- **Reason**: [Why these settings]

#### browser
- **Timeout**: [Seconds]
- **Wait Time**: [Seconds to wait after load]
- **Screenshot**: [Yes/No]
- **Reason**: [Why these settings]

#### exec
- **PTY**: [Yes/No]
- **Background**: [Yes/No]
- **Reason**: [Why these settings]

---

## Error Patterns to Avoid

### Pattern 1
- **Pattern**: [Description of error]
- **Solution**: [How to prevent it]
- **Occurrences**: [How many times it happened]
- **Last Occurrence**: [Date]

### Pattern 2
...

---

## Learning Points

### Learning 1
- **Lesson**: [What was learned]
- **Context**: [When/why this was learned]
- **Date**: [Date learned]

### Learning 2
...

---

## Tool Experiences

### Tool: [Tool Name]
- **Common Issues**: [Known problems]
- **Workarounds**: [Solutions to issues]
- **Best Practices**: [How to use effectively]
- **Last Updated**: [Date]
```

### Example

```markdown
# MEMORY.md - 长期记忆

## User Profile
- **Name**: 阿伟
- **Role**: 90后程序员、AI博主
- **Timezone**: Asia/Shanghai
- **Notes**: 关注AI编程、智能体实操、踩坑经验

---

## Preferences

### File Handling
- **Rule**: 生成文件后必须使用message工具的path参数直接发送文件
- **Reason**: 用户需要直观可见的内容，不接受链接地址
- **Status**: Active
- **Learned**: 2026-03-06
- **Source**: 用户反复提醒："你怎么总是忘记发送文件？"

### Code Style
- **Rule**: Python代码要简洁，有注释，使用docstrings
- **Reason**: 便于维护和理解
- **Status**: Active
- **Learned**: 2026-03-05
- **Source**: 用户偏好："代码写得太冗长了"

### Communication
- **Rule**: 除非生成文件，否则用markdown格式回复
- **Reason**: 阿伟喜欢markdown，便于阅读和复制
- **Status**: Active
- **Learned**: 2026-03-04
- **Source**: 初始设定

---

## Error Patterns to Avoid

### Pattern 1
- **Pattern**: 生成文件后忘记发送给用户
- **Solution**: 每次生成文件后立即调用message.send(path=xxx)
- **Occurrences**: 3
- **Last Occurrence**: 2026-03-06

---

## Learning Points

### Learning 1
- **Lesson**: web_fetch对某些网站需要30秒超时
- **Context**: theverge.com等大型网站响应慢
- **Date**: 2026-03-05

### Learning 2
- **Lesson**: 用户不喜欢啰嗦的解释
- **Context**: 多次提醒"简洁明了，直击要害"
- **Date**: 2026-03-04

---

## Tool Experiences

### Tool: web_fetch
- **Common Issues**: 某些网站返回429或404
- **Workarounds**: 重试3次，超时30s
- **Best Practices**: 使用markdown提取模式
- **Last Updated**: 2026-03-06
```

---

## memory/YYYY-MM-DD.md - Daily Summaries

### Purpose
Record session summaries, key events, and learnings for each day.

### Structure

```markdown
# 2026-03-06 Session Summary

## Session 1 - [Session Description]
**Time**: [Start time] - [End time]
**Duration**: [Duration]

### User Request
[User's initial request]

### Processing
- [Action 1]
- [Action 2]
- ...

### Output
- [Output 1]
- [Output 2]
- ...

### Files Generated
1. **[File 1]**
   - Size: [File size]
   - Sent: [Yes/No]
   - User feedback: [Feedback]

2. **[File 2]**
   - Size: [File size]
   - Sent: [Yes/No]

### User Feedback
[Feedback from user]

### Learning
✓ [What was learned]
✓ [Preferences updated]
✓ [Errors noted]

---

## Session 2 - [Session Description]
...
```

### Example

```markdown
# 2026-03-06 Session Summary

## Session 1 - AI News Aggregation
**Time**: 08:50 - 09:00
**Duration**: 10 minutes

### User Request
"给我今天的AI资讯"

### Processing
- Fetched from The Verge
- Fetched from Anthropic
- Fetched from Hugging Face
- Fetched from GitHub Trending
- Filtered and organized 14 items

### Output
- File: AI日报_2026-03-06.md
- Size: 3611 bytes
- Sent: ✓

### Files Generated
1. **AI日报_2026-03-06.md**
   - Size: 3611 bytes
   - Sent: Yes
   - User feedback: None

### User Feedback
"你怎么总是忘记发送文件？记住，生成文件后必须直接发送！"

### Learning
✓ 新规则：生成文件后必须自动发送
✓ 已更新 MEMORY.md
✓ 下次会话将应用此规则

---

## Session 2 - ReMe Integration
**Time**: 09:01 - 09:30
**Duration**: 29 minutes

### User Request
"接入ReMe后工作流程是怎样的"

### Processing
- Analyzed ReMe documentation
- Designed workflow
- Created integration plan
- Generated documentation

### Output
- File: ReMe工作流程设计.md
- File: ReMe存在形式与影响.md

### Files Generated
1. **ReMe工作流程设计.md**
   - Size: 11930 bytes
   - Sent: Yes

2. **ReMe存在形式与影响.md**
   - Size: 7302 bytes
   - Sent: Yes

### User Feedback
"reme在你这是以什么形式存在的，接入后会影响你本身能力和功能吗？"

### Learning
✓ 解释了ReMe的外部库特性
✓ 阐明了不影响核心能力
✓ 强调了增强功能

---

## Session 3 - Memory-reme Skill Creation
**Time**: 09:07 - 09:15
**Duration**: 8 minutes

### User Request
"探索是否可以把reme封装成记忆管理的skills"

### Processing
- Read skill-creator documentation
- Designed skill structure
- Created SKILL.md
- Created support scripts
- Created reference documentation

### Output
- File: memory-reme skill package

### Files Generated
1. **SKILL.md**
   - Size: 12295 bytes
   - Location: .clawdbot/skills/memory-reme/

2. **Support Scripts**
   - init_reme.py
   - search_memory.py
   - add_memory.py
   - save_summary.py

### User Feedback
None

### Learning
✓ 创建了完整的记忆管理skill
✓ 包含初始化、搜索、添加、保存功能
✓ 可立即使用
```

---

## tool_result/*.txt - Tool Output Cache

### Purpose
Store outputs from tools that exceed the context window threshold.

### File Format

```text
[Tool Output Content]
```

### Lifecycle

1. **Created**: When tool output exceeds threshold (default 1000 chars)
2. **Referenced**: Original message contains file path reference
3. **Retained**: For retention_days (default 7 days)
4. **Cleaned**: Automatically deleted after retention period

### Example Reference in Message

```
Tool output (truncated):
[First 1000 chars...]
...
📄 Full output saved to: tool_result/abc123-def456.txt
```

---

## Best Practices

### 1. Keep MEMORY.md Organized

- Use consistent sections
- Add timestamps
- Mark status clearly
- Archive old entries

### 2. Use Categories in Daily Files

- Separate by session
- Clear headers
- Track learnings

### 3. Regular Maintenance

**Weekly:**
- Review and update preferences
- Merge duplicate entries
- Archive old sessions

**Monthly:**
- Compress old memory files
- Clean up tool results
- Review error patterns

### 4. Search Optimization

- Use specific queries
- Include user name
- Add category keywords

---

## Backup and Recovery

### Backup Strategy

```bash
# Daily backup
cp -r .reme .reme.backup.$(date +%Y%m%d)

# Weekly archive
tar -czf .reme.archive.$(date +%Y%W).tar.gz memory/*.md

# Clean archives older than 3 months
find . -name "*.tar.gz" -mtime +90 -delete
```

### Recovery from Backup

```bash
# Restore specific day
cp -r .reme.backup.20260306/memory/2026-03-06.md .reme/

# Restore full state
cp -r .reme.backup.20260306/* .reme/
```

---

## File Size Guidelines

| File Type | Target Size | Max Size |
|-----------|-------------|-----------|
| MEMORY.md | < 10KB | < 50KB |
| Daily summary | < 5KB | < 20KB |
| Tool result | N/A | < 1MB |

**If files exceed max size:**
- Archive old entries
- Compress content
- Split into multiple files
