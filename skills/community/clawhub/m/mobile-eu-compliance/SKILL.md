---
name: mobile-eu-compliance
description: "Assesses Android, iOS, Flutter and connected-device companion apps against the EU Cyber Resilience Act, the Radio Equipment Directive delegated act with EN 18031-1, -2 and -3, and GDPR with ePrivacy: inventory, requirement mapping, evidence, gaps and a remediation plan in a gap report table. Engineering guidance, not legal advice. Use for CRA or EN 18031 readiness, SBOM and vulnerability handling, BLE or Wi-Fi companion apps, or GDPR reviews of mobile apps."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile EU compliance

Turn EU product rules into engineering work for a mobile app or a connected device's companion app: find out
which rules apply, map the code and processes to each requirement, collect evidence, and list the gaps with
concrete fixes and owners.

**This is engineering guidance, not legal advice.** The agent states what the code and documents show and
which requirement they relate to. Scope decisions, conformity routes and anything contractual go to the
team's compliance or legal owner. Where a point cannot be verified, the agent says so instead of guessing.

## When to use

- "Is our BLE companion app ready for the CRA and EN 18031?"
- CRA readiness: security updates, vulnerability handling, SBOM, coordinated disclosure, support period.
- A Wi-Fi, BLE or cellular device is sold in the EU and its app handles pairing, accounts, firmware updates
  or device data (RED delegated act, EN 18031).
- GDPR or ePrivacy review of an app: telemetry, analytics and ad SDKs, consent, deletion, retention.
- Preparing technical documentation or answering a customer or notified-body questionnaire.

Not for: a general security audit with MASVS findings (use `mobile-security`, then map its findings here),
store submission rules (use `mobile-release`), or accessibility law (use `mobile-accessibility`).

## Verified key facts

Checked against the Official Journal texts listed in `docs/SOURCES.md` of this pack. Re-check before
quoting them in customer-facing documents.

| Rule | Fact |
|---|---|
| Cyber Resilience Act, Regulation (EU) 2024/2847 | Applies from 11 December 2027. Article 14 (reporting) applies from 11 September 2026; Chapter IV (notified bodies) from 11 June 2026 (Art. 71) |
| CRA reporting (Art. 14) | Actively exploited vulnerability and severe incident: early warning within 24 hours, notification within 72 hours, to the coordinating CSIRT and ENISA via the single reporting platform. Final report: 14 days after a fix is available (vulnerability), one month after the notification (incident) |
| CRA support period (Art. 13(8)) | At least five years, or the expected use time if the product is expected to be in use for less |
| CRA SBOM (Annex I Part II(1)) | "commonly used and machine-readable format covering at the very least the top-level dependencies" |
| RED delegated act, Regulation (EU) 2022/30 | Applies from 1 August 2025 (date set by Delegated Regulation (EU) 2023/2444) |
| EN 18031-1 / -2 / -3:2024 | Cited with restrictions by Implementing Decision (EU) 2025/138 of 28 January 2025 for RED Art. 3(3)(d), (e) and (f) |
| GDPR breach notification (Art. 33) | To the supervisory authority without undue delay and, where feasible, within 72 hours |
| ePrivacy Directive Art. 5(3) | Storing or reading information on the user's device needs consent, unless strictly necessary for the service the user explicitly requested |

## Workflow

1. **Scope and roles.** Establish what is placed on the EU market and by whom.
   - Products: the app, the device, the cloud backend. Under the CRA a "product with digital elements"
     includes its remote data processing solutions: backend software designed by the manufacturer without
     which the product cannot perform one of its functions.
   - Role: manufacturer, importer or distributor. Most app teams are the manufacturer of the app.
   - Use the decision table in [CRA](references/cra.md) and [RED and EN 18031](references/red-en18031.md).
     If the scope cannot be settled from facts, record it as an open question for the legal owner.
2. **Inventory.** Build it from the code and build files before reading any policy document.
   - Data: what is collected, where it is stored, where it is sent, retention. Third-party SDKs and what they collect.
   - Components: dependencies from lock files (`Package.resolved`, `pubspec.lock`, Gradle dependencies).
   - Interfaces: network endpoints, BLE services and characteristics, deep links, exported components.
   - Security functions: authentication, pairing, update path (app and firmware), logging, deletion.
   - Template: [evidence templates](references/evidence-templates.md).
