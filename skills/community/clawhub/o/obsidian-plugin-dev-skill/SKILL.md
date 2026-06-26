---
name: obsidian-plugin-dev
description: >
  Comprehensive skill for Obsidian plugin development with TypeScript.
  Covers plugin lifecycle, CodeMirror 6 editor extensions, React/Svelte integration,
  Vault API patterns, settings with migration pipelines, SecretStorage, CSS theming,
  CLI debugging workflow, testing, CI/CD, and community plugin submission.
  Trigger on: create obsidian plugin, obsidian plugin dev, obsidian API, obsidian editor extension,
  obsidian CM6, obsidian view, obsidian modal, obsidian settings, obsidian command,
  obsidian manifest, obsidian publish, obsidian submit plugin, obsidian plugin test,
  obsidian vite config, obsidian react, obsidian theme, obsidian CLI debug.
version: 1.0.0
---

# Obsidian Plugin Development

## When This Skill Applies

Use this skill when the user is:
- Creating a new Obsidian plugin from scratch
- Implementing plugin features (commands, views, modals, settings, editor extensions)
- Debugging plugin issues or unexpected behavior
- Configuring build tools (Vite, esbuild, rollup)
- Writing tests for Obsidian plugins
- Setting up CI/CD and release workflows
- Preparing a plugin for community submission
- Working with CodeMirror 6 editor extensions
- Integrating React/Svelte/Vue into Obsidian views

## Critical Rules (Always Follow)

| # | Rule | Why |
|---|------|-----|
| 1 | **Never use global `app`** — use `this.app` | Global `app` breaks in multi-window; submission rejected |
| 2 | **Never use `innerHTML`/`outerHTML`** — use `createEl()`, `createDiv()`, `setText()` | XSS vulnerability; instant rejection |
| 3 | **Use `registerEvent()`** for all event subscriptions | Auto-cleanup on unload; prevents memory leaks |
| 4 | **No default hotkeys** — let users configure | Hotkey conflicts with other plugins |
| 5 | **Use `requestUrl()` over `fetch()`** | Bypasses CORS; works on mobile |
| 6 | **Use `normalizePath()`** for user-provided paths | Handles cross-platform path differences |
| 7 | **Prefer `vault.process()`** over `vault.modify()` | Atomic operation; safe with concurrent edits |
| 8 | **Use `FileManager.processFrontMatter()`** for YAML | Never parse/serialize YAML manually |
| 9 | **Use Sentence case** for all UI text | Obsidian convention; submission requirement |
| 10 | **Use `setHeading()`** not `<h1>`/`<h2>` | Semantic; supports RTL; submission requirement |
| 11 | **Import only what you use** — no unused classes | Cleaner code; easier audits; submission reviewers check this |
| 12 | **Use `checkCallback` when command depends on context** | `callback` = always available; `checkCallback` = conditionally shown; `editorCallback` = needs editor |
| 13 | **Always provide `.theme-dark` / `.theme-light` CSS variants** | Obsidian CSS vars auto-adapt, but explicit theme blocks ensure edge cases render correctly; submission reviewers check this |
| 14 | **No regex lookbehind** — `(?!...)` OK, `(?<=...)` NOT OK | Breaks on iOS Safari < 16.4; submission rejected |
| 15 | **All interactive elements keyboard accessible** | Tab navigation + Enter/Space; submission requirement |
| 16 | **ARIA labels on all icon-only buttons** | Screen reader support; submission requirement |
| 17 | **Touch targets ≥ 44×44px** | Mobile usability; submission requirement |
| 18 | **Use `vault.configDir` not `.obsidian`** | Cross-platform compatibility; submission requirement |
| 19 | **Use `fileManager.trashFile()` not `vault.delete()`** | Respects user trash settings |
| 20 | **Use `AbstractInputSuggest` not `TextInputSuggest`** | Built-in API; Liam's copy-pasted implementation is banned |
| 21 | **Create `versions.json`** — maps plugin version → min Obsidian version | Submission bot checks for it; auto-reject if missing |
| 22 | **Version your settings schema** — `_settingsVersion` field | Enables migration pipeline on upgrade; prevents data loss |

