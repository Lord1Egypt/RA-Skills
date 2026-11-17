---
name: perryts
description: >
  Perry TypeScript-to-native compiler skill. Use when working with the Perry compiler, Perry projects, or TypeScript code that compiles to native executables.
  Covers: compile/run/dev commands, cross-compilation targets (macOS/iOS/Android/HarmonyOS/Windows/Linux/Web),
  perry.toml configuration, Standard Library (npm packages compiled natively), Multi-Threading (parallelMap/spawn),
  Native UI widgets (VStack/HStack/State), System APIs, Widgets (home screen), Internationalization, Auto-Update, Plugins, and CLI reference.
  Triggers on: "perry compile", "perry run", perry.toml, perry/ui, perry/system, perry/thread, perry/i18n, perry/media,
  perry/updater, perry/tui, native UI, cross-compilation, HarmonyOS target, ArkUI codegen.
---

# Perry TypeScript-to-Native Compiler

Perry compiles TypeScript directly to native executables via HIR → LLVM codegen. No VM, no runtime interpreter.

## Quick Start

```bash
perry init my-app && cd my-app
perry run src/main.ts                     # Compile + run
perry compile src/main.ts -o app          # Build native binary
perry dev src/main.ts                     # Watch mode
```

## Cross-Compilation

```bash
perry compile src/main.ts --target ios-simulator -o app
perry compile src/main.ts --target android -o app.apk
perry compile src/main.ts --target harmonyos
perry compile src/main.ts --target web -o dist/
```

## Key Imports

```typescript
import { VStack, HStack, Text, Button, state } from "perry/ui"
import { parallelMap, spawn } from "perry/thread"
import { openURL, isDarkMode, keychainSave } from "perry/system"
import { i18n } from "perry/i18n"
import { createPlayer, play, setNowPlaying } from "perry/media"
import { Box, Text, render } from "perry/tui"
import { checkForUpdate, installUpdate } from "perry/updater"
```

## Reference Documentation

Load these as needed for detailed API docs, configuration, and examples:

- **[CLI & Configuration](references/cli-reference.md)** — All 11 CLI commands, compilation targets, global flags, perry.toml sections, environment variables, CI/CD integration
- **[Standard Library](references/stdlib.md)** — HTTP (fastify/fetch/axios/ws), Database (sqlite/mysql2/pg/mongodb/redis), Crypto (bcrypt/argon2/jwt/ethers), File System, Utilities (lodash/dayjs/uuid/commander), Media (sharp/cheerio/zlib/cron), binary size table
- **[Multi-Threading](references/threading.md)** — parallelMap, parallelFilter, spawn, capture rules, safety model, architecture
- **[Native UI](references/ui.md)** — Layout widgets, 14+ widget types, inline StyleProps, State & reactivity, events, Canvas, Menus & Dialogs, multi-window, Table, Animation, Geisterhand testing API, platform support matrix
- **[Platforms](references/platforms.md)** — All 10 targets (macOS/iOS/visionOS/tvOS/watchOS/Android/HarmonyOS/Windows/Linux/Web), per-platform build commands and architecture
- **[Internationalization](references/i18n.md)** — i18n.t(), CLDR plural rules, format wrappers (Currency/Percent/ShortDate), perry.toml [i18n] config, compile-time validation
- **[System APIs](references/system.md)** — openURL, isDarkMode, preferences, keychain, notifications (local + push), audio capture, media playback, clipboard, environment variables
- **[Widgets (Home Screen)](references/widgets.md)** — Widget() declaration, entryFields, family-specific rendering, timeline provider, platform notes
- **[Plugins & Auto-Update](references/plugins.md)** — PluginApi, hook modes (filter/action/waterfall), FFI, plugin discovery, manifest schema v2, Ed25519 signing

## Common Patterns

### Native App

```typescript
import { App, VStack, Text, Button, state } from "perry/ui"

const count = state(0)

App({
  body: VStack([
    count.text(),
    Button("+", () => count.set(count.get() + 1))
  ])
})
```

### HTTP Server

```typescript
import Fastify from "fastify"

const server = Fastify()
server.get("/", async () => ({ hello: "perry" }))
server.listen({ port: 3000 })
```

### Parallel Processing

```typescript
import { parallelMap } from "perry/thread"

const results = parallelMap([1, 2, 3, 4], (n) => n * 2)
// [2, 4, 6, 8]
```
