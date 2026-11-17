# iOS security reference

Load this for Swift, Objective-C, `Info.plist`, `.entitlements`, `.xcconfig` and `PrivacyInfo.xcprivacy`.
Call out every `Info.plist` and entitlement change explicitly in the report; they affect App Review,
signing and provisioning.

## Quick scan

| Pattern | Why | Usual severity |
|---|---|---|
| Keys like `API_SECRET`, `PASSWORD`, `TOKEN` in `Info.plist` or `.xcconfig` | Secret in the IPA | Critical if privileged |
| `NSAllowsArbitraryLoads` = YES | ATS disabled globally | High, needs App Review justification |
| `NSExceptionAllowsInsecureHTTPLoads`, `NSExceptionMinimumTLSVersion` lowered | Cleartext or weak TLS for a domain | High |
| `.useCredential` with `serverTrust` and no `SecTrustEvaluateWithError` | Trust-all | Critical |
| `UserDefaults` / `@AppStorage` with token, password, PIN | Plaintext plist | Medium |
| `kSecAttrAccessibleAlways` / `kSecAttrAccessibleAlwaysThisDeviceOnly` | Deprecated, readable while locked | Medium |
| `evaluatePolicy(` result used as the only gate | Hookable boolean | High for secrets or payments |
| `print(`, `NSLog(`, `privacy: .public` with personal data | Leak via device logs | Medium |
| `WKScriptMessageHandler` without origin check | Any frame calls native code | High |
| `loadFileURL(_:allowingReadAccessTo:)` with a broad directory | Web content reads app files | Medium |
| `open(url)` or routing from `onOpenURL` without validation | Deep link abuse | Medium to High |
| `CC_MD5`, `Insecure.MD5`, `Insecure.SHA1` for security | Broken hash | Medium |
| `get-task-allow` = true in a distribution entitlement | Debuggable release | High |
| CocoaMQTT / other MQTT clients with SSL disabled or port 1883 | Cleartext MQTT | Critical |

## Keychain accessibility classes

| Class | Readable when | Migrates to new device | Use for |
|---|---|---|---|
| `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` | Unlocked, only while a passcode is set | No | Highest-value secrets, biometric-bound items |
| `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` | Unlocked | No | Secrets used only in the foreground |
| `kSecAttrAccessibleWhenUnlocked` | Unlocked | Yes | Default; foreground secrets that may migrate |
| `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` | After first unlock until reboot | No | Tokens needed by background refresh, BLE restoration, push handling |
| `kSecAttrAccessibleAfterFirstUnlock` | After first unlock until reboot | Yes | Background secrets that may migrate |

- `ThisDeviceOnly` items are not restored onto a different device from a backup.
- Keychain items can survive app deletion. Clear stale credentials on first launch after install
  (detect with a flag in `UserDefaults`, which is removed on uninstall).
- Shared access across your apps uses a Keychain access group entitlement; keep it as narrow as possible.

## Biometric-bound Keychain item

```swift
func storeVaultKey(_ secret: Data) throws {
    var error: Unmanaged<CFError>?
    guard let access = SecAccessControlCreateWithFlags(
        nil, kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly, .biometryCurrentSet, &error
    ) else { throw error!.takeRetainedValue() as Error }

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: "com.example.vault",
        kSecAttrAccount as String: "vaultKey",
        kSecAttrAccessControl as String: access,
        kSecValueData as String: secret,
    ]
    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else { throw KeychainError(status: status) }
}

// Blocks while the system prompt is shown: never call on the main thread.
func readVaultKey() throws -> Data {
    let context = LAContext()
    context.localizedReason = String(localized: "Unlock your vault")
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: "com.example.vault",
        kSecAttrAccount as String: "vaultKey",
        kSecReturnData as String: true,
        kSecUseAuthenticationContext as String: context,
    ]
    var result: CFTypeRef?
    let status = SecItemCopyMatching(query as CFDictionary, &result)
    guard status == errSecSuccess, let data = result as? Data else { throw KeychainError(status: status) }
    return data
}
```

