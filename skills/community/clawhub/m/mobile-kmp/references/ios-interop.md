# iOS interop reference

Load this when designing the API Swift sees, choosing or configuring the coroutine bridge, consuming a
shared ViewModel from SwiftUI, or evaluating Swift export.

## How Kotlin reaches Swift today

The default path is Objective-C export: the Kotlin compiler produces an Apple framework with an
Objective-C header, and Swift imports that header. Swift export (direct Kotlin to Swift) is Alpha.

| Kotlin | Seen from Swift through Objective-C export | What to do |
|---|---|---|
| `suspend fun` | Completion handler; `async` from Swift 5.5 is "highly experimental" | Use SKIE (or KMP-NativeCoroutines) |
| `Flow<T>`, `StateFlow<T>` | `Flow` interface, element type lost | Use SKIE (or KMP-NativeCoroutines) |
| Generic class `Box<T>` | Objective-C generic class, some information lost | Use `T : Any` bound to keep non-null |
| Generic interface or function | Generics dropped | Concrete facade types |
| `enum class` | Class; `switch` needs `default` | SKIE turns it into a Swift enum |
| `sealed class` / `sealed interface` | Class hierarchy; cast with `as?` | SKIE `onEnum(of:)` |
| Default arguments | Not exported; every argument required | Explicit overloads or a parameter object |
| `value class` / inline class | Underlying primitive type or `id` | Keep out of Swift-facing signatures |
| `object`, `companion object` | Class with `shared` / `companion` property | `MyObject.shared.x` |
| Top-level function in `Devices.kt` | Static on `DevicesKt` | Group Swift-facing API in classes |
| `Int`, `Long` | `Int32`, `Int64`; `KotlinInt` when nullable or generic | Avoid nullable primitives in Swift API |
| `List`, `Map`, `Set` | `Array`, `Dictionary`, `Set` | Do not subclass collection interfaces |
| Function type `(Int) -> Unit` | Block returning `KotlinUnit` | Prefer `suspend` or a small interface |
| Kotlin exception | Terminates the process unless declared with `@Throws` | See below |

## Exceptions

```kotlin
// GOOD: non-suspend function, declared exception types become a Swift `throws`
@Throws(FrameException::class)
fun decode(bytes: ByteArray): Frame

// GOOD: suspend functions must include CancellationException (or a supertype) in the list
@Throws(DeviceException::class, CancellationException::class)
suspend fun connect(id: String): DeviceSession
```

- Exceptions not listed in `@Throws` that reach Swift are unhandled and terminate the app.
- Non-suspend functions without `@Throws` propagate no exception at all.
- Suspend functions without `@Throws` propagate only `CancellationException` as an `NSError`.
- Swift errors thrown from Swift code are not translated into Kotlin exceptions. A Swift implementation
  of a Kotlin interface reports failure through a return value or callback.
- Keep `@Throws` on Swift-facing functions even with SKIE; it documents the contract and keeps
  behaviour correct if the bridge changes.

## Naming and visibility

```kotlin
@ObjCName(swiftName = "DeviceClient")
class KmpDeviceClient {
    @ObjCName("connect")
    fun connectTo(@ObjCName("id") deviceId: String) { /* ... */ }
}

@HiddenFromObjC          // visible to other Kotlin modules, hidden from Swift
fun internalDebugDump(): String = ""

@ShouldRefineInSwift     // exported with a __ prefix so Swift can wrap it in a nicer API
fun rawReadings(): List<Long> = emptyList()
```

- `@ObjCName` needs the `kotlin.experimental.ExperimentalObjCName` opt-in.
- Prefer `internal` for anything Swift does not call. Every public declaration in an exported module
  becomes part of the framework header.

## Interfaces implemented in Swift

Passing a Swift implementation into Kotlin is a clean way to keep CoreBluetooth, Keychain or HealthKit
code in Swift.

```kotlin
// commonMain: callback-based, no generics, no suspend, easy to conform to from Swift
interface KeyValueVault {
    fun write(key: String, value: ByteArray): Boolean
    fun read(key: String): ByteArray?
}
```