3. **Map to requirements.** For each applicable rule, walk its list in order:
   - CRA Annex I Part I points (a) to (m) and Part II points (1) to (8): [CRA](references/cra.md).
   - EN 18031 mechanisms for the device and the app side: [RED and EN 18031](references/red-en18031.md).
   - GDPR articles and ePrivacy Art. 5(3): [GDPR for mobile](references/gdpr.md).
4. **Collect evidence.** Every "Met" needs a file, config, test, document or process reference. No evidence
   means "Partial" or "Missing", even if the team says it is done.
5. **Gaps.** Describe each gap as a missing capability, not a missing document. Rate it by the date it must
   be met (11 September 2026, 11 December 2027, already applicable).
6. **Remediation plan.** One fix per gap, with an owner role and a target date. Code fixes get a snippet;
   process fixes get a short template.
7. **Report** in the output format below. Do not edit code unless asked.

## Rules

### 1. Security updates must reach every user (CRA Annex I Part I(c), Part II(7) and (8))

The team must be able to ship a fix and get it installed. A store update alone is not enough if old builds
keep working with a known vulnerability.

```kotlin
// BAD: no way to stop a vulnerable build; users stay on it for years
class App : Application()

// GOOD: server-driven minimum version, checked on start, plus Play In-App Updates for the immediate flow
if (BuildConfig.VERSION_CODE < remoteConfig.minSupportedVersionCode) {
    appUpdateManager.startUpdateFlowForResult(info, launcher, AppUpdateOptions.newBuilder(AppUpdateType.IMMEDIATE).build())
}
```

```swift
// GOOD: compare against a minimum build served by your backend and block with an update prompt
let build = Int(Bundle.main.object(forInfoDictionaryKey: "CFBundleVersion") as? String ?? "") ?? 0
if build < config.minimumSupportedBuild {
    state = .updateRequired(appStoreURL)
}
```

- Ship security fixes separately from feature releases where technically feasible (Part II(2)).
- Firmware updates delivered through the app count too: see rule 3.

### 2. No default or skippable passwords (CRA Annex I Part I(d); EN 18031 restriction on 6.2.5.1 and 6.2.5.2)

Implementing Decision (EU) 2025/138 removes the presumption of conformity for all three EN 18031 parts if
the user is allowed not to set and use any password.

```kotlin
// BAD: every device ships with the same PIN, and onboarding offers "Skip"
const val DEFAULT_PAIRING_PIN = "000000"
fun onSkipPasswordClicked() = finishOnboarding()

// GOOD: per-device secret printed on the label or set during onboarding; the step cannot be skipped
fun onSetPassword(password: String) {
    require(passwordPolicy.isAcceptable(password)) { "rejected by policy" }
    device.setAdminPassword(password)
}
```

- Brute-force protection on PIN and password entry (rate limit or lockout) on the device side.

### 3. Firmware updates are verified on the device, not only checksummed (CRA Annex I Part I(c) and (f); EN 18031 secure update)

CRC16 or CRC32 detects transmission errors. It does not stop a modified image.

```kotlin
// BAD: app downloads over HTTP and the device only checks a CRC
val image = httpClient.get("http://fw.example.com/latest.bin")
dfu.send(image, crc32(image))

// GOOD: HTTPS download, signed image, signature verified by the bootloader with a key the app never holds
val image = api.downloadFirmware(release.id)           // TLS, pinned to your backend if required
require(sha256(image).contentEquals(release.sha256))   // integrity of the download
dfu.send(image)                                          // device verifies the vendor signature before applying
```

- EN 18031-3 (financial assets): the decision says clause 6.3.2.4's secure-update assessment criteria do not
  confer a presumption of conformity. Treat secure update for payment-capable devices as needing extra justification.

### 4. Collect only what the purpose needs (CRA Annex I Part I(g); GDPR Art. 5(1)(c) and Art. 25)

