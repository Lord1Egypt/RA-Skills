---
name: harmonyos
description: Assist with HarmonyOS and OpenHarmony application development in ArkTS and ArkUI. Use when Codex needs to inspect, build, debug, refactor, review, or generate HarmonyOS projects, especially DevEco Studio or Stage model apps that use UIAbility, app.json5, module.json5, oh-package.json5, ohpm, hvigorw, hdc, permissions, routing, state management, HAP or HAR packaging, and signing.
---

# HarmonyOS Developer Skills

## Core Rules

- Use `.equals()` for string comparison, not `==`
- HarmonyOS uses ArkTS/TypeScript
- UI built with ArkUI framework
- App signing requires certificate configuration

---

## Development Environment

- **IDE**: DevEco Studio
- **Language**: ArkTS (TypeScript superset)
- **SDK**: HarmonyOS SDK
- **API**: HarmonyOS Next API

---

## ArkUI Basics

### Components

```typescript
// Basic component
@Entry
@Component
struct Index {
  @State message: string = 'Hello World'

  build() {
    Column() {
      Text(this.message)
        .fontSize(50)
        .fontWeight(FontWeight.Bold)
    }
    .alignItems(HorizontalAlign.Center)
    .width('100%')
    .height('100%')
  }
}
```

### State Management

```typescript
// @State - Component internal state
@State count: number = 0

// @Prop - Parent component prop
@Prop message: string

// @Link - Two-way binding
@Link childCount: number

// @Observed + @ObjectLink - Deep observation
@Observed
class Person {
  name: string = ''
  age: number = 0
}

@ObjectLink person: Person
```

### Lifecycle

```typescript
// Component lifecycle
aboutToAppear() {}    // About to display
onDidBuild() {}       // Build complete
aboutToDisappear() {} // About to destroy
```

---

## Common Components

- **Text** - Text display
- **Image** - Image display
- **Button** - Interactive button
- **Column/Row** - Layout containers
- **List** - Scrollable list
- **Grid** - Grid layout
- **Stack** - Stacked layout
- **Swiper** - Carousel
- **TabContent** - Tab pages

---

## Layouts

```typescript
// Linear layout
Column() { }  // Vertical
Row() { }     // Horizontal

// Flex layout
Flex() { 
  direction: FlexDirection.Row 
}

// Grid layout
Grid() { 
  columnsTemplate: '1fr 1fr 1fr' 
}

// Stack
Stack() { }
```

---

## Routing

```typescript
import router from '@ohos.router'

// Navigate
router.pushUrl('pages/Detail')

// Go back
router.back()

// With params
router.pushUrl({
  url: 'pages/Detail',
  params: { id: 123 }
})

// Get params
const params = router.getParams()
```

---

## Network Requests

```typescript
import http from '@ohos.net.http'

let httpRequest = http.createHttp()
httpRequest.request(
  'https://api.example.com/data',
  {
    method: http.RequestMethod.GET,
    header: { 'Content-Type': 'application/json' }
  },
  (err, data) => {
    if (!err) {
      console.log(JSON.stringify(data.result))
    }
  }
)
```

---

## Local Storage

```typescript
import preferences from '@ohos.data.preferences'

// Write
let preferences = await preferences.getPreferences(context, 'myPrefs')
await preferences.put('username', 'tom')
await preferences.flush()

// Read
let value = await preferences.get('username', 'default')
```

---

## Permissions

```typescript
import abilityAccessCtrl from '@ohos.abilityAccessCtrl'

// Declare in module.json5
// "requestPermissions": [
//   { "name": "ohos.permission.INTERNET" }
// ]

// Request at runtime
let atManager = abilityAccessCtrl.createAtManager()
atManager.requestPermissionsFromUser(context, ['ohos.permission.INTERNET'])
```

---

## Common Permissions

- `ohos.permission.INTERNET` - Network access
- `ohos.permission.GET_NETWORK_INFO` - Network status
- `ohos.permission.CAMERA` - Camera access
- `ohos.permission.WRITE_MEDIA` - Media write
- `ohos.permission.READ_MEDIA` - Media read

---

## Build & Signing

1. **DevEco Studio** → Build → Build Hap
2. Configure signing in `Project Structure` → Signing Configs
3. Requires `.p12` certificate and `.cer` public key
4. Use debug signing for development, release for production