```swift
final class KeychainVault: KeyValueVault {
    func write(key: String, value: KotlinByteArray) -> Bool { /* SecItemAdd / SecItemUpdate */ }
    func read(key: String) -> KotlinByteArray? { /* SecItemCopyMatching */ }
}
```

- Kotlin interfaces become Objective-C protocols. Suspend members become completion-handler
  requirements, which are awkward to implement; bridge to `suspend` on the Kotlin side with
  `suspendCancellableCoroutine` instead.
- `ByteArray` arrives as `KotlinByteArray`. For large payloads, convert once at the boundary rather
  than per element.
- Threading: the Kotlin caller decides the thread. Swift implementations must be safe to call off the
  main thread, or the Kotlin side switches to `Dispatchers.Main` first.

## Coroutine bridge: SKIE vs KMP-NativeCoroutines

| | SKIE | KMP-NativeCoroutines |
|---|---|---|
| Mechanism | Compiler plugin that modifies the produced framework and adds generated Swift | Compiler plugin plus Swift packages; generates native wrappers for annotated declarations |
| Kotlin-side changes | None | `@NativeCoroutines` / `@NativeCoroutinesState` on each exposed declaration |
| Suspend | Native Swift `async`, two-way cancellation, callable from any thread | `asyncFunction(for:)` wrapper, cancellation via the Swift `Task` |
| Flow | `SkieSwiftFlow`, `SkieSwiftStateFlow`: typed `AsyncSequence` | `asyncSequence(for:)`, Combine publisher or RxSwift observable |
| Sealed, enums | Exhaustive Swift switch (`onEnum(of:)`), Swift enums | Not covered |
| Default arguments | Opt-in, at most 5 per function, interface methods unsupported | Not covered |
| Kotlin version support | Each SKIE release supports a fixed Kotlin range; can lag new Kotlin releases | Also version-matched; releases have tracked new Kotlin versions closely |
| Swift side dependency | None | `KMPNativeCoroutinesAsync` (or Combine, RxSwift) via SPM or CocoaPods |
| Swift export | Not documented | Compatibility mode exists; native wrappers not supported under Swift export |

Recommendation: SKIE for app projects. It fixes suspend, Flow, sealed classes and enums for the whole
framework with no Kotlin annotations, so shared code stays idiomatic and the iOS team gets native
types. The cost is a hard dependency on SKIE supporting the project's Kotlin version.

Pick KMP-NativeCoroutines when:
- the project must adopt a Kotlin release SKIE does not support yet, and that cannot wait;
- only coroutines need bridging and the team wants explicit, opt-in API exposure;
- the framework is an SDK for external apps that may not accept a framework-modifying plugin.

Never use both in one framework. Switching later touches every Swift call site, so decide once.

## SKIE setup and usage

```kotlin
// Only in the module that builds the Xcode framework
plugins {
    alias(libs.plugins.skie) // id "co.touchlab.skie"
}
```

- SKIE processes everything exported from that framework, including exported dependencies.
- Before every Kotlin upgrade, check the supported Kotlin range in the SKIE documentation.

```swift
// suspend: plain async call, Task cancellation cancels the coroutine
let session = try await facade.connect(id: deviceId)

// Flow / StateFlow: typed AsyncSequence
for await readings in viewModel.readings {
    self.readings = readings
}

// sealed class: exhaustive switch over the generated enum, no default branch
@ViewBuilder
func content(for state: DevicesUiState) -> some View {
    switch onEnum(of: state) {
    case .loading: ProgressView()
    case .content(let content): DeviceList(devices: content.devices)
    case .error(let error): ErrorView(reason: error.reason)
    }
}
```

- A cancelled Kotlin suspend function surfaces as `CancellationError` in Swift.
- Swift `async` functions may run off the main thread. Mark the Swift model `@MainActor` and update UI
  state there.
- Generic Kotlin classes need SKIE's `skie(_:)` wrapper for their suspend members.

## KMP-NativeCoroutines setup and usage

