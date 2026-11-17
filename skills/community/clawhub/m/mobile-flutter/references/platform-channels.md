# Platform channels reference

Load this when Dart needs to call Kotlin or Swift, or native code needs to call or stream into Dart.
Use `pigeon` (dev dependency) to generate type-safe channels. Hand-written `MethodChannel` code is only
acceptable for a single trivial call in a legacy plugin.

## Why Pigeon

| Hand-written `MethodChannel` | Pigeon |
|---|---|
| Method names and argument keys are strings, typos fail at runtime | Generated, compile-time checked on all sides |
| Arguments are `Map<Object?, Object?>`, casts everywhere | Typed data classes |
| Dart and native drift apart silently | One definition file, regenerate both sides |

## Definition file

```dart
// pigeons/device_api.dart -- not part of the app build, only input to the generator
import 'package:pigeon/pigeon.dart';

@ConfigurePigeon(PigeonOptions(
  dartOut: 'lib/src/platform/device_api.g.dart',
  kotlinOut: 'android/app/src/main/kotlin/com/example/app/DeviceApi.g.kt',
  kotlinOptions: KotlinOptions(package: 'com.example.app'),
  swiftOut: 'ios/Runner/DeviceApi.g.swift',
))
class DeviceInfo {
  DeviceInfo({required this.model, required this.batteryLevel});
  String model;
  int batteryLevel;
}

@HostApi() // Dart calls native
abstract class DeviceApi {
  DeviceInfo getDeviceInfo();

  @async
  bool requestPairing(String deviceId);

  @TaskQueue(type: TaskQueueType.serialBackgroundThread)
  String hashFile(String path);
}

@FlutterApi() // native calls Dart
abstract class DeviceEvents {
  void onConnectionChanged(bool connected);
}
```

Generate, then commit the generated files so builds do not need the generator:

```bash
dart run pigeon --input pigeons/device_api.dart
```

- Dart `int` is a 64-bit integer: `Long` in Kotlin, `Int64` in Swift.
- Change the definition, never the `.g.` files. Regenerate on every Pigeon version bump.

## Android (Kotlin)

```kotlin
class DeviceApiImpl(private val context: Context) : DeviceApi {
    override fun getDeviceInfo(): DeviceInfo =
        DeviceInfo(model = Build.MODEL, batteryLevel = readBatteryLevel(context).toLong())

    // Generated handlers launch this on the main dispatcher: switch for blocking work
    override suspend fun requestPairing(deviceId: String): Boolean =
        withContext(Dispatchers.IO) { pairingManager.pair(deviceId) }

    // Runs on the background task queue requested with @TaskQueue
    override fun hashFile(path: String): String = sha256Of(File(path))
}

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        DeviceApi.setUp(flutterEngine.dartExecutor.binaryMessenger, DeviceApiImpl(applicationContext))
    }
}
```

- Pass `applicationContext`, never the `Activity`, to long-lived implementations.
- Recent Pigeon versions generate `suspend fun` for `@async` methods; older versions generate a
  `callback: (Result<T>) -> Unit` parameter. Follow the generated signature.

## iOS (Swift)

```swift
final class DeviceApiImpl: DeviceApi {
    func getDeviceInfo() throws -> DeviceInfo {
        DeviceInfo(model: UIDevice.current.model, batteryLevel: Int64(currentBatteryLevel()))
    }

    // Generated code calls this from a main-actor Task: keep heavy work off the main actor
    func requestPairing(deviceId: String) async throws -> Bool {
        try await pairingService.pair(deviceId)
    }

    func hashFile(path: String) throws -> String { try sha256(of: URL(fileURLWithPath: path)) }
}

// AppDelegate, after GeneratedPluginRegistrant.register(with: self)
let controller = window?.rootViewController as! FlutterViewController
DeviceApiSetup.setUp(binaryMessenger: controller.binaryMessenger, api: DeviceApiImpl())
```

- Throw `PigeonError(code:message:details:)` (Swift) or `FlutterError` (Kotlin) for expected failures;
  Dart receives a `PlatformException` with that code.
- Apps using the scene-based lifecycle register in the plugin or engine setup hook their template
  provides; follow the generated project, not an old snippet.

## Dart side

```dart
// BAD: generated API called straight from widgets, PlatformException leaks into UI
final info = await DeviceApi().getDeviceInfo();

// GOOD: wrapped in a repository that maps errors to domain types
final class PlatformDeviceRepository implements DeviceRepository {
  PlatformDeviceRepository(this._api);
  final DeviceApi _api;

  @override
  Future<bool> pair(DeviceId id) async {
    try {
      return await _api.requestPairing(id.value);
    } on PlatformException catch (e) {
      throw PairingException(e.code);
    }
  }
}
```

- The generated class is a detail of the data layer. Tests replace the repository, not the channel.
- Native-to-Dart calls (`@FlutterApi`) are registered in Dart with the generated `setUp` and must be
  invoked from the platform main thread on the native side.

## Streams from native

- For continuous data (BLE notifications, sensor readings, download progress) use `@EventChannelApi()`
  in the definition file. Pigeon generates a Dart `Stream` function and a native stream handler class.
- Cancel the Dart subscription when the screen or provider goes away; native `onCancel` must stop the
  underlying work (scan, sensor listener) or it keeps draining the battery.
- Throttle on the native side when the source emits faster than the UI can use (more than 60 per second).

## Threading rules

| Side | Default thread | Move off it with |
|---|---|---|
| Kotlin handler | Android main thread | `@TaskQueue` or `withContext(Dispatchers.IO)` |
| Swift handler | Main thread / main actor | `@TaskQueue`, or async work on another actor |
| Native -> Dart call | Must start on the platform main thread | Post to main before calling |
| Dart handler | UI isolate | `Isolate.run` for heavy processing of the result |

BLE callbacks arrive on binder threads (Android) or the central manager queue (iOS). Hop to the main
thread before calling a `@FlutterApi` or emitting on an event sink.

## Security

- Native code treats every argument from Dart as untrusted input: validate paths, IDs, lengths.
- Do not expose a generic "run this command" or "read this file path" API to Dart.
- Do not send secrets, tokens or raw device identifiers through channels when an opaque handle works.
- New permissions, `AndroidManifest.xml` entries, `Info.plist` usage strings or entitlements needed by
  native code are listed in the MR.
