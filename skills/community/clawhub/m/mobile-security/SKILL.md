---
name: mobile-security
description: "Audits Android, iOS and Flutter apps against OWASP MASVS v2 and the Mobile Top 10 2024: hardcoded secrets, insecure storage (Keystore, Keychain), TLS and pinning, exported components, deep links, WebViews, biometrics, logging of personal data and supply chain. Reports findings with MASVS IDs, severity and evidence. Use for security reviews, pentest prep, or changes to auth, crypto, storage, network or IPC code."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile security audit

Audit a mobile app the way a mobile pentester and a compliance reviewer would together: find what an
attacker on the network, a malicious app on the device, or someone holding an unlocked or rooted phone can
actually exploit, map it to an OWASP MASVS v2 control, and show the smallest fix that closes it.

## When to use

- The user asks for a security audit, security review, MASVS or OWASP Mobile Top 10 check, or pentest prep.
- A change touches credentials, tokens, crypto, local storage, networking, TLS, pinning, IPC, deep links,
  WebViews, biometrics, logging or third-party SDKs.
- An IoT companion app talks to devices over BLE, MQTT or HTTPS and handles device identifiers.
- Preparing evidence for GDPR, Cyber Resilience Act, RED Delegated Act (EN 18031) or ETSI EN 303 645 reviews.

Not for: general code quality or concurrency review (use `mobile-code-review`), or CI pipeline setup
(use `mobile-ci-cd`, though this skill flags missing dependency scanning and SBOM steps).

## Workflow

1. Define scope and threat model before reading code.
   - What is sensitive: credentials, tokens, keys, health or location data, device identifiers, payment data.
   - Which attackers matter: network attacker (public Wi-Fi), malicious app on the same device, lost or
     stolen unlocked device, user with a rooted or jailbroken device, reverse engineer of the binary.
   - Which backends and devices are under the developer's control (relevant for pinning and attestation).
2. Inventory the attack surface and load the matching references:
   [Android](references/android.md), [iOS](references/ios.md), [Flutter](references/flutter.md),
   [MASVS controls and Top 10 map](references/masvs-map.md).
   For CRA, RED delegated act / EN 18031 or GDPR questions, hand the findings to `mobile-eu-compliance`.
   - Android: merged release manifest, network security config, backup rules, release build type, catalogs.
   - iOS: `Info.plist`, entitlements, `PrivacyInfo.xcprivacy`, `.xcconfig`, lock files. Flutter: both of these.
3. Run the quick-scan patterns from the references. Each hit is a candidate, not a finding.
4. Walk the MASVS categories in order: STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, RESILIENCE, PRIVACY.
   Read the full code path for every candidate, not just the matching line.
5. Judge the release build: check flavor manifests, `debug-overrides`, `#if DEBUG` and `kDebugMode` guards.
   A debug-only issue is Low at most, unless it can ship.
6. Verify each finding: reachable in release? Mitigated elsewhere (server check, interceptor, OS default)?
   If static review cannot confirm it, list it under "Needs dynamic verification", not as a finding.
7. Rate severity, assign one MASVS v2 control ID and the matching Mobile Top 10 2024 item, and write a fix.
   Only use control IDs listed in [MASVS controls](references/masvs-map.md).
8. Report using the output format, including what was not checked. Do not edit files unless asked.

## Severity levels

| Severity | Definition | Examples |
|---|---|---|
| Critical | Exploitable remotely or at scale with no special access; compromises accounts, keys or many users' data | Backend admin key in the binary, trust-all `TrustManager`, cleartext login, MQTT credentials over port 1883 |
| High | Exploitable with realistic preconditions (same network, malicious app installed, brief physical access); exposes sensitive data or bypasses auth | Exported component leaking tokens, unvalidated deep link loading any URL in a WebView with a JS bridge, boolean-only biometric gate on secrets |
| Medium | Needs strong preconditions (root, jailbreak, backup extraction) or weakens defense in depth | Tokens in plaintext app storage, sensitive screens without screenshot protection, `allowBackup` with tokens |
| Low | Hardening gap with little direct impact | No obfuscation, verbose non-sensitive logs, missing CT awareness, debug-only issue |

Rate by impact and likelihood in this app's threat model. A finding without a realistic attacker is not
High because a checklist says so.

## Rules

### 1. No secrets in the app package (MASVS-CRYPTO-2, MASVS-AUTH-1, M1)

