# L76 Core Architecture - Usage Examples

This file contains concrete examples of how to use and extend the L76 Core Architecture skill.

## Basic Usage

### Run as Standalone Script

```bash
cd D:\OpenClaw\workspace\skills\l76-core-arch
node index.js
```

### Run with Options

```bash
# Verbose output
node index.js --verbose

# Dry run (no side effects)
node index.js --dry-run

# Force execution
node index.js --force
```

## Integration Patterns

### Pattern 1: Tool Chaining

Chain multiple OpenClaw tools in sequence:

```javascript
// Read → Transform → Write
const content = await read({ path: 'input.md' });
const transformed = transformMarkdown(content);
await write({ path: 'output.md', content: transformed });
```

### Pattern 2: Conditional Workflows

```javascript
// Check if file exists before editing
const check = await exec({ command: 'test -f config.json' });
if (check.exitCode === 0) {
  await edit({ 
    path: 'config.json',
    oldText: '"debug": false',
    newText: '"debug": true'
  });
}
```

### Pattern 3: Error Recovery

```javascript
try {
  await riskyOperation();
} catch (error) {
  // Log the error
  await write({ 
    path: 'error.log', 
    content: `${new Date().toISOString()}: ${error.message}` 
  });
  
  // Attempt recovery
  await recoveryStep();
  
  // Report to user
  return { 
    status: 'recovered', 
    error: error.message,
    recovery: 'Completed fallback procedure'
  };
}
```

### Pattern 4: Batch Processing

```javascript
// Process multiple files efficiently
const files = await exec({ command: 'ls *.md' });
const results = [];

for (const file of files.stdout.split('\n').filter(Boolean)) {
  const content = await read({ path: file });
  const processed = processFile(content);
  results.push({ file, status: 'done' });
}

console.log(`Processed ${results.length} files`);
```

### Pattern 5: State Management

```javascript
// Track state across runs
const state = {
  lastRun: new Date().toISOString(),
  itemsProcessed: 42,
  errors: []
};

await write({
  path: 'state.json',
  content: JSON.stringify(state, null, 2)
});
```

## Real-World Skill Examples

### Example 1: File Organizer Skill

```markdown
---
name: file-organizer
description: Organize files in a directory by type, date, or custom rules.
---

# File Organizer

## Workflow

### 1. Scan Directory

```bash
ls -la {target_directory}
```

### 2. Categorize Files

Group by extension, size, or modification date.

### 3. Create Structure

```bash
mkdir -p documents images code archives
```

### 4. Move Files

```bash
mv *.pdf documents/
mv *.jpg images/
mv *.js code/
```

### 5. Report

List what was moved and where.
```

### Example 2: Git Hygiene Skill

```markdown
---
name: git-hygiene
description: Clean up Git repository, prune branches, and optimize storage.
---

# Git Hygiene

## Workflow

### 1. Check Status

```bash
git status
git branch -a
```

### 2. Prune Merged Branches

```bash
git branch --merged | grep -v '\*\|main\|master' | xargs git branch -d
```

### 3. Clean Reflog

```bash
git reflog expire --expire=30.days.ago
git gc --prune=30.days.ago
```

### 4. Report

Show disk space saved and branches removed.
```

### Example 3: Health Check Skill

```markdown
---
name: health-check
description: Run system health checks and report status.
---

# Health Check

## Workflow

### 1. Disk Space

```bash
df -h /
```

### 2. Memory Usage

```bash
free -m
```

### 3. Running Processes

```bash
ps aux | head -20
```

### 4. Recent Errors

```bash
journalctl -p 3 -xb --no-pager
```

### 5. Summary

Compile all checks into a single report.
```

## Error Handling Examples

### Handle Missing Dependencies

```javascript
try {
  await exec({ command: 'which required-tool' });
} catch (error) {
  return {
    status: 'error',
    error: 'Missing dependency: required-tool',
    recovery: 'Install with: npm install -g required-tool'
  };
}
```

### Handle Permission Errors

```javascript
try {
  await write({ path: '/system/file', content: 'data' });
} catch (error) {
  if (error.code === 'EACCES') {
    return {
      status: 'error',
      error: 'Permission denied',
      recovery: 'Run with elevated permissions or choose a different path'
    };
  }
  throw error;
}
```

### Handle Network Timeouts

```javascript
const timeout = setTimeout(() => {
  throw new Error('Network request timed out');
}, 30000);

try {
  const result = await fetch(url);
  clearTimeout(timeout);
  return result;
} catch (error) {
  return {
    status: 'partial',
    error: error.message,
    recovery: 'Retry with --timeout flag or check network connection'
  };
}
```

## Testing Your Skill

### Manual Testing

```bash
# Test in isolation
cd D:\OpenClaw\workspace\skills\your-skill
node index.js --verbose

# Test with sample data
echo "test input" | node index.js
```

### Integration Testing

```bash
# Test within OpenClaw context
# (Skill will be auto-loaded by OpenClaw)
```

### Validation Checklist

- [ ] Skill loads without errors
- [ ] All tool calls work correctly
- [ ] Error paths are tested
- [ ] Output is clear and actionable
- [ ] No sensitive data is leaked
- [ ] Skill is idempotent (safe to re-run)
- [ ] Documentation is complete

## Publishing to ClawHub

### 1. Prepare Metadata

Update SKILL.md frontmatter:

```yaml
---
name: your-skill
description: Clear, concise description
metadata:
  author: your-name
  version: "1.0.0"
---
```

### 2. Login to ClawHub

```bash
clawhub login
```

### 3. Publish

```bash
clawhub publish ./your-skill \
  --slug your-skill \
  --name "Your Skill Name" \
  --version 1.0.0 \
  --changelog "Initial release with core features"
```

### 4. Verify

```bash
clawhub list
clawhub search "your-skill"
```

## Memory Items to Track

For skills that maintain state:

```markdown
### Skill: your-skill

- **Last Run:** 2026-03-22 13:07
- **Total Runs:** 42
- **Items Processed:** 1,234
- **Errors:** 3 (see error.log)
- **Configuration:**
  - `target_dir`: ./workspace
  - `verbose`: false
  - `auto_backup`: true
```

---

## Quick Reference

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Sequential | Linear workflows | Read → Process → Write |
| Conditional | Branching logic | If file exists, then edit |
| Error Recovery | Unreliable operations | Network calls, external APIs |
| Batch Processing | Multiple items | Process all files in directory |
| State Management | Persistence needed | Track progress across runs |

---

**Remember:** The goal is to make skills that are **reliable**, **clear**, and **easy to maintain**. When in doubt, favor simplicity over cleverness.
