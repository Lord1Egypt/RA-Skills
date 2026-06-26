---
name: exec-truncate
description: AI agent tool for compressing/executing shell commands with domain-aware output truncation. Use when exec tool output needs to be compressed, when running git diff/log/grep commands, or when exec output exceeds reasonable length.
location: ~/.openclaw/workspace/skills/exec-truncate
---

# Exec-Truncate Skill

Domain-aware output truncation for shell command execution. Compresses verbose output while preserving critical information.

## What It Does

This skill provides intelligent truncation for common command patterns:

- **git diff** — Keeps first 100 + last 20 lines, shows only additions (`+`)
- **git log** — Condensed one-liners with short hashes (7 chars), subjects, branches
- **grep/rg/find** — Caps at 50 matches, strips path prefixes
- **ls -la/ls -l** — Max 100 entries, keeps filename + abbreviated size
- **build tools** — Strips ANSI codes, progress bars; keeps errors/warnings only

## Integration Note

**This is a standalone skill**, not wired into OpenClaw's exec tool. OpenClaw distributions are compiled/bundled, so this runs as a utility the AI applies manually to output it already has.

## Available Functions

### Individual Truncation Functions

```typescript
import {
  truncateGitDiff,
  truncateGitLog,
  truncateGrepOutput,
  truncateLsOutput,
  truncateBuildOutput,
  truncateExecOutput,
} from "./mod.ts";

// Direct usage
const truncated = truncateGitDiff(rawOutput);
const condensed = truncateGitLog(rawOutput);
const matches = truncateGrepOutput(rawOutput, 50); // custom max
const listing = truncateLsOutput(rawOutput);
const build = truncateBuildOutput(rawOutput);

// Auto-dispatcher (routes based on command string)
const result = truncateExecOutput("git diff HEAD~5", rawOutput);
```

### FilteredExecutor (Recommended for Programmatic Use)

```typescript
import { createFilteredExecutor } from "./index.ts";

// Wrap your exec function
const executor = createFilteredExecutor(
  async (cmd: string) => {
    const { stdout } = await Deno.Command.output(cmd, { shell: true });
    return new TextDecoder().decode(stdout);
  }
);

// Execute with automatic truncation
const diff = await executor.run("git diff HEAD~5");
const log = await executor.run("git log --oneline -20");
const grep = await executor.run("grep -r 'TODO' src/");
```

### Config Options (Phase 3)

```typescript
const executor = createFilteredExecutor(myExecFn, {
  outputTransform: false,       // Bypass all filtering, return raw
  oversizedOutputLog: 10000,  // Log when raw output > 10KB
});
```

## Usage Examples

### Manual Truncation Pattern

When you already have exec output and want to compress it:

```typescript
// 1. Run command normally
const raw = await exec("git diff HEAD~10");

// 2. Apply truncation
const compressed = truncateGitDiff(raw);

// 3. Use the compressed result
console.log(compressed);
```

### Batch Processing

```typescript
import { truncateExecOutput } from "./mod.ts";

const commands = [
  "git diff HEAD~5",
  "git log --oneline -20",
  "grep -r 'TODO' src/"
];

for (const cmd of commands) {
  const raw = await exec(cmd);
  const compressed = truncateExecOutput(cmd, raw);
  console.log(`=== ${cmd} ===\n${compressed}\n`);
}
```

### Custom Filtering

```typescript
import { FilterRegistry, FilteredExecutor } from "./index.ts";

const customRegistry = new FilterRegistry();
customRegistry.register(/^npm run /i, (_cmd, output) => {
  // Custom logic for npm scripts
  return output.split("\n").slice(0, 30).join("\n");
});

const executor = new FilteredExecutor(myExecFn, customRegistry);
```

## Fail-Safe Behavior

All truncation functions are wrapped in `truncateWithFailSafe`. If ANY error occurs during processing (TypeError, RangeError, regex crash), the original output is returned unchanged with an error logged to stderr.

## Module Overview

| Module | Purpose |
|--------|---------|
| `mod.ts` | Core truncation functions (git diff/log, grep, ls, build) |
| `filter-registry.ts` | Command pattern matching + filter composition |
| `filtered-executor.ts` | Wraps exec functions with configurable filtering |
| `index.ts` | Public API re-exports + `createFilteredExecutor` factory |

## See Also

- `README.md` — Practical examples and copy-pasteable snippets
- `scripts/exec-truncate-wrapper.sh` — Shell wrapper for CLI use
- `scripts/simple-truncater.py` — Pure Python reimplementation