Everything in an APK, IPA or Flutter bundle is readable: `BuildConfig`, `strings.xml`, `Info.plist`,
`.xcconfig`, assets, `--dart-define` values. Obfuscation does not change that.

```kotlin
// BAD: ends up as a constant in the APK
buildConfigField("String", "PAYMENTS_SECRET", "\"sk_live_...\"")

// GOOD: app gets a short-lived, user-scoped token from your backend after login
val token = authRepository.sessionToken()
```

```swift
// BAD: Info.plist and xcconfig values ship in plain text
let key = Bundle.main.object(forInfoDictionaryKey: "BROKER_PASSWORD") as? String
```

- Restricted public identifiers (OAuth client ID, Maps key locked to package and signing cert) are fine.
  Anything that grants privilege on its own (server keys, signing keys, shared broker passwords) is not.
- Check git history and CI config too; a secret ever committed must be rotated, not just deleted.

### 2. Sensitive data at rest uses platform key stores (MASVS-STORAGE-1, MASVS-CRYPTO-2, M9)

`androidx.security:security-crypto` (`EncryptedSharedPreferences`, `EncryptedFile`, `MasterKey`) is
deprecated. Do not add it; plan migration for existing users. Replacement: an Android Keystore key, either
directly with `Cipher` or via Tink AEAD, with ciphertext stored in DataStore or a file.

```kotlin
// BAD: plaintext token in SharedPreferences or DataStore
prefs.edit { putString("refresh_token", token) }

// GOOD: Tink AEAD, keyset wrapped by an Android Keystore key (setup in references/android.md)
val ciphertext = aead.encrypt(token.encodeToByteArray(), "refresh_token".encodeToByteArray())
dataStore.edit { it[REFRESH_TOKEN] = Base64.encodeToString(ciphertext, Base64.NO_WRAP) }
```

```swift
// BAD
UserDefaults.standard.set(token, forKey: "refreshToken")

// GOOD: Keychain, not migrated to other devices or backups
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrService as String: "com.example.auth",
    kSecAttrAccount as String: "refreshToken",
    kSecValueData as String: Data(token.utf8),
    kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
]
let status = SecItemAdd(query as CFDictionary, nil)
```

```dart
// BAD
await prefs.setString('refresh_token', token);

// GOOD
const storage = FlutterSecureStorage(
  iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock_this_device),
);
await storage.write(key: 'refresh_token', value: token);
```

- Pick the strictest Keychain accessibility class the feature allows; background refresh needs `AfterFirstUnlock`.
- Never roll custom crypto: no ECB, no static IVs, no keys derived from device IDs, no `Random` for secrets.

### 3. Sensitive data does not leak through side channels (MASVS-STORAGE-2, MASVS-PLATFORM-3, M9)

Logs, backups, screenshots, the app switcher snapshot, clipboard and keyboard caches all leak.

```kotlin
// BAD: Log.d survives in release unless stripped
Log.d("Auth", "login ok token=$token user=$email")

// GOOD: no secrets or personal data in logs; strip debug logs in release with R8 rules
Log.d("Auth", "login ok")
```

```swift
// BAD: explicitly public in the unified log
logger.info("token \(token, privacy: .public)")

// GOOD
logger.info("login ok for user \(userId, privacy: .private(mask: .hash))")
```

- Android: `window.setFlags(FLAG_SECURE, FLAG_SECURE)` on screens with credentials, OTPs, payment or health data.
- iOS has no API to block screenshots; cover sensitive content when `scenePhase` leaves `.active`.
- Android backup: exclude token and keyset files via `dataExtractionRules` and `fullBackupContent`, or disable
  backup. Keystore keys never leave the device, so restored ciphertext cannot be decrypted; handle that path.

### 4. All traffic uses TLS with platform validation (MASVS-NETWORK-1, M5)

```xml
<!-- BAD -->
<application android:usesCleartextTraffic="true" ... >

<!-- GOOD: res/xml/network_security_config.xml -->
<network-security-config>
    <base-config cleartextTrafficPermitted="false" />
</network-security-config>
```

```kotlin
// BAD: disables certificate and hostname validation for everything
OkHttpClient.Builder()
    .sslSocketFactory(trustAllFactory, trustAllManager)
    .hostnameVerifier { _, _ -> true }

// GOOD: platform defaults
OkHttpClient.Builder().build()
```

- iOS: no `NSAllowsArbitraryLoads`; no `.useCredential` for a server trust that skipped `SecTrustEvaluateWithError`.
- Dart: no `badCertificateCallback` returning `true`. `dart:io` does not apply ATS or the Android network config.

