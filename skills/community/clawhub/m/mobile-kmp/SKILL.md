---
name: mobile-kmp
description: "Builds and reviews Kotlin Multiplatform and Compose Multiplatform code for Android and iOS: source sets and the default hierarchy template, interfaces with DI over expect/actual, shared AndroidX ViewModels, Ktor, Room KMP or SQLDelight, kotlinx.serialization, Flow and suspend from Swift via SKIE, Objective-C and Swift export limits, XCFramework and SPM publishing, commonTest. Use when setting up, migrating to or reviewing a KMP shared module."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Kotlin Multiplatform

Share business logic between Android and iOS without making either app worse. A good result has a
`commonMain` that compiles without platform imports, platform services behind interfaces, a Swift API that
feels native, a build on the current Gradle plugins, and tests that run on every target.

## When to use

- Setting up a shared KMP module, or adding iOS to an existing Android codebase.
- Moving repositories, ViewModels, networking or persistence from Android code into `commonMain`.
- Choosing between expect/actual and interfaces, Room KMP and SQLDelight, SKIE and KMP-NativeCoroutines,
  shared Compose UI and native UI.
- Fixing Swift-side pain: lost generics, `KotlinInt` boxes, non-exhaustive `switch`, crashes from Kotlin
  exceptions, Flows that SwiftUI cannot observe.
- Upgrading to AGP 9, where the KMP plugin no longer works with `com.android.application` or
  `com.android.library` in the same module.
- Publishing the shared code to an iOS team as an XCFramework or Swift package.

Not for: Android-only Kotlin style (use `mobile-kotlin`), Swift-only code (use `mobile-swift`), CI pipelines
(use `mobile-ci-cd`), or Flutter (use `mobile-flutter`).

## Workflow

1. Read the build before writing code.
   - `gradle/libs.versions.toml`: Kotlin, AGP, Compose Multiplatform, coroutines, Ktor, Room or SQLDelight,
     SKIE or KMP-NativeCoroutines versions.
   - `settings.gradle.kts` and each module's plugins: where `org.jetbrains.kotlin.multiplatform` is applied
     and which Android plugin sits next to it.
   - Declared targets, framework `baseName`, `export(...)` calls, and how Xcode consumes the framework
     (build-phase script, local package, CocoaPods, remote XCFramework).
2. Check compatibility before adding or upgrading anything. SKIE, KSP, Room and Compose Multiplatform each
   support a specific Kotlin range. Do not bump Kotlin, AGP, `compileSdk` or the iOS deployment target
   without asking.
3. Load the reference for the area being touched:
   [Structure and Gradle](references/structure-and-gradle.md), [iOS interop](references/ios-interop.md),
   [Data and networking](references/data-and-networking.md), [Testing](references/testing.md).
4. Decide what is shared. Default: domain, data, networking, persistence and ViewModels in `commonMain`;
   UI per Rule 13. Hardware stacks (BLE, camera, location, push) stay platform code behind an interface.
5. Write common code first, then platform implementations, then the Swift-facing facade.
6. Add `commonTest` tests for new shared logic; run them on the JVM and the iOS simulator target.
7. Build both apps: `./gradlew :androidApp:assembleDebug` and the iOS app in Xcode (or
   `./gradlew :shared:linkDebugFrameworkIosSimulatorArm64`). A green Android build says nothing about iOS.
8. Report what moved to common code, new dependencies, Swift API changes, and every `Info.plist`,
   entitlement, Gradle property or Xcode build-phase change. These need explicit sign-off.

## Rules

### 1. Use the default hierarchy template; never wire `dependsOn` by hand

```kotlin
// BAD: manual intermediate source set, disables the default template with a warning
val iosMain by creating { dependsOn(commonMain.get()) }
iosArm64Main.get().dependsOn(iosMain)

// GOOD: iosMain, appleMain and nativeMain exist automatically for the declared targets
kotlin {
    iosArm64()
    iosSimulatorArm64()
    sourceSets {
        commonMain.dependencies { implementation(libs.kotlinx.coroutines.core) }
        iosMain.dependencies { implementation(libs.ktor.client.darwin) }
    }
}
```

