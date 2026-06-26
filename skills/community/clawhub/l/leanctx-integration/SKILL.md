---
name: leanctx-integration
description: Automatically compresses OpenClaw tool outputs to reduce token usage by 60-99%
homepage: https://github.com/jackkeller/leanctx-integration
metadata:
  clawdbot:
    emoji: "📦"
    requires:
      env: []
    files: ["dist/*", "install.sh", "package.json"]
---

# LeanContext Integration

LeanContext integration for OpenClaw that automatically compresses tool outputs to reduce token usage by 60-99%.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | N/A | This skill operates entirely locally |

No external API calls are made. All processing happens on your local machine.

## Security & Privacy

- **Local-only operation**: All compression and caching happens locally
- **No data leaves your machine**: No files, commands, or content is sent to external services
- **Cache location**: Stored in memory (optional filesystem cache can be configured)
- **No telemetry**: No usage data, metrics, or analytics are transmitted

## Model Invocation

This skill operates autonomously during OpenClaw's normal operation. It intercepts `read` and `exec` tool calls transparently without requiring explicit user approval for each invocation. This is standard behavior for OpenClaw skills.

To disable automatic invocation, set `enabled: false` in your OpenClaw config.

## Trust Statement

By using this skill, your file contents and command outputs are processed locally for compression purposes. No data is sent to external services. Only install if you are comfortable with this local processing.

## What it does

Intercepts OpenClaw's `read` and `exec` tool calls and applies intelligent compression:

- **File reads**: AST-aware compression removes comments, whitespace, collapses function bodies
- **Shell exec**: Pattern-matching compresses common commands (git, npm, docker, etc.)
- **Session caching**: Re-reads cost ~13 tokens instead of thousands

## Installation

```bash
openclaw skills install leanctx-integration
```

Or manually:
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/your-repo/leanctx-integration.git
cd leanctx-integration
npm install
npm run build
```

## Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "leanctx-integration": {
      "enabled": true,
      "config": {
        "threshold": 100,
        "cacheEnabled": true,
        "excludedPaths": ["node_modules", ".git", "dist"],
        "excludedCommands": ["cat", "echo"]
      }
    }
  }
}
```

## Usage

Once installed, LeanContext works **automatically** - no code changes required!

### Check Metrics

**Note:** Metrics tracking has been temporarily disabled. The skill automatically compresses tool outputs, but session-level metrics reporting is not currently available. This feature may be revisited in a future update.

### Clear Cache

**Via your agent:**
Ask: "Clear the LeanCTX cache"

**Direct CLI:**
```bash
npx leanctx clear-cache
```

## Compression Examples

### TypeScript File (800 lines)

**Before**: ~2000 tokens  
**After**: ~50 tokens  
**Savings**: 97.5%

### Git Log

**Before**: ~500 tokens (full commit info)  
**After**: ~30 tokens (hashes + messages)  
**Savings**: 94%

### NPM Install

**Before**: ~200 tokens (all download messages)  
**After**: ~10 tokens (summary only)  
**Savings**: 95%

## Supported Languages

- TypeScript / JavaScript
- Python
- Svelte
- Go
- Rust
- Java / Kotlin
- Generic (fallback)

## Supported Commands

- `git log` → Commit hashes + first line
- `git status` → Changed files only
- `git diff` → Diff markers + changes
- `npm install` → Package count
- `npm test` → Test results + summary
- `cargo build` → Errors only
- `docker ps` → Header + first 10 rows
- `kubectl` → Header + first 15 rows

## Performance

- **Cache hit**: <5ms overhead
- **First read**: ~10ms (AST parse)
- **Compression**: 60-99% token reduction

## Troubleshooting

### Not working?

1. Check if skill is enabled in config
2. Verify threshold isn't too high
3. Check excluded paths aren't matching

### Want to disable for specific files?

Add to `excludedPaths` in config:

```json
{
  "excludedPaths": ["node_modules", ".git", "**/*.spec.ts"]
}
```

### Cache too large?

Ask your agent: "Clear the LeanCTX cache"

Or via CLI:
```bash
npx leanctx clear-cache
```

## How it works

1. OpenClaw makes a tool call (read or exec)
2. LeanContext intercepts the call
3. Checks cache (instant return if hit)
4. Compresses based on file type or command pattern
5. Caches result
6. Returns compressed output to OpenClaw
7. Metrics updated

## License

MIT