IoT and MQTT: TLS always, including on "internal" networks. Never cleartext brokers.

```kotlin
// BAD
MqttClient("tcp://broker.example.com:1883", clientId, MemoryPersistence())

// GOOD: TLS, per-device or per-user credentials, broker-side topic ACLs
MqttClient("ssl://broker.example.com:8883", clientId, MemoryPersistence())
```

- BLE: CRC16 or CRC32 detects corruption, not tampering. Commands that change device state need an
  authenticated channel (LE Secure Connections pairing plus app-layer authentication, or a MAC/AEAD).

### 5. Pinning only with a rotation plan (MASVS-NETWORK-2, M5)

Default: standard CA validation, which Certificate Transparency enforcement strengthens where the platform
applies it. Pin only when the threat model requires it (high-value targets, controlled backends, IoT
provisioning endpoints) and the team owns key rotation.

```kotlin
// BAD: one pin, no backup; the app stops connecting when the server key rotates
.add("api.example.com", "sha256/<current-spki>")

// GOOD: SPKI pins for current key and a pre-generated backup key, with monitoring and a release plan
CertificatePinner.Builder()
    .add("api.example.com", "sha256/<current-spki>")
    .add("api.example.com", "sha256/<backup-spki>")
    .build()
```

- Android `<pin-set>` needs an `expiration` and a backup pin; iOS uses `NSPinnedDomains`. Never pin
  third-party endpoints you do not control (analytics, CDNs, identity providers).
- Pinning is bypassable on a rooted device; it protects users from network attackers, not the app from its user.

### 6. Biometrics unlock a key, not a boolean (MASVS-AUTH-2, MASVS-AUTH-3, M3)

A success callback alone can be hooked on a rooted or jailbroken device. Bind the secret to authentication.

```kotlin
// BAD: boolean gate
biometricPrompt.authenticate(promptInfo)
// onAuthenticationSucceeded { showVault() }

// GOOD: Keystore key with setUserAuthenticationRequired(true); only an authenticated Cipher decrypts
biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
// onAuthenticationSucceeded { result -> result.cryptoObject?.cipher?.doFinal(encryptedToken) }
```

```swift
// BAD: boolean gate
if try await LAContext().evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Unlock") {
    showVault()
}

// GOOD: Keychain item protected by access control; the OS releases it only after biometry
let access = SecAccessControlCreateWithFlags(
    nil, kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly, .biometryCurrentSet, nil)
// add with kSecAttrAccessControl: access; read with kSecUseAuthenticationContext off the main thread
```

- `BIOMETRIC_STRONG` for crypto-bound auth. `setInvalidatedByBiometricEnrollment(true)` and `.biometryCurrentSet`
  invalidate the key on new enrollment. iOS requires `NSFaceIDUsageDescription` in `Info.plist`.

### 7. Sessions are controlled by the server (MASVS-AUTH-1, M3)

- OAuth / OIDC uses the system browser (Custom Tabs, `ASWebAuthenticationSession`) with PKCE, not an
  embedded WebView. Passkeys via Credential Manager or `AuthenticationServices` where supported.
- Short-lived access tokens, refresh tokens in secure storage, server-side revocation on logout.
- Authorization is enforced by the backend. A hidden button or a local `isAdmin` flag is not access control.

```kotlin
// BAD: role decided on the client
if (prefs.getBoolean("is_admin", false)) showAdminPanel()

// GOOD: UI hint only; every admin API call is authorized server-side
if (session.claims.roles.contains("admin")) showAdminPanel()
```

### 8. IPC entry points are minimal and validate input (MASVS-PLATFORM-1, MASVS-CODE-4, M4, M8)

```xml
<!-- BAD: internal screen reachable by any app -->
<activity android:name=".DebugMenuActivity" android:exported="true" />

<!-- GOOD -->
<activity android:name=".DebugMenuActivity" android:exported="false" />
```

```kotlin
// BAD: deep link parameter goes straight into a privileged action
webView.loadUrl(intent.data?.getQueryParameter("url").orEmpty())

// GOOD: allowlist scheme and host
val target = intent.data?.getQueryParameter("url")?.toUri()
if (target?.scheme == "https" && target.host in trustedHosts) webView.loadUrl(target.toString())
```