```kotlin
// BAD
Telemetry(email = user.email, mac = device.macAddress, gps = location, rssi = rssi)

// GOOD
Telemetry(installId = rotatingInstallId, firmware = device.firmwareVersion, rssi = rssi)
```

```dart
// BAD
analytics.log('pair_ok', {'serial': device.serial, 'user': user.email});

// GOOD
analytics.log('pair_ok', {'model': device.model});
```

- MAC addresses, serial numbers, push tokens and advertising IDs are personal data when they can be linked
  to a person. Hashing them is pseudonymisation, not anonymisation.

### 5. No non-essential device storage or SDK start before consent (ePrivacy Art. 5(3); GDPR Art. 6 and 7)

```kotlin
// BAD: analytics and ad SDKs start in Application.onCreate for every user
override fun onCreate() { super.onCreate(); Analytics.init(this); Ads.init(this) }

// GOOD: start only after the user agreed; strictly necessary storage (session, settings) needs no consent
fun onConsentChanged(consent: Consent) {
    if (consent.analytics) Analytics.init(context) else Analytics.disable(context)
}
```

```swift
// GOOD: same rule on iOS; App Tracking Transparency is an additional Apple requirement, not GDPR consent
if consentStore.analyticsAllowed { Analytics.start() }
```

### 6. Users can delete all their data and settings (CRA Annex I Part I(m); GDPR Art. 17)

```kotlin
// BAD: "Delete account" only clears local preferences
fun deleteAccount() = prefs.edit { clear() }

// GOOD: server-side deletion, device unpairing and factory reset command, then local wipe
suspend fun deleteAccount() {
    api.deleteAccount()                 // backend deletes account and device records
    device.sendFactoryResetIfConnected()
    localStore.wipe()                   // databases, files, Keystore aliases, caches
}
```

### 7. Security-relevant events are logged without personal data, with a user opt-out (CRA Annex I Part I(l))

```kotlin
// BAD: no record of security events, or a record full of personal data
Log.d("Auth", "login ok for $email token=$token")

// GOOD: structured security events, no identifiers beyond what is needed, opt-out respected
securityLog.record(SecurityEvent.PairingFailed(reason = Reason.WrongPin, attempt = 3))
```

### 8. Every release has an SBOM (CRA Annex I Part II(1))

```kotlin
// GOOD: build.gradle.kts, CycloneDX Gradle plugin (pin the version in libs.versions.toml)
plugins { id("org.cyclonedx.bom") }
// ./gradlew cyclonedxBom  -> archive the generated BOM with the release
```

- iOS and Flutter: generate from `Package.resolved`, `Podfile.lock` or `pubspec.lock` with an SBOM tool
  that reads them, in CI, per release tag. Keep the SBOM with the build, not only in a dashboard.

### 9. A vulnerability contact and disclosure policy exist and are findable (CRA Annex I Part II(5) and (6); Annex II(2))

```markdown
<!-- BAD: no SECURITY.md, no contact in the app or on the website -->

<!-- GOOD: SECURITY.md in the repository, the same contact on the product website and in the app's About screen -->
## Reporting a vulnerability
Email security@example.com or use https://example.com/security. We acknowledge within 5 working days.
Supported versions and the support end date: see https://example.com/support-period.
```

- Publish information about fixed vulnerabilities once the update is available (Part II(4)).

### 10. Actively exploited vulnerabilities are reported on time (CRA Art. 14, from 11 September 2026)

This is a process, so the deliverable is a runbook, not code.

```text
BAD:  "Security issues go to the backlog."
GOOD: Runbook: triage owner on call; if exploitation is confirmed, early warning to the coordinating CSIRT
      and ENISA via the single reporting platform within 24 h, notification within 72 h, final report
      14 days after the fix ships; inform affected users about the issue and mitigations.
```

### 11. The support period is declared (CRA Art. 13(8); Annex II(7))

- The end date of security support is stated where users see it before and after purchase (store listing,
  website, About screen). At least five years unless the expected use time is shorter.

## Anti-patterns

