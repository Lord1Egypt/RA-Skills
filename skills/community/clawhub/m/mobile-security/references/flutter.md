# Flutter security reference

Load this when the project has `pubspec.yaml`. A Flutter app is also an Android app and an iOS app: audit
`android/` with [Android](android.md) and `ios/` with [iOS](ios.md) as well. Most platform findings
(manifest, ATS, entitlements, backup, `FLAG_SECURE`) live there, not in Dart.

## Quick scan

| Pattern | Why | Usual severity |
|---|---|---|
| `--dart-define` / `String.fromEnvironment` holding secrets | Compiled into the binary | Critical if privileged |
| `.env` files bundled as assets (`flutter_dotenv` and similar) | Plain text in the app bundle | Critical if privileged |
| `SharedPreferences` / `Hive` box (unencrypted) with tokens | Plaintext storage | Medium |
| `badCertificateCallback = (...) => true` | Trust-all | Critical |
| `http://` base URLs, `Uri.http(` | Cleartext | High |
| `MqttServerClient` with `secure` not set, port 1883 | Cleartext MQTT | Critical |
| `print(` / `debugPrint(` / logger calls with token, email, mac, serial | Leak via device logs in release | Medium |
| `JavaScriptMode.unrestricted` plus `addJavaScriptChannel` on untrusted URLs | Bridge exposed to any page | High |
| `launchUrl(Uri.parse(param))` with deep link input | Open redirect, scheme abuse | Medium |
| `local_auth` `authenticate()` result as the only gate | Hookable boolean | High for secrets |
| Packages with `any` or wide version ranges, `pubspec.lock` not committed for the app | Unreproducible builds | Low to Medium |

## Secrets and configuration

```dart
// BAD: anyone can extract this from libapp.so or App.framework
const brokerPassword = String.fromEnvironment('BROKER_PASSWORD');

// GOOD: the backend issues a short-lived, per-user credential after login
final creds = await authApi.mqttCredentials();
```

- `--dart-define` and `--dart-define-from-file` are build configuration, not secret storage.
- `--obfuscate --split-debug-info=<dir>` renames Dart symbols in release builds. It does not hide string
  literals and is not a security control. Keep the symbol files private for crash symbolication.

## Secure storage

```dart
const storage = FlutterSecureStorage(
  iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock_this_device),
);
await storage.write(key: 'refresh_token', value: token);
```

- iOS backend is the Keychain; choose the accessibility class per [iOS](ios.md).
- Android backend uses an Android Keystore-protected key. Check the pinned plugin version and its changelog:
  older Android options were built on the deprecated `androidx.security:security-crypto` library, and
  major versions have changed the Android storage format, which needs a tested migration path.
- Exclude the plugin's Android preferences file from backup, or restored data will fail to decrypt.
- Large or structured sensitive data: encrypt with a key kept in secure storage, not in Dart constants.

## Network

```dart
// BAD
final client = HttpClient()..badCertificateCallback = (cert, host, port) => true;

// GOOD: default validation
final client = HttpClient();
```

Pinning with `dart:io` (only with a rotation plan):

```dart
SecurityContext pinnedContext(List<int> caPem) {
  final context = SecurityContext(withTrustedRoots: false);
  context.setTrustedCertificatesBytes(caPem); // pinned CA, ship current and backup
  return context;
}

final client = HttpClient(context: pinnedContext(caBytes));
```

- Dio on mobile uses `IOHttpClientAdapter`; apply the same `HttpClient` configuration through its
  `createHttpClient` callback rather than disabling checks.
- `network_security_config.xml` and ATS govern platform networking (WebViews, native plugins). `dart:io`
  `HttpClient` uses its own TLS stack and does not consult them, so Dart code must enforce `https` itself.
- MQTT (`mqtt_client`): set `secure = true`, port 8883, and keep certificate validation on.

```dart
// BAD
final client = MqttServerClient.withPort('broker.example.com', clientId, 1883);

// GOOD
final client = MqttServerClient.withPort('broker.example.com', clientId, 8883)
  ..secure = true;
```

## Local authentication

- `local_auth` returns a boolean. For secrets, store them behind platform key protection instead: Keychain
  access control on iOS and a `CryptoObject`-bound Keystore key on Android, exposed through a platform
  channel or a plugin that implements the crypto binding.
- Do not treat `canCheckBiometrics` or `isDeviceSupported` as proof that the user authenticated.

## WebView (`webview_flutter`)

```dart
controller
  ..setJavaScriptMode(JavaScriptMode.unrestricted)
  ..setNavigationDelegate(NavigationDelegate(
    onNavigationRequest: (request) {
      final uri = Uri.parse(request.url);
      return uri.scheme == 'https' && trustedHosts.contains(uri.host)
          ? NavigationDecision.navigate
          : NavigationDecision.prevent;
    },
  ))
  ..addJavaScriptChannel('Bridge', onMessageReceived: _onBridgeMessage)
  ..loadRequest(Uri.parse('https://app.example.com/help'));
```

- JavaScript channels are reachable by every page the controller loads; the navigation allowlist is the
  control that makes the bridge safe.
- Validate every message received on a channel as untrusted input.

## Deep links

- Routes from `go_router` or another router receive path and query parameters from other apps. Validate
  them before triggering actions (pairing a device, opening a URL, changing settings).
- Use verified App Links and Universal Links for anything carrying codes or tokens; configure them in the
  native projects.

## Logging

- `print` and `debugPrint` reach logcat and the device console in release builds.
- Route logs through one logger that drops debug output and redacts identifiers when `kReleaseMode` is true.

```dart
// BAD
debugPrint('connected to ${device.mac} with token $token');

// GOOD
appLog.info('connected to device ref=${device.pseudonymousId}'); // project logger, redacts in release
```

## Supply chain

- Commit `pubspec.lock` for apps. Review new packages for maintenance status, publisher and native code.
- Scan `pubspec.lock` together with the Android and iOS lock files; plugins pull native dependencies
  (Gradle artifacts, CocoaPods or SwiftPM packages) that also belong in the SBOM.
