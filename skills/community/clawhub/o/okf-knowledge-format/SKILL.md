---
name: "okf-knowledge-format"
description: "Create, read, validate, and manage OKF (Open Knowledge Format) knowledge bundles for AI agents. Google's vendor-neutral markdown+YAML spec."
---

# OKF (Open Knowledge Format) — Skill for AI Agents

This skill teaches AI agents how to read, traverse, create, and maintain knowledge bases stored in Google's Open Knowledge Format (OKF) using the `okf-toolkit` CLI.

## What is OKF?

The Open Knowledge Format (OKF) is an open, vendor-neutral specification for representing knowledge as a directory tree of markdown files with YAML frontmatter. Announced by Google Cloud on June 12, 2026, it is designed to be both human-readable and AI-agent-friendly.

Key concepts:
- **Bundle:** A directory tree of markdown files
- **Concept:** A single `.md` file = one unit of knowledge. Has YAML frontmatter between `---` delimiters
- **index.md:** Directory listing (no frontmatter)
- **log.md:** Update history (no frontmatter)
- **Linking:** Standard markdown links between concepts

### Frontmatter Fields

Required:
- `type` (string) — e.g., "BigQuery Table", "API Endpoint", "Metric", "Playbook", "Reference"

Recommended:
- `title` (string)
- `description` (string)
- `resource` (URI string)
- `tags` (YAML list)
- `timestamp` (ISO 8601 string)

## How Agents Should Use OKF

### 1. Reading and Traversing a Bundle

Start by reading the bundle's `index.md`. This file lists all top-level sections with links. Follow those links to discover individual concepts.

### 2. Understanding a Concept

The `type` field tells you what kind of knowledge this is:
- `BigQuery Table` → Contains schema definitions, partitioning info, usage notes
- `Metric` → Contains a business metric definition, SQL query, business rules
- `Playbook` → Contains operational procedures, severity levels, step-by-step instructions
- `API Endpoint` → Contains request/response formats, authentication, examples

### 3. Creating New Concepts

Use the `okf-toolkit` CLI:
```bash
okf new <bundle-path> <concept-id>
```

Or create manually with proper frontmatter (YAML between `---` delimiters + markdown body).

### 4. Validating and Maintaining

Always validate after making changes:
```bash
okf validate <bundle-path>
```

### 5. CLI Quick Reference

```bash
okf list <bundle>       # List all concepts
okf show <bundle> <id>  # Display a concept
okf search <bundle> <q> # Full-text search
okf index <bundle>      # Auto-generate index.md
okf graph <bundle>      # Visualize link graph
okf stats <bundle>      # Statistics + tag cloud
okf init <path>         # Create new bundle
```

## Best Practices

1. One concept per file
2. Use descriptive type values ("BigQuery Table" > "Table")
3. Link freely to build traversable knowledge graphs
4. Use tags for discoverability ("core", "pii", "deprecated")
5. Keep descriptions concise but informative
6. Set timestamps for freshness tracking
7. Never modify index.md or log.md directly — use `okf index`
8. Validate before committing

## Error Tolerance

OKF consumers MUST tolerate unknown frontmatter keys. If you encounter a field you don't recognize, skip it rather than failing.

## Resources

- OKF Spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- okf-toolkit: https://github.com/akdira/okf-toolkit
- Project home: [akdira](https://www.akdira.id)
- Install: `pip install git+https://github.com/akdira/okf-toolkit.git`

---

*Created by [akdira](https://www.akdira.id).*
