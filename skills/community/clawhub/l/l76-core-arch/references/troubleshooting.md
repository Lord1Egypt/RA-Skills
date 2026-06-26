# L76 Core Architecture - Troubleshooting Guide

Common issues, diagnostic steps, and solutions for skill development and execution.

## Quick Diagnostic Flow

```
Skill not working?
├─→ Check SKILL.md frontmatter (name, description, metadata)
├─→ Validate file structure (required files present?)
├─→ Test in isolation (node index.js --verbose)
├─→ Check OpenClaw logs for tool call failures
└─→ Review error categorization (recoverable vs fatal)
```

## Issue Categories

### 1. Skill Not Triggering

**Symptoms:**
- Skill doesn't activate when expected
- OpenClaw ignores skill description triggers

**Causes & Solutions:**

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Vague description | Skill doesn't match user query | Rewrite `description:` with specific trigger phrases |
| Missing frontmatter | YAML delimiter absent or malformed | Ensure `---` at start, valid YAML syntax |
| Name collision | Another skill has same name | Use unique kebab-case name |
| Skill not loaded | OpenClaw didn't discover skill | Check skill is in `workspace/skills/` or installed via clawhub |

**Debug Steps:**

```bash
# 1. Validate frontmatter
grep -A 10 "^---" SKILL.md

# 2. Check skill discovery
# (In OpenClaw chat)
/status skills

# 3. Test trigger manually
# Ask: "Can you help me with [skill description]?"
```

**Example Fix:**

```yaml
# ❌ Bad - Too vague
description: |
  A skill for doing things.

# ✅ Good - Specific triggers
description: |
  Create production-ready AgentSkills with complete architecture.
  USE when: building new skills, auditing skill structure, learning AgentSkills patterns.
```

---

### 2. Tool Call Failures

**Symptoms:**
- Skill starts but fails mid-execution
- Error messages about tool permissions or missing dependencies

**Common Tool Errors:**

#### `read` / `write` Failures

```javascript
// ❌ Fails silently if path doesn't exist
await read({ path: 'nonexistent/file.txt' });

// ✅ Check first, then read
const exists = await exec({ command: 'test -f file.txt' });
if (exists.exitCode === 0) {
  const content = await read({ path: 'file.txt' });
}
```

**Recovery Pattern:**

```javascript
try {
  await read({ path: 'config.json' });
} catch (error) {
  if (error.code === 'ENOENT') {
    return {
      status: 'error',
      error: 'Configuration file not found',
      recovery: 'Run setup first: node scripts/init.js',
      details: { path: 'config.json' }
    };
  }
  throw error;
}
```

#### `exec` Failures

```javascript
// ❌ Assumes command exists
await exec({ command: 'which non-existent-tool' });

// ✅ Check exit code
const result = await exec({ command: 'which node' });
if (result.exitCode !== 0) {
  return {
    status: 'error',
    error: 'Node.js not installed',
    recovery: 'Install Node.js from nodejs.org'
  };
}
```

#### `browser` / `web_search` Failures

- **Timeout**: Increase `timeoutMs` parameter
- **Rate limit**: Add retry with exponential backoff
- **Blocked by CORS**: Use `web_fetch` instead of `browser` for simple page reads

---

### 3. State Management Issues

**Symptoms:**
- State not persisting between runs
- State file corrupted or unreadable

**Diagnosis:**

```bash
# Check state file
cat state.json

# Validate JSON
node -e "JSON.parse(require('fs').readFileSync('state.json'))"
```

**Common Causes:**

| Issue | Cause | Solution |
|-------|-------|----------|
| State resets every run | State file in wrong location | Use absolute path or `__dirname` |
| JSON parse errors | Concurrent writes corrupting file | Use file locking or atomic writes |
| State grows unbounded | Not trimming old entries | Limit arrays (e.g., last 10 errors) |

**Robust State Pattern:**

```javascript
class StateManager {
  save() {
    try {
      // Atomic write: write to temp, then rename
      const tempFile = this.stateFile + '.tmp';
      fs.writeFileSync(tempFile, JSON.stringify(this.state, null, 2));
      fs.renameSync(tempFile, this.stateFile);
    } catch (error) {
      console.error('State save failed:', error.message);
      // Don't throw - state loss is not fatal
    }
  }

  trimErrors(maxErrors = 10) {
    if (this.state.errors.length > maxErrors) {
      this.state.errors = this.state.errors.slice(-maxErrors);
    }
  }
}
```

---

### 4. Performance Degradation

**Symptoms:**
- Skill takes >30 seconds to complete
- Memory usage grows over time
- Tool calls timeout frequently

**Diagnosis:**

```bash
# Measure execution time
time node index.js

# Check memory usage (Node.js)
node --inspect index.js
# Then check Chrome DevTools Memory tab
```

