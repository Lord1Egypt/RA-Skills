# GDPR and ePrivacy for mobile apps

Regulation (EU) 2016/679 (GDPR) and Directive 2002/58/EC as amended (ePrivacy). Load this for any app that
processes personal data of people in the EU. Engineering guidance, not legal advice: lawful basis, legitimate
interest balancing and transfer mechanisms are decisions for the controller's privacy owner.

## What counts as personal data in an app

- Personal data includes online identifiers. Recital 30: people "may be associated with online identifiers
  provided by their devices, applications, tools and protocols, such as internet protocol addresses, cookie
  identifiers or other identifiers".
- In practice: account IDs, emails, IP addresses, advertising IDs, push tokens, `identifierForVendor`, install
  IDs, device MAC addresses and serial numbers linked to an account, precise location, BLE scan results that
  identify nearby devices.
- Pseudonymised data (hashed IDs) is still personal data. Only truly anonymous data is outside the GDPR.
- Health data (Art. 9 special category) includes data revealing physical or mental health, for example heart
  rate or sleep data from a wearable. It needs an Art. 9(2) condition, usually explicit consent.

## Article map for app teams

| Article | Topic | What to check in the app |
|---|---|---|
| 5(1)(b), (c), (e) | Purpose limitation, data minimisation, storage limitation | Each collected field has a purpose; retention periods exist and are enforced |
| 6 | Lawful basis | Basis documented per purpose (contract, consent, legitimate interest, legal obligation) |
| 7 | Conditions for consent | Consent is a separate, unticked choice; refusing is as easy as accepting; withdrawal is possible in the app |
| 8 | Child's consent for information society services | Age 16 by default, Member States may lower to 13; parental authorisation below that |
| 9 | Special categories (health, biometrics) | Explicit consent or other Art. 9(2) condition; extra protection |
| 12-13 | Transparency | Privacy notice reachable in the app before and after sign-up |
| 15, 16, 17, 18, 20, 21 | Access, rectification, erasure, restriction, portability, objection | In-app or documented request path; export in a machine-readable format; full deletion |
| 25 | Data protection by design and by default | Optional data collection off by default; least-privilege permissions |
| 28 | Processor | Contract (data processing agreement) with every SDK vendor or backend that processes data on your behalf |
| 30 | Records of processing | Each SDK and data flow appears in the record |
| 32 | Security of processing | Encryption in transit and at rest, access control (see `mobile-security`) |
| 33, 34 | Breach notification | Supervisory authority "without undue delay and, where feasible, not later than 72 hours"; users when high risk |
| 35 | Data protection impact assessment | Likely needed for large-scale location tracking, health data, children, or systematic monitoring |
| 44 onwards | Transfers outside the EEA | SDKs and backends sending data to third countries have a transfer mechanism |

## ePrivacy Art. 5(3): storage and access on the device

"The storing of information, or the gaining of access to information already stored, in the terminal
equipment of a subscriber or user is only allowed on condition that the subscriber or user concerned has given
his or her consent", except where strictly necessary for transmission or "for the provider of an information
society service explicitly requested by the subscriber or user to provide the service".

For apps this covers more than cookies:
- Reading the advertising ID, writing analytics IDs, SDK caches used for tracking, device fingerprinting.
- Strictly necessary (no consent needed): login session, user settings, offline data of the feature the user uses.
- Consent must be collected before the SDK starts, not after.

## Third-party SDKs

| SDK type | Typical role | What to verify |
|---|---|---|
| Crash reporting | Processor, sometimes controller for its own purposes | DPA, data fields, opt-out, retention, region |
| Product analytics | Processor or joint controller | Consent before start (if not strictly necessary), IP handling, user ID mapping |
| Advertising, attribution | Often independent controller | Consent under ePrivacy 5(3) and a lawful basis; disclosure in the notice |
| Push notifications | Processor | Token handling, deletion on logout |
| Customer support chat | Processor | What is sent with each message (device info, logs) |

Check what each SDK collects by default. Many send device identifiers and IP addresses on first start.

## Store declarations

Google Play's Data safety form and Apple's App Privacy details are store requirements, not GDPR, but they
must match what the code and the privacy notice say. A mismatch is both a store rejection risk and evidence
of poor transparency. See `mobile-release`.

## Practical checks

- [ ] Data inventory lists every field, purpose, lawful basis, retention, recipients and region
- [ ] No non-essential SDK starts before consent; consent can be withdrawn in settings
- [ ] Account deletion removes data from app, backend, processors and connected devices
- [ ] Export of the user's data exists or a documented process covers it
- [ ] Logs and crash reports contain no direct identifiers, tokens or location
- [ ] Breach response process names who notifies the supervisory authority within 72 hours
- [ ] DPIA considered for location, health, children or large-scale monitoring