- Put iOS code in `iosMain`, not `iosArm64Main`. Per-target source sets are for rare ABI differences.
- `iosX64` (Intel simulator) is Tier 3. Declare it only if the team still builds on Intel Macs, and check
  that every dependency still publishes it.

### 2. The shared module is a library; app entry points live in app modules

```kotlin
// BAD: KMP plugin and the Android application plugin in one module (unsupported from AGP 9)
plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.application)
}

// GOOD: shared/build.gradle.kts
plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.kotlin.multiplatform.library)
}
kotlin {
    android {
        namespace = "com.example.shared"
        compileSdk = 36
        minSdk = 26
    }
    iosArm64()
    iosSimulatorArm64()
}
```

- `com.android.kotlin.multiplatform.library` has one variant and no top-level `android {}` block. From
  AGP 8.12 the target is `kotlin { android { } }`; older AGP uses the now-deprecated `androidLibrary { }`.
- `MainActivity` and the app manifest move to an `androidApp` module that depends on `projects.shared`.
  Layout and AGP 9 migration: [Structure and Gradle](references/structure-and-gradle.md).

### 3. Platform services are interfaces bound in DI; `commonMain` stays platform-free

```kotlin
// BAD: expect class for a service, Android types in shared signatures, nothing to fake in tests
expect class SecureStore() { fun put(key: String, value: String) }
class ReadingRepository(private val context: android.content.Context) {
    fun now(): Long = System.currentTimeMillis()
}

// GOOD: interfaces in commonMain, implementations in androidMain / iosMain, bound per platform
interface SecureStore {
    suspend fun put(key: String, value: ByteArray)
    suspend fun get(key: String): ByteArray?
}
interface Clock { fun nowMillis(): Long }
class ReadingRepository(private val clock: Clock, private val store: SecureStore)

// GOOD: expect/actual for a tiny, stateless platform fact
expect val platformName: String
```

- Expect/actual classes are Beta and need `-Xexpect-actual-classes`. Prefer an interface plus an
  `expect fun` factory, or bind the implementation in each platform's DI module.
- An implementation can be written in Swift and passed in from the iOS app (a CoreBluetooth or Keychain
  wrapper), which keeps Apple APIs in the language the iOS team owns.
- `java.*`, `android.*` and `platform.*` imports belong in platform source sets only. Use multiplatform
  libraries (coroutines, serialization, Ktor, kotlinx-datetime, kotlinx-io) instead of wrapping JVM APIs.
- Hilt does not run in `commonMain`. Use the KMP DI library the project already has (Koin, kotlin-inject,
  Metro) or constructor injection with a small composition root per platform.

### 4. Share the ViewModel with AndroidX lifecycle; scopes and dispatchers stay structured

```kotlin
// BAD: Hilt and Android types in a shared ViewModel; a scope nobody cancels
@HiltViewModel
class DevicesViewModel @Inject constructor(app: Application) : AndroidViewModel(app)
private val scope = CoroutineScope(Dispatchers.Default)

// GOOD: commonMain, androidx.lifecycle:lifecycle-viewmodel
class DevicesViewModel(private val repo: DeviceRepository) : ViewModel() {
    private val _state = MutableStateFlow<DevicesUiState>(DevicesUiState.Loading)
    val state: StateFlow<DevicesUiState> = _state.asStateFlow()
    fun refresh() = viewModelScope.launch { _state.value = repo.load().toUiState() }
}

val devicesViewModelFactory = viewModelFactory {
    initializer { DevicesViewModel(repo = AppGraph.deviceRepository) }
}
```

- Non-JVM targets have no reflection: in Compose Multiplatform call `viewModel { DevicesViewModel(...) }`,
  never a bare `viewModel()`.
