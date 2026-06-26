# Contributing to Edicts

Thanks for taking the time to contribute.

Edicts is intentionally small: a standalone TypeScript library for managing ground-truth facts for AI agents. The core should stay framework-agnostic, dependency-light, and boring in the best possible way.

## Development setup

Clone the repo, install dependencies, and run the standard checks:

```bash
npm install
npm test
npm run build
npm run lint
```

Important: this is a library, not a web app.

- Build uses **tsup** via `npm run build`
- Type-checking uses `tsc --noEmit` via `npm run lint`
- Tests use **vitest**
- Do **not** use `vite build` here. That road leads nowhere useful.

## Test expectations

Before opening a PR, run:

```bash
npm test
```

Use watch mode while iterating:

```bash
npm run test:watch
```

The full suite should stay green. If the current bar is 168+ tests, keep it there or raise it.

## Code style and architectural rules

A few project rules matter more than personal taste:

- TypeScript runs in **strict mode**
- Public methods return `structuredClone()` copies, never internal references
- File I/O uses **atomic writes**
- Optimistic concurrency uses SHA-256 content hashing for conflict detection
- Category and tag normalization must stay consistent
- `_tokens` is internal and must never leak into serialized output
- This package keeps dependencies minimal; `yaml` is the only runtime dependency today

If you are changing store behavior, read the code carefully before “simplifying” anything. A lot of the odd-looking edges are there because the library is protecting correctness.

## Making changes

Typical workflow:

1. Fork the repo
2. Create a branch for your change
3. Add or update tests first when behavior changes
4. Implement the change
5. Run `npm test`, `npm run build`, and `npm run lint`
6. Open a pull request with a clear summary

Small, focused PRs are strongly preferred over giant kitchen-sink refactors.

## Adding tests

Every public API method should have test coverage.

General expectations:

- Mirror source structure in tests: `src/store.ts` → `tests/store.test.ts`
- Use temp directories for file-based tests
- Clean up temp data in `afterEach`
- Cover success paths, edge cases, and failure modes
- For bug fixes, include a regression test

If you are changing CLI behavior, add or update CLI tests too.

## What we want

Contributions we will happily review:

- Bug fixes
- Better tests and regression coverage
- Documentation improvements
- Performance improvements that do not complicate the API
- Small ergonomic improvements grounded in real use cases

## What we do not want

Please do **not** turn core into a framework bundle.

That means no:

- LangChain-only abstractions in the core package
- CrewAI, AutoGen, or other framework adapters mixed into the store implementation
- Heavy runtime dependencies for features that can stay optional
- Large speculative rewrites without a concrete problem statement

Framework integrations are welcome when they are clearly isolated from the core library.

## Documentation

If you add or change public behavior, update the docs in the same PR:

- `README.md` for repo-level overview changes
- `CONTRIBUTING.md` if contributor workflow changes
- `edicts.ai` docs for user-facing API or guide changes

## Pull request notes

A good PR description includes:

- what changed
- why it changed
- any compatibility implications
- which tests cover it

If the change is intentionally opinionated, say so plainly.

## Questions

If something is unclear, open an issue before building a large feature. That is usually cheaper than showing up with a heroic but misaligned PR.