- iOS `onOpenURL` / `application(_:continue:)` and Flutter routers validate the same way before routing.
- Custom URL schemes can be claimed by any app. Use verified App Links (`android:autoVerify="true"` plus
  `assetlinks.json`) and Universal Links (Associated Domains) for anything carrying tokens or codes.
- Never launch an `Intent` taken from another app's extras (intent redirection).
- `PendingIntent` uses `FLAG_IMMUTABLE` unless mutability is required, with an explicit target component.
- Content providers: `exported="false"` or signature-level permissions; no raw path joins on `openFile`.

### 9. WebViews load trusted content and expose minimal bridges (MASVS-PLATFORM-2, M4)

```kotlin
// BAD: JS bridge on any page the WebView navigates to
webView.settings.javaScriptEnabled = true
webView.addJavascriptInterface(TokenBridge(session), "Android")
webView.loadUrl(urlFromServerOrDeepLink)

// GOOD: origin-scoped message listener, navigation restricted to an allowlist
if (WebViewFeature.isFeatureSupported(WebViewFeature.WEB_MESSAGE_LISTENER)) {
    WebViewCompat.addWebMessageListener(webView, "bridge", setOf("https://app.example.com"), listener)
}
```

- iOS: every `WKScriptMessageHandler` checks `message.frameInfo.securityOrigin` and `isMainFrame`.
- Keep `allowFileAccess`, `allowFileAccessFromFileURLs` and `allowUniversalAccessFromFileURLs` off.
  Serve local content through `WebViewAssetLoader`.
- External links open in the browser, not inside the app WebView.

### 10. Dependencies are known and scanned (MASVS-CODE-3, M2)

```kotlin
// BAD: dynamic version, unreproducible and unscannable
implementation("com.example:sdk:+")

// GOOD
implementation(libs.example.sdk)
```

- Commit lock files (`Package.resolved`, `pubspec.lock`, `Podfile.lock`); scan them in CI (OSV-Scanner,
  OWASP Dependency-Check, Dependabot or Renovate) and fail on Critical.
- Generate a CycloneDX or SPDX SBOM per release and archive it with the build.
- MASVS-CODE-1: no unjustified support for unpatched OS versions. MASVS-CODE-2: a forced-update path
  exists (Play In-App Updates immediate flow, or a server-driven minimum version).

### 11. Obfuscation and attestation raise cost; the server decides (MASVS-RESILIENCE-1 to 4, M7)

R8, Swift symbol stripping and Flutter `--obfuscate` slow reverse engineering. None is a security boundary.

```kotlin
// BAD: local check is the only control, patched out in minutes
if (RootChecker.isRooted()) finish()

// GOOD: attestation token sent with the sensitive request; backend verifies and decides
val token = integrityTokenProvider.request(
    StandardIntegrityTokenRequest.builder().setRequestHash(requestHash).build()).await()
api.transfer(request, integrityToken = token.token())
```

- Android: Play Integrity API, verdict decrypted and checked on the server. SafetyNet Attestation is gone.
- iOS: App Attest (`DCAppAttestService`) with server-side attestation and assertion verification;
  DeviceCheck for per-device bits.
- Release builds: `isMinifyEnabled = true`, `android:debuggable` not set, no `get-task-allow` in distribution.

### 12. Collect the minimum and treat device identifiers as personal data (MASVS-PRIVACY-1 to 4, M6)

```kotlin
// BAD: telemetry carries direct identifiers it does not need
Telemetry(mac = device.macAddress, serial = device.serial, email = user.email, rssi = rssi)

// GOOD: only what the feature needs, pseudonymous ID rotated per installation
Telemetry(installId = installId, firmware = device.firmwareVersion, rssi = rssi)
```

- MAC addresses, serials, IMEI, advertising IDs and IP addresses are personal data under GDPR when linkable
  to a person; pseudonymised data is still personal data.
- Request runtime permissions at point of use; prefer coarse location, `neverForLocation` for BLE scans
  on Android 12+, and the photo picker over broad media access.
- iOS: `PrivacyInfo.xcprivacy` declares collected data and required-reason APIs, consistent with the
  App Store privacy labels. Android: the Play Data safety form matches what the code does.

## Anti-patterns

- Reporting checklist items without an attacker and a path. "No root detection" is not a finding by itself.
- Auditing the debug build or a single file and calling the app secure.
- Recommending pinning by default without a rotation, backup-pin and monitoring plan.
- Treating R8, obfuscation, root or jailbreak detection as a fix for a server-side authorization flaw.
- "Encrypting" with a key hardcoded next to the ciphertext, or moving a secret to native code and calling it hidden.
- Suggesting `EncryptedSharedPreferences` for new code, or CRC as protection against an attacker.
- Inventing MASVS control IDs, CVE numbers or legal deadlines. If unsure, say so.
- Dumping real secrets found during the audit into the report. Show the location and a redacted prefix only.

