# Settings & Data Migration

## Settings UI (PluginSettingTab)

```typescript
import { PluginSettingTab, Setting } from 'obsidian'

interface MyPluginSettings {
  apiKey: string
  enableFeature: boolean
  mode: 'auto' | 'manual'
  fontSize: number
}

const DEFAULT_SETTINGS: MyPluginSettings = {
  apiKey: '',
  enableFeature: true,
  mode: 'auto',
  fontSize: 14
}

export class MySettingTab extends PluginSettingTab {
  plugin: MyPlugin

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin)
    this.plugin = plugin
  }

  display(): void {
    const { containerEl } = this
    containerEl.empty()

    new Setting(containerEl)
      .setName('API key')
      .setDesc('Your API key for authentication')
      .addText((text) =>
        text
          .setPlaceholder('Enter your API key')
          .setValue(this.plugin.settings.apiKey)
          .onChange(async (value) => {
            this.plugin.settings.apiKey = value
            await this.plugin.saveSettings()
          })
      )

    new Setting(containerEl)
      .setName('Enable feature')
      .setDesc('Toggle the main feature')
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.enableFeature)
          .onChange(async (value) => {
            this.plugin.settings.enableFeature = value
            await this.plugin.saveSettings()
          })
      )

    new Setting(containerEl)
      .setName('Mode')
      .setDesc('Select operation mode')
      .addDropdown((dropdown) =>
        dropdown
          .addOption('auto', 'Automatic')
          .addOption('manual', 'Manual')
          .setValue(this.plugin.settings.mode)
          .onChange(async (value: 'auto' | 'manual') => {
            this.plugin.settings.mode = value
            await this.plugin.saveSettings()
          })
      )

    new Setting(containerEl)
      .setName('Font size')
      .setDesc('Adjust the font size')
      .addSlider((slider) =>
        slider
          .setLimits(8, 32, 1)
          .setValue(this.plugin.settings.fontSize)
          .setDynamicTooltip()
          .onChange(async (value) => {
            this.plugin.settings.fontSize = value
            await this.plugin.saveSettings()
          })
      )

    // Use setHeading() for sections (NOT <h2>)
    new Setting(containerEl)
      .setName('Advanced')
      .setHeading()
  }
}
```

### Setting Headings

```typescript
// Correct: Use setHeading() on Setting
new Setting(containerEl)
  .setName('General')
  .setHeading()

// Wrong: Don't use HTML headings
// containerEl.createEl('h2', { text: 'General' })  // NO
```

### Settings with Buttons

```typescript
new Setting(containerEl)
  .setName('Reset data')
  .setDesc('Clear all stored data')
  .addButton((btn) =>
    btn
      .setButtonText('Reset')
      .setWarning()
      .onClick(async () => {
        this.plugin.settings = { ...DEFAULT_SETTINGS }
        await this.plugin.saveSettings()
        this.display()  // Re-render
      })
  )
```

## Data Persistence

```typescript
export default class MyPlugin extends Plugin {
  settings: MyPluginSettings

  async onload() {
    await this.loadSettings()
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData())
  }

  async saveSettings() {
    await this.saveData(this.settings)
  }
}
```

## Deep Merge Pattern

For nested settings objects, use deep merge instead of `Object.assign()`.

```typescript
function deepMerge(target: any, source: any): any {
  const result = { ...target }
  for (const key of Object.keys(source)) {
    if (
      source[key] &&
      typeof source[key] === 'object' &&
      !Array.isArray(source[key]) &&
      target[key] &&
      typeof target[key] === 'object' &&
      !Array.isArray(target[key])
    ) {
      result[key] = deepMerge(target[key], source[key])
    } else {
      result[key] = source[key] ?? target[key]
    }
  }
  return result
}

async loadSettings() {
  const saved = await this.loadData()
  this.settings = deepMerge(DEFAULT_SETTINGS, saved)
}
```

## Settings Migration Pipeline

When your plugin evolves and settings schema changes, use a migration pipeline.

### Version Tracking

```typescript
interface MyPluginSettings {
  _settingsVersion: number  // Track schema version
  // ... your settings
}

const DEFAULT_SETTINGS: MyPluginSettings = {
  _settingsVersion: 2,  // Current version
  // ... defaults
}
```

### Migration Architecture

**Critical order: Shape migration FIRST, deep merge SECOND.**

```typescript
async loadSettings() {
  const saved = await this.loadData() ?? {}

  // Step 1: Shape migration (before merge!)
  const migrated = this.migrateSettings(saved)

  // Step 2: Deep merge with defaults
  this.settings = deepMerge(DEFAULT_SETTINGS, migrated)
}

private migrateSettings(raw: any): any {
  let version = raw._settingsVersion ?? 0
  const data = { ...raw }

  // Migration v0 → v1: renamed field
  if (version < 1) {
    if (data.oldFieldName !== undefined) {
      data.newFieldName = data.oldFieldName
      delete data.oldFieldName
    }
    version = 1
  }

  // Migration v1 → v2: restructured nested object
  if (version < 2) {
    if (data.flatOption) {
      data.nested = { option: data.flatOption }
      delete data.flatOption
    }
    version = 2
  }

  data._settingsVersion = version
  return data
}
```

### Why Migration Before Merge

```
WRONG: merge → migrate
  saved = { oldFieldName: "value" }
  merged = { oldFieldName: "value", newFieldName: "" }  // default fills it
  migrate checks newFieldName → already exists → skip!
  DATA LOSS: oldFieldName ignored

CORRECT: migrate → merge
  saved = { oldFieldName: "value" }
  migrated = { newFieldName: "value" }  // renamed
  merged = { newFieldName: "value", ...defaults }  // clean
```

### Migration Rules

1. **Idempotent** — running twice produces same result
2. **One-directional** — old → new only, no rollback
3. **Additive** — only add fields, never remove (unless explicitly deleting)
4. **Pure function** — no side effects, no I/O, testable

### Detecting New Install vs Upgrade

```typescript
async onload() {
  const saved = await this.loadData()
  const isNewInstall = !saved || Object.keys(saved).length === 0

  if (!isNewInstall && (saved._settingsVersion ?? 0) < CURRENT_VERSION) {
    // Upgrading — run migration
    new Notice('Settings migrated to new format')
  }

  await this.loadSettings()
}
```

## External Settings Change

Handle when `data.json` is modified externally (e.g., sync):

```typescript
async onExternalSettingsChange() {
  await this.loadSettings()
  // Re-apply settings to UI if needed
  this.app.workspace.trigger('my-plugin:settings-changed')
}
```

## Best Practices

1. **Always provide defaults** — `Object.assign({}, DEFAULT, saved)`
2. **Version your schema** — `_settingsVersion` field
3. **Migrate before merge** — prevents default values from blocking migration
4. **Debounce save** — don't save on every keystroke
5. **Use `setHeading()`** not HTML headings in settings
6. **Sentence case** for all setting names
7. **Test migrations** — write unit tests for each version bump
