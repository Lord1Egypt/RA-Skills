# File Format Reference

Parsing rules for common Obsidian vault file types.

## open-questions.md

Parsed as tasks. Expected format:

```markdown
## 🔴 Critical
- [ ] **Task title here** — additional description
- [ ] Another critical task

## 🟡 Important
- [ ] Important task — Owner: Dave
- [x] Completed task

## 🟢 Nice to Know
- [ ] Lower priority item
```

**Parsing rules:**
- `- [ ]` → status: todo
- `- [x]` → status: done
- Section header containing 🔴 → priority: critical
- Section header containing 🟡 → priority: important
- Section header containing 🟢 → priority: nice
- Text after `**bold**` → title
- Text after `—` → description
- Pattern `Owner: <name>` → owner field

## team.md

Parsed as team roster. Expected format:

```markdown
### Dave Manock — CEO / CPO
- Domain expert in S1000D
- Responsible for: product, customers

### Alex 🔧 — CTO
- AI/ML engineer
- Telegram: @alexcto_manock_bot
```

**Parsing rules:**
- `### Name — Role` → name + role fields
- `Telegram: @botname` → telegram_bot field
- Bullet points → responsibilities list

## milestones section (in various files)

```markdown
| Milestone | Status | Target |
|---|---|---|
| Business plan drafted | done | Mar 11 |
| Customer discovery | active | Mar 18 |
| First pilot customer | pending | Month 5-6 |
```

**Parsing rules:**
- Table rows with status column
- Status values: done, active, pending

## s1000d-business-plan.md

Large narrative document — return as raw markdown. Extractable fields:
- Sections from `##` headers
- Last updated from frontmatter
- Status from frontmatter

## Generic markdown files

For files without a specific parser:
- Extract frontmatter metadata
- Return content as markdown
- Extract all `##` headers as section list