## Checklist

- [ ] Threat model and data classification written down before findings
- [ ] Release manifest, `Info.plist`, entitlements, network config and build types reviewed
- [ ] No privileged secrets in code, resources, `BuildConfig`, `Info.plist`, `--dart-define` or git history
- [ ] Tokens and keys in Keystore / Keychain-backed storage; no new `security-crypto` usage
- [ ] Keychain accessibility class and Android backup rules checked
- [ ] No secrets or personal data in release logs; `FLAG_SECURE` or snapshot cover on sensitive screens
- [ ] Cleartext disabled; no trust-all managers, hostname verifiers or `badCertificateCallback`
- [ ] MQTT and other IoT channels use TLS; BLE commands authenticated, not only CRC-checked
- [ ] Pinning, if present, has backup pins, expiry and a rotation plan
- [ ] Biometric auth bound to a `CryptoObject` or Keychain access control
- [ ] OAuth via system browser with PKCE; authorization enforced server-side
- [ ] Every exported component, deep link and App / Universal Link validated
- [ ] WebView bridges origin-scoped; file access off; untrusted URLs not loaded
- [ ] Dependencies pinned and scanned in CI, SBOM per release, attestation verified server-side if used
- [ ] Telemetry minimised; device identifiers handled as personal data
- [ ] "Not checked" section lists everything outside static review

## Output format

~~~markdown
## Security audit: <app / module / MR>

Scope: <files, modules, commit>. Platforms: <Android | iOS | Flutter>. Build reviewed: <release variant>.
Threat model: <assets, attackers considered>.

### Findings

1. [Critical] MASVS-NETWORK-1 / M5 -- Trust-all TrustManager in production client
   Evidence: app/src/main/java/com/example/net/HttpModule.kt:42
   Impact: any network attacker can read and modify all API traffic, including login credentials.
   Fix:
   ```kotlin
   OkHttpClient.Builder().build() // remove custom sslSocketFactory and hostnameVerifier
   ```

2. [High] MASVS-AUTH-2 / M3 -- Biometric unlock is a boolean gate
   Evidence: ios/App/Vault/VaultUnlock.swift:88
   Impact: ...
   Fix: ...

### Needs dynamic verification
- <items that static review could not confirm, for example "pinning behaviour on proxy interception">

### Summary

| MASVS category | Critical | High | Medium | Low | Notes |
|---|---|---|---|---|---|
| STORAGE | 0 | 0 | 1 | 0 | |
| CRYPTO | 0 | 0 | 0 | 0 | |
| AUTH | 0 | 1 | 0 | 0 | |
| NETWORK | 1 | 0 | 0 | 0 | |
| PLATFORM | 0 | 0 | 0 | 0 | |
| CODE | 0 | 0 | 0 | 1 | |
| RESILIENCE | 0 | 0 | 0 | 0 | |
| PRIVACY | 0 | 0 | 1 | 0 | |

### Not checked
- Backend authorization and API security
- Runtime behaviour (proxy interception, Frida, rooted / jailbroken device testing)
- Compiled binary (only source reviewed)
- <modules, flavors or SDKs out of scope>

### Compliance notes (if EU market or IoT)
- <findings relevant to the CRA, EN 18031 or GDPR; map them with `mobile-eu-compliance`>
~~~

Rules for the report:
- One root cause is one finding; list extra locations under Evidence.
- Every Critical and High has a concrete fix snippet or config change.
- Redact any real secret found: show the file, line and first four characters only, and say "rotate".

## Related skills

- `mobile-eu-compliance` -- maps these findings to CRA, RED / EN 18031 and GDPR requirements
- `mobile-code-review` -- general correctness, concurrency and lifecycle review
- `mobile-ci-cd` -- wiring dependency scanning, SBOM generation and signing into the pipeline
- `mobile-kotlin`, `mobile-java`, `mobile-swift`, `mobile-flutter` -- platform idioms behind the fixes
- `mobile-merge-request` -- describing security fixes and permission or entitlement changes in the MR
- `mobile-ble` -- pairing, command authentication and firmware update on the device link
- `mobile-release` -- privacy manifests, Data safety and store privacy declarations
