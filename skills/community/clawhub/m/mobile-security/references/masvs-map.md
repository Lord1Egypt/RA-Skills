# MASVS v2 controls and Mobile Top 10 map

Load this before assigning control IDs. Use only the IDs in this table. MASVS v2 removed the old v1
levels (L1, L2, R); use MAS testing profiles from the MASTG if the user asks for levels.

## MASVS v2 controls

| Control | Statement (short) | Typical findings |
|---|---|---|
| MASVS-STORAGE-1 | The app securely stores sensitive data | Tokens in SharedPreferences, UserDefaults, plain files, SQLite without protection |
| MASVS-STORAGE-2 | The app prevents leakage of sensitive data | Secrets in logs, backups, screenshots, app switcher snapshot, clipboard, keyboard cache, crash reports |
| MASVS-CRYPTO-1 | The app employs current strong cryptography and uses it according to industry best practices | ECB, static IV, MD5 or SHA-1 for security, `java.util.Random` for secrets, custom crypto |
| MASVS-CRYPTO-2 | The app performs key management according to industry best practices | Hardcoded keys, keys derived from device IDs, keys outside Keystore / Keychain |
| MASVS-AUTH-1 | The app uses secure authentication and authorization protocols and follows the relevant best practices | Client-side role checks, long-lived tokens, OAuth in embedded WebView, no PKCE, shared credentials in app |
| MASVS-AUTH-2 | The app performs local authentication securely according to the platform best practices | Boolean-only biometric gate, weak fallback, key not invalidated on enrollment change |
| MASVS-AUTH-3 | The app secures sensitive operations with additional authentication | Payments, device unlock commands or credential changes without step-up auth |
| MASVS-NETWORK-1 | The app secures all network traffic according to the current best practices | Cleartext, trust-all managers, disabled hostname checks, ATS exceptions, cleartext MQTT |
| MASVS-NETWORK-2 | The app performs identity pinning for all remote endpoints under the developer's control | Pinning missing where the threat model needs it, or pinning without backup pins |
| MASVS-PLATFORM-1 | The app uses IPC mechanisms securely | Exported components, intent redirection, mutable PendingIntents, unvalidated deep links, providers |
| MASVS-PLATFORM-2 | The app uses WebViews securely | JS bridges on untrusted content, file access enabled, loading arbitrary URLs |
| MASVS-PLATFORM-3 | The app uses the user interface securely | No screenshot protection on sensitive screens, overlay or tapjacking, sensitive data in notifications |
| MASVS-CODE-1 | The app requires an up-to-date platform version | Very old `minSdk` or deployment target without justification |
| MASVS-CODE-2 | The app has a mechanism for enforcing app updates | No way to block a known-vulnerable version |
| MASVS-CODE-3 | The app only uses software components without known vulnerabilities | Vulnerable or unmaintained dependencies, no scanning, dynamic versions |
| MASVS-CODE-4 | The app validates and sanitizes all untrusted inputs | Deep link params, IPC extras, server or BLE payloads used without validation, SQL or path injection |
| MASVS-RESILIENCE-1 | The app validates the integrity of the platform | No attestation where the threat model needs it |
| MASVS-RESILIENCE-2 | The app implements anti-tampering mechanisms | No signature or integrity verification for high-value apps |
| MASVS-RESILIENCE-3 | The app implements anti-static analysis mechanisms | No obfuscation in release, debug symbols shipped |
| MASVS-RESILIENCE-4 | The app implements anti-dynamic analysis techniques | Debuggable release build, no debugger or instrumentation awareness where required |
| MASVS-PRIVACY-1 | The app minimizes access to sensitive data and resources | Over-broad permissions, collecting identifiers the feature does not need |
| MASVS-PRIVACY-2 | The app prevents identification of the user | Stable cross-app identifiers, linkable telemetry, fingerprinting |
| MASVS-PRIVACY-3 | The app is transparent about data collection and usage | Privacy manifest or Data safety form inconsistent with code, undisclosed SDK collection |
| MASVS-PRIVACY-4 | The app offers user control over their data | No account or data deletion path, no opt-out for optional telemetry |

RESILIENCE controls apply only when the threat model includes the device owner or reverse engineers
(banking, DRM, anti-cheat, high-value IoT control). Do not report them as gaps for every app.

## OWASP Mobile Top 10 (2024)

| ID | Risk | Main MASVS controls |
|---|---|---|
| M1 | Improper Credential Usage | MASVS-AUTH-1, MASVS-CRYPTO-2, MASVS-STORAGE-1 |
| M2 | Inadequate Supply Chain Security | MASVS-CODE-3 |
| M3 | Insecure Authentication/Authorization | MASVS-AUTH-1, MASVS-AUTH-2, MASVS-AUTH-3 |
| M4 | Insufficient Input/Output Validation | MASVS-CODE-4, MASVS-PLATFORM-1, MASVS-PLATFORM-2 |
| M5 | Insecure Communication | MASVS-NETWORK-1, MASVS-NETWORK-2 |
| M6 | Inadequate Privacy Controls | MASVS-PRIVACY-1 to MASVS-PRIVACY-4, MASVS-STORAGE-2 |
| M7 | Insufficient Binary Protections | MASVS-RESILIENCE-1 to MASVS-RESILIENCE-4 |
| M8 | Security Misconfiguration | MASVS-PLATFORM-1, MASVS-NETWORK-1, MASVS-CODE-1 |
| M9 | Insecure Data Storage | MASVS-STORAGE-1, MASVS-STORAGE-2 |
| M10 | Insufficient Cryptography | MASVS-CRYPTO-1, MASVS-CRYPTO-2 |

The mapping is a guide for the report, not an official one-to-one table. Pick the single control that
best describes the root cause.