```kotlin
plugins {
    id("com.rickclephas.kmp.nativecoroutines") version "<version matching kotlin>"
}
kotlin.sourceSets.all {
    languageSettings.optIn("kotlin.experimental.ExperimentalObjCName")
}

class DevicesViewModel(private val repo: DeviceRepository) : ViewModel() {
    @NativeCoroutinesState
    val state: StateFlow<DevicesUiState> = repo.observe()
        .stateIn(viewModelScope, SharingStarted.Eagerly, DevicesUiState.Loading)

    @NativeCoroutines
    suspend fun refresh(): Unit = repo.refresh()
}
```

```swift
import KMPNativeCoroutinesAsync

let task = Task {
    do {
        for try await state in asyncSequence(for: viewModel.stateFlow) { self.state = state }
    } catch {
        self.failure = error
    }
}
// cancelling the task cancels collection
try await asyncFunction(for: viewModel.refresh())
```

- Keep the Swift package version identical to the Kotlin plugin version.
- Unannotated exposed suspend functions and Flows produce a warning; raise it with
  `nativeCoroutines { exposedSeverity = ExposedSeverity.ERROR }`.

## Shared ViewModel from SwiftUI

The AndroidX ViewModel needs a `ViewModelStore` on iOS so `onCleared` runs and `viewModelScope` is
cancelled.

```kotlin
// iosMain
@BetaInteropApi
@Throws(IllegalArgumentException::class)
fun ViewModelStore.resolveViewModel(
    modelClass: ObjCClass,
    factory: ViewModelProvider.Factory,
    key: String?,
    extras: CreationExtras? = null,
): ViewModel {
    @Suppress("UNCHECKED_CAST")
    val vmClass = getOriginalKotlinClass(modelClass) as? KClass<ViewModel>
    require(vmClass != null) { "The modelClass parameter must be a ViewModel type." }
    val provider = ViewModelProvider.Companion.create(this, factory, extras ?: CreationExtras.Empty)
    return key?.let { provider[key, vmClass] } ?: provider[vmClass]
}
```

```swift
final class IosViewModelStoreOwner: ObservableObject, ViewModelStoreOwner {
    let viewModelStore = ViewModelStore()

    func viewModel<T: ViewModel>(
        key: String? = nil,
        factory: ViewModelProviderFactory,
        extras: CreationExtras? = nil
    ) -> T {
        do {
            return try viewModelStore.resolveViewModel(
                modelClass: T.self, factory: factory, key: key, extras: extras
            ) as! T
        } catch {
            fatalError("Failed to create ViewModel of type \(T.self)")
        }
    }

    deinit { viewModelStore.clear() }
}

struct DevicesScreen: View {
    @StateObject private var owner = IosViewModelStoreOwner()

    var body: some View {
        let vm: DevicesViewModel = owner.viewModel(factory: DevicesViewModelKt.devicesViewModelFactory)
        DevicesContent(viewModel: vm)
    }
}
```

- Add `api(libs.androidx.lifecycle.viewmodel)` and `export(libs.androidx.lifecycle.viewmodel)` so
  Swift sees `ViewModel`, `ViewModelStore` and `ViewModelStoreOwner` without package prefixes.
- The `as!` and `fatalError` mirror the documented sample: a wrong type is a programming error. Keep
  them out of any code path driven by user input.
- One store owner per screen. A store held at app level keeps every ViewModel alive forever.

## Swift export (Alpha)

```kotlin
kotlin {
    iosArm64()
    iosSimulatorArm64()
    swiftExport {
        moduleName = "Shared"
        flattenPackage = "com.example.shared"
    }
}
```

Xcode build phase: `./gradlew :shared:embedSwiftExportForXcode` instead of
`embedAndSignAppleFrameworkForXcode`.

- Maps suspend to `async`, Flow to `AsyncSequence` (`asAsyncSequence()`), sealed hierarchies to Swift
  enums, Kotlin enums to Swift enums.
- Limits: direct integration only; generics erased to upper bounds; only final classes that inherit
  directly from `Any`; types inheriting `List`, `Set` or `Map` are ignored; breaking changes expected.
- KMP-NativeCoroutines native wrappers do not work under Swift export.
- Use it in a spike branch to track progress. Do not ship production apps on it until it leaves Alpha.