## Quick Reference

### Plugin Lifecycle

```typescript
import { Plugin } from 'obsidian'

export default class MyPlugin extends Plugin {
  async onload() {
    // 1. Load settings FIRST
    await this.loadSettings()
    // 2. Add settings tab
    this.addSettingTab(new MySettingTab(this.app, this))
    // 3. Register commands
    this.addCommand({ id: 'my-command', name: 'My command', callback: () => {} })
    // 4. Register views
    this.registerView(MY_VIEW_TYPE, (leaf) => new MyView(leaf))
    // 5. Register editor extensions
    this.registerEditorExtension(myExtension)
    // 6. Register events
    this.registerEvent(this.app.vault.on('modify', (file) => {}))
    this.registerDomEvent(document, 'click', (evt) => {})
    this.registerInterval(window.setInterval(() => {}, 1000))
  }

  async onunload() {
    // Resources registered with register*() are auto-cleaned
    // Manual cleanup needed for: MutationObserver, React root, vault.on() in React
  }
}
```

### Essential API Cheatsheet

| Need | API |
|------|-----|
| Get active file | `this.app.workspace.getActiveFile()` |
| Read file | `this.app.vault.cachedRead(file)` |
| Modify file (background) | `this.app.vault.process(file, (data) => data)` |
| Modify file (editor) | `editor.replaceSelection()`, `editor.getRange()` |
| Create file | `this.app.vault.create(path, content)` |
| Delete file | `this.app.fileManager.trashFile(file)` |
| Rename file | `this.app.fileManager.renameFile(file, newPath)` |
| Read frontmatter | `this.app.metadataCache.getFileCache(file)?.frontmatter` |
| Write frontmatter | `this.app.fileManager.processFrontMatter(file, (fm) => {})` |
| Show notification | `new Notice('message', duration)` |
| Open modal | `new MyModal(this.app).open()` |
| Get active editor | `this.app.workspace.activeEditor?.editor` |
| Platform check | `Platform.isMacOS`, `Platform.isMobile`, `Platform.isDesktop` |
| Network request | `requestUrl({ url, method, headers, body })` |
| Persist data | `this.loadData()` / `this.saveData(data)` |
| Secure storage | `this.app.secretStorage.setSecret(id, value)` (v1.11.4+) |
| Detect theme | `document.body.classList.contains('theme-dark')` |

### Command Callback Decision Tree

```
Does the command need an active editor?
├─ YES → editorCallback
│        (automatically hidden when no editor; gives you editor + view)
│
└─ NO → Does it need any context to run? (active file, leaf, etc.)
         ├─ YES → checkCallback
         │        (return true when available; run action on !checking)
         │
         └─ NO → callback
                  (always visible, always runs)
```

**Examples:**

```typescript
// Always available — no conditions
this.addCommand({
  id: 'open-settings',
  name: 'Open plugin settings',
  callback: () => { this.openSettings() }
})

// Needs active file — use checkCallback
this.addCommand({
  id: 'copy-stats',
  name: 'Copy note statistics',
  checkCallback: (checking) => {
    const file = this.app.workspace.getActiveFile()
    if (file) {
      if (!checking) this.copyStats(file)
      return true
    }
    return false
  }
})

// Needs editor — use editorCallback
this.addCommand({
  id: 'wrap-callout',
  name: 'Wrap selection in callout',
  editorCallback: (editor) => {
    const sel = editor.getSelection()
    editor.replaceSelection(`> [!note]\n> ${sel}`)
  }
})
```

### Import Hygiene

Only import what you actually use. Submission reviewers flag unused imports.

```typescript
// Good — only what's needed
import { MarkdownView, Notice, Plugin, PluginSettingTab, Setting } from 'obsidian'

// Bad — unused imports
import { App, Editor, Modal, Notice, Plugin, PluginSettingTab, Setting } from 'obsidian'
//      ^^^ ^^^^^^ ^^^^^ — never used
```

## Common Pitfalls

