---
name: linear-cli
description: Use the linear-cli agent-native runtime to read and mutate Linear from Claude Code, Codex, or other agents. Use when the runtime needs default JSON output, startup discovery, dry-run previews, operation receipts, workflow-safe automation, or direct CLI control over Linear issues, projects, cycles, documents, notifications, webhooks, or related resources.
allowed-tools: Bash(linear:*), Bash(curl:*)
---

# Linear CLI

An agent-native Linear runtime for the current `v3` execution model, with stable JSON contracts, startup discovery, dry-run previews, timeout-aware write semantics, source-adjacent intake, and git/jj workflow integration.

## Recommended Agent Loop

When using this CLI from an agent runtime, prefer this order:

1. Discover command traits with `linear capabilities`; use `--compat v1` only when an older consumer still expects the trimmed legacy shape
2. Read Linear state with default-JSON core surfaces or `--json`
3. Preview writes with `--dry-run --json` when available
4. Apply writes on the default machine-readable surface, then inspect `operation`, `receipt`, and `error.details`
5. Inspect exit codes and `error.details` instead of parsing styled terminal text

Prompt-driven human/debug flows are secondary and explicit. When a command supports prompts or editor entry, pass `--profile human-debug --interactive`; otherwise missing required inputs fail fast.

Agent-safe execution semantics are now the default runtime behavior. `--text` and `--profile human-debug` are the explicit human/debug escape hatches for maintainers, and `--profile agent-safe` remains accepted for compatibility with older automation.

When upstream tooling hands the runtime a normalized Slack, ticket, or similar source envelope, prefer `--context-file`, add `--apply-triage` if that envelope already contains deterministic team/state/label hints, and choose `--autonomy-policy` explicitly when the wrapper needs suggest-only or preview-required staging.

Recommended supporting docs:

- [../../docs/agent-first.md](../../docs/agent-first.md)
- [../../docs/v2-to-v3-migration-cookbook.md](../../docs/v2-to-v3-migration-cookbook.md)
- [../../docs/json-contracts.md](../../docs/json-contracts.md)
- [../../docs/stdin-policy.md](../../docs/stdin-policy.md)

## Prerequisites

The `linear` command must be available on PATH. To check:

```bash
linear --version
```

If not installed, follow the instructions at:\
https://github.com/kyaukyuai/linear-cli?tab=readme-ov-file#install

## Best Practices for Markdown Content

When working with issue descriptions or comment bodies that contain markdown, prefer file-based flags for existing files and stdin for generated pipeline content:

- Use `--description-file` for `issue create` and `issue update` commands when the content already exists on disk
- Use `--body-file` for `comment add` and `comment update` commands when the content already exists on disk
- Pipe stdin for generated markdown, for example `cat description.md | linear issue create --title "My Issue" --team ENG`

**Why avoid large inline flags:**

- Ensures proper formatting in the Linear web UI
- Avoids shell escaping issues with newlines and special characters
- Prevents literal `\n` sequences from appearing in markdown
- Makes it easier to work with multi-line content in scripts and pipelines

**Example workflow:**

```bash
# Write markdown to a temporary file
cat > /tmp/description.md <<'EOF'
## Summary

- First item
- Second item

## Details

This is a detailed description with proper formatting.
EOF

# Create issue using the file
linear issue create --title "My Issue" --description-file /tmp/description.md

# Or pipe generated markdown directly
cat /tmp/description.md | linear issue create --title "My Issue" --team ENG

# Or for comments
linear issue comment add ENG-123 --body-file /tmp/comment.md
```

**Only use inline flags** (`--description`, `--body`) for simple, single-line content.

## Available Commands

{{COMMANDS}}

## Reference Documentation

{{REFERENCE_TOC}}

For curated examples of organization features (initiatives, labels, projects, bulk operations), see [organization-features](references/organization-features.md).

## Discovering Options

To see available subcommands and flags, run `--help` on any command:

```bash
linear --help
linear issue --help
linear issue list --help
linear issue create --help
```

Each command has detailed help output describing all available flags and options.

For machine-readable discovery, prefer:

```bash
linear capabilities
linear capabilities --compat v1
```

## Using the Linear GraphQL API Directly

**Prefer the CLI for all supported operations.** The `api` command should only be used as a fallback for queries not covered by the CLI.

### Check the schema for available types and fields

Write the schema to a tempfile, then search it:

```bash
linear schema -o "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -i "cycle" "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -A 30 "^type Issue " "${TMPDIR:-/tmp}/linear-schema.graphql"
```

### Make a GraphQL request

**Important:** GraphQL queries containing non-null type markers (e.g. `String` followed by an exclamation mark) must be passed via heredoc stdin to avoid escaping issues. Simple queries without those markers can be passed inline.

```bash
# Simple query (no type markers, so inline is fine)
linear api '{ viewer { id name email } }'

# Query with variables — use heredoc to avoid escaping issues
linear api --variable teamId=abc123 <<'GRAPHQL'
query($teamId: String!) { team(id: $teamId) { name } }
GRAPHQL

# Search issues by text
linear api --variable term=onboarding <<'GRAPHQL'
query($term: String!) { searchIssues(term: $term, first: 20) { nodes { identifier title state { name } } } }
GRAPHQL

# Numeric and boolean variables
linear api --variable first=5 <<'GRAPHQL'
query($first: Int!) { issues(first: $first) { nodes { title } } }
GRAPHQL

# Complex variables via JSON
linear api --variables-json '{"filter": {"state": {"name": {"eq": "In Progress"}}}}' <<'GRAPHQL'
query($filter: IssueFilter!) { issues(filter: $filter) { nodes { title } } }
GRAPHQL

# Pipe to jq for filtering
linear api '{ issues(first: 5) { nodes { identifier title } } }' | jq '.data.issues.nodes[].title'
```

### Advanced: Using curl directly

For cases where you need full HTTP control, use `linear auth token`:

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $(linear auth token)" \
  -d '{"query": "{ viewer { id } }"}'
```
