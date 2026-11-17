# Anatomy of a Hook

**Purpose:** Field-by-field breakdown of AI-GCE hook files — what each field means, how events map to actions, and how to diagnose or create hooks manually.

**Derived from:** Pattern: Conditional Generation + Pattern: Progressive Activation

---

## What a Hook Is

A hook is a JSON file in `.kiro/hooks/` that automates governance enforcement. It maps an IDE event (file edit, tool use, prompt submit) to an action (ask the AI to check something, or run a command).

```json
{
  "name": "API Contract Compliance",
  "version": "1.0.0",
  "description": "Ensures new endpoints have corresponding OpenAPI spec entries",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.controller.ts", "src/**/*.route.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Verify this endpoint change has a corresponding OpenAPI spec entry."
  }
}
```

---

## Field-by-Field Reference

### Top-Level Fields

| Field | Required | Type | Purpose |
|-------|:--------:|------|---------|
| `name` | ✅ | string | Human-readable hook name (displayed in UI) |
| `version` | ✅ | string | Semantic version of the hook |
| `description` | ⚪ | string | What this hook does (documentation) |

### `when` Block — The Trigger

| Field | Required | Type | Purpose |
|-------|:--------:|------|---------|
| `when.type` | ✅ | enum | Which IDE event fires this hook |
| `when.patterns` | Conditional | string[] | File glob patterns (required for file events) |
| `when.toolTypes` | Conditional | string[] | Tool categories or regex (required for tool events) |

#### Event Types (`when.type`)

| Event | Fires When | Requires |
|-------|-----------|----------|
| `fileEdited` | User saves a code file | `patterns` (which files) |
| `fileCreated` | User creates a new file | `patterns` (which files) |
| `fileDeleted` | User deletes a file | `patterns` (which files) |
| `promptSubmit` | Message sent to AI agent | Nothing (fires on every prompt) |
| `agentStop` | AI agent execution completes | Nothing |
| `preToolUse` | Before a tool is about to execute | `toolTypes` (which tools) |
| `postToolUse` | After a tool has executed | `toolTypes` (which tools) |
| `userTriggered` | User manually clicks the hook button | Nothing |
| `preTaskExecution` | Before a spec task starts | Nothing |
| `postTaskExecution` | After a spec task completes | Nothing |

#### File Patterns (`when.patterns`)

Standard glob syntax:
- `*.ts` — TypeScript files in root only
- `**/*.ts` — TypeScript files recursively
- `src/**/*.controller.ts` — Controller files under src/
- `!**/*.test.ts` — Exclude test files (negation)

#### Tool Types (`when.toolTypes`)

Built-in categories:
- `read` — file reading tools
- `write` — file writing/editing tools
- `shell` — terminal command execution
- `web` — web search/fetch tools
- `spec` — specification tools
- `*` — all tools

Regex patterns for MCP tools:
- `.*sql.*` — any tool with "sql" in name
- `.*deploy.*` — any deployment-related tool

### `then` Block — The Action

| Field | Required | Type | Purpose |
|-------|:--------:|------|---------|
| `then.type` | ✅ | enum | `askAgent` or `runCommand` |
| `then.prompt` | If askAgent | string | Instruction sent to the AI when hook fires |
| `then.command` | If runCommand | string | Shell command to execute |

#### Action: `askAgent`

Sends a prompt to the AI assistant. The AI processes it and may:
- Remind itself of a rule
- Check the current change against a governance standard
- Provide guidance to the developer

```json
"then": {
  "type": "askAgent",
  "prompt": "Check if this file follows the naming convention in naming-conventions.md. If it violates, explain the correct pattern."
}
```

#### Action: `runCommand`

Executes a shell command. Useful for automated checks:

```json
"then": {
  "type": "runCommand",
  "command": "npm run lint -- --quiet"
}
```

---

## Complete Examples by Category

### Naming Enforcement (Tier 1)

```json
{
  "name": "Naming Convention Check",
  "version": "1.0.0",
  "description": "Validates new files follow project naming conventions",
  "when": {
    "type": "fileCreated",
    "patterns": ["src/**/*"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check if this new file's name follows the naming conventions defined in .kiro/steering/naming-conventions.md. Files must use kebab-case. Classes must use PascalCase. If non-compliant, suggest the correct name."
  }
}
```

### Session Governance (Tier 1)

```json
{
  "name": "Spec-First Reminder",
  "version": "1.0.0",
  "description": "Reminds to reference specification before implementing",
  "when": {
    "type": "promptSubmit"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Before implementing, verify: Is there a specification or design document for this work? If implementing without a spec, remind the developer to create one first (even a brief comment-level spec is better than none)."
  }
}
```

### Security Gate (Tier 1)

```json
{
  "name": "Secrets Detection",
  "version": "1.0.0",
  "description": "Checks for hardcoded secrets before writing files",
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Before writing this file, scan the content for potential secrets: API keys, passwords, tokens, connection strings. If any are found, block the write and suggest using environment variables instead."
  }
}
```

### Module Boundary (Tier 2)

```json
{
  "name": "Module Boundary Check",
  "version": "1.0.0",
  "description": "Enforces module import restrictions",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check imports in this file against module boundaries defined in .kiro/steering/module-structure.md. Flag any cross-boundary imports that violate the dependency direction rules."
  }
}
```

### Test Coverage (Tier 2)

```json
{
  "name": "Test Companion Check",
  "version": "1.0.0",
  "description": "Ensures new source files have corresponding tests",
  "when": {
    "type": "fileCreated",
    "patterns": ["src/**/*.ts", "!src/**/*.test.ts", "!src/**/*.spec.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A new source file was created. Remind the developer: this file needs a corresponding test file. Check if a test already exists at the expected location. If not, suggest creating one."
  }
}
```

---

## Hook Metadata (AI-GCE Provenance)

Generated hooks include extra fields for provenance:

```json
{
  "name": "...",
  "version": "1.0.0",
  "generatedBy": "AI-GCE",
  "generatedVersion": "1.0.0",
  "source": ".kiro/steering/api-standards.md",
  "tier": 2,
  "category": "API",
  "when": { ... },
  "then": { ... }
}
```

| Metadata Field | Purpose |
|---------------|---------|
| `generatedBy` | Which package created this hook |
| `generatedVersion` | Version of the generating package |
| `source` | Which steering file this hook derives from |
| `tier` | Which governance tier this hook belongs to |
| `category` | Rule category (ARCH, SEC, API, NAME, TEST, GOV, SESSION) |

---

## Diagnosing Hook Problems

| Problem | Check |
|---------|-------|
| Hook doesn't fire | Verify `when.type` matches the event; verify `patterns` match the file path |
| Hook fires too often | Tighten `patterns` (more specific globs) |
| Hook fires on wrong files | Check glob patterns — `*.ts` ≠ `**/*.ts` |
| askAgent prompt is unhelpful | Rewrite prompt with clearer rule + context + verification steps |
| runCommand fails | Test command manually in terminal first |
| Hook seems outdated | Check `source` field — is that steering file still current? |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Hook Generation Works | `knowledge_docs/HOW_HOOK_GENERATION_WORKS.md` |
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| Pattern: Conditional Generation | `knowledge_docs/PATTERN_CONDITIONAL_GENERATION.md` |
| Pattern: Progressive Activation | `knowledge_docs/PATTERN_PROGRESSIVE_ACTIVATION.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