---

## Quick Reference

| Need | Solution |
|------|----------|
| State management | @State, @Prop, @Link, @Observed |
| Lists | List + ListItem |
| Network | @ohos.net.http |
| Storage | @ohos.data.preferences |
| Routing | router.pushUrl() |
| Toast | promptAction.showToast() |
| Dialog | dialog.showDialog() |

---

## Learning Resources

- Official: https://developer.harmonyos.com/
- API Docs: https://docs.openharmony.cn/
- Samples: https://gitee.com/openharmony/app_samples

---

## Extended Project Guidance

Keep the sections above as the fast reference layer. Use the guidance below when the task involves a real repository instead of isolated code snippets.

### Project-first workflow

Before changing code, inspect the real project structure:

- `AppScope/app.json5`
- `src/main/module.json5`
- `oh-package.json5`
- `build-profile.json5`
- `hvigorfile.ts` or `hvigorfile.js`
- `src/main/ets`

Start by answering:

1. Which module is runnable?
2. Which module owns the target page or ability?
3. Which import style does the repository already use: `@kit.*` or `@ohos.*`?
4. Does the repository wrap build commands in scripts?

### Stage model default

Unless the repository clearly uses an older pattern, treat it as a Stage model project.

Check these first:

- `UIAbility`
- `EntryAbility`
- `WindowStage`
- `module.json5`
- page routing and param flow

White screens, startup failures, and route bugs are often caused by incorrect entry, registration, or lifecycle assumptions rather than bad UI code.

### Change strategy

- Keep `build()` as pure as possible.
- Do not place request logic, persistent writes, or broad state mutations inside `build()`.
- Prefer the smallest state scope that solves the requirement.
- Reuse existing service or request wrappers instead of calling low-level HTTP APIs directly from pages when the repo already has an abstraction.
- Do not mix new import styles into old modules unless the task is explicitly a migration.

### Task routing

Classify the task before editing:

- **Page change**: identify the page, module, route entry, and data source first.
- **State bug**: check `@State`, `@Prop`, `@Link`, `@Observed`, `@ObjectLink`, `AppStorage`, and `PersistentStorage` before changing UI code.
- **Routing bug**: inspect `UIAbility`, `module.json5`, route paths, params shape, and launch mode before changing pages.
- **Network or permission bug**: inspect request wrappers, permission declarations, runtime permission flow, and device-only differences.
- **Build or signing bug**: separate dependency, compile, packaging, signing, installation, and launch failures instead of treating them as one class.

### Command strategy

Prefer this order:

1. repository scripts
2. `./hvigorw`
3. `ohpm`
4. `hdc`
5. DevEco Studio output

Safe default command directions:

```bash
ohpm install
./hvigorw clean
./hvigorw assembleHap
```

If the repository provides a higher-level script, use the repository script first.

### Debugging order

When debugging, use this order:

1. Reproduce the issue
2. Confirm the module
3. Confirm the entry point
4. Confirm config files
5. Confirm state ownership
6. Confirm the network layer
7. Confirm permissions
8. Confirm the build chain
9. Read the first real log or compiler error
10. Then change code

### Reporting expectations

When finishing a task, report:

- exact module touched
- exact page, ability, or config file touched
- exact command executed
- exact verification boundary
- what was not verified

Preferred format:

- Module: `entry`
- Page: `src/main/ets/pages/Index.ets`
- Ability: `EntryAbility.ets`
- Config: `module.json5`
- Build: `./hvigorw assembleHap`
- Verification: build passed / Previewer passed / device not verified

---

## Official ArkUI and Stage Model Additions

The sections above remain the original fast-reference layer. The additions below extend that material with guidance aligned to current official HarmonyOS documentation.

### Navigation and routing updates

- Current official HarmonyOS docs recommend the `Navigation` component path for modern ArkTS page flow.
- Current official routing docs explicitly mark page routing through `@ohos.router` as not recommended.
- If an older repository already uses `router.pushUrl()` and related APIs everywhere, preserve repository consistency unless the task is an intentional migration.
- If you are creating new page flow in a newer ArkTS project, inspect whether the repository already uses `Navigation`, `NavPathStack`, or a wrapper built on top of them before adding new routing code.

Practical extension rule:

- old repository with router-based flow already established: extend carefully
- newer repository or migration task: prefer the repository's `Navigation`-based pattern

### UIAbility and WindowStage understanding

- Official Stage model docs separate `UIAbility` lifecycle from display-related window lifecycle.
- `UIAbility` lifecycle focuses on create, destroy, foreground, and background transitions.
- Display and page-loading behavior is tied to `WindowStage` callbacks and setup flow.
- When debugging startup or white-screen issues, inspect both the `UIAbility` entry and the window-stage setup path instead of only reading page-level ArkUI code.

Recommended inspection order:

1. inspect the real ability entry such as `EntryAbility.ets`
2. inspect `onWindowStageCreate`
3. inspect what page or navigation root is loaded there
4. then inspect page-level `aboutToAppear()` and related UI logic

### Official state scope layering

Official state-management docs distinguish several storage scopes. Choose the smallest scope that fits the requirement:

- `LocalStorage`: page-level UI state storage, suitable for state sharing within a page scope and closely related pages in the same `UIAbility`.
- `AppStorage`: application-global UI state storage. Official docs describe it as a special singleton `LocalStorage` object created by the framework at app startup.
- `PersistentStorage`: persists selected `AppStorage` properties so they survive application restarts.
- `Preferences`: lightweight key-value persistence for configuration and small local values.

Practical extension rule:

- page-local interaction: prefer local decorators first
- shared UI state across pages in one running session: consider `LocalStorage` or `AppStorage`
- restart persistence for UI-facing values: consider `PersistentStorage`
- configuration, flags, or small local values: consider `Preferences`

### State management version awareness

- Current official docs clearly separate state management V1 and V2.
- `@Component` and many familiar decorators belong to the V1-style custom component model.
- Newer patterns may depend on V2-style components and should not be mixed casually into older files.
- If the touched file is clearly V1-based, avoid partial migration during a small bug fix.
- If the repository is already adopting V2 patterns, keep new code consistent with that direction.

Practical extension rule:

- bug fix task: preserve the state-management generation already used in the touched file
- migration task: migrate intentionally, not incidentally

### ArkUI reuse mechanisms from official docs

Official ArkUI docs emphasize several reuse patterns:

- `@Builder`: reusable UI construction blocks
- `@BuilderParam`: passing builder logic into components
- `@Styles`: reusable style blocks
- `@Extend`: extending component style capability

Use them when:

- repeated UI fragments appear in the same page or module
- the repository already uses builder-based composition
- you want to reduce duplication without forcing a full component extraction

Avoid forcing them when:

- a normal component extraction is clearer
- the repository does not use these patterns and the task is small
- the abstraction would make the current page harder for the team to maintain

### Persistence reminders

- Official docs position `Preferences` as lightweight persistence rather than a general-purpose database.
- Do not turn `Preferences` into a catch-all storage layer for large structured data.
- If a feature needs larger or more structured persistence, inspect the repository's current persistence approach before introducing a new one.

### Officially aligned review checklist

Before finalizing a HarmonyOS change, ask:

1. Did I preserve the repository's active routing generation: `Navigation` or router-based flow?
2. Did I choose the correct state scope: local, page-level, app-level, or persistent?
3. Did I inspect `UIAbility` and `WindowStage` before blaming page code?
4. Did I keep V1 and V2 state-management patterns consistent with the touched file?
5. Did I use `Preferences` only for lightweight persisted data?

### Recommended official topics to revisit

If the task depends on current best practice rather than just matching an old repository, revisit official docs for:

- Stage model development overview
- UIAbility lifecycle
- component navigation and page routing
- Navigation component usage
- state management overview, V1, and V2
- `AppStorage` and `PersistentStorage`
- `Preferences`
- ArkUI component extension and reuse

---

## Chinese Notes

- 先看工程结构，再改页面代码。
- 先确认模块归属、入口 Ability、`module.json5` 和构建链路。
- `build()` 里尽量不要做副作用。
- 要明确区分构建通过、Previewer 通过、真机通过。
- 官方当前更推荐 `Navigation`，`@ohos.router` 在新文档里已经标成不推荐。
- `UIAbility` 生命周期和 `WindowStage` 的显示/加载链路要分开理解。
- `LocalStorage`、`AppStorage`、`PersistentStorage`、`Preferences` 要按职责使用，不要混用。
