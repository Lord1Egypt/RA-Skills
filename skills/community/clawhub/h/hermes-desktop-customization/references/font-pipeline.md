# Desktop font pipeline map

Two independent mono-font systems exist; `desktop-custom` bridges them. Written
after the FiraCode-in-chat investigation (2026-08-22).

## Terminal path (upstream feature)

`config.yaml terminal.font_family` → `use-hermes-config.ts` →
`setTerminalFontFamilyFromConfig()` → `$terminalFontFamily` nanostore atom
(`src/app/right-sidebar/terminal/terminal-font.ts`) → xterm
`options.fontFamily`. Empty → bundled JetBrains Mono stack
(`DEFAULT_TERMINAL_FONT_FAMILY`). `resolveTerminalFontFamily()` quotes single
family names and appends the bundled stack as fallback.

## Chat path (was theme-only; bridged on desktop-custom)

Theme presets (`src/themes/presets.ts`) declare optional `typography.fontMono`;
most inherit `DEFAULT_TYPOGRAPHY`/SYSTEM_MONO = `Menlo, Monaco, 'SF Mono',
'Courier Prime', monospace` — macOS-centric faces that miss on Linux, falling
through to fontconfig generic monospace. `applyTheme()` in
`src/themes/context.tsx` paints `--dt-font-mono` on `:root`; every Tailwind
`font-mono` consumer inherits it.

Upstream intentionally kept themes owning chat typography (DESIGN.md contract;
auto-injecting config makes theme previews lie). #37566 asked for an app-wide
font selector — closed P3; what shipped was the TERMINAL picker
(`0399711be feat(desktop): add terminal font picker`). #40399's closing PR
#43292 delivered VS Code marketplace COLOR themes only, not typography.

## The bridge (commit ef94c674b, branch desktop-custom)

- `preferredMonoFamily()` (terminal-font.ts): configured family as quoted CSS
  entry; `null` when unset.
- `context.tsx applyTheme()`: paints `--dt-font-mono` as
  `` `${preferredMono}, ${typo.fontMono}` `` — prepend, NOT replace (first
  test draft replaced the stack and the intent test caught it).
- `ThemeProvider` subscribes to `$terminalFontFamily`; the paint effect takes
  it as a dep → live repaint when config arrives or Settings changes.
- Intent tests: `context.test.tsx` → describe
  `ThemeProvider ← terminal.font_family mono composition`.
- Settings copy updated in en/ja/zh-hant ("terminals and chat code/diff text").

## Dead ends (don't retry)

- Custom/user themes CANNOT carry typography: the VS Code theme converter
  validates `background/foreground/primary` only; hand-editing the
  `hermes-desktop-user-themes-v1` localStorage blob is unsupported and
  hardcodes one font instead of tracking Settings.
- Grep-based verification must target `app.asar.unpacked/dist/` — see
  SKILL.md pitfalls.
