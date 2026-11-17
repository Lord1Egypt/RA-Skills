# TypeScript On Node — The Runtime Half

Scope: getting `.ts` to run, resolve, and ship correctly on Node. Type-system design, generics, and tsconfig strictness belong to the typescript skill; everything here is about the runtime believing you.

## Pick One Execution Model

| Model | What runs | Use when |
|---|---|---|
| Type stripping (`node file.ts`) | Node erases types, executes the rest — no transform, no source map layer | Apps deployed from source on node >=24 (backported to 22.18) |
| Loader (`tsx`, `ts-node`) | Transpiles in-process at import time | Older majors, or code using non-erasable syntax |
| Build step (`tsc`, or a bundler) | Emits `.js` + `.d.ts`, Node runs plain JavaScript | Published libraries, anything that must ship declarations |

- Default to the build step for anything published to a registry: consumers need `.js` and `.d.ts`, and neither stripping nor a loader produces them.
- Default to type stripping for services on a current runtime: one fewer dependency, one fewer transform, and stacks that point at the real file.
- Never mix: a repository where some entry points are stripped and others are built has two resolution behaviors and one confused debugger.

## Type Stripping Limits

Stripping erases types in place; it cannot emit code that was not written. Anything with runtime semantics is rejected or requires a transform flag:

- Not erasable: `enum` (emits an object), `namespace` with runtime members, parameter properties (`constructor(private x: string)`), legacy `experimentalDecorators` metadata emit.
- Erasable and fine: interfaces, type aliases, generics, `satisfies`, `as`, and type-only imports/exports.
- `verbatimModuleSyntax: true` in tsconfig forces `import type` where a type is meant, which makes the "erasable-only" subset explicit at compile time instead of at first run.
- The practical migration: turn on `erasableSyntaxOnly` in tsconfig, fix what it flags (usually enums → union types or `as const` objects), then drop the loader.

## Module Resolution (where most of the pain is)

- `moduleResolution` must match how Node actually resolves. For ESM on Node: `"module": "nodenext"` and `"moduleResolution": "nodenext"`. Anything else lets `tsc` accept imports that fail at runtime.
- Relative imports in ESM need the extension, and the extension is `.js` even in a `.ts` source file — you are naming the emitted file, not the source. `import { x } from './util.js'` inside `util.ts`'s neighbor is correct, and looks wrong to everyone the first time.
- `allowImportingTsExtensions` lets you write `./util.ts`, but only with `noEmit` (or `rewriteRelativeImportExtensions`) — otherwise the emitted JavaScript imports a `.ts` file that will not exist at runtime.
- `esModuleInterop: true` changes what a default import means. With it, `import express from 'express'` works against a CJS module; without it, you need `import * as express`. Turning it on later flips both behaviors across the codebase at once.
- Path aliases (`paths` in tsconfig) are a compile-time fiction: Node has never heard of `@/lib/foo`. They need a bundler, a loader that reads them, or Node's `imports` field (`#lib/foo`) which works at runtime with no tooling.
- Two package.json fields decide what consumers get: `main` (legacy CJS entry) and `exports` (modern, wins where supported, and blocks deep imports). `types` must sit alongside each entry in `exports`, or consumers see `any`.

## Types Do Not Survive To Runtime

- Type checking is not validation. Data crossing a boundary — HTTP body, env, JSON file, database row — arrives as `any` or a lie. Validate with a runtime schema at the boundary and derive the static type from it, so the two cannot drift.
- `as` is an assertion the compiler stops arguing with, not a conversion: `JSON.parse(body) as User` gives you a `User`-shaped hole at runtime.
- `strict: true` is a floor, not a guarantee: a non-null assertion or an `any` from an untyped dependency reopens everything downstream of it.
- `process.env.PORT` is typed `string | undefined` for a reason — parse it once at startup with the rest of the environment (→ `production.md`).

## Stacks, Source Maps, and Debugging

- Without source maps, a stack trace points into emitted JavaScript at line numbers that mean nothing. With a build step: `"sourceMap": true` and run with `--enable-source-maps`.
- Type stripping keeps line positions aligned by replacing types with whitespace, so stacks point at the real `.ts` lines without a map. That is one of its practical advantages over a transpiling loader.
- Source maps in production are a tradeoff: readable stacks in your logs, and readable source for anyone who obtains the bundle. Ship them to the error reporter rather than into the public artifact.

## Testing and Building

- Type check and test are different jobs: `tsc --noEmit` in CI catches type errors; the test runner catches behavior. A transpile-only test setup (tsx, esbuild, swc) is fast precisely because it skips type checking — if `tsc --noEmit` is not a separate CI step, nothing is checking types.
- `node --test` runs `.ts` directly where stripping is available; Jest needs a transform layer (ts-jest or babel) and Vitest handles it natively (→ `testing.md`).
- Ship the built output, not the sources, and verify with `npm pack --dry-run` that `.d.ts` files are actually in the tarball (→ `packages.md`). A published package whose types are missing degrades every consumer to `any` silently.
- `skipLibCheck: true` is near-universal and hides genuine conflicts between two dependencies' type versions; when a mysterious type error appears after an upgrade, turning it off temporarily is the diagnostic.