- `viewModelScope` runs on `Dispatchers.Main.immediate`, the main queue on iOS. Inject IO and Default
  dispatchers into repositories; rethrow `CancellationException` exactly as on Android (`mobile-kotlin`).
- SwiftUI needs a `ViewModelStoreOwner` held as `@StateObject` so `clear()` runs on `deinit`:
  [iOS interop](references/ios-interop.md).

### 5. One Ktor client per app, an explicit engine per platform, TLS only

```kotlin
// BAD: new client per call, logging prints the bearer token, cleartext URL
suspend fun fetch() = HttpClient { install(Logging) { level = LogLevel.ALL } }
    .get("http://api.example.com/readings").body<List<ReadingDto>>()

// GOOD: engine comes from androidMain (OkHttp) or iosMain (Darwin)
fun createHttpClient(engine: HttpClientEngine, json: Json) = HttpClient(engine) {
    expectSuccess = true
    install(ContentNegotiation) { json(json) }
    install(HttpTimeout) { requestTimeoutMillis = 15_000 }
    install(Logging) {
        level = LogLevel.HEADERS
        sanitizeHeader { it == HttpHeaders.Authorization }
    }
    defaultRequest { url("https://api.example.com/") }
}
```

- Each client owns a connection pool; create it once in the app graph.
- Telemetry and device identifiers are personal data: no `LogLevel.BODY` in release builds.

### 6. DTOs are `@Serializable` and mapped at the data edge

```kotlin
// BAD: domain model doubles as the wire format; a new server field breaks old clients
@Serializable data class Device(val id: String, val rssi: Int)

// GOOD
@Serializable
data class DeviceDto(@SerialName("device_id") val id: String, val rssi: Int? = null)

val appJson = Json { ignoreUnknownKeys = true }
fun DeviceDto.toDomain() = Device(id = DeviceId(id), rssi = rssi)
```

- One injected `Json` instance. Apply `org.jetbrains.kotlin.plugin.serialization`, versioned with Kotlin.
- Engines, error mapping and polymorphic payloads: [Data and networking](references/data-and-networking.md).

### 7. Pick the database by team and schema, not by habit

| Choose | When |
|---|---|
| Room KMP (`androidx.room3`, or Room 2.7+ already in use) | Android team knows Room, annotation-defined entities, migrating an existing Room database |
| SQLDelight | SQL-first schema reviewed by both teams, compile-time checked queries, `.sqm` migrations, no KSP per target |

```kotlin
// BAD: blocking DAO and LiveData, neither works in commonMain
@Query("SELECT * FROM reading") fun all(): LiveData<List<ReadingEntity>>

// GOOD: Room in commonMain, bundled SQLite driver on every platform
@Query("SELECT * FROM reading ORDER BY ts DESC") fun observeAll(): Flow<List<ReadingEntity>>
fun buildDb(builder: RoomDatabase.Builder<AppDatabase>) =
    builder.setDriver(BundledSQLiteDriver()).build()
```

- Room 3 is a new package (`androidx.room3`), KSP-only and coroutines-only, with no `SupportSQLite` types.
  Room 2.x and 3.x can coexist during a migration.
- Either option needs real migrations and a migration test.

### 8. Design the Swift-facing API; do not ship the raw Kotlin surface

```kotlin
// BAD: generic interface (type lost in Objective-C), default arg Swift cannot omit, value class param
interface Store<T> { suspend fun load(id: DeviceId, refresh: Boolean = false): T }

// GOOD: small concrete facade with explicit overloads
class DeviceFacade internal constructor(private val repo: DeviceRepository) {
    @Throws(DeviceException::class, CancellationException::class)
    suspend fun load(id: String): DeviceSnapshot = repo.load(DeviceId(id), refresh = false)

    @Throws(DeviceException::class, CancellationException::class)
    suspend fun refresh(id: String): DeviceSnapshot = repo.load(DeviceId(id), refresh = true)
}
```