- Declaring the app "compliant". The report states what was found; conformity is a manufacturer decision.
- Treating the CRA as a document exercise. Most Annex I items are product capabilities that need code.
- Assuming a BLE-only device is out of RED delegated-act scope. Article 1(1) covers equipment that can
  communicate over the internet "directly or via any other equipment"; whether a phone link counts for a
  given product is not settled by official guidance, so record it as a scope question.
- Using EN 18031 "guidance" or "rationale" sections as evidence. The decision says they confer no presumption.
- Relying on CRC for update integrity, or on obfuscation for confidentiality.
- Hashing identifiers and calling the data anonymous.
- Inventing article numbers, dates or clause numbers. If a citation cannot be confirmed, say so.

## Checklist

- [ ] Scope written down: products, roles, which of CRA, RED delegated act, GDPR and ePrivacy apply, open questions
- [ ] Inventory built from code and lock files: data, SDKs, components, interfaces, security functions
- [ ] Every CRA Annex I Part I point (a)-(m) and Part II point (1)-(8) has a status and evidence
- [ ] EN 18031 part(s) identified for the device; app-side mechanisms mapped
- [ ] No default or skippable passwords; brute-force protection exists
- [ ] Update path for app and firmware: forced minimum version, signed firmware, verified on device
- [ ] Data minimisation applied to telemetry; consent before non-essential SDKs and device storage
- [ ] Full deletion path: account, backend data, device reset, local data
- [ ] SBOM generated per release; vulnerability contact, disclosure policy and support end date published
- [ ] Article 14 reporting runbook exists with owners
- [ ] Report says "engineering guidance, not legal advice" and lists unverified points

## Output format

~~~markdown
## EU compliance gap report: <product / app / version>

Engineering assessment, not legal advice. Scope and conformity decisions belong to <compliance owner>.

Scope: <app, device model, backend>. Role: <manufacturer | importer | distributor>.
Applies: CRA <yes | open question>, RED delegated act <yes | no | open question>, GDPR <yes>, ePrivacy 5(3) <yes>.
Key dates: CRA reporting 11 Sep 2026; CRA full application 11 Dec 2027; RED delegated act applies since 1 Aug 2025.

| Requirement | Status | Evidence | Gap | Fix | Owner |
|---|---|---|---|---|---|
| CRA Annex I Part I(c) security updates | Partial | Play In-App Updates in `UpdateManager.kt:31`; no minimum-version gate | Old builds keep working after a security fix | Server-driven minimum version check (rule 1) | Mobile lead |
| EN 18031-1 6.2.5 passwords / CRA I.I(d) | Missing | Onboarding has a Skip button (`OnboardingScreen.kt:88`) | User can keep no password; no presumption of conformity | Remove Skip, enforce password policy | Product + firmware |
| CRA Annex I Part II(1) SBOM | Missing | No SBOM step in `.github/workflows/release.yml` | No SBOM per release | Add CycloneDX generation and archive | DevOps |
| GDPR Art. 5(1)(c) minimisation | Met | `Telemetry.kt` sends model, firmware, RSSI only | - | - | - |
| ePrivacy Art. 5(3) consent | Not applicable | No analytics or ad SDKs in `build.gradle.kts` | - | - | - |

### Open questions for the compliance owner
- Is the device "internet-connected radio equipment" when it reaches the cloud only through the app?

### Remediation plan
1. <fix> -- owner, target date, deadline driver (for example CRA Art. 14 from 11 Sep 2026)

### Not assessed
- Backend and cloud infrastructure, device firmware internals, contracts with SDK vendors, <other>
~~~

Status values: Met, Partial, Missing, Not applicable. "Met" always has evidence.

## Related skills

- `mobile-security` -- technical MASVS audit whose findings feed this gap report
- `mobile-ble` -- pairing, secure update and protocol work on the app side of a device
- `mobile-ci-cd` -- SBOM generation, dependency scanning and signed release pipelines
- `mobile-release` -- store privacy declarations, account deletion and release process
- `mobile-merge-request` -- describing compliance-relevant changes in the MR
- `mobile-accessibility` -- the European Accessibility Act, which this skill does not cover
