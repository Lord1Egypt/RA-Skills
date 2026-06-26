---
name: mdstr
description: This skill should be used when the user asks to "convert markdown to JSON string", "escape markdown for JSON", "make markdown JSON-safe", "embed markdown in JSON", "stringify markdown", or needs to convert a markdown file or text into a JSON-safe string for API calls, LLM prompts, or config files.
---

# mdstr - Markdown to JSON-safe String

Zero-config CLI for converting markdown to a JSON-safe string. Pass a file or pipe stdin, get a properly escaped JSON string on stdout. No flags required.

## Prerequisites

Ensure mdstr is available:

```bash
# Check if installed
which mdstr

# Install globally if needed
npm install -g mdstr

# Or use npx for one-off conversions
npx mdstr <file>
```

Requires Node.js 20 or later.

## Basic Usage

### From a file

```bash
mdstr README.md
mdstr ./docs/guide.md
```

### From stdin

```bash
cat notes.md | mdstr
echo '# "Hello" World' | mdstr
# → "# \"Hello\" World"
```

The output is always a single JSON string on stdout, surrounded by quotes, with all special characters properly escaped. Ready to embed directly into JSON structures.

## Options

| Flag | Description |
|---|---|
| `--preserve-newline` | Keep trailing newline in output (stripped by default) |
| `--version` | Show version number |
| `--help` | Show help with examples |

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Read/conversion error |
| `2` | Invalid usage (file not found, no input) |

## Common Workflows

### Convert a markdown file to a JSON-safe string

```bash
mdstr instructions.md
# → "# Instructions\n\nDo this and that.\n\nSaid \"hello\" and left."
```

### Embed markdown in a JSON payload

Use `jq` to build JSON structures with markdown content:

```bash
jq -n --argjson content "$(mdstr instructions.md)" '{prompt: $content}' > payload.json
```

### Inject markdown into LLM prompts

```bash
SYSTEM_PROMPT=$(mdstr system-prompt.md)
curl -s https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "$(jq -n --argjson prompt "$SYSTEM_PROMPT" '{
    model: "gpt-4o",
    messages: [{role: "system", content: $prompt}]
  }')"
```

### Build payloads from multiple markdown files

```bash
jq -n \
  --argjson system "$(mdstr system.md)" \
  --argjson user "$(mdstr user-prompt.md)" \
  '{messages: [{role: "system", content: $system}, {role: "user", content: $user}]}'
```

### Pipe markdown into JSON

```bash
echo '- line 1
- line 2' | mdstr | jq '{content: .}'
# → {"content": "- line 1\n- line 2"}
```

### Keep trailing newline

By default, mdstr strips the trailing newline. To preserve it:

```bash
mdstr README.md --preserve-newline
```

## Output Characteristics

The output is always:

- A single JSON string on stdout (with surrounding quotes)
- All special characters escaped (`"`, `\`, newlines, tabs, etc.)
- Trailing newline stripped by default (use `--preserve-newline` to keep)
- Errors on stderr
- Deterministic exit codes

No confirmation prompts. No color codes. No spinners. Designed for automated pipelines and agent tool calls.

## Error Handling

When conversion fails, check:

1. File exists and is readable
2. Input is provided (either a file argument or piped stdin)
3. Node.js 20 or later is installed

Errors are printed to stderr with actionable context.

## Use Cases

### API payloads

Convert markdown documentation or prompts into JSON-safe strings for REST API calls:

```bash
mdstr prompt.md
# Use the output directly in curl or httpie commands
```

### LLM prompt construction

Convert system prompts, user messages, or few-shot examples stored as markdown files into strings suitable for LLM API payloads.

### Configuration files

Embed markdown content (descriptions, help text, documentation) into JSON config files.

### CI/CD pipelines

Convert release notes or changelogs from markdown to JSON-safe strings for automated notifications or API integrations.
