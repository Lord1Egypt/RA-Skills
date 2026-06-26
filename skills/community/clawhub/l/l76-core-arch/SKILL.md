---
name: l76-core-arch
description: >
  Demonstration skill showcasing complete AgentSkills core architecture.
  Includes SKILL.md structure, main entry logic, tool integration patterns,
  error handling, and production-ready patterns. Use as a template for
  building new skills.
metadata:
  author: openclaw
  version: "1.0.0"
  emoji: "🏗️"
  openclaw:
    requires:
      bins: ["node"]
    install:
      - id: node
        kind: node
        package: null
        bins: ["node"]
        label: "Node.js runtime (built-in)"
---

# L76 Core Architecture Skill

This skill demonstrates a complete, production-ready AgentSkills architecture.

## When to Use

✅ **USE this skill when:**

- Building a new skill from scratch
- Reviewing or auditing existing skill structure
- Learning AgentSkills best practices
- Needing a template for tool integration

## Architecture Overview

```
l76-core-arch/
├── SKILL.md           # Skill manifest + instructions (YOU ARE HERE)
├── index.js           # Main entry point (optional for simple skills)
├── references/        # Supporting docs, examples, templates
│   └── examples.md
└── scripts/           # Helper scripts (optional)
    └── validate.sh
```

## Core Components

### 1. Frontmatter (Required)

```yaml
---
name: skill-name              # kebab-case, unique identifier
description: |                # Clear trigger conditions
  When to use this skill.
metadata:
  author: your-name
  version: "1.0.0"
  emoji: "🎯"                 # Optional visual identifier
  openclaw:                   # OpenClaw-specific metadata
    requires:
      bins: ["tool1", "tool2"]
    install:                  # Installation instructions
      - id: tool1
        kind: node
        package: package-name
        bins: ["binary-name"]
        label: "Install description"
---
```

### 2. Skill Instructions Structure

```markdown
# Skill Name

Brief description (1-2 sentences).

## When to Use

✅ **USE this skill when:**
- Clear trigger condition 1
- Clear trigger condition 2

❌ **DON'T use this skill when:**
- Anti-pattern 1
- Anti-pattern 2

## Workflow

### Step 1 — Preflight

Check prerequisites before starting.

### Step 2 — Main Logic

Core skill functionality.

### Step 3 — Cleanup

Finalize and report results.

## Error Handling

Common errors and recovery steps.

## Examples

Concrete usage examples.
```

## Tool Integration Patterns

### Pattern 1: Sequential Tool Calls

```javascript
// Read file, then process, then write
const content = await read({ path: "input.txt" });
const processed = transform(content);
await write({ path: "output.txt", content: processed });
```

### Pattern 2: Conditional Execution

```javascript
// Check first, then act
const exists = await exec({ command: "test -f file.txt" });
if (exists.exitCode === 0) {
  await edit({ path: "file.txt", oldText: "...", newText: "..." });
}
```

### Pattern 3: Error Recovery

```javascript
try {
  await riskyOperation();
} catch (error) {
  // Log error
  await write({ path: "error.log", content: error.message });
  // Attempt recovery
  await recoveryStep();
  // Report to user
  return { status: "recovered", error: error.message };
}
```

### Pattern 4: Batch Operations

```javascript
// Process multiple items efficiently
const items = await discoverItems();
const results = await Promise.all(
  items.map(item => processItem(item))
);
```

## Error Handling Strategy

### Error Categories

1. **Recoverable** — Retry with backoff, fallback to alternative
2. **User Action Required** — Prompt user for input/permission
3. **Fatal** — Report clearly, suggest workaround

### Error Response Format

```javascript
{
  status: "error" | "partial" | "success",
  error: "Human-readable error message",
  recovery: "Suggested next step",
  details: { /* Technical details */ }
}
```

## Memory Items

Skills should track state when needed:

```markdown
### Skill State

- Last run: 2026-03-22
- Items processed: 42
- Errors encountered: 3
- Configuration: {...}
```

## Testing Checklist

- [ ] Skill triggers correctly
- [ ] All tool calls succeed
- [ ] Error paths tested
- [ ] Output is clear and actionable
- [ ] No sensitive data leaked
- [ ] Idempotent (safe to re-run)

## Publishing to ClawHub

```bash
# Login first
clawhub login

# Publish
clawhub publish ./l76-core-arch \
  --slug l76-core-arch \
  --name "L76 Core Architecture" \
  --version 1.0.0 \
  --changelog "Initial release"

# Verify
clawhub list
```

## References

- [AgentSkills Spec](https://github.com/OpenClaw/spec)
- [ClawHub Documentation](https://clawhub.com/docs)
- [OpenClaw Skills](D:\OpenClaw\app-data\migrated\npm\node_modules\openclaw\skills)
