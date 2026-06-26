# Best Practices for Memory Management

This guide provides advanced patterns and best practices for using the memory-reme skill effectively.

---

## Core Principles

### 1. Memory is Useless Without Retrieval

**Principle**: Storing information is only valuable if it's retrieved and applied.

**Bad Practice:**
```python
# Store preference but never use it
reme.add_memory("User prefers concise code")

# Later... generate verbose code without checking
```

**Good Practice:**
```python
# Store AND retrieve
reme.add_memory("User prefers concise code")

# Later... always check first
prefs = await reme.memory_search("代码风格")
if "简洁" in prefs:
    apply_concise_style()
```

---

### 2. Be Specific When Storing

**Bad:**
```markdown
- User likes good code
```

**Good:**
```markdown
- User prefers concise, well-commented Python code
  - Use docstrings for all functions
  - Maximum 3 levels of nesting
  - Prefer list comprehensions
  - Comments in Chinese
```

**Why**: Specificity enables automatic application.

---

### 3. Update, Don't Duplicate

**Bad:**
```markdown
- User prefers concise code
- User likes short functions
- User wants minimal comments
```

**Good:**
```markdown
- User prefers concise, well-commented Python code
  - Use docstrings
  - Short functions (< 20 lines)
  - Comments only for complex logic
```

**Why**: Duplicates waste tokens and create ambiguity.

---

### 4. Use Timestamps

**Always include:**
- When the preference was learned
- Last time it was used
- When it was last updated

**Format:**
```markdown
- **Rule**: [Rule description]
- **Learned**: 2026-03-06
- **Last Used**: 2026-03-06
- **Last Updated**: 2026-03-06
```

**Why**: Helps identify stale preferences.

---

## Workflow Patterns

### Pattern 1: Preference-First Workflow

**When**: User clearly states a preference

```python
async def handle_with_preference(user_input):
    # 1. Search for relevant preferences
    prefs = await reme.memory_search(
        query=f"{get_task_type(user_input)} 偏好",
        max_results=3
    )

    # 2. Apply preferences
    if prefs:
        print(f"✓ Applying {len(prefs)} preferences")
        for pref in prefs:
            apply_preference(pref)

    # 3. Execute task
    result = execute_task(user_input)

    # 4. Verify application
    if result.needs_verification():
        prefs_applied = verify_preferences_applied(prefs)
        if not prefs_applied:
            log_error("Preferences not applied!")

    return result
```

---

### Pattern 2: Feedback Learning Workflow

**When**: User corrects your behavior

```python
async def learn_from_feedback(user_feedback):
    # 1. Analyze feedback
    if "忘记" in user_feedback or "忘记" in user_feedback:
        rule = extract_rule_from_feedback(user_feedback)
        category = categorize_rule(rule)

        # 2. Add to memory
        await reme.add_memory(
            content=f"用户偏好：{rule}",
            category=category,
            priority="high",
            source="用户纠正"
        )

        # 3. Acknowledge
        print(f"✓ 已记住：{rule}")

        # 4. Immediate verification
        if can_verify_now():
            await demonstrate_rule_application(rule)

    # 5. Update MEMORY.md
    await reme.summary_memory([{
        "role": "user",
        "content": user_feedback
    }])
```

---

### Pattern 3: Context-Aware Search

**When**: Different tasks require different memories

```python
async def get_context_preferences(task_type):
    queries = {
        "coding": "代码风格 Python 注释",
        "writing": "写作风格 格式",
        "file_generation": "文件发送 偏好 自动",
        "research": "搜索策略 来源"
    }

    query = queries.get(task_type, "偏好")
    return await reme.memory_search(query=query, max_results=5)


# Usage
if user_wants_code():
    prefs = await get_context_preferences("coding")
    apply_coding_prefs(prefs)
elif user_wants_file():
    prefs = await get_context_preferences("file_generation")
    apply_file_prefs(prefs)
```

---

### Pattern 4: Memory Cleanup Workflow

**When**: Periodic maintenance

