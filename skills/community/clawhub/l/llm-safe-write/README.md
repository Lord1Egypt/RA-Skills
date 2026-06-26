# llm-safe-write

A prompt/skill that reliably writes large files or files containing CJK/special characters, using an incremental Edit strategy instead of direct Write. Works with any AI coding environment that has Write and Edit tools (opencode, Cursor, Claude Code, etc.).

## Why this skill exists

The Write tool in AI coding environments serializes file content as JSON for transport. When files are long (>50 lines) or contain CJK characters (Chinese, Japanese, Korean), multi-byte UTF-8 sequences can cross internal buffer boundaries, causing `Unterminated string` errors and silent truncation. This skill works around the limitation by writing a short ASCII skeleton first, then filling in content via the Edit tool in small increments.

## How it works

1. **Skeleton + Edit**: Write an ASCII-only skeleton (<50 lines) with unique placeholder comments, then use the Edit tool to replace each placeholder with real content (<30 lines per Edit).
2. **CJK handling**: Replace all CJK strings with ASCII placeholders in the skeleton, then fill them via Edit — Edit's short `oldString`/`newString` pairs never trigger truncation.
3. **Append support**: Use the last line of a file as an anchor for the Edit tool to simulate appending.

## Installation

### For opencode

Clone this repository into your opencode skills directory:

```bash
git clone https://github.com/ThinkDonk/llm-safe-write.git ~/.config/opencode/skills/llm-safe-write
```

Or add it as a submodule:

```bash
git submodule add https://github.com/ThinkDonk/llm-safe-write.git ~/.config/opencode/skills/llm-safe-write
```

### For other AI coding tools

Copy or symlink `SKILL.md` to wherever your tool loads custom prompts, rules, or skills from. The file is self-contained and requires no additional dependencies.

## When to use

- Writing a file longer than 50 lines
- File contains CJK characters or special escape sequences
- A Write tool call failed with `Unterminated string` or JSON truncation
- Writing Python/JS/TS files with multiple functions
- Embedding CJK strings in source code

## When NOT to use

- The file is short (<50 lines) and ASCII-only — just use Write directly
- Making small edits to an existing file — just use Edit directly

## Key strategies

| Scenario | Strategy |
|---|---|
| New file > 50 lines | ASCII skeleton + Edit to fill |
| CJK content | ASCII skeleton with placeholders + Edit to insert CJK |
| Existing file, small edit | Edit tool directly |
| Existing file, large rewrite | Read → Edit in small chunks |
| Append to file | Use last line as anchor for Edit |

## File structure

```
llm-safe-write/
├── SKILL.md    # The prompt — read by the LLM at runtime
├── README.md   # This file — for humans
└── LICENSE     # MIT License
```

`SKILL.md` is the only file the LLM reads. It contains the complete routing logic, strategy workflows, error handling, and anti-patterns.

## License

MIT