- Objective-C export keeps generics on classes only, maps `enum class` to a class, drops default
  arguments and exports inline classes as their underlying type or `id`. Mapping table:
  [iOS interop](references/ios-interop.md).
- `@ObjCName(swiftName = ...)` fixes names, `@HiddenFromObjC` hides Kotlin-only API, and
  `@ShouldRefineInSwift` lets the iOS team wrap an API in Swift.

### 9. Every function Swift calls that can fail declares `@Throws`

```kotlin
// BAD: an exception reaching Swift terminates the app
fun parse(bytes: ByteArray): Frame = decoder.decode(bytes) // throws on malformed input

// GOOD: becomes `throws` in Swift; suspend functions must also list CancellationException
@Throws(FrameException::class)
fun parse(bytes: ByteArray): Frame = decoder.decode(bytes)

@Throws(IOException::class, CancellationException::class)
suspend fun upload(frame: Frame) { api.post(frame) }
```

```swift
// GOOD: the Kotlin exception arrives as a Swift Error
do { try await facade.upload(frame: frame) } catch { state = .failed(error) }
```

- A non-suspend function without `@Throws` propagates no exception, and any Kotlin exception reaching
  Swift is unhandled and terminates the process. A suspend function without it propagates only
  `CancellationException`.
- Return a sealed result for expected failures; keep exceptions for the unexpected.

### 10. Flow, suspend and sealed types reach Swift through SKIE; one bridge per project

```kotlin
// BAD: Swift receives a Flow with no element type and needs a hand-written collector
val readings: Flow<List<Reading>> = repo.observe()

// GOOD with SKIE: no annotation, StateFlow becomes a typed AsyncSequence
val readings: StateFlow<List<Reading>> = repo.observe()
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
```

```swift
// BAD: cast chain over a sealed class, silently wrong when a case is added
if let c = state as? DevicesUiStateContent { show(c.devices) } else { showSpinner() }

// GOOD: collection cancelled with the view; exhaustive switch, no default branch
.task { for await list in viewModel.readings { self.readings = list } }

switch onEnum(of: state) {
case .loading: showSpinner()
case .content(let c): show(c.devices)
case .error(let e): showError(e.reason)
}
```

- Recommendation: SKIE for app projects where one framework is consumed by the team's own app. It covers
  suspend, Flow, sealed classes and enums with no Kotlin-side annotations.
- Choose KMP-NativeCoroutines when Kotlin must move to a release SKIE does not support yet, when
  coroutines are the only gap, or when shipping an SDK to third parties. Never apply both. Trade-offs and
  setup: [iOS interop](references/ios-interop.md).
- Swift export (Alpha) maps suspend to `async`, Flow to `AsyncSequence` and sealed types to Swift enums,
  but it works only with direct integration and breaking changes are expected. Do not ship it yet.

### 11. Export only what Swift uses

```kotlin
// BAD: every transitive API in the header, dead-code elimination disabled for all of it
binaries.framework {
    export(libs.ktor.client.core)
    transitiveExport = true
}

// GOOD: export only modules Swift calls directly; they must be `api` dependencies
iosMain.dependencies { api(projects.core.model) }
binaries.framework {
    baseName = "Shared"
    export(projects.core.model)
}
```

- Mark helpers `internal`. Every public declaration in exported modules becomes Swift API and binary size.
- One umbrella framework per app. Two Kotlin frameworks in one app duplicate the runtime and types.

### 12. Distribute by repository layout

| Layout | Integration |
|---|---|
| Monorepo, one team | Direct integration: Xcode build phase runs `embedAndSignAppleFrameworkForXcode` |
| Separate iOS repo or external consumers | Zipped XCFramework consumed via SPM `binaryTarget(url:checksum:)` |
| CocoaPods dependencies used from Kotlin | Kotlin CocoaPods Gradle plugin |