```python
async def cleanup_memory():
    # 1. Identify old entries
    old_entries = await find_old_entries(days=30)

    # 2. Check relevance
    still_relevant = []
    for entry in old_entries:
        if is_still_relevant(entry):
            still_relevant.append(entry)

    # 3. Archive
    archived = [e for e in old_entries if e not in still_relevant]
    await archive_entries(archived)

    # 4. Merge duplicates
    duplicates = find_duplicates()
    await merge_duplicates(duplicates)

    print(f"✓ Archived {len(archived)} entries")
    print(f"✓ Merged {len(duplicates)} duplicates")
```

---

## Search Optimization

### 1. Use Hierarchical Queries

**Bad:**
```python
prefs = await reme.memory_search(query="偏好")
```

**Good:**
```python
# Narrow down by category
file_prefs = await reme.memory_search(query="文件发送 偏好")
code_prefs = await reme.memory_search(query="代码风格 偏好")
tool_prefs = await reme.memory_search(query="工具 超时 偏好")

# Apply by context
if generating_file():
    apply_prefs(file_prefs)
elif writing_code():
    apply_prefs(code_prefs)
```

---

### 2. Include User Identifier

**Bad:**
```python
prefs = await reme.memory_search(query="文件发送")
```

**Good:**
```python
prefs = await reme.memory_search(query="文件发送 偏好 阿伟")
```

**Why**: Distinguishes between multiple users.

---

### 3. Use Time-Sorted Results

```python
# Get results sorted by time
results = await reme.memory_search(
    query="代码风格",
    max_results=10
)

# Sort by recency
sorted_results = sorted(
    results,
    key=lambda x: x.get('time_created', 0),
    reverse=True
)

# Apply most recent first
for result in sorted_results:
    apply_preference(result)
```

---

## Error Prevention Patterns

### Pattern 1: Checklist-Based Prevention

**Before critical actions, check:**

```python
async def before_file_generation():
    # 1. Check file preferences
    file_prefs = await reme.memory_search("文件发送 偏好")

    # 2. Set flags
    auto_send = "必须发送" in str(file_prefs)

    # 3. Verify configuration
    if auto_send:
        print("✓ Auto-send configured")

    return auto_send


# After generation
async def after_file_generation(filepath):
    auto_send = await before_file_generation()

    if auto_send:
        await message.send(path=filepath)
        print("✓ File sent automatically")
```

---

### Pattern 2: Pattern Recognition

```python
async def detect_and_prevent_patterns():
    # Search for error patterns
    patterns = await reme.memory_search("错误模式 避免")

    current_action = get_current_action()

    for pattern in patterns:
        if matches_pattern(current_action, pattern):
            # Apply prevention
            solution = pattern.get('solution')
            apply_prevention(solution)

            print(f"✓ Prevented: {pattern['name']}")
            print(f"   Solution: {solution}")

            return True

    return False
```

---

## Advanced Techniques

### 1. Memory Clustering

**Group related preferences:**

```markdown
## Code Style Preferences

### Python
- Concise functions
- Docstrings required
- Type hints preferred

### JavaScript
- ES6+ syntax
- Async/await patterns
- Error handling with try/catch

### General
- Clear variable names
- Consistent formatting
- Meaningful comments
```

**Benefits:**
- Easier to find related preferences
- Better context understanding
- Reduced search scope

---

### 2. Preference Priority System

```python
async def get_prioritized_preferences(task):
    results = await reme.memory_search(query=f"{task} 偏好")

    # Sort by priority
    def priority_score(pref):
        if pref.get('priority') == 'high':
            return 3
        elif pref.get('priority') == 'normal':
            return 2
        else:
            return 1

    sorted_results = sorted(
        results,
        key=priority_score,
        reverse=True
    )

    return sorted_results


# Apply in priority order
for pref in get_prioritized_preferences("file_generation"):
    apply_preference(pref)
```

---

### 3. Memory Expiration

```python
async def check_expiration():
    entries = await reme.list_memory()

    for entry in entries:
        # Check if expired
        if 'expiration' in entry:
            if datetime.now() > entry['expiration']:
                # Delete or archive
                await reme.delete_memory(entry['id'])
                print(f"✓ Expired: {entry['content'][:50]}...")
```

**Use cases:**
- Time-sensitive preferences
- Temporary settings
- Experimental rules

---

## Common Pitfalls

### Pitfall 1: Over-Generalization

**Problem**: Storing too-general rules that can't be applied automatically.

**Example:**
```markdown
- User wants good code
```

**Fix:**
```markdown
- User wants concise, well-commented Python code with docstrings
```

