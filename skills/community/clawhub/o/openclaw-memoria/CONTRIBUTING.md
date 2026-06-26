# Contributing to Memoria

Thanks for your interest in contributing! 🧠

## Getting Started

1. Fork the repo
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/openclaw-memoria.git
   cd openclaw-memoria
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Run tests:
   ```bash
   npx tsx tests/test-core.ts
   ```

## Development Setup

### Requirements
- Node.js 20+
- Ollama with `gemma3:4b` and `nomic-embed-text-v2-moe` (for full integration tests)
- OpenClaw (for plugin testing)

### Running in OpenClaw
1. Symlink or copy the extension into `~/.openclaw/extensions/memoria/`
2. Add to `openclaw.json`:
   ```json
   { "plugins": { "allow": ["memoria"], "entries": { "memoria": { "enabled": true } } } }
   ```
3. Restart gateway: `openclaw gateway restart`

## What to Contribute

### High-impact areas
- **New LLM providers** — implement `LLMProvider` interface in `providers/`
- **Better extraction prompts** — improve fact quality from conversations
- **Benchmark datasets** — more diverse test scenarios in `benchmarks/`
- **Contradiction detection** — improve stale fact supersession
- **Performance** — optimize FTS5/embedding queries for large DBs (10K+ facts)

### Good first issues
- Add tests for individual modules (graph, topics, observations)
- Improve `.md` regeneration formatting
- Add provider for Groq, Together, Mistral API

## Code Style

- TypeScript (strict when possible)
- Imports use `.js` extension (ESM resolution)
- Functions documented with JSDoc where non-obvious
- Error handling: prefer graceful degradation over throwing

## Pull Request Process

1. Create a branch: `git checkout -b feat/my-feature`
2. Write tests if applicable
3. Run existing tests: `npx tsx tests/test-core.ts`
4. Commit with clear message: `feat: add Groq provider support`
5. Open PR against `main` with:
   - What changed and why
   - Test results
   - Breaking changes (if any)

## Commit Convention

```
feat: new feature
fix: bug fix
docs: documentation only
perf: performance improvement
test: adding tests
refactor: code restructuring
```

## License

By contributing, you agree that your contributions will be licensed under Apache 2.0.