```kotlin
// GOOD: produces build/XCFrameworks/release/Shared.xcframework
val xcf = XCFramework("Shared")
listOf(iosArm64(), iosSimulatorArm64()).forEach {
    it.binaries.framework { baseName = "Shared"; xcf.add(this) }
}
```

- Publish `Package.swift` from its own repository with semantic version tags. Commands and manifest:
  [Structure and Gradle](references/structure-and-gradle.md).
- The app target embeds and signs the framework. Flag any change to build phases, `Embed Frameworks` or
  signing settings for the iOS owner.

### 13. Share UI with Compose Multiplatform only when it pays off

| Share UI (Compose Multiplatform) | Keep native UI (SwiftUI on iOS) |
|---|---|
| Internal, B2B or tooling apps where consistency beats platform feel | Consumer apps where users expect native navigation, text input and gestures |
| Team is mostly Kotlin developers | Strong iOS team that owns the app |
| Complex custom drawing or charts duplicated today | Heavy use of widgets, Live Activities, App Intents |
| New app, no existing iOS UI | Mature SwiftUI app: share logic first, screens later |

```kotlin
// GOOD: iosMain entry point; SwiftUI hosts it with UIViewControllerRepresentable
fun MainViewController(): UIViewController = ComposeUIViewController { App() }
```

- Compose Multiplatform for iOS is Stable. Screens can mix both ways (`UIKitViewController` with a
  `UIHostingController` puts SwiftUI inside Compose).
- Info.plist change: add `CADisableMinimumFrameDurationOnPhone` set to `true`, or the app crashes at
  runtime. Call it out in the summary.
- Use direct library coordinates in the catalog; the `compose.ui`-style plugin aliases are deprecated
  since Compose Multiplatform 1.10.

### 14. Shared logic is tested in `commonTest` with fakes, on every target

```kotlin
// BAD: MockK in commonTest is JVM-only, so the iOS test compilation fails
val repo = mockk<DeviceRepository>()

// GOOD: kotlin.test, kotlinx-coroutines-test, Turbine, hand-written fake
class DevicesViewModelTest {
    @BeforeTest fun setUp() = Dispatchers.setMain(StandardTestDispatcher())
    @AfterTest fun tearDown() = Dispatchers.resetMain()

    @Test fun refreshEmitsContent() = runTest {
        val vm = DevicesViewModel(FakeDeviceRepository(devices = listOf(sensor)))
        vm.state.test {
            assertEquals(DevicesUiState.Loading, awaitItem())
            vm.refresh()
            assertEquals(DevicesUiState.Content(listOf(sensor)), awaitItem())
        }
    }
}
```

- Run `./gradlew :shared:allTests` so iOS simulator tests run too: [Testing](references/testing.md).

## Anti-patterns

- `commonMain` code that only "works" because the iOS target was never built.
- Manual `dependsOn` wiring or `by creating` source sets that disable the default hierarchy template.
- Keeping the KMP and Android application plugins in one module on AGP 9, or treating
  `android.enableLegacyVariantApi=true` as a permanent fix.
- Raw `Flow`, generic interfaces or default arguments exposed to Swift for the iOS team to cope with.
- SKIE and KMP-NativeCoroutines together, `transitiveExport = true`, or two Kotlin frameworks in one app.
- An `HttpClient` per request; `LogLevel.ALL` or `BODY` in release; `http://` endpoints.
- `runBlocking` on the iOS main thread to make a Swift call look synchronous.
- BLE, camera or location stacks forced into common code. Share protocol parsing and state machines,
  keep the radio APIs native (see `mobile-ble`).
- Moving a mature SwiftUI app to Compose Multiplatform without the iOS team agreeing.

## Checklist

