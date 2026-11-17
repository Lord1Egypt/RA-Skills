# Cyber Resilience Act for mobile and companion apps

Regulation (EU) 2024/2847. Load this when mapping an app or a device's app to CRA requirements.
Quotes are from the Official Journal text; article and annex numbers refer to that text. Engineering
guidance, not legal advice.

## Timeline (Art. 71)

| Date | What applies |
|---|---|
| 10 December 2024 | Entry into force |
| 11 June 2026 | Chapter IV (Articles 35 to 51): notification of conformity assessment bodies |
| 11 September 2026 | Article 14: reporting of actively exploited vulnerabilities and severe incidents |
| 11 December 2027 | Everything else, including Annex I essential requirements and conformity assessment |

Reporting applies to products already on the market, so the Article 14 process is needed before 2027.

## Scope

- Art. 2(1): applies to "products with digital elements made available on the market, the intended purpose
  or reasonably foreseeable use of which includes a direct or indirect logical or physical data connection
  to a device or network". A mobile app and a connected device both meet this.
- Art. 3(1): a "product with digital elements" is "a software or hardware product and its remote data
  processing solutions".
- Art. 3(2): "remote data processing" is data processing at a distance whose software is designed by or
  under the responsibility of the manufacturer, "the absence of which would prevent the product with digital
  elements from performing one of its functions". A backend the app needs to work is usually in scope as part
  of the product; a general-purpose website or unrelated SaaS is not.
- Excluded by Art. 2(2)-(4): products covered by the medical device regulations (EU) 2017/745 and 2017/746,
  vehicle type approval (EU) 2019/2144, civil aviation (EU) 2018/1139 certification, and marine equipment
  Directive 2014/90/EU. Art. 2(5) allows further limitation for sectors with equivalent rules.
- Free and open-source software that is not supplied in the course of a commercial activity is treated
  differently (open-source software stewards have lighter duties). Whether a given app is "commercial" is a
  legal question; record it if unclear.

### Decision table

| Situation | Typical CRA position | Check with the compliance owner |
|---|---|---|
| Paid or monetised app on Google Play or the App Store in the EU | Product with digital elements; the publisher is the manufacturer | Monetisation model, who places it on the market |
| Free app of a company that sells a device or service | Usually in scope as part of a commercial activity | Whether the app is a separate product or part of the device |
| Companion app required to operate a connected device | Device and app both in scope; backend may be remote data processing | Whether the device maker or the app publisher is the manufacturer of each part |
| Medical device app under (EU) 2017/745 | Excluded from the CRA | Medical device classification |

## Important and critical products (Art. 7, Annex III, Annex IV)

Products whose core functionality matches Annex III are "important" and need a stricter conformity route if
harmonised standards are not fully applied (Art. 32(2) and (3)). Examples relevant to mobile and IoT from
Annex III class I: identity management and access control including biometric readers, password managers,
VPN products, smart home general purpose virtual assistants, smart home products with security functionalities
(smart door locks, security cameras, baby monitoring systems, alarm systems), internet-connected toys with
social interactive or location tracking features, and personal wearables with a health monitoring purpose
not covered by the medical device rules.

- Art. 7(1): "The integration of a product with digital elements which has the core functionality of a product
  category set out in Annex III shall not in itself render the product in which it is integrated subject to the
  conformity assessment procedures" for important products. Whether a companion app shares the classification
  of the device it controls is not settled by the text; flag it as a scope question.
- Default products use internal control (module A, Art. 32(1)(a)): the manufacturer self-assesses.

## Annex I Part I mapped to mobile work

