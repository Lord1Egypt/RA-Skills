---
name: missing-imports
description: Code uses a symbol that isn't imported, or imports a symbol that doesn't exist in the source module.
emoji: 📦
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# missing-imports

The generated code uses a name that hasn't been brought into scope, or imports from a module that doesn't export the named symbol. A guaranteed runtime `NameError` / `ReferenceError` / `ImportError`.

## Symptoms

- Code uses `Foo` but `Foo` is never imported.
- `from mod import X` where `mod` exists but does not export `X`.
- `import { x } from "pkg"` with no matching named export.
- Static analysis flags `unused-import` alongside `undefined-name` — common when the agent copy-pastes between files.

## What to do

- For every symbol used in the diff, confirm there is a corresponding import in the same file or that the symbol is defined locally.
- For every new import, verify the target module actually exports that name. Open the module if needed.
- Don't guess at package layout. When unsure, read the package's `package.json` exports, `__init__.py`, or equivalent.
- Run the static checker (tsc, mypy, pyright, etc.) after every non-trivial change. Missing imports almost always surface there.
- Remove unused imports in the same change so the surface stays honest — stale imports mask real failures.
