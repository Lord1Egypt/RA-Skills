# Verification — commands and exit codes

## Tier 0 (zero-install, always available)

| Command | What it checks | Exit codes |
|---|---|---|
| `npm test` | Unit tests via `node --test` (lib + scanner). | `0` pass, non-zero fail |
| `npm run verify:lite -- <bundle.prompt.md>` | Single-file scan: S1/S2/S3 present, colophon, no `TODO:` leaks, no plaintext secrets, ≥ 3 binary acceptance items, packaging/security sections present. | `0` clean, `1` findings, `2` file error |
| `npm run verify:lite -- --template <template.prompt.md>` | Same but tolerates `<replace: ...>` placeholders (for the unfilled templates in this repo). | `0` clean, `1` findings |
| `npm run smoke` | 60s repo-wide sanity: INDEX.json valid, every referenced template exists, every template scans clean in `--template` mode, no secret leaks anywhere in repo, and ClawHub skill scripts clear the safety deny-list. | `0` clean, `1` findings |
| `npm run validate` | `smoke` plus template, eval, package, and ClawHub cleanliness checks. | `0` clean, `1` findings |
| `npm run pack` | Builds a deterministic ClawHub tarball with fixed archive mtimes and forbidden-entry checks. | `0` clean, `1` findings |
| `npm run quality:score -- <bundle.prompt.md>` | Prints 0–100 score with missing axes. | `0` informational, `1` if `--strict` and score < 80, `2` file error |

## Tier 1 (executed by the calling coding agent, not by this skill)

Whatever build tool the bundle's mode requires:

| Mode | Tier 1 command |
|---|---|
| A-01 | `npm run tauri build` |
| A-02 / A-04 | `xcodebuild archive` |
| A-03 | `msbuild /restore /p:Configuration=Release` |
| A-05 | `./gradlew bundleRelease` |
| A-06 | `hvigorw assembleHap` |
| A-07 | `flutter build ipa` / `flutter build appbundle` |
| A-08 | `eas build --platform all` |
| A-09 | `miniprogram-ci upload` |
| A-10 | `docker compose up -d` |
| A-11 | `npm run build` |
| A-12 | `npm run build` or `python -m build` |

These are **never** run by `npm test`. The skill stays zero-install.

## What `verify:lite` does (in detail)

1. Read the file.
2. Extract the YAML front-matter if present (templateId, mode).
3. Locate the section headers: `## S1`, `## S2`, `## S3`, `## Acceptance`, `## Packaging`, `## Security` (case-insensitive prefix match).
4. For each header, require non-empty body (or in `--template` mode, allow `<replace: ...>` markers).
5. Scan body for:
   - Secret patterns: `sk_live_*`, `ghp_*`, `AKIA*`, `xox[bapr]-*`, `AIza[0-9A-Za-z_-]{35}`, private-key PEM blocks
   - Unfilled brace-style placeholders `{like this}` (not in `--template` mode)
   - Literal `TODO:`, `FIXME:`, `lorem ipsum` (not in `--template` mode)
   - Bare `http://` URLs in security-sensitive contexts
6. Locate `## Acceptance` and count `- [ ]` checkbox lines; require ≥ 3 (≥ 1 in `--template` mode).
7. Locate the colophon line `— shaped with ifq.ai/app-builder`.
8. Print findings; exit accordingly.

## What it does NOT do

- It does **not** check that the described app actually builds. That's Tier 1.
- It does **not** validate that the user's three sentences are *good*; only that they exist and aren't placeholder leftovers. Use `quality:score` for fit-and-finish.
- It does **not** make network calls.

## CI

The root repository CI runs this ClawHub package through `npm run validate`, prompt verification, strict quality scoring, and deterministic packing on Node 18, 20, 22 across macOS, Ubuntu, and Windows.