| Point | Requirement (shortened) | Mobile evidence to look for |
|---|---|---|
| (1) | Appropriate level of cybersecurity based on risks | Written risk assessment (Art. 13(2)) referenced in the technical documentation |
| (2)(a) | No known exploitable vulnerabilities at release | Dependency scan results per release, triage records |
| (2)(b) | Secure by default configuration, with reset to original state | Defaults: TLS only, no debug flags, no default passwords, factory reset |
| (2)(c) | Vulnerabilities addressed through security updates, automatic where applicable, with opt-out and user notification | Forced update / minimum version, Play In-App Updates, firmware update path |
| (2)(d) | Protection from unauthorised access, report possible unauthorised access | Authentication, pairing, session handling, lockout, login notifications |
| (2)(e) | Confidentiality of stored, transmitted, processed data, encryption at rest and in transit | Keystore / Keychain storage, TLS, BLE link encryption plus app-layer protection |
| (2)(f) | Integrity of data, commands, programs and configuration; report corruptions | Signed firmware, authenticated BLE commands, integrity checks |
| (2)(g) | Data minimisation | Telemetry field list with purposes |
| (2)(h) | Availability of essential functions, resilience against denial of service | Offline behaviour, retry and backoff, rate limits |
| (2)(i) | Limit negative impact on other devices or networks | Scan and reconnect throttling, no network flooding |
| (2)(j) | Limited attack surface including external interfaces | Exported components, deep links, open ports, debug endpoints removed |
| (2)(k) | Exploitation mitigation | Platform hardening, R8, no dynamic code loading, input validation |
| (2)(l) | Recording and monitoring of security-relevant activity, with user opt-out | Security event log design, no personal data in it |
| (2)(m) | Users can securely and permanently remove all data and settings | Account deletion, device reset, local wipe |

## Annex I Part II vulnerability handling

| Point | Requirement (shortened) | Evidence |
|---|---|---|
| (1) | Identify and document vulnerabilities and components, SBOM "covering at the very least the top-level dependencies" | SBOM per release in a commonly used machine-readable format (CycloneDX or SPDX) |
| (2) | Remediate without delay; security updates separate from feature updates where feasible | Hotfix process, release history |
| (3) | Effective and regular security tests and reviews | Test reports, review records, pentest scope |
| (4) | Publicly disclose fixed vulnerabilities once an update is available | Security advisories or release notes |
| (5) | Coordinated vulnerability disclosure policy | Published CVD policy |
| (6) | Facilitate information sharing, provide a contact address for reports | `SECURITY.md`, website security page, `security.txt` |
| (7) | Secure distribution of updates, automatic where applicable | Signed builds, store distribution, signed firmware |
| (8) | Security updates disseminated without delay, free of charge, with advisory messages | Release policy, user-facing advisory text |

## Manufacturer obligations most relevant to app teams (Art. 13)

- Cybersecurity risk assessment, documented and kept up to date (Art. 13(2) and (3)).
- Due diligence for third-party components, including open source (Art. 13(5)).
- Support period: "at least five years. Where the product with digital elements is expected to be in use for
  less than five years, the support period shall correspond to the expected use time" (Art. 13(8)).
- Technical documentation (Annex VII) and EU declaration of conformity; CE marking for products placed on the market.
- User information (Annex II): manufacturer contact, single point of contact for vulnerability reports and
  the CVD policy, intended purpose, security properties, end date of the support period, how to install
  security updates, how to securely decommission and remove data.

## Reporting (Art. 14), from 11 September 2026

| Event | Early warning | Notification | Final report |
|---|---|---|---|
| Actively exploited vulnerability | Within 24 hours of becoming aware | Within 72 hours | No later than 14 days after a corrective or mitigating measure is available |
| Severe incident affecting the product's security | Within 24 hours | Within 72 hours | Within one month after the incident notification |

- Sent simultaneously to the CSIRT designated as coordinator and to ENISA via the single reporting platform.
- An incident is severe if it affects, or can affect, the protection of availability, authenticity, integrity
  or confidentiality of sensitive or important data or functions, or has led or can lead to malicious code
  in the product or the user's systems (Art. 14(5)).
- Impacted users are informed about the vulnerability or incident and the mitigations they can take.

## What an app team can do now

1. Name an owner for vulnerability handling and the Article 14 runbook.
2. Publish a vulnerability contact and CVD policy; add `SECURITY.md` and a website security page.
3. Generate and archive an SBOM per release; scan dependencies in CI.
4. Add a forced-update mechanism to every app, and a signed, verified firmware update path to every device.
5. Decide and publish the support period.
6. Start the risk assessment and technical documentation; feed in `mobile-security` audit findings.
