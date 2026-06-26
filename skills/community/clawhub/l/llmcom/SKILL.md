---
name: llmcom
description: Compress prompts for Claude Code and Cursor CLI. Reduces tokens by removing filler words and abbreviating terms. Self-contained, no external dependencies required.
---

# LLMCOM Prompt Compression

Self-contained prompt compression tool. No installation required - just read this skill and apply the compression rules.

## Compression Rules

1. **Remove filler words**: the, a, an, is, are, with, of, to, in, on, at, and, for, that, this
2. **Abbreviate terms**:
   - refactor -> refac
   - review -> rev
   - function -> func
   - security -> sec
   - performance -> perf
   - module -> mod
   - component -> comp
   - authentication -> auth
   - implementation -> impl

3. **Output format for Claude Code**: agent[task]|scope|focus|action|context|constraints

## Example

**Input**: "Refactor the authentication module to improve type security"

**Output**: agent[refac]|mod|sec|review|@src|strict

**Stats**: 11 -> 6 tokens (45% reduction)

## How to Use

Apply these rules manually when writing prompts for Claude Code CLI or Cursor agent.

1. Identify task type: refactor, review, fix, test, audit
2. Remove filler words
3. Abbreviate key terms
4. Format as pipe-separated values

## Quick Reference

| Task | Format |
|------|--------|
| Refactor | agent[refac]|scope|focus|review|@path|constraints |
| Security audit | agent[audit]|scope|sec|report|@path|high |
| Bug fix | agent[fix]|scope|error|debug|@path|fallback |
| Test coverage | agent[test]|scope|cov|jest|@path|edge-cases |

## Integration

Use before sending prompts to:
- Claude Code CLI (gent command)
- Cursor agent
- Any LLM API to reduce token costs
