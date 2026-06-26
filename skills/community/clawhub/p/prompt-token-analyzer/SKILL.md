---
name: Prompt Token Analyzer
description: A Node.js CLI tool that analyzes prompt token usage using a GPT-compatible tokenizer. Helps agents estimate prompt size, debug context overflow, and optimize token cost.
read_when:
  - Analyzing prompt token usage
  - Estimating LLM token cost
  - Debugging context window overflow
  - Optimizing prompts or RAG contexts
metadata: {"clawdbot":{"emoji":"🧮","requires":{"bins":["node","npm"]}}}
allowed-tools: Bash(prompt-token:*)
---

# Prompt Token Analyzer

Prompt Token Analyzer is a lightweight CLI tool that calculates how many tokens a prompt contains.  
It uses the `gpt-tokenizer` package to approximate GPT-style tokenization.

This helps AI agents and developers:

- estimate prompt size
- reduce unnecessary token usage
- debug large prompts
- optimize RAG pipelines

---

# Installation

Install the tokenizer:

```bash
npm install -g gpt-tokenizer
```

Create the CLI tool:

```bash
cat <<'EOF' > prompt-token
#!/usr/bin/env node

import { encode } from "gpt-tokenizer"
import fs from "fs"

const args = process.argv.slice(2)

if (args.length === 0) {
  console.log("Usage:")
  console.log("  prompt-token analyze <file>")
  console.log("  prompt-token text \"your prompt here\"")
  process.exit(1)
}

let text = ""

if (args[0] === "analyze") {
  const file = args[1]

  if (!file) {
    console.error("Missing file path")
    process.exit(1)
  }

  text = fs.readFileSync(file, "utf8")
}

else if (args[0] === "text") {
  text = args.slice(1).join(" ")
}

else {
  console.error("Unknown command")
  process.exit(1)
}

const tokens = encode(text)

console.log("Prompt Token Analysis")
console.log("---------------------")
console.log("Characters:", text.length)
console.log("Tokens:", tokens.length)
console.log("Average chars/token:", (text.length / tokens.length).toFixed(2))

const estimatedCost = tokens.length / 1000000 * 5

console.log("")
console.log("Estimated cost (example $5 / 1M tokens):")
console.log("$" + estimatedCost.toFixed(6))

EOF
```

Make the tool executable:

```bash
chmod +x prompt-token
```

Move it into PATH:

```bash
sudo mv prompt-token /usr/local/bin/
```

---

# Quick Start

Analyze a prompt file:

```bash
prompt-token analyze prompt.txt
```

Example output:

```
Prompt Token Analysis
---------------------
Characters: 7341
Tokens: 1832
Average chars/token: 4.01

Estimated cost (example $5 / 1M tokens):
$0.009160
```

---

# Analyze raw text

```bash
prompt-token text "Explain reinforcement learning in simple terms"
```

Example output:

```
Prompt Token Analysis
---------------------
Characters: 47
Tokens: 9
Average chars/token: 5.22
```

---

# Use Cases

### Prompt Engineering

Measure how prompt changes affect token size.

```bash
prompt-token text "You are an AI assistant..."
```

---

### RAG Context Analysis

Check how large retrieved documents are before sending them to an LLM.

```bash
prompt-token analyze rag_context.txt
```

---

### Debugging Context Overflow

Large prompts may exceed model limits.

Analyze them before sending to the model.

---

# Troubleshooting

If the tokenizer is missing:

```bash
npm install -g gpt-tokenizer
```

Check Node installation:

```bash
node --version
```

---

# Notes

- Token counts are approximate but close to OpenAI-style tokenization.
- Actual API usage may include additional system tokens.
- Long RAG contexts are the most common cause of token waste.

---

# Reporting Issues

Reinstall tokenizer if needed:

```bash
npm install -g gpt-tokenizer
```