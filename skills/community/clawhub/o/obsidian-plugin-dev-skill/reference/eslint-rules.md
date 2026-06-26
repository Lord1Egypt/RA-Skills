# ESLint Rules — eslint-plugin-obsidianmd v0.1.9

## Setup (Flat Config — ESLint v9+)

```typescript
// eslint.config.mjs
import tsparser from "@typescript-eslint/parser";
import { defineConfig } from "eslint/config";
import obsidianmd from "eslint-plugin-obsidianmd";

export default defineConfig([
  ...obsidianmd.configs.recommended,
  {
    files: ["**/*.ts"],
    languageOptions: {
      parser: tsparser,
      parserOptions: { project: "./tsconfig.json" },
    },
    rules: {
      // Override or add rules as needed
      "obsidianmd/sample-names": "off",
      "obsidianmd/prefer-file-manager-trash": "error",
    },
  },
]);
```

**Configurations:**
- `recommended` — all recommended rules enabled
- `recommendedWithLocalesEn` — extends to `en*.json`, `en*.ts`, `en*.js` locale files

## Auto-fix

Many rules are auto-fixable:

```bash
npx eslint --fix .
```

## All 28 Rules

### Commands (5 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `commands/no-command-in-command-id` | error | ❌ | Disallow "command" in command IDs |
| `commands/no-command-in-command-name` | error | ❌ | Disallow "command" in command names |
| `commands/no-default-hotkeys` | error | ❌ | No default hotkeys — let users configure |
| `commands/no-plugin-id-in-command-id` | error | ❌ | Don't include plugin ID in command IDs |
| `commands/no-plugin-name-in-command-name` | error | ❌ | Don't include plugin name in command names |

```typescript
// ❌ Bad
this.addCommand({ id: 'my-plugin-show-command', name: 'Show Command', ... })
// ✅ Good
this.addCommand({ id: 'show', name: 'Show todo', ... })
```

### Settings Tab (2 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `settings-tab/no-manual-html-headings` | error | ✅ | Use `.setHeading()` instead of `<h2>` |
| `settings-tab/no-problematic-settings-headings` | warn | ✅ | Avoid "General", "settings", or plugin name in headings |

```typescript
// ❌ Bad
containerEl.createEl('h2', { text: 'General' })
// ✅ Good
new Setting(containerEl).setName('General').setHeading()
```

### UI (3 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `ui/sentence-case` | warn | ✅ | Enforce sentence case for UI strings |
| `ui/sentence-case-json` | warn | ✅ | Sentence case in English JSON locale files |
| `ui/sentence-case-locale-module` | warn | ✅ | Sentence case in English TS/JS locale modules |

```typescript
// ❌ Bad — Title Case
.setName('Advanced Settings')
// ✅ Good — Sentence case
.setName('Advanced settings')
```

**Options:**
```typescript
"obsidianmd/ui/sentence-case": ["warn", {
  brands: ["Obsidian", "GitHub"],
  acronyms: ["API", "URL", "HTML"],
  enforceCamelCaseLower: true,  // flags "autoReveal" as incorrect
}]
```

### Lifecycle & Memory (5 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `detach-leaves` | error | ✅ | Don't detach leaves in `onunload()` |
| `no-plugin-as-component` | error | ❌ | Don't pass plugin as Component to MarkdownRenderer |
| `no-view-references-in-plugin` | error | ❌ | Don't store view references in plugin properties |
| `no-sample-code` | error | ✅ | Remove all sample/template code |
| `sample-names` | error | ✅ | Rename `MyPlugin`, `SampleSettingTab`, etc. |

```typescript
// ❌ Bad
class MyPlugin extends Plugin {
  view: MyView;  // stored reference = memory leak
  onunload() {
    this.app.workspace.detachLeavesOfType(VIEW_TYPE);  // don't do this
  }
}
// ✅ Good
class TodoPlugin extends Plugin {
  onunload() {
    // Let Obsidian handle cleanup
  }
}
```

### Type Safety (2 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `no-tfile-tfolder-cast` | error | ❌ | Use `instanceof` instead of type casting |
| `no-static-styles-assignment` | warn | ❌ | Use CSS classes instead of inline styles |

```typescript
// ❌ Bad
const file = abstractFile as TFile
el.style.color = 'red'
// ✅ Good
if (abstractFile instanceof TFile) { ... }
el.addClass('my-plugin-highlight')
```

### API Best Practices (4 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `platform` | error | ❌ | Use `Platform` API, not `navigator` |
| `regex-lookbehind` | error | ❌ | Avoid regex lookbehind (iOS < 16.4 incompatible) |
| `vault/iterate` | warn | ✅ | Don't iterate all files to find by path |
| `hardcoded-config-path` | error | ❌ | Don't hardcode `.obsidian` — use `vault.configDir` |

```typescript
// ❌ Bad
navigator.platform  // → Platform.isMacOS
/(?<=#).+/         // → breaks on iOS
vault.getFiles().find(f => f.path === path)  // → vault.getFileByPath(path)
'.obsidian/plugins' // → `${vault.configDir}/plugins`
```

### Security & DOM (5 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `no-forbidden-elements` | error | ❌ | Don't create `<link>` or `<style>` elements |
| `object-assign` | warn | ❌ | Don't mutate defaults with `Object.assign(defaults, ...)` |
| `validate-license` | error | ❌ | LICENSE copyright holder ≠ "Dynalist Inc."; year must be current |
| `validate-manifest` | error | ❌ | manifest.json structure must be valid |
| `prefer-file-manager-trash-file` | error | ❌ | Use `FileManager.trashFile()`, not `Vault.trash()` or `Vault.delete()` |

```typescript
// ❌ Bad
Object.assign(DEFAULT_SETTINGS, saved)  // mutates defaults!
await vault.delete(file)
// ✅ Good
Object.assign({}, DEFAULT_SETTINGS, saved)
await fileManager.trashFile(file)
```

### Other (2 rules)

| Rule | Severity | Fixable | Description |
|------|----------|---------|-------------|
| `prefer-abstract-input-suggest` | error | ❌ | Use `AbstractInputSuggest`, not Liam's `TextInputSuggest` |
| `rule-custom-message` | — | ❌ | Allows redefining error messages from other rules |

## Pre-Submission ESLint Audit

```bash
# Run full check
npx eslint .

# Run with auto-fix
npx eslint --fix .

# Check specific rule
npx eslint --rule '{"obsidianmd/ui/sentence-case": "error"}' .
```

All errors must be resolved before submission. Warnings are informational but recommended to fix.