1. **Storing view references** → use `getLeavesOfType()` on demand
2. **Passing plugin as Component** → use `this.addChild()` instead
3. **Detaching leaves in onunload** → they reinitialize on update
4. **Not removing sample code** → `MyPlugin`, `SampleSettingTab` must be renamed
5. **Using `vault.modify()` on active file** → use Editor API instead
6. **Manual YAML parsing** → use `processFrontMatter()` instead
7. **`fetch()` for API calls** → use `requestUrl()` instead
8. **Hardcoded colors in CSS** → use `var(--text-normal)`, etc.
9. **`navigator.platform`** → use `Platform.isMacOS` instead
10. **`var` declarations** → use `const`/`let` instead
11. **Promise chains** → use `async/await` instead
12. **`console.log` in production** → remove or use `console.debug` with conditional
13. **Regex lookbehind `(?<=...)`** → breaks on iOS Safari < 16.4; use alternative patterns
14. **`Object.assign(defaults, saved)`** → mutates defaults; use `Object.assign({}, defaults, saved)`
15. **Hardcoded `.obsidian` path** → use `this.app.vault.configDir` instead
16. **Shallow merge for nested settings** → use deep merge; shallow merge loses nested defaults
17. **`vault.delete()` for removing files** → use `fileManager.trashFile()` to respect user settings
18. **Liam's `TextInputSuggest`** → use built-in `AbstractInputSuggest` instead
19. **Missing `styles.css`** → create empty file if no styles (submission bot checks for it)
20. **Missing `versions.json`** → create with `{ "1.0.0": "1.0.0" }` (submission bot checks for it)
21. **No settings version tracking** → add `_settingsVersion` to settings interface for migration support

## Detailed References

| Topic | File | When to Load |
|-------|------|--------------|
| Lifecycle & Core API | `reference/lifecycle.md` | Always; building any plugin feature |
| ESLint Rules (28 rules) | `reference/eslint-rules.md` | ESLint setup, pre-submission audit, rule reference |
| Accessibility (MANDATORY) | `reference/accessibility.md` | Keyboard nav, ARIA labels, focus indicators, touch targets |
| CodeMirror 6 Editor Extensions | `reference/editor-extensions.md` | Editor decorations, syntax highlighting, live preview |
| React / Svelte / Vue Integration | `reference/frameworks.md` | Using React/Vue/Svelte in views or settings |
| Vault & File Operations | `reference/vault-operations.md` | File CRUD, frontmatter, events, caching |
| Settings & Data Migration | `reference/settings-migration.md` | Settings UI, load/save, deep merge, migration pipelines |
| Security & SecretStorage | `reference/security.md` | API keys, credentials, XSS prevention, network requests |
| CSS Styling | `reference/css-accessibility.md` | Theming, CSS variables, scoping, mobile styles |
| Dev Workflow & CLI | `reference/dev-workflow.md` | Build, hot-reload, CLI debugging, Obsidian CLI, ESLint config |
| Testing | `reference/testing.md` | Unit tests, mocking Obsidian API, Jest/Vitest |
| CI/CD & Release | `reference/cicd-release.md` | GitHub Actions, version bump, community submission |

## Development Workflow

### Quick Dev Loop (with Obsidian CLI)

```bash
# Build and hot-reload
npm run build && obsidian plugin:reload id=<plugin-id>

# Check for errors
obsidian dev:errors

# Inspect DOM
obsidian dev:dom selector=".my-plugin-view"

# Take screenshot
obsidian dev:screenshot

# Evaluate JS in Obsidian context
obsidian eval code="app.plugins.plugins"
```

### Without Obsidian CLI

```bash
# Build and copy to test vault
npm run build && cp main.js manifest.json styles.css /path/to/TestVault/.obsidian/plugins/<plugin-id>/
# Then reload in Obsidian: Ctrl+P → "Reload app without saving"
```

## Pre-Submission Checklist

Before creating a release or submitting to community plugins, verify:

### Submission Validation (Bot checks — will auto-reject if incorrect)

