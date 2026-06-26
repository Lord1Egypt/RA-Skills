# Testing

## Why Test Obsidian Plugins?

- Catch regressions before community submission
- Verify settings migration logic
- Test utility functions without running Obsidian
- CI/CD integration for automated checks

## What to Test

| Type | Priority | Approach |
|------|----------|----------|
| **Pure functions** | High | Unit test with Jest/Vitest |
| **Settings migration** | High | Unit test each version path |
| **Markdown parsing** | High | Unit test with sample strings |
| **DOM interactions** | Medium | Integration test with mocked Obsidian |
| **Full plugin lifecycle** | Low | Manual testing or E2E with Obsidian CLI |

## Setting Up Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    setupFiles: ['./tests/setup.ts'],
  },
})
```

## Mocking Obsidian API

Create a mock module that replaces `obsidian` imports in tests.

```typescript
// tests/mocks/obsidian.ts
import { vi } from 'vitest'

// Mock Notice
export class Notice {
  message: string
  constructor(message: string, timeout?: number) {
    this.message = message
  }
}

// Mock Plugin
export class Plugin {
  app: any
  manifest: any
  loadData = vi.fn()
  saveData = vi.fn()
  addCommand = vi.fn()
  addSettingTab = vi.fn()
  addRibbonIcon = vi.fn()
  registerEvent = vi.fn()
  registerDomEvent = vi.fn()
  registerInterval = vi.fn()
  registerView = vi.fn()
  registerEditorExtension = vi.fn()
}

// Mock App
export function createMockApp() {
  return {
    vault: {
      read: vi.fn(),
      create: vi.fn(),
      modify: vi.fn(),
      delete: vi.fn(),
      getMarkdownFiles: vi.fn(() => []),
      getFileByPath: vi.fn(),
      on: vi.fn(),
      off: vi.fn(),
      offref: vi.fn(),
      process: vi.fn(),
      cachedRead: vi.fn(),
    },
    workspace: {
      getActiveFile: vi.fn(),
      getActiveViewOfType: vi.fn(),
      getLeavesOfType: vi.fn(() => []),
      on: vi.fn(),
      trigger: vi.fn(),
    },
    metadataCache: {
      getFileCache: vi.fn(),
      getBacklinksForFile: vi.fn(),
    },
    fileManager: {
      processFrontMatter: vi.fn(),
      trashFile: vi.fn(),
      renameFile: vi.fn(),
    },
    secretStorage: {
      getSecret: vi.fn(),
      setSecret: vi.fn(),
      listSecrets: vi.fn(),
      deleteSecret: vi.fn(),
    },
  }
}

// Mock TFile
export class TFile {
  path: string
  name: string
  basename: string
  extension: string

  constructor(path: string = 'test.md') {
    this.path = path
    this.name = path.split('/').pop() ?? ''
    this.basename = this.name.replace(/\.[^.]+$/, '')
    this.extension = this.name.split('.').pop() ?? ''
  }
}

// Mock Modal
export class Modal {
  app: any
  open = vi.fn()
  close = vi.fn()
  onOpen = vi.fn()
  onClose = vi.fn()
  constructor(app: any) { this.app = app }
}

// Mock Setting
export class Setting {
  setName = vi.fn().mockReturnThis()
  setDesc = vi.fn().mockReturnThis()
  addText = vi.fn().mockReturnThis()
  addToggle = vi.fn().mockReturnThis()
  addDropdown = vi.fn().mockReturnThis()
  addSlider = vi.fn().mockReturnThis()
  addButton = vi.fn().mockReturnThis()
  setHeading = vi.fn().mockReturnThis()
  constructor(public containerEl?: HTMLElement) {}
}

// Mock debounce
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  ms: number,
  callFirst?: boolean
): T & { cancel: () => void } {
  const debounced = fn as T & { cancel: () => void }
  debounced.cancel = vi.fn()
  return debounced
}

// Mock normalizePath
export function normalizePath(path: string): string {
  return path.replace(/\\/g, '/').replace(/\/+/g, '/')
}

// Mock requestUrl
export const requestUrl = vi.fn()
```

### Vitest Config with Module Mock

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import { resolve } from 'path'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
  },
  resolve: {
    alias: {
      'obsidian': resolve(__dirname, 'tests/mocks/obsidian.ts'),
    },
  },
})
```

