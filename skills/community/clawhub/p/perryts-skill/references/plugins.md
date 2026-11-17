# Plugins & Auto-Update

## Plugins

Perry plugins are shared libraries (`.dylib`/`.so`/`.dll`) loaded at runtime.

### Plugin Structure

```typescript
// my-plugin/index.ts
import { PluginApi } from 'perry/plugin'

export default function(api: PluginApi) {
  // Register hooks
  api.registerHook('beforeCompile', (ctx) => {
    console.log('Compiling:', ctx.entryFile)
  })

  // Register tools
  api.registerTool({
    name: 'myTool',
    description: 'Does something useful',
    execute: (args) => {
      return { result: 'done' }
    }
  })

  // Register event listeners
  api.on('buildComplete', (output) => {
    console.log('Built:', output.path)
  })
}
```

### Hook Modes

| Mode | Behavior |
|------|----------|
| **filter** | Transform input → output. Chain multiple hooks. |
| **action** | Execute side effects. No return value. |
| **waterfall** | Sequential pipeline. Each hook receives previous result. |

### Native Extensions (FFI)

Plugins can call native code via FFI:

```typescript
// Load native library
const lib = perry.dlopen('./mylib.so')
const fn = lib.getFunction('my_native_fn', 'int', ['int'])
const result = fn(42)
```

### Plugin Discovery

Plugins are loaded from:
1. `node_modules/perry-plugin-*` (npm packages)
2. `plugins/` directory (local development)
3. Configured paths in `perry.toml`

### App Store Review

Plugins distributed via app stores must follow platform guidelines:
- iOS: No dynamic library loading (static linking only)
- Android: Native libraries must be in `jniLibs/`
- macOS: Signed and notarized

## Auto-Update

```typescript
import { checkForUpdate, installUpdate, initUpdater } from 'perry/updater'
```

### Basic Usage

```typescript
// Initialize updater with manifest URL
await initUpdater({
  manifestUrl: 'https://updates.example.com/manifest.json',
  publicKey: '...'  // Ed25519 public key for signature verification
})

// Check for updates
const update = await checkForUpdate()
if (update.available) {
  console.log(`Update available: ${update.version}`)
  await installUpdate()
}
```

### Manifest Schema (v2)

```json
{
  "version": "1.2.0",
  "build": 42,
  "channel": "stable",
  "platforms": {
    "macos": { "url": "https://cdn.example.com/app-1.2.0-macos.tar.gz", "hash": "sha256:..." },
    "windows": { "url": "https://cdn.example.com/app-1.2.0-windows.zip", "hash": "sha256:..." }
  },
  "signature": "ed25519:...",
  "notes": "Bug fixes and performance improvements"
}
```

### Security

- All manifests must be served over HTTPS
- Ed25519 signatures verify manifest integrity
- Asset hashes (SHA-256) verify download integrity
- Signature covers the entire manifest body

### Configuration (perry.toml)

```toml
[publish]
channel = "stable"
manifest_url = "https://updates.example.com/manifest.json"
signing_key = "@perry/updater/signing-key"  // keychain reference
```
