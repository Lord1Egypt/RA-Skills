---
name: obclip
description: Install, verify, and operate the obclip CLI to clip live web pages into Markdown or Obsidian notes. Use when Codex needs to install the @harris7/obclip npm package, choose between default Playwright Chromium and a real Chromium executable/profile, run clipping commands with stable waiting rules, save notes to disk or Obsidian, or diagnose incomplete capture, login walls, and browser startup issues.
---

# Obclip

Use this skill to make `obclip` work predictably instead of trial-and-error.

## Workflow

1. Verify how `obclip` should be invoked.
2. Pick the browser mode that matches the target site.
3. Run the smallest command that can succeed.
4. Escalate waiting and browser state only when the output is incomplete.
5. Report the final saved path or the concrete failure reason.

## 1. Verify Invocation

- Prefer `obclip` if it is already on `PATH`.
- If `obclip` is missing, install the npm package from [install-and-invoke.md](./references/install-and-invoke.md).
- If you are working inside the source repo and the global command is unavailable, fall back to `node <repo>\\dist\\cli.cjs ...`.
- After installation, verify with `obclip --help` or `npx @harris7/obclip --help`.

## 2. Pick Browser Mode

- Use the default bundled Playwright Chromium for public pages that do not need login state.
- Use `--browser-executable "<path>"` when the user already has a dedicated Chromium build and wants a fixed browser binary.
- Use `--browser-profile "<dir>"` for sites that require login state, cookies, or a persistent session.
- Use `--headful` when the user needs to see the browser or perform the initial login into a fresh profile.
- Do not point `--browser-profile` at the user's normal daily Chrome profile. Prefer a dedicated profile directory.

## 3. Start With The Smallest Command

- Default public-page capture: `obclip <url> --output "<dir>\\"`
- Logged-in or anti-bot page: add `--browser-executable`, `--browser-profile`, and usually `--headful`
- If the user wants Markdown on stdout, omit `--output`
- If the user wants the note opened in Obsidian, add `--open` and the optional vault/URI flags

Use the concrete command templates in [command-recipes.md](./references/command-recipes.md).

## 4. Escalate Waiting In Order

- First run without custom waits when the page is simple.
- If the page is incomplete but visibly loading dynamic content, add `--settle-ms 3000` or `--settle-ms 5000`.
- If the page is an SPA and the content mounts later, add `--wait-selector "<css>"`.
- Prefer broad, content-bearing selectors such as `article`, `main`, `[role="main"]`, or a stable post container. Avoid selectors that only match nav, login shells, or skeleton loaders.
- If the page still shows a login wall, fix browser state with `--browser-profile`; extra delay does not solve missing authentication.

Use [troubleshooting.md](./references/troubleshooting.md) when the first pass fails.

## 5. Interpret Results Correctly

- Successful file saves print `Saved note: <full-path>` to `stderr`.
- Failures print a direct reason such as save failure, invalid browser path, or wait timeout.
- Keep `stdout` clean unless the user explicitly wants the Markdown body in the terminal or piped into another command.

## 6. Windows Path Rules

- Quote Windows paths that may contain spaces.
- For `--output`, prefer an existing directory or a path ending in `\\` or `/` when you want directory semantics.
- Example: `--output "D:\\data\\Clippings\\"`

## References

- Installation and invocation: [install-and-invoke.md](./references/install-and-invoke.md)
- Command templates: [command-recipes.md](./references/command-recipes.md)
- Failure handling: [troubleshooting.md](./references/troubleshooting.md)
