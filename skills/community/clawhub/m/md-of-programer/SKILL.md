---
name: md-of-programer
version: 0.1.0
description: Insert mind maps and architecture diagrams into Markdown documents. Triggered when the user says "draw a mind map", "draw an architecture diagram", "insert a diagram", "mind map", or "diagram".
argument-hint: [diagram description, optional]
allowed-tools: Write, Bash, Read
metadata:
  openclaw:
    requires:
      bins:
        - mddoc
        - d2
---

When inserting diagrams into a Markdown document, always follow the rules below.

## Dependency Check

**Before doing anything, check that dependencies are installed:**

```bash
which mddoc && which d2
```

If `mddoc` is not installed:

```bash
npm install -g mddoc-cli
```

If `d2` is not installed:

- macOS: `brew install d2`
- Windows: `winget install terrastruct.d2`
- Linux / others: see https://d2lang.com/tour/install

Make sure both are available before continuing.

## Rules

- All diagram source files and PNGs go **only in the `.mddoc/` directory** (alongside the Markdown file)
- File names must use **lowercase English + hyphens** (`auth-flow`, `module-overview`) — no spaces or numbers
- **Always write the source file first, then generate the PNG, then embed into Markdown** — in that order
- **Never** write D2 or markmap code blocks directly in the Markdown body
- Create `.mddoc/` if it does not exist

## Mind Map (.mmd)

**1. Write the source file** → `.mddoc/<name>.mmd` in markmap markdown format:

```markdown
# Root node

## Branch one
- Leaf node
- Leaf node

## Branch two
- Leaf node
  - Child leaf
```

**2. Generate PNG:**

```bash
mddoc mindmap .mddoc/<name>.mmd
```

**3. Embed in Markdown:**

```markdown
![Mind map: <description>](.mddoc/<name>.png)
*Source: [<name>.mmd](.mddoc/<name>.mmd)*
```

## Architecture Diagram (.d2)

**1. Write the source file** → `.mddoc/<name>.d2` in D2 language:

```d2
direction: right

client: Client {shape: rectangle}
gateway: API Gateway {shape: rectangle}
db: Database {shape: cylinder}

client -> gateway -> db
```

**2. Generate PNG:**

```bash
mddoc arch .mddoc/<name>.d2
```

**3. Embed in Markdown:**

```markdown
![Architecture: <description>](.mddoc/<name>.png)
*Source: [<name>.d2](.mddoc/<name>.d2)*
```

## Regenerate All Diagrams

```bash
mddoc build
```

## Feedback

Issues and suggestions → https://github.com/drunkpig/md-of-programer/issues