---

### Pitfall 2: Ignoring Context

**Problem**: Applying preferences without considering current context.

**Example:**
```python
# Apply file preference to ALL file operations
prefs = await reme.memory_search("文件发送")
for op in all_file_operations:
    if "必须发送" in prefs:
        await send_file(op.path)
```

**Fix:**
```python
# Only apply to user-facing files
if op.is_user_facing():
    if "必须发送" in prefs:
        await send_file(op.path)
```

---

### Pitfall 3: Stale Memory

**Problem**: Old preferences no longer relevant.

**Example:**
```markdown
- User prefers Python 2.7 code
- **Learned**: 2018
- **Status**: Active (outdated!)
```

**Fix:**
```markdown
- User prefers Python 3.11+ code
- **Learned**: 2026-03-06
- **Status**: Active
- **Supersedes**: Python 2.7 preference
```

---

## Performance Tips

### 1. Batch Operations

```python
# Bad: Multiple individual searches
file_prefs = await reme.memory_search("文件")
code_prefs = await reme.memory_search("代码")
style_prefs = await reme.memory_search("风格")

# Good: Single search with broader query
all_prefs = await reme.memory_search("偏好 规则")

# Filter locally
file_prefs = [p for p in all_prefs if "文件" in p['content']]
code_prefs = [p for p in all_prefs if "代码" in p['content']]
```

---

### 2. Use Efficient Queries

**Bad:**
```python
prefs = await reme.memory_search(
    query="用户的关于代码的编写的风格方面的偏好",
    max_results=10
)
```

**Good:**
```python
prefs = await reme.memory_search(
    query="代码风格 偏好",
    max_results=10
)
```

**Why**: Shorter queries are more efficient and accurate.

---

### 3. Cache Frequently Accessed Memories

```python
class MemoryCache:
    def __init__(self, reme):
        self.reme = reme
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes

    async def get(self, query):
        # Check cache
        if query in self.cache:
            cached = self.cache[query]
            if time.time() - cached['time'] < self.cache_ttl:
                return cached['results']

        # Fetch from ReMe
        results = await self.reme.memory_search(query=query)

        # Update cache
        self.cache[query] = {
            'results': results,
            'time': time.time()
        }

        return results


# Usage
cache = MemoryCache(reme)
prefs = await cache.get("代码风格")
```

---

## Monitoring and Metrics

### 1. Track Memory Usage

```python
async def get_memory_stats():
    all_memories = await reme.list_memory()

    stats = {
        'total': len(all_memories),
        'by_type': {},
        'by_date': {},
        'by_priority': {}
    }

    for mem in all_memories:
        # Count by type
        mem_type = mem.get('type', 'unknown')
        stats['by_type'][mem_type] = stats['by_type'].get(mem_type, 0) + 1

        # Count by date
        date = mem.get('date', 'unknown')
        stats['by_date'][date] = stats['by_date'].get(date, 0) + 1

        # Count by priority
        priority = mem.get('priority', 'normal')
        stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + 1

    return stats
```

---

### 2. Track Application Rate

```python
class ApplicationTracker:
    def __init__(self):
        self.applications = {}
        self.successes = {}
        self.failures = {}

    def record(self, memory_id, success=True):
        # Record application
        if memory_id not in self.applications:
            self.applications[memory_id] = 0
        self.applications[memory_id] += 1

        # Track outcome
        if success:
            self.successes[memory_id] = self.successes.get(memory_id, 0) + 1
        else:
            self.failures[memory_id] = self.failures.get(memory_id, 0) + 1

    def get_effectiveness(self, memory_id):
        total = self.applications.get(memory_id, 0)
        successes = self.successes.get(memory_id, 0)

        if total == 0:
            return 0

        return (successes / total) * 100


# Usage
tracker = ApplicationTracker()
tracker.record(memory_id="abc123", success=True)
effectiveness = tracker.get_effectiveness("abc123")
```

---

## Summary

**Key takeaways:**

1. **Retrieve and apply**: Memory is useless without application
2. **Be specific**: Detailed rules enable automation
3. **Keep organized**: Structure prevents chaos
4. **Update regularly**: Stale memory causes errors
5. **Monitor usage**: Track effectiveness to improve

**Remember**: The goal is not just to remember, but to remember AND apply consistently.
