# Output Patterns & Templates

## High-Quality Output Characteristics

1. **Clear structure**: Use headings, bullet points, tables
2. **Actionable**: Tell the user exactly what to do next
3. **Contextual**: Explain why, not just what
4. **Error handling**: Anticipate failure modes

## Template: Error Message

```
❌ [Action] failed: [specific error]

**Why**: [brief explanation]

**Try**:
1. [First fix]
2. [Second fix]
```

## Template: Success Message

```
✅ [Action] completed

**Result**: [what was created/changed]
**Next steps**:
- [optional follow-up]
- [optional verification]
```

## Template: Ask for Input

```
I need some information to proceed:

**Required**:
- [Field 1]: [description]
- [Field 2]: [description]

Please provide these details.
```

## Template: Progress Update

```
📋 [Task Name]

**Status**: [in progress / completed / blocked]

- [x] Step 1
- [ ] Step 2 (current)
- [ ] Step 3
```

## Code Output Patterns

### Shell Commands

Always explain what a command does:

```bash
# Create a new directory for the skill
mkdir -p skills/my-new-skill
```

### File Creation

```bash
# Create SKILL.md with template
cat > skills/my-new-skill/SKILL.md << 'EOF'
---
name: my-new-skill
description: [description]
---

# My New Skill

[TODO: add content]
EOF
```

## Markdown Patterns

### Tables

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Skill name |
| description | string | Yes | Trigger description |

### Code Blocks

Use language identifier:

```python
def process_file(input_path):
    """Process the input file."""
    pass
```

### Callouts

> ℹ️ **Note**: This is additional context.

> ⚠️ **Warning**: This is a common pitfall.

> ✅ **Tip**: This improves effectiveness.

## Common Quality Issues

### Verbose explanations

**Bad**: "As you can see, there are many benefits..."

**Good**: "Benefits: faster, simpler, more reliable"

### Missing examples

**Bad**: "Use the API correctly"

**Good**: "Call GET /api/users to fetch user list"

### No error handling

**Bad**: "Run the script"

**Good**: "Run python script.py. If you get 'Permission denied', run chmod +x script.py first."
