# Evidence templates

Load this when building the inventory, collecting evidence or writing the process documents the gap report
asks for. Copy, fill and keep with the technical documentation.

## 1. Product inventory

```markdown
## Products
| Product | Type | Placed on EU market by | Version / model | Notes |
|---|---|---|---|---|
| <App name> Android | App | <company> | 3.4.0 | Google Play |
| <App name> iOS | App | <company> | 3.4.0 | App Store |
| <Device model> | Radio equipment (BLE, Wi-Fi) | <company> | HW rev C, FW 2.1.0 | |
| <Backend> | Remote data processing | <company> | | Needed for remote control and updates |

## Data
| Field | Source | Purpose | Lawful basis | Stored where | Sent to | Retention |
|---|---|---|---|---|---|---|

## Third-party components and SDKs
| Component | Version | Purpose | Data it receives | Role (processor/controller) | Contract |
|---|---|---|---|---|---|

## Interfaces
| Interface | Direction | Authentication | Encryption | Notes |
|---|---|---|---|---|
| HTTPS API | app -> backend | OAuth 2.0 PKCE | TLS 1.2+ | |
| MQTT | device -> broker | per-device cert | TLS | port 8883 |
| BLE GATT | app <-> device | LE Secure Connections + app-layer token | link + AEAD | commands authenticated |

## Security functions
| Function | Implemented in | Evidence |
|---|---|---|
| Pairing / onboarding | app + device | `OnboardingFlow.kt`, firmware spec section 4 |
| App update enforcement | app + backend | `UpdateGate.kt`, remote config `min_version_code` |
| Firmware update | app + device + backend | `DfuManager.kt`, bootloader signature check |
| Deletion | app + backend + device | `AccountDeletion.kt`, API `DELETE /me`, reset command 0x7F |
```

## 2. Evidence rules

| Status | Needs |
|---|---|
| Met | A file and line, a config, a test, a CI job, a published URL or a named process document |
| Partial | Evidence for part of the requirement and a clear statement of what is missing |
| Missing | Nothing found. Say where the agent looked |
| Not applicable | The reason, for example "no payment function, EN 18031-3 does not apply" |

Statements from the team without evidence are recorded as "Partial: stated, not evidenced".

## 3. Coordinated vulnerability disclosure policy (CRA Annex I Part II(5) and (6))

```markdown
# Security policy

## Reporting a vulnerability
Report security issues to security@<domain> or through <web form>. Please do not open public issues.
Include the product, version, steps to reproduce and impact.

## What happens next
- We acknowledge your report within <N> working days.
- We keep you informed while we investigate and fix.
- We publish an advisory once a fix is available, and credit you if you wish.

## Supported versions
Security updates are provided until <support end date> for <product and versions>.
```

Publish the same contact as `/.well-known/security.txt` on the product website (RFC 9116) and in the app's
About or Help screen.

## 4. Article 14 reporting runbook (from 11 September 2026)

```markdown
# Exploited vulnerability and severe incident runbook

Owner: <role>. Deputy: <role>. On-call contact: <channel>.

1. Triage: confirm active exploitation or a severe incident (Art. 14(5) criteria).
2. Within 24 h of awareness: early warning to the CSIRT designated as coordinator and ENISA via the single
   reporting platform. Record the timestamp of awareness.
3. Within 72 h: full notification with general information, nature of the exploit or incident, and
   mitigations.
4. Fix: ship the security update (separate from feature work where feasible).
5. Final report: vulnerability, no later than 14 days after the fix is available; incident, within one month
   after the notification.
6. Inform impacted users about the issue and the measures they can take (Art. 14(8)).
7. Post-mortem and update the risk assessment.
```

## 5. Support period statement (CRA Art. 13(8), Annex II(7))

```markdown
<Product> receives security updates until <date>. Updates are delivered through <Google Play / App Store /
in-app firmware update>. After that date, known vulnerabilities may not be fixed.
```

## 6. SBOM per release (CRA Annex I Part II(1))

```yaml
# CI step sketch; pin every action by commit SHA and every tool version.
- name: SBOM (Android, Gradle)
  run: ./gradlew cyclonedxBom          # CycloneDX Gradle plugin, id org.cyclonedx.bom
- name: Archive SBOM with the release
  run: cp "$BOM_PATH" "dist/sbom-${VERSION}.cdx.json"   # BOM_PATH: the file the plugin version you pin writes
```

- iOS and Flutter: use an SBOM generator that reads `Package.resolved`, `Podfile.lock` or `pubspec.lock`, and
  confirm in its output that the app's direct dependencies are listed. The CRA minimum is "at the very least
  the top-level dependencies".
- Store the SBOM with each release build; regenerate on every release, not once.
