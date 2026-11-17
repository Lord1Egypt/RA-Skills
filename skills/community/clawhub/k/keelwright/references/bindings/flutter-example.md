# Binding example — Flutter / Dart / Supabase

This is an EXAMPLE binding. Copy it to `references/bindings/<your-stack>.md` and swap the commands
for your ecosystem. The engine (SKILL.md + phases/security-gates/writing-code/stability/match)
never changes — only this file does.

Stack: Flutter + Dart (+ Supabase). Feature-first clean architecture.

## Backpressure gate commands

| Gate | Command |
|---|---|
| Tests | `flutter test` |
| Typecheck / analyze | `dart analyze` |
| Lint | `dart analyze` (covers) / `flutter analyze` |
| Build | `flutter build <target>` |

Rules: fix CODE, not tests, to make a gate green (reward-hacking guard). Two identical errors in
a row → stop → counterfactual ("A failed because… → B because… → root cause is…") → then fix.
3 attempts → escalate.

## Quality scan (all MIT-licensed)

| Concern | Tool | License | Command |
|---|---|---|---|
| Duplication | jscpd | MIT | `npx jscpd --threshold 10 ./lib` (sync with dup>10% ceiling) |
| Complexity + metrics (Dart-native) | dart_code_linter | MIT | `dart run dart_code_linter:metrics analyze lib` |
| Dead code / analysis | dart_code_linter + `dart analyze` | MIT / SDK | `dart run dart_code_linter:metrics check-unused-code lib` |

For JS/TS stacks, the structural-integrity gate uses **madge** (`npx madge --circular ./src`, MIT) for
cycles, **eslint-plugin-boundaries** (MIT) for layer enforcement, and **knip** (ISC) for dead code.
Dart covers cycles/boundaries via `dart analyze` + dart_code_linter; add madge-equivalent only if needed.

`dart_code_linter` (DCL) is the maintained open-source MIT fork of the old dart_code_metrics —
it reports cyclomatic complexity, nesting, parameter counts, and anti-patterns, and is fully free
(no license key, no LOC cap). It replaces vendor tools that moved metrics behind a paywall.

Build a quality score by combining duplication% (jscpd) with the count of functions over your CCN
threshold (dart_code_linter). You set the thresholds → the score is transparent and can't be
gamed. Two worsening iterations → clean-code-review.

## Language-specific security grep (Gate 1 second layer)

What generic SAST doesn't know about this stack. Grep on added lines:

```bash
# Backend-only secret used client-side (e.g. a privileged DB key) — RLS bypass
git diff --cached | grep "^+" | grep -iE "service_role|SERVICE_KEY"
# Disabled TLS verification
git diff --cached | grep "^+" | grep -iE "badCertificateCallback|allowInsecure|http://"
# SQL/RPC string concatenation (injection)
git diff --cached | grep "^+" | grep -iE "\.rpc\(.*\$|\.raw\(.*\$|'\s*\+\s*.*SELECT"
# Logging sensitive data
git diff --cached | grep "^+" | grep -iE "print\(.*(password|token|secret)|debugPrint\(.*(password|token)"
```
Any match → a security concern, fix before commit. (Primary layer Gitleaks + Semgrep is in
`../security-gates.md` Gate 1.)

## Layers (feature-first clean architecture)

- `data/` — repositories, DTOs, sources (DB, API)
- `domain/` — models, use cases, repository interfaces
- `presentation/` — screens, widgets, state
- `core/` — utilities, constants, DI
- `app/` — root, routing, themes

Dependencies point inward: `presentation → domain ← data` (domain depends on no one). Details —
the `clean-architecture` skill.

## Reuse-ladder specifics for this stack

At ladder step L2 check the framework SDK / language stdlib; at L3 check the dependency manifest
(`pubspec.yaml`) before adding a package; at L4 check the existing state mechanism before adding
another.

## Release

`git push` (per git-safety: new branch, never main without asking) → CI builds → "✅ Shipped."