- [ ] `id` in manifest.json does not contain "obsidian"; doesn't end with "plugin"; lowercase only
- [ ] `name` does not contain "Obsidian"; doesn't end with "Plugin"; doesn't start with "Obsi" or end with "dian"
- [ ] `description` does not contain "Obsidian" or "This plugin"; must end with `.?!)` punctuation; max 250 chars
- [ ] `manifest.json` `id`, `name`, `description` match submission entry in `community-plugins.json`
- [ ] `LICENSE` file present; copyright holder ≠ "Dynalist Inc."; year is current
- [ ] `styles.css` exists (empty if no styles)
- [ ] `versions.json` exists with correct version mapping
- [ ] GitHub release has `main.js`, `manifest.json`, `styles.css` attached

### Code Quality

- [ ] All sample/template code removed (`MyPlugin`, `SampleSettingTab`, `SampleModal`)
- [ ] No `innerHTML`/`outerHTML` anywhere in code
- [ ] No default hotkeys set
- [ ] No `console.log` in production (remove or use conditional `console.debug`)
- [ ] No unused imports
- [ ] `setHeading()` used instead of `<h2>` in settings
- [ ] Sentence case for all UI text (run ESLint to verify)
- [ ] `this.app` used everywhere (not global `app`)
- [ ] All resources cleaned up in `onunload()`
- [ ] No `Object.assign(defaults, saved)` — use `Object.assign({}, defaults, saved)`
- [ ] Use `fileManager.trashFile()` not `vault.delete()`
- [ ] No regex lookbehind (`(?<=...)`) — breaks on iOS
- [ ] Use `vault.configDir` not hardcoded `.obsidian`

### Accessibility (MANDATORY)

- [ ] All interactive elements keyboard accessible (Tab, Enter, Space)
- [ ] ARIA labels on all icon-only buttons
- [ ] `:focus-visible` styled with Obsidian CSS variables
- [ ] Touch targets ≥ 44×44px
- [ ] Can use entire plugin without a mouse

### ESLint & Release

- [ ] ESLint passes with `eslint-plugin-obsidianmd` (`npx eslint .`)
- [ ] `manifest.json` version correct, `minAppVersion` set
- [ ] `isDesktopOnly: true` only if using Node/Electron APIs

## Reference Source Tracking

| Reference File | Primary Sources | Last Verified |
|----------------|----------------|---------------|
| `lifecycle.md` | obsidian API docs, gapmiss/obsidian-plugin-skill | 2026-03 |
| `eslint-rules.md` | obsidianmd/eslint-plugin v0.1.9, gapmiss/obsidian-plugin-skill | 2026-03 |
| `accessibility.md` | gapmiss/obsidian-plugin-skill, obsidian plugin guidelines | 2026-03 |
| `editor-extensions.md` | CM6 docs, @codemirror/view source | 2026-03 |
| `frameworks.md` | Leonezz/obsidian-plugin-dev-skill, React docs | 2026-03 |
| `vault-operations.md` | obsidian API docs, official plugin guidelines | 2026-03 |
| `settings-migration.md` | Leonezz/obsidian-plugin-dev-skill | 2026-03 |
| `security.md` | gapmiss/obsidian-plugin-skill, obsidian developer policies | 2026-03 |
| `css-accessibility.md` | davidvkimball/obsidian-dev-skills, obsidian sample theme | 2026-03 |
| `dev-workflow.md` | adriangrantdotorg/Obsidian-Skills, obsidian CLI docs | 2026-03 |
| `testing.md` | Leonezz/obsidian-plugin-dev-skill | 2026-03 |
| `cicd-release.md` | Leonezz/obsidian-plugin-dev-skill, obsidian submission docs | 2026-03 |

To update references: check each source for new content, cross-reference with obsidian developer docs changelog.

## Design Decisions

1. **SKILL.md stays under 500 lines** — quick reference + links to detailed docs
2. **Reference files are topic-based** — load only what you need
3. **Code examples are real** — from actual plugin patterns, not toy demos
4. **Do/Don't tables** — clear before/after comparisons