- [ ] Kotlin, AGP, Compose Multiplatform, KSP and bridge versions confirmed compatible
- [ ] Targets `iosArm64` and `iosSimulatorArm64` (`iosX64` only if needed); no manual `dependsOn`
- [ ] Shared module uses `com.android.kotlin.multiplatform.library`; app entry points in app modules
- [ ] `commonMain` free of `java.*`, `android.*`, `platform.*`; platform services are interfaces in DI
- [ ] Shared ViewModels extend AndroidX `ViewModel`, built via initializer or factory, no Hilt
- [ ] Scopes owned, dispatchers injected, `CancellationException` rethrown
- [ ] One Ktor client, platform engine, timeouts, `expectSuccess`, sanitized logs, HTTPS only
- [ ] DTOs `@Serializable` and mapped; one `Json` with `ignoreUnknownKeys`
- [ ] Database choice justified; bundled driver; migrations and a migration test
- [ ] Swift API reviewed: concrete types, overloads instead of defaults, clear names
- [ ] `@Throws` on every Swift-callable throwing function (suspend ones include `CancellationException`)
- [ ] One coroutine bridge; Swift collects Flows with cancellation; sealed types switched exhaustively
- [ ] Only needed modules exported; one framework per app; signing and build-phase changes flagged
- [ ] Compose Multiplatform decision recorded; `CADisableMinimumFrameDurationOnPhone` set if used
- [ ] `commonTest` covers new shared logic with fakes; `allTests` passes; both apps build

## Output format

Use the review report for an existing KMP codebase and the migration plan for moving Android code to KMP.

~~~markdown
## KMP review: <module or branch>

Targets: <android, iosArm64, iosSimulatorArm64>. Versions: Kotlin <x>, AGP <x>, CMP <x | none>,
bridge <SKIE x | KMP-NativeCoroutines x | none>. iOS integration: <direct | SPM | CocoaPods>.

### Findings
1. [Blocker] shared/src/commonMain/.../FrameParser.kt:31 -- `parse` throws to Swift without `@Throws`
   Why: any malformed frame terminates the iOS app.
   Fix:
   ```kotlin
   @Throws(FrameException::class)
   fun parse(bytes: ByteArray): Frame
   ```
2. [Major] ... -- ...

### Swift API
- <names, generics, default args, Flows, sealed types that need work>

### Platform impact
- Info.plist / entitlements / Xcode build phases / Gradle properties: <list or "none">

### Verdict
Request changes -- 1 Blocker, 1 Major.
~~~

~~~markdown
## KMP migration plan: <app>

Goal: <what is shared and why>. UI: <native | Compose Multiplatform for screens X, Y>.

| Phase | Scope | Exit criteria |
|---|---|---|
| 0 Build | AGP 9 module split, Android-KMP library plugin, iOS integration | Both apps build in CI with an empty shared module |
| 1 Models | DTOs, domain types, serialization | `commonTest` green on JVM and iOS simulator |
| 2 Data | Ktor, database, repositories behind interfaces | Android on the shared data layer; one iOS feature reads it |
| 3 State | Shared ViewModels, coroutine bridge | One iOS screen driven by a shared ViewModel |
| 4 UI (optional) | Compose Multiplatform screens | Agreed with the iOS team; accessibility checked |

Risks: <version lock-in, binary size, iOS ramp-up, database migration>.
Platform changes: <Info.plist keys, entitlements, build phases>.
~~~

## Related skills

- `mobile-kotlin` -- Kotlin, coroutine and Compose rules that also apply in `commonMain`
- `mobile-swift` -- Swift concurrency and SwiftUI on the consuming side
- `mobile-mvvm`, `mobile-mvi` -- state and event design for shared ViewModels
- `mobile-ble` -- keeping radio code native while sharing protocol logic
- `mobile-testing` -- test strategy beyond `commonTest`
- `mobile-ci-cd` -- building the XCFramework and running iOS simulator tests in CI
- `mobile-security` -- secure storage, TLS and logging for shared networking code
- `mobile-code-review` -- general review dimensions applied to KMP diffs