**Optimization Strategies:**

1. **Batch tool calls** - Don't call `read` 100 times in a loop; read once and parse
2. **Use pagination** - For large file sets, process in chunks of 10-20
3. **Cache expensive operations** - Store results in state if reused
4. **Avoid tight poll loops** - Use `yieldMs` or `timeout` in exec calls

**Example: Batch Processing**

```javascript
// ❌ Slow - sequential file reads
for (const file of files) {
  const content = await read({ path: file }); // 100 calls, 100s
}

// ✅ Fast - batch with concurrency limit
const BATCH_SIZE = 10;
for (let i = 0; i < files.length; i += BATCH_SIZE) {
  const batch = files.slice(i, i + BATCH_SIZE);
  const results = await Promise.all(
    batch.map(f => read({ path: f }))
  );
}
```

---

### 5. Publishing Failures (ClawHub)

**Symptoms:**
- `clawhub publish` returns errors
- Skill doesn't appear in search after publish

**Common Errors:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid frontmatter` | Missing required fields | Add `name`, `description`, `metadata.author`, `metadata.version` |
| `Skill name taken` | Name collision | Choose unique name or increment version |
| `Authentication failed` | Not logged in | Run `clawhub login` |
| `Validation failed` | Placeholder text or invalid structure | Run `scripts/validate.ps1` before publish |

**Debug Publish:**

```bash
# 1. Validate locally
powershell -ExecutionPolicy Bypass -File scripts/validate.ps1

# 2. Check login status
clawhub whoami

# 3. Dry-run publish (if supported)
clawhub publish . --dry-run

# 4. Publish with verbose output
clawhub publish . --verbose --changelog "Detailed changelog"
```

---

### 6. Memory Item Conflicts

**Symptoms:**
- Memory items overwrite each other
- Can't find previously saved memory

**Best Practices:**

1. **Use specific categories** - `Skills / Architecture` not just `Skills`
2. **Add unique tags** - `#skills #template #l76` for easy filtering
3. **Prefix skill-specific items** - `L76: Skill Structure Template`
4. **Don't save sensitive data** - No API keys, passwords, personal info

**Example Memory Item:**

```markdown
### L76: Tool Integration Patterns

**Category:** Skills / Tools / Patterns  
**Tags:** #skills #tools #patterns #l76  
**Content:**
Five core patterns for tool integration in AgentSkills: Sequential (Read→Process→Write), 
Conditional (check before acting), Error Recovery (catch-log-recover-report), 
Batch Processing (Promise.all with concurrency limits), State Management (JSON persistence).
```

---

## Diagnostic Commands

Quick reference for troubleshooting:

```bash
# Validate skill structure
powershell -ExecutionPolicy Bypass -File scripts/validate.ps1

# Test skill in isolation
node index.js --verbose

# Check JavaScript syntax
node --check index.js

# View state file
cat state.json | jq .

# Search for placeholder text
grep -r "TODO\|{placeholder}\|FIXME" .

# Check file sizes (should be <1MB each)
Get-ChildItem -File | Select-Object Name, Length

# Test tool calls manually
# (In OpenClaw chat, run individual tool commands)
```

---

## Error Response Templates

Use these templates for consistent error reporting:

### Recoverable Error

```javascript
return {
  status: 'partial',
  error: 'Network timeout while fetching data',
  recovery: 'Retry with --timeout 60 flag or check network connection',
  details: {
    attemptedUrl: 'https://api.example.com/data',
    timeout: 30000
  }
};
```

### User Action Required

```javascript
return {
  status: 'error',
  error: 'Missing configuration file',
  recovery: 'Run setup: node scripts/init.js or create config.json manually',
  details: {
    expectedPath: './config.json',
    exampleConfig: { apiKey: 'your-key-here' }
  }
};
```

### Fatal Error

```javascript
return {
  status: 'error',
  error: 'Critical dependency missing: Python 3.8+',
  recovery: 'Install Python from python.org, then retry',
  details: {
    required: 'python3',
    found: null,
    minVersion: '3.8'
  }
};
```

---

## Getting Help

When troubleshooting doesn't resolve the issue:

1. **Check existing skills** - Compare with working skills in `D:\OpenClaw\app-data\migrated\npm\node_modules\openclaw\skills`
2. **Review AgentSkills spec** - https://github.com/OpenClaw/spec
3. **Search ClawHub** - See how similar skills are structured
4. **Ask in OpenClaw community** - Provide error logs and skill structure

**When reporting bugs, include:**

- Skill name and version
- Full error message (not truncated)
- Steps to reproduce
- Expected vs actual behavior
- OpenClaw version (`openclaw --version`)

---

**Last Updated:** 2026-03-22  
**Version:** 1.0.0  
**Maintainer:** openclaw
