# Jest Skill

An AI agent skill for writing, debugging, and reviewing Jest tests with modern best practices.

Created by **[Anivar Aravind](https://anivar.net)**

## The Problem

AI agents frequently generate outdated or incorrect Jest patterns — wrong mock cleanup semantics (`clearAllMocks` vs `restoreAllMocks`), missing `await` on async assertions, incorrect timer mock usage, factory hoisting bugs, and anti-patterns that cause tests to silently pass without actually asserting anything. These produce test suites that compile and pass but don't test what they claim to test.

## This Solution

28 rules with incorrect→correct code examples that teach agents Jest's actual API behavior, mock lifecycle, async patterns, timer control, module mocking, snapshot testing, configuration, and CI optimization. Each rule targets a specific mistake and shows exactly how to fix it.

## Install

```bash
npx skills add anivar/jest-skill -g
```

Or with full URL:

```bash
npx skills add https://github.com/anivar/jest-skill
```

## Baseline

- jest ^29.0.0 / ^30.0.0
- JavaScript / TypeScript

## What's Inside

### 28 Rules Across 9 Categories

| Priority | Category | Rules | Impact |
|----------|----------|-------|--------|
| 1 | Mock Design | 5 | CRITICAL |
| 2 | Async Testing | 3 | CRITICAL |
| 3 | Matcher Usage | 3 | HIGH |
| 4 | Timer Mocking | 3 | HIGH |
| 5 | Test Structure | 3 | HIGH |
| 6 | Module Mocking | 3 | MEDIUM |
| 7 | Snapshot Testing | 3 | MEDIUM |
| 8 | Configuration | 3 | MEDIUM |
| 9 | Performance & CI | 2 | MEDIUM |

Each rule file contains:
- Why it matters
- Incorrect code with explanation
- Correct code with explanation
- Decision tables and additional context

### 9 Deep-Dive References

| Reference | Covers |
|-----------|--------|
| `matchers.md` | All matchers: equality, truthiness, numbers, strings, arrays, objects, asymmetric, custom |
| `mock-functions.md` | jest.fn, jest.spyOn, .mock property, return values, implementations, mock matchers |
| `jest-object.md` | jest.mock, jest.useFakeTimers, jest.setTimeout, jest.retryTimes, jest.replaceProperty |
| `async-patterns.md` | Promises, async/await, done callbacks, .resolves/.rejects, expect.assertions |
| `configuration.md` | Key config options: testMatch, transform, moduleNameMapper, coverage, environments |
| `snapshot-testing.md` | toMatchSnapshot, inline snapshots, property matchers, serializers, updating |
| `module-mocking.md` | Manual mocks, __mocks__ directory, ESM mocking, partial mocking, jest.requireActual |
| `anti-patterns.md` | 15 common mistakes with BAD/GOOD examples |
| `ci-and-debugging.md` | CI optimization, --runInBand, --shard, debugging with inspector, troubleshooting |

## Structure

```
├── SKILL.md                          # Entry point for AI agents
├── AGENTS.md                         # Compiled guide with all rules expanded
├── rules/                            # Individual rules (Incorrect→Correct)
│   ├── mock-*                        # Mock design (CRITICAL)
│   ├── async-*                       # Async testing (CRITICAL)
│   ├── matcher-*                     # Matcher usage (HIGH)
│   ├── timer-*                       # Timer mocking (HIGH)
│   ├── structure-*                   # Test structure (HIGH)
│   ├── module-*                      # Module mocking (MEDIUM)
│   ├── snapshot-*                    # Snapshot testing (MEDIUM)
│   ├── config-*                      # Configuration (MEDIUM)
│   └── perf-*                        # Performance & CI (MEDIUM)
└── references/                       # Deep-dive reference docs
    ├── matchers.md
    ├── mock-functions.md
    ├── jest-object.md
    ├── async-patterns.md
    ├── configuration.md
    ├── snapshot-testing.md
    ├── module-mocking.md
    ├── anti-patterns.md
    └── ci-and-debugging.md
```

## Ecosystem — Skills by [Anivar Aravind](https://anivar.net)

This Jest skill covers Jest's own API surface — the foundation layer. For framework-specific testing patterns built on top of Jest, use companion skills:

### Testing Skills (Jest Foundation)

| Need | Skill | Install |
|------|-------|---------|
| **API mocking** (network-level) | [msw-skill](https://github.com/anivar/msw-skill) — MSW 2.0 handlers, server lifecycle, per-test overrides | `npx skills add anivar/msw-skill -g` |
| **React Native components** | [react-native-testing](https://github.com/anivar/react-native-testing) — RNTL v13/v14 queries, userEvent, async render | `npx skills add anivar/react-native-testing -g` |
| **Zod schema validation** | [zod-testing](https://github.com/anivar/zod-testing) — safeParse testing, mock data, property-based testing | `npx skills add anivar/zod-testing -g` |
| **Redux-Saga side effects** | [redux-saga-testing](https://github.com/anivar/redux-saga-testing) — expectSaga, testSaga, providers | `npx skills add anivar/redux-saga-testing -g` |

### Library & Framework Skills

| Skill | What it covers | Install |
|-------|---------------|---------|
| [zod-skill](https://github.com/anivar/zod-skill) | Zod v4 schema validation, parsing, error handling, type inference | `npx skills add anivar/zod-skill -g` |
| [redux-saga-skill](https://github.com/anivar/redux-saga-skill) | Redux-Saga effects, fork model, channels, RTK integration | `npx skills add anivar/redux-saga-skill -g` |
| [msw-skill](https://github.com/anivar/msw-skill) | MSW 2.0 API mocking — handlers, responses, GraphQL, v1→v2 migration | `npx skills add anivar/msw-skill -g` |

### Engineering Analysis Skills

| Skill | What it covers | Install |
|-------|---------------|---------|
| [contributor-codebase-analyzer](https://github.com/anivar/contributor-codebase-analyzer) | Deep-dive code analysis, annual reviews, promotion readiness | `npx skills add anivar/contributor-codebase-analyzer -g` |

## Author

**[Anivar Aravind](https://anivar.net)** — Building AI agent skills for modern JavaScript/TypeScript development.

## License

MIT
