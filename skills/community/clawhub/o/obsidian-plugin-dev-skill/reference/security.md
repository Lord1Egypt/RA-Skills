# Security & SecretStorage

## XSS Prevention

### Never Use These

```typescript
// ❌ NEVER
el.innerHTML = userInput
el.outerHTML = html
el.insertAdjacentHTML('beforeend', html)
document.write(html)
```

### Always Use These

```typescript
// ✅ Safe DOM API
el.createEl('div', { text: 'Hello' })
el.createEl('span', { cls: 'my-class', text: userContent })
el.createEl('a', { href: 'https://example.com', text: 'Link' })
el.createDiv({ cls: 'container' })
el.createSpan({ text: 'safe text' })

// ✅ Clear element
el.empty()

// ✅ Set text safely
el.setText(userInput)
```

### Escaping User Input

```typescript
// createEl with text: automatically escaped
el.createEl('span', { text: userInput })

// If you must use DOM manipulation:
function escapeHtml(str: string): string {
  const div = document.createElement('div')
  div.textContent = str
  return div.innerHTML
}
```

## SecretStorage (Obsidian >= 1.11.4)

### Feature Detection

```typescript
const hasSecretStorage = typeof this.app.secretStorage?.getSecret === 'function'
```

### Basic API

```typescript
// Store a secret
await this.app.secretStorage.setSecret('my-plugin-openai-key', apiKey)

// Read a secret
const apiKey = await this.app.secretStorage.getSecret('my-plugin-openai-key')

// List all secrets
const keys = await this.app.secretStorage.listSecrets()

// Delete a secret
await this.app.secretStorage.deleteSecret('my-plugin-openai-key')
```

### Secret ID Convention

```
{plugin-id}-{category}-{provider}-apikey
```

Examples:
- `noclaw-openai-apikey`
- `noclaw-anthropic-apikey`
- `noclaw-github-token`

### Extract/Resolve Pattern

Save API key: extract from settings → store in SecretStorage → clear from settings.

```typescript
// When saving settings
async saveSettings() {
  // Extract sensitive fields
  if (this.settings.apiKey) {
    if (hasSecretStorage) {
      await this.app.secretStorage.setSecret(
        `${this.manifest.id}-apikey`,
        this.settings.apiKey
      )
      this.settings.apiKey = ''  // Clear from plain text
    }
  }
  await this.saveData(this.settings)
}
```

Load API key: read from SecretStorage → inject into settings.

```typescript
// When loading settings
async loadSettings() {
  this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData())

  if (hasSecretStorage) {
    const key = await this.app.secretStorage.getSecret(`${this.manifest.id}-apikey`)
    if (key) {
      this.settings.apiKey = key
    }
  }
}
```

### One-Time Migration (Plaintext → SecretStorage)

```typescript
async migrateToSecretStorage() {
  if (!hasSecretStorage) return

  const saved = await this.loadData()
  if (saved?.apiKey && saved._settingsVersion < 2) {
    await this.app.secretStorage.setSecret(
      `${this.manifest.id}-apikey`,
      saved.apiKey
    )
    saved.apiKey = ''
    saved._settingsVersion = 2
    await this.saveData(saved)
  }
}
```

### Fallback for Older Obsidian

```typescript
// Graceful degradation
const storeSecret = async (id: string, value: string) => {
  if (typeof this.app.secretStorage?.setSecret === 'function') {
    await this.app.secretStorage.setSecret(id, value)
  } else {
    // Fallback: store encrypted in settings (less secure)
    this.settings._legacy_secrets = this.settings._legacy_secrets ?? {}
    this.settings._legacy_secrets[id] = btoa(value)
    await this.saveData(this.settings)
  }
}
```

### Testing SecretStorage

```typescript
// Mock for tests
class MockSecretStorage {
  private store = new Map<string, string>()

  async setSecret(id: string, value: string) {
    this.store.set(id, value)
  }

  async getSecret(id: string) {
    return this.store.get(id) ?? null
  }

  async listSecrets() {
    return Array.from(this.store.keys())
  }

  async deleteSecret(id: string) {
    this.store.delete(id)
  }
}
```

## Other Security Rules

| Rule | Correct | Wrong |
|------|---------|-------|
| Global app | `this.app` | `app` |
| User text | `createEl('span', { text })` | `innerHTML` |
| URLs | `createEl('a', { href: url })` | String concatenation |
| Paths | `normalizePath(userInput)` | Direct use |
| Network | `requestUrl()` | `fetch()` |
| Platform | `Platform.isMacOS` | `navigator.platform` |
| Regex lookbehind | Avoid | `(?<=...)` — breaks on iOS Safari |

## Network Requests

```typescript
import { requestUrl } from 'obsidian'

// GET
const response = await requestUrl({
  url: 'https://api.example.com/data',
  method: 'GET',
  headers: { 'Authorization': `Bearer ${apiKey}` }
})

// POST
const response = await requestUrl({
  url: 'https://api.example.com/data',
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' }),
  contentType: 'application/json'
})

// Response
const data = response.json  // Parsed JSON
const text = response.text   // Raw text
const status = response.status
```

### Why `requestUrl()` Over `fetch()`

1. Bypasses CORS restrictions
2. Works on mobile (Obsidian mobile uses a different runtime)
3. Consistent behavior across platforms
4. Handles cookies and redirects properly

## Best Practices

1. **Never store API keys in plain text** — use SecretStorage or at minimum base64 encode
2. **Never use `innerHTML`** — even if you control the content
3. **Always use `this.app`** — not global `app`
4. **Use `requestUrl()`** — not `fetch()`
5. **Normalize paths** — `normalizePath(userInput)`
6. **No regex lookbehind** — `(?!...)` is OK, `(?<=...)` breaks on iOS
7. **Feature detect** — check API existence before using newer features
