---
name: asset-graph-management
description: Build, maintain, validate, and publish an evidence-backed asset graph or OKF-style resource map for operations, ops, DevOps, SRE, platform engineering, infrastructure inventory, CMDB-like service catalogs, dependency mapping, incident handoff, and 运维 discovery. Use when mapping operational assets such as repositories, compute, services, databases, queues, websites, pipelines, storage, networks, identity systems, MCP servers, Jenkins/CI jobs, APIs, external services, or business systems; when a user provides an entrypoint or config such as SSH, URL/API, MCP, Jenkins, Git, database, object storage, cloud, Kubernetes, monitoring, or SaaS access and expects discovery; when turning scattered operational knowledge into agent-readable Markdown plus structured frontmatter; or when preparing open-source/demo-safe asset-management methodology without exposing private infrastructure.
---

# Asset Graph Management

Use this skill to turn scattered infrastructure and operational knowledge into a reusable asset graph. The graph should be safe to share, easy for agents to update, and grounded in evidence rather than guesses.

## Core Workflow

1. Treat any user-provided operational entrypoint or configuration as a discovery seed, not only SSH.
2. Classify the seed and the asset being discussed, then choose the closest generic type.
3. Create or update one record under `resources/<type>/<asset-id>/index.md`.
4. Put durable structured facts in frontmatter and reviewable operating notes in Markdown.
5. Represent relationships with stable asset IDs, not display names, URLs, or ports.
6. Separate confirmed facts, clues, gaps, and operations; do not promote guesses into the graph.
7. Store reusable read-only commands in the asset's local `scripts/` directory when needed.
8. Keep sensitive or organization-specific values out of public records, examples, logs, and scripts.
9. Rebuild the catalog and run validators before publishing or handing off the package.

## What To Read

- For the asset model and record format, read `references/asset-model.md`.
- For DevOps discovery steps, read `references/devops-discovery.md`.
- For safety, evidence, and secret-handling rules, read `references/evidence-and-safety.md`.
- For script entrypoint rules, read `references/script-requirements.md`.
- Before publishing or sharing the package, read `references/publishing-checklist.md`.
- To see a complete sanitized example, inspect `demo/resources/` and open `ui/index.html`.

## Required Record Shape

Every asset record is a Markdown file with YAML frontmatter. Keep the shape small and stable:

```markdown
---
asset:
  id: acme-checkout-api
  type: repository
  name: Acme Checkout API
  environment: shared
  status: active
  owners:
    - platform-team
  last_verified:
    at: 2026-01-01
    by: demo-agent
    evidence:
      - "Generated fictional public demo record."
  relationships:
    runs_on:
      - acme-prod-api-01
  evidence:
    - "Demo source: public example generated for this skill."
---

# Acme Checkout API

Short summary, operating notes, and links to scripts or references.
```

Use `unknown` for unknown facts. Do not invent owners, dependency edges, endpoints, regions, or status values.

## Operating Boundary

Read-only discovery, file inspection, validation, and catalog building are allowed by default and should proceed proactively after the user provides an asset, entrypoint, or access configuration. Entrypoints include SSH targets, URLs, API base URLs, MCP server configs, Jenkins or other CI job URLs, Git remotes, database connection details, object storage endpoints, cloud consoles, SaaS admin URLs, and monitoring dashboards. Restarting services, triggering builds, calling mutating API or MCP tools, deploying code, mutating data, changing DNS/firewalls/IAM, rotating credentials, sensitive reads, or touching live production state requires explicit user authorization and an operation log.

For open-source packages, publish only fictional demo assets, reserved example domains, placeholder repository URLs, and sanitized scripts. If a private organization uses this methodology internally or during evaluation, put real-target artifacts outside the public skill repository, label catalogs as private/eval output, and keep real endpoints and credentials out of the public package.

## Demo And Tools

This skill includes a self-contained demo graph with no private assets:

```bash
python scripts/validate_demo.py demo
python scripts/build_catalog.py demo demo/catalog/catalog.json --generated-from "fictional public demo records"
python scripts/check_public_safety.py .
python scripts/validate_skill_package.py .
```

Open `ui/index.html` in a browser to inspect the demo graph. The UI reads the bundled demo JSON by default, accepts `?catalog=<catalog-json-url>`, and can import a local catalog JSON file.

## Publication Boundary

This package is designed for open publication. Put methodology in `references/`, deterministic checks in `scripts/`, fictional examples in `demo/`, and browser presentation in `ui/`. Do not include real hosts, IP addresses, repository URLs, customer names, internal system names, cloud account IDs, local machine paths, tokens, or credentials.
