# Android security reference

Load this for Kotlin, Java, `AndroidManifest.xml`, `res/xml/*` and Gradle files. Always audit the merged
release manifest (`app/build/intermediates/merged_manifests/release/...` or the APK Analyzer view), since
libraries add components and permissions.

## Quick scan

| Pattern | Why | Usual severity |
|---|---|---|
| `buildConfigField(` with key, secret, password, token | Secret in the APK | Critical if privileged |
| `usesCleartextTraffic="true"`, `cleartextTrafficPermitted="true"` | Cleartext HTTP | High, Critical for credentials |
| `<certificates src="user"` outside `debug-overrides` | Trusts user-installed CAs in release | High |
| `X509TrustManager` with empty `checkServerTrusted` | Trust-all | Critical |
| `hostnameVerifier { _, _ -> true }`, `ALLOW_ALL_HOSTNAME_VERIFIER` | Hostname check disabled | Critical |
| `tcp://` broker URI, port `1883` | Cleartext MQTT | Critical |
| `EncryptedSharedPreferences`, `EncryptedFile`, `MasterKey` | Deprecated library | Low (migrate), not a vulnerability by itself |
| `getSharedPreferences(` / DataStore keys named token, password, pin | Plaintext secrets | Medium |
| `MODE_WORLD_READABLE`, `MODE_WORLD_WRITEABLE` | Other apps read the file | High (throws on modern targets) |
| `getExternalStorageDirectory`, `getExternalFilesDir` with sensitive data | Shared or removable storage | Medium |
| `android:exported="true"` | Entry point for other apps | Review each |
| `android:allowBackup="true"` without `dataExtractionRules` | Tokens restorable to another device | Medium |
| `android:debuggable="true"` in a release manifest | Debugger and data access | High |
| `addJavascriptInterface(` | JS bridge | High if untrusted content can load |
| `setAllowFileAccess(true)`, `allowUniversalAccessFromFileURLs` | File theft via WebView | High |
| `PendingIntent.FLAG_MUTABLE`, implicit base intent | Hijackable PendingIntent | High |
| `getParcelableExtra<Intent>` then `startActivity` | Intent redirection | High |
| `Log.` / `println(` / `Timber.` with token, password, email, mac, serial | Leak via logcat or crash reports | Medium to High |
| `Cipher.getInstance("AES")`, `"AES/ECB/..."`, `"DES"` | Weak mode or default ECB | High |
| `MessageDigest.getInstance("MD5")` / `"SHA-1"` for security | Broken hash | Medium |
| `java.util.Random` for tokens, nonces, keys | Predictable | High |
| `isMinifyEnabled = false` in release | No shrinking or obfuscation | Low |

## Storage and keys

`androidx.security:security-crypto` is deprecated. Existing users need a one-time migration: read with the
old API, write with the new scheme, delete the old file, keep the old dependency only until migration ships.

Direct Android Keystore key (no extra library):

```kotlin
fun getOrCreateKey(alias: String): SecretKey {
    val ks = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
    (ks.getKey(alias, null) as? SecretKey)?.let { return it }
    val spec = KeyGenParameterSpec.Builder(
        alias, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
    )
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setKeySize(256)
        .build()
    return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        .apply { init(spec) }
        .generateKey()
}

// Encrypt: let the Keystore generate the IV, store iv + ciphertext together
val cipher = Cipher.getInstance("AES/GCM/NoPadding").apply { init(Cipher.ENCRYPT_MODE, key) }
val blob = cipher.iv + cipher.doFinal(plaintext)
```

Tink AEAD (keyset stored in its own preferences file, encrypted by an Android Keystore master key):

```kotlin
AeadConfig.register()
val aead: Aead = AndroidKeysetManager.Builder()
    .withSharedPref(context, "auth_keyset", "auth_keyset_prefs")
    .withKeyTemplate(KeyTemplates.get("AES256_GCM"))
    .withMasterKeyUri("android-keystore://auth_master_key")
    .build()
    .keysetHandle
    .getPrimitive(RegistryConfiguration.get(), Aead::class.java)

// Associated data binds the ciphertext to its slot, so it cannot be swapped into another key
val ciphertext = aead.encrypt(token.encodeToByteArray(), "refresh_token".encodeToByteArray())
```

- Older Tink versions use `keysetHandle.getPrimitive(Aead::class.java)`; match the pinned Tink version.
- Build the `Aead` once (it is thread-safe) and off the main thread; keyset loading touches disk and Keystore.
- `setIsStrongBoxBacked(true)` throws `StrongBoxUnavailableException` on devices without StrongBox; fall back.
- Keystore operations can be slow and can fail after OS updates or lock-screen changes; handle
  `KeyPermanentlyInvalidatedException` by re-authenticating the user, not by crashing.
- Room / SQLite with sensitive data: encrypt the fields that matter or use an encrypted database library
  with a Keystore-wrapped key.

## Backup

```xml
<!-- AndroidManifest.xml -->
<application
    android:allowBackup="true"
    android:dataExtractionRules="@xml/data_extraction_rules"
    android:fullBackupContent="@xml/backup_rules" ... >
```