## Writing Tests

### Test Pure Functions

```typescript
// tests/unit/parse-wikilink.test.ts
import { describe, it, expect } from 'vitest'

function parseWikilink(text: string): { target: string; alias?: string } | null {
  const match = text.match(/^\[\[([^\]|]+)(?:\|([^\]]+))?\]\]$/)
  if (!match) return null
  return { target: match[1], alias: match[2] }
}

describe('parseWikilink', () => {
  it('parses simple link', () => {
    expect(parseWikilink('[[Note Name]]')).toEqual({
      target: 'Note Name',
    })
  })

  it('parses link with alias', () => {
    expect(parseWikilink('[[Note Name|Display]]')).toEqual({
      target: 'Note Name',
      alias: 'Display',
    })
  })

  it('returns null for non-wikilink', () => {
    expect(parseWikilink('[Not a wikilink]')).toBeNull()
  })
})
```

### Test Settings Migration

```typescript
// tests/unit/migration.test.ts
import { describe, it, expect } from 'vitest'

function migrateSettings(raw: any): any {
  let version = raw._settingsVersion ?? 0
  const data = { ...raw }

  if (version < 1) {
    if (data.oldFieldName !== undefined) {
      data.newFieldName = data.oldFieldName
      delete data.oldFieldName
    }
    version = 1
  }

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

describe('migrateSettings', () => {
  it('migrates v0 to v1 (field rename)', () => {
    const result = migrateSettings({ oldFieldName: 'value', _settingsVersion: 0 })
    expect(result.newFieldName).toBe('value')
    expect(result.oldFieldName).toBeUndefined()
    expect(result._settingsVersion).toBe(2)
  })

  it('migrates v1 to v2 (nested restructure)', () => {
    const result = migrateSettings({ flatOption: true, _settingsVersion: 1 })
    expect(result.nested).toEqual({ option: true })
    expect(result.flatOption).toBeUndefined()
    expect(result._settingsVersion).toBe(2)
  })

  it('is idempotent', () => {
    const first = migrateSettings({ oldFieldName: 'test', _settingsVersion: 0 })
    const second = migrateSettings(first)
    expect(first).toEqual(second)
  })

  it('handles fresh install (no migration needed)', () => {
    const result = migrateSettings({ _settingsVersion: 2 })
    expect(result._settingsVersion).toBe(2)
  })
})
```

### Test with Mocked Obsidian API

```typescript
// tests/unit/plugin.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createMockApp, TFile } from '../mocks/obsidian'

describe('Plugin feature', () => {
  let app: ReturnType<typeof createMockApp>

  beforeEach(() => {
    app = createMockApp()
    vi.clearAllMocks()
  })

  it('reads file content', async () => {
    const file = new TFile('test.md')
    app.vault.cachedRead.mockResolvedValue('# Hello')

    const content = await app.vault.cachedRead(file)
    expect(content).toBe('# Hello')
  })

  it('processes frontmatter', async () => {
    const file = new TFile('test.md')
    app.fileManager.processFrontMatter.mockImplementation(
      async (f: any, fn: Function) => {
        const fm = { title: 'Old' }
        fn(fm)
        return fm
      }
    )

    await app.fileManager.processFrontMatter(file, (fm: any) => {
      fm.title = 'New'
    })

    expect(app.fileManager.processFrontMatter).toHaveBeenCalled()
  })
})
```

## Test Structure

```
tests/
├── setup.ts                    # Global test setup
├── mocks/
│   └── obsidian.ts             # Mock Obsidian API
├── unit/
│   ├── parse-wikilink.test.ts  # Pure function tests
│   ├── migration.test.ts       # Settings migration tests
│   └── plugin.test.ts          # Plugin logic tests
└── fixtures/
    └── sample-vault/           # Test data
```

## Best Practices

1. **Test pure functions first** — highest ROI, easiest to test
2. **Always test migration paths** — each version upgrade
3. **Mock at module level** — alias `obsidian` in vitest config
4. **Use `vi.clearAllMocks()`** in `beforeEach`
5. **Test edge cases** — empty strings, null, undefined, missing fields
6. **Don't test Obsidian internals** — test your logic, mock theirs
