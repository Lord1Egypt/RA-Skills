# Modules — ESM, CommonJS, and Resolution

## CommonJS

- `exports = x` rebinds a local alias — only `module.exports = x` changes what require returns.
- `require()` caches by resolved path: everyone gets the same object, mutations are global. Corollary: a package installed twice in the tree loads twice — two caches, two singletons, `instanceof` fails across them.
- Circular require returns whatever the partial export was at that moment — restructure, or require lazily inside the function that needs it.
- `require` is synchronous and blocking: a `require` inside a request handler that resolves a cold path reads and compiles files on the event loop (SKILL.md rule 1). Lazy-load with dynamic `import()` instead.
- `delete require.cache[...]` to force a reload leaves every already-captured reference pointing at the old copy. It is a development trick, never a production mechanism.

## ESM

- `__dirname`/`__filename` don't exist — `import.meta.dirname` (node >=20.11), else `fileURLToPath(import.meta.url)`. `import.meta.url` is a URL string, not a path: passing it to `fs` fails on any path containing a space (it arrives percent-encoded).
- Relative imports require the extension (`./util.js`) — CJS's extension guessing is gone; TypeScript compiled to ESM still needs `.js` in source imports (→ `typescript.md`).
- Directory imports (`./lib`) do not resolve to `./lib/index.js` in ESM. Name the file.
- `import` is hoisted and static — conditional or lazy loading needs dynamic `import()`, which returns a promise. Imports execute before any code in the importing module, so a `process.env` mutation at the top of your entry file happens *after* every imported module already read it.
- Top-level await blocks every importer — a module that awaits at the top level pauses evaluation of the whole import graph that depends on it until the promise settles.
- Live bindings: an imported binding tracks the exporter's value and cannot be reassigned by the importer. `import { count }` then `count++` is a TypeError, not a silent no-op like the CJS equivalent.
- Import maps do not exist in Node; the equivalents are the `imports` field for internal aliases (`#db/client`) and `exports` for the public surface. Both work at runtime with no bundler.

## Interop

- CJS → ESM: `require()` of a synchronous ESM graph works on node >=22.12; below that, dynamic `import()` is the only door — and it makes the caller async, which is why the change ripples.
- ESM → CJS: the default import receives `module.exports`; named imports work only when the exports are statically detectable (cjs-module-lexer) — the fallback is `pkg.default.thing`. Print the namespace when unsure: `node -p "Object.keys(await import('pkg'))"`.
- `"type": "module"` flips every `.js` file in the package; `.cjs`/`.mjs` override per file. The nearest package.json wins, so a nested directory can carry its own format.
- Dual-package hazard: a package shipped as both CJS and ESM can load twice into one app — two module instances, `instanceof` and module-level state break across them. Ship one format plus a thin wrapper, or go ESM-only (→ SKILL.md Where Experts Disagree).
- Symptom of the hazard in the wild: a singleton (a database connection, a registry, an event bus) that "resets itself", or an `instanceof` check failing on an object that clearly is that class. `npm ls <pkg>` showing two paths confirms it.

## The Package Entry Contract

- `exports` is the modern surface and wins where supported; `main` is the legacy fallback for old tooling. Conditions resolve in declaration order — put `types` first, `default` last:

```json
{
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "default": "./dist/index.cjs" },
    "./package.json": "./package.json"
  }
}
```

- The `exports` map blocks deep imports (`pkg/lib/internal`) by design — that's your API surface; add subpath exports rather than removing the field when a consumer complains.
- Exporting `./package.json` explicitly is worth the line: a surprising number of tools read it and fail loudly when the map blocks them.
- Conditions are matched, not merged: the first match wins for the whole entry, so a `types` condition placed after `import` never applies.
- Removing or renaming a subpath in `exports` is a breaking change even when the file still exists.

## Resolution Order and Debugging

1. Node's builtins (and anything prefixed `node:`) always win — `node:fs` cannot be shadowed, plain `fs` can be by a local package of that name.
2. Relative and absolute specifiers resolve as files, with ESM requiring the exact extension.
3. Bare specifiers walk up `node_modules` from the importing file, so the same specifier can resolve differently in two directories of one repository — that is how a monorepo ends up with two versions loaded at once.
4. `imports` entries (`#alias`) resolve from the nearest package.json and never touch `node_modules`.

Tools: `node -p "require.resolve('pkg')"` (CJS) or `node -p "import.meta.resolve('pkg')"` in ESM prints the exact file. `npm ls <pkg>` prints every copy in the tree. When both disagree with your assumption, believe them.