```xml
<!-- res/xml/data_extraction_rules.xml (API 31+) -->
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="sharedpref" path="auth_keyset_prefs.xml" />
        <exclude domain="file" path="datastore/session.preferences_pb" />
    </cloud-backup>
    <device-transfer>
        <exclude domain="sharedpref" path="auth_keyset_prefs.xml" />
        <exclude domain="file" path="datastore/session.preferences_pb" />
    </device-transfer>
</data-extraction-rules>
```

`fullBackupContent` covers API 30 and below. Restored Tink keysets whose Keystore master key did not
travel cannot be decrypted; exclude them rather than crash on restore.

## Network

```xml
<!-- res/xml/network_security_config.xml -->
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <!-- Optional pinning, only with a rotation plan -->
    <domain-config>
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set expiration="2027-06-30">
            <pin digest="SHA-256">CURRENT_SPKI_BASE64=</pin>
            <pin digest="SHA-256">BACKUP_SPKI_BASE64=</pin>
        </pin-set>
    </domain-config>

    <!-- Debug builds only: allow a proxy CA for testing -->
    <debug-overrides>
        <trust-anchors>
            <certificates src="user" />
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

- After the `pin-set` expiration date, pins are no longer enforced; the app keeps working on normal validation.
- OkHttp `CertificatePinner` pins apply in addition to platform validation; same backup-pin rules apply.
- MQTT (Paho, HiveMQ client): `ssl://` / TLS on 8883, hostname verification on, credentials per device or
  per user, never a shared broker password compiled into the app. Prefer client certificates or short-lived
  tokens issued by the backend.

## IPC

- Since Android 12 every component with an intent filter must declare `android:exported`. Audit each `true`.
- Exported components that need to be reachable only by your own apps use a `signature` protection level
  permission.
- Read extras defensively: `IntentCompat.getParcelableExtra(intent, key, Foo::class.java)`, validate every field.
- Never forward an `Intent` received from another app to `startActivity` or `sendBroadcast`.
- Runtime receivers: `ContextCompat.registerReceiver(..., ContextCompat.RECEIVER_NOT_EXPORTED)` unless other
  apps must send to it.
- App Links: `<intent-filter android:autoVerify="true">` with `https` scheme and a matching
  `/.well-known/assetlinks.json` listing the release signing certificate fingerprint.

```kotlin
// BAD: mutable, implicit PendingIntent
PendingIntent.getActivity(ctx, 0, Intent("com.example.OPEN"), PendingIntent.FLAG_MUTABLE)

// GOOD
PendingIntent.getActivity(
    ctx, 0, Intent(ctx, DetailActivity::class.java), PendingIntent.FLAG_IMMUTABLE,
)
```

## WebView

- `javaScriptEnabled` only when needed. No `addJavascriptInterface` on a WebView that can reach
  third-party or user-controlled URLs; every `@JavascriptInterface` method is callable by any frame.
- Prefer `WebViewCompat.addWebMessageListener` with an explicit allowed-origin set.
- `shouldOverrideUrlLoading` allowlists hosts and sends everything else to the browser.
- Local content through `WebViewAssetLoader` over `https://appassets.androidplatform.net`, with file access off.
- No `onReceivedSslError { handler.proceed() }`.

## Biometrics

```kotlin
val spec = KeyGenParameterSpec.Builder("vault", KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG) // API 30+
    .setInvalidatedByBiometricEnrollment(true)
    .build()

val promptInfo = BiometricPrompt.PromptInfo.Builder()
    .setTitle(getString(R.string.unlock_title))
    .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG)
    .setNegativeButtonText(getString(R.string.cancel))
    .build()

biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
```

- Timeout `0` means every use of the key needs a fresh authentication.
- Decrypt or sign inside `onAuthenticationSucceeded` with `result.cryptoObject`; the GATT or network call
  that follows must not run on the assumption that a flag was set.

## UI and side channels

- `FLAG_SECURE` on windows showing credentials, OTPs, payment or health data. In Compose apps set it on the
  Activity window or the dialog window.
- `Activity.setRecentsScreenshotEnabled(false)` (API 33+) keeps the recents thumbnail blank.
- Clipboard: mark copied secrets sensitive with `ClipDescription.EXTRA_IS_SENSITIVE` (API 33+).
- Notifications with sensitive content use `VISIBILITY_PRIVATE` or a public version.

## Release build

```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}
```

```proguard
# Strip debug and verbose logging from release
-assumenosideeffects class android.util.Log {
    public static int v(...);
    public static int d(...);
}
```

- Stripping log calls does not remove string building done before the call in all cases; do not log
  secrets in the first place.
- Play Integrity standard request: prepare a token provider once, request a token per sensitive action with
  a `requestHash` of the action, send it to the backend, decrypt and evaluate the verdict there.
- SBOM: the CycloneDX Gradle plugin (`org.cyclonedx.bom`) generates a CycloneDX SBOM from resolved
  dependencies. Gradle dependency verification (`gradle/verification-metadata.xml`) and dependency locking
  protect against tampered or drifting artifacts.
