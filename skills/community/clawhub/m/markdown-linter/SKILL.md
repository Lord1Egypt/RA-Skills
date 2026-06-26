---
name: markdown-linter
description: Validates Markdown files in the workspace for broken local links, missing file references, and basic syntax issues. Use to maintain documentation integrity and prevent broken references in MEMORY.md or SKILL.md files.
---

# Markdown Linter

A lightweight tool to validate Markdown files in the workspace. It focuses on ensuring internal consistency, particularly broken file links and missing references.

## Capabilities

- **Link Validation**: Checks `[link](path)` references to ensure the target file exists locally.
- **Header Check**: Verifies that headers follow a logical hierarchy (e.g., H1 -> H2).
- **Code Block Check**: Ensures code blocks have language identifiers where appropriate.

## Usage

```javascript
const linter = require('./index');
const results = await linter.scan('.'); // Scans current directory recursively
console.log(JSON.stringify(results, null, 2));
```

## Output Format

```json
{
  "totalFiles": 15,
  "brokenLinks": [
    {
      "file": "docs/README.md",
      "line": 10,
      "link": "./missing-image.png",
      "error": "File not found"
    }
  ],
  "syntaxErrors": []
}
```
