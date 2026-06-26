---
templateId: T-pc-tauri
ifqMode: A-01
stack: "Tauri 2 + React + Vite + TypeScript"
artifact: ".dmg / .exe / .AppImage"
---

# T-pc-tauri · cross-platform desktop · ifq-app-builder

Fork this file into the user workspace as `<slug>.prompt.md`, fill every `<replace: ...>` block, run `npm run verify:lite -- <slug>.prompt.md`, then hand to the calling coding agent.

## S1 — WHO + WHAT
<replace: who uses this app, what they do every day, what data goes in and what artifact comes out>

## S2 — WHERE
- Platforms: macOS 12+ (Apple Silicon + Intel), Windows 10/11 x64, Linux x64 (AppImage)
- Stack (pinned): Tauri 2 + Rust stable + React 18 + Vite 5 + TypeScript 5
- Runtime: 100% local; no telemetry; no required network at first launch
- Distribution: <replace: signed installer / private link / GitHub Release / company MDM>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements that describe a successful build on a fresh laptop>

## Acceptance (binary, yes/no observable)
- [ ] `cargo tauri dev` opens a window in under 3s on a 2020-era laptop
- [ ] Primary workflow described in S1 succeeds end-to-end with <replace: a real sample input>
- [ ] All copy localized in `zh-CN` and `en`, single source under `src/i18n/`
- [ ] App size <30 MB compressed installer
- [ ] No console errors, no panics, no crashes during the primary workflow
- [ ] Uninstalling cleanly removes app data unless user opted in to keep it

## Scaffold (run order)
1. `npm create vite@latest <slug> -- --template react-ts`
2. `cd <slug> && npm install`
3. `npm install --save-dev @tauri-apps/cli @tauri-apps/api`
4. `npx tauri init` — answer prompts to match S2
5. Drop `assets/ifq-brand/ifq-tokens.css` into `src/styles/` and `@import` it in `src/main.tsx`
6. Implement the primary workflow per S1; keep heavy I/O in a Tauri `command` (Rust side) and call from React via `invoke()`
7. Add `src/i18n/{zh-CN,en}.json` and a small `useT()` hook
8. `npm run tauri build` for each target platform

## Packaging
- macOS: `.dmg` + `.app`, signed with Developer ID (if available), notarized via `xcrun notarytool`
- Windows: `.exe` (NSIS) + MSIX (optional), signed with EV cert if available
- Linux: `.AppImage` (+ `.deb` if requested)
- All three are produced by `npm run tauri build` with matrix CI; do **not** claim signing unless certs are present

## Security baseline (OWASP-aligned)
- Tauri `allowlist`: enable only the file-system + dialog scopes actually used; deny everything else
- No `tauri.conf.json -> tauri.security.dangerousRemoteDomainIpcAccess`
- Use `keytar` / OS keychain for any credential; never plaintext in `localStorage`
- CSP enforced via `tauri.conf.json -> tauri.security.csp`
- All user-supplied paths validated against `tauri::api::path::resolve`

## IFQ ambient
- CSS tokens: `assets/ifq-brand/ifq-tokens.css` imported globally
- Footer / About dialog: contains exactly one colophon line `— shaped with ifq.ai/app-builder`
- App icon may include the IFQ mark only if the product is IFQ-owned; otherwise use the user's brand

## Agent execution contract
- Before scaffolding, **print the three sentences back to the user** for sanity
- Run `cargo --version`, `node --version`, `rustup target list --installed` and report mismatches before installing toolchains
- If macOS code-signing cert is missing, build unsigned and label `S3.packaging` as `(blocked: need Developer ID)`
- Never `--no-verify` on git commits

— shaped with ifq.ai/app-builder · A-01 · T-pc-tauri