- `.biometryCurrentSet` invalidates the item when enrolled biometrics change; `.biometryAny` does not.
- `.userPresence` allows passcode fallback; choose deliberately and document it.
- For signing use cases, create a Secure Enclave key (`kSecAttrTokenIDSecureEnclave`) with the same access
  control and have the server verify signatures.
- `NSFaceIDUsageDescription` is required in `Info.plist` when Face ID is used.

## Files and data protection

```swift
try data.write(to: url, options: [.atomic, .completeFileProtection])
```

- Default file protection is `completeUntilFirstUserAuthentication`. Use `.complete` for sensitive files
  that are not needed in the background.
- Exclude caches and regenerable data from backup with `isExcludedFromBackup` on `URLResourceValues`.
- Core Data / SwiftData stores inherit file protection; set it on the store file when it holds sensitive data.

## Network

```xml
<!-- Info.plist: ATS on by default; pin only domains you control -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSPinnedDomains</key>
    <dict>
        <key>api.example.com</key>
        <dict>
            <key>NSIncludesSubdomains</key>
            <true/>
            <key>NSPinnedCAIdentities</key>
            <array>
                <dict>
                    <key>SPKI-SHA256-BASE64</key>
                    <string>CURRENT_CA_SPKI_BASE64=</string>
                </dict>
                <dict>
                    <key>SPKI-SHA256-BASE64</key>
                    <string>BACKUP_CA_SPKI_BASE64=</string>
                </dict>
            </array>
        </dict>
    </dict>
</dict>
```

- Custom trust evaluation must call `SecTrustEvaluateWithError` and only then compare pins.
- Apple platforms require Certificate Transparency for publicly trusted TLS certificates, so standard
  validation already rejects many mis-issued certificates.
- ATS exceptions in `Info.plist` need a justification at App Review; local-network IoT devices are a valid
  case only for the specific local domain or `NSAllowsLocalNetworking`, never a global exception.
- Local network access to IoT devices needs `NSLocalNetworkUsageDescription`.

## WebView

```swift
let config = WKWebViewConfiguration()
config.defaultWebpagePreferences.allowsContentJavaScript = needsJavaScript
config.userContentController.add(handler, name: "bridge")

func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction) async -> WKNavigationActionPolicy {
    guard let host = action.request.url?.host, trustedHosts.contains(host) else {
        if let url = action.request.url { _ = await UIApplication.shared.open(url) }
        return .cancel
    }
    return .allow
}
```

- Every `WKScriptMessage` handler checks `frameInfo.isMainFrame` and `frameInfo.securityOrigin` before acting.
- OAuth and SSO use `ASWebAuthenticationSession`, not a `WKWebView` the app can read.

## Logging

- `os.Logger` redacts dynamic interpolations by default in release logs. Never mark tokens, emails, device
  identifiers or locations `privacy: .public`.
- `print` and `NSLog` output reaches the device console; remove or guard them.
- Crash reporters and analytics SDKs: check breadcrumbs and custom keys for personal data.

## UI

- Hide sensitive content when the scene is inactive, so the app switcher snapshot is clean:

```swift
.overlay { if scenePhase != .active { PrivacyCover() } }
```

- Secure text fields (`SecureField`) for passwords and PINs; set `textContentType` so autofill works and
  the keyboard does not learn secrets.
- `UIPasteboard`: use `setItems(_:options:)` with `.localOnly` and `.expirationDate` for copied secrets.

## Integrity and attestation

- App Attest: `DCAppAttestService.shared.isSupported`, `generateKey()`, `attestKey(_:clientDataHash:)` once,
  then `generateAssertion(_:clientDataHash:)` per sensitive request. The server verifies the attestation,
  stores the public key and checks assertion counters.
- Requires the App Attest entitlement (`com.apple.developer.devicecheck.appattest-environment`); flag it as
  an entitlement and provisioning change.
- Jailbreak detection is advisory only; never rely on it as the sole control.

## Privacy

- `PrivacyInfo.xcprivacy` lists collected data types and required-reason API usage, and third-party SDKs ship
  their own manifests. Check consistency with the App Store privacy label.
- Bluetooth needs `NSBluetoothAlwaysUsageDescription`; ask only when the user starts a BLE feature.
- `identifierForVendor` is still an identifier; treat it as personal data in telemetry.
