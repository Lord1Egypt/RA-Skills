# Writing Coach Pro — Security

## How Text Is Processed

Writing Coach Pro runs as an agent skill inside your OpenClaw instance. When you submit text for review, it is processed by whatever LLM backend your agent is configured to use (Claude, GPT-4, Gemini, a local model, etc.).

**Your text goes wherever your LLM calls go.** If your agent uses a cloud-hosted model (most do), your text is sent to that model's API. If your agent uses a local model (Ollama, llama.cpp), your text is processed locally.

We do not operate any servers that receive, store, or process your text. Writing Coach Pro is a set of instructions and scripts that your agent executes locally.

## What Gets Stored Locally

Writing Coach Pro stores the following files on your machine:

- **Style profile** (`config/settings.json`): Your writing preferences — style guide, tone, vocabulary level, custom rules. Contains no actual text you've submitted.
- **Learning log** (`data/learning-log.json`): Metadata about past sessions — dates, word counts, issue counts, acceptance rates. Contains issue descriptions but not your original text.
- **Session history** (`data/session-history/`): Per-session analysis summaries. May contain excerpts from your submitted text alongside suggested corrections.
- **Exported reports** (`reports/`): Analysis reports you explicitly generate. Contain excerpts and analysis of your text.

## What We Can and Cannot Guarantee

**We can tell you:**
- Writing Coach Pro does not phone home, ping any NormieClaw server, or transmit data anywhere
- The skill files are readable plaintext — you can audit every line
- No analytics, telemetry, or tracking is built into this skill

**We cannot guarantee:**
- How your LLM provider handles text sent via API calls (review their privacy policies)
- The security of your local filesystem or OpenClaw installation
- That future OpenClaw updates won't change how skills interact with external services

## Recommendations

- Review your LLM provider's data handling policies if you process sensitive documents
- Use a local model (Ollama, llama.cpp) if you need text to stay on your machine
- The `data/` directory contains analysis metadata — protect it like any personal file
- Run `rm -rf ~/.openclaw/skills/writing-coach-pro/data` to delete all stored analysis data

## Reporting Issues

If you discover a security concern with Writing Coach Pro, email security@normieclaw.ai.
