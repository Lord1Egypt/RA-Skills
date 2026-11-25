# EAA, EN 301 549 and WCAG 2.2 for mobile apps

Load this when deciding whether the European Accessibility Act applies to an app, when mapping findings to
EN 301 549 or WCAG 2.2, or when drafting the accessibility information a service provider has to publish.
Quotes are from the Official Journal text of Directive (EU) 2019/882
(https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng), EN 301 549 V4.1.1 (2026-09) and the WCAG 2.2
Recommendation (https://www.w3.org/TR/WCAG22/). Engineering guidance, not legal advice.

## Dates

| Date | What happens | Source |
|---|---|---|
| 28 June 2022 | Member States adopt and publish national transposition measures | Art. 31(1) |
| 28 June 2025 | National measures apply; products placed on the market and services provided to consumers after this date are covered | Art. 31(2), Art. 2(1) and (2) |
| 28 June 2027 | Latest date for the 112 emergency-number answering obligations (Art. 4(8)) if a Member State uses the derogation | Art. 31(3) |
| 28 June 2030 | End of the transitional period for services using products lawfully used before 28 June 2025; first Commission report | Art. 32(1), Art. 33(1) |

The EAA is a directive: obligations reach companies through each Member State's national law, which can add
details (enforcement body, penalties under Art. 30). Check the national law of each market the app serves.

## Scope: products

Art. 2(1) covers products placed on the market after 28 June 2025: consumer general purpose computer hardware
and their operating systems, payment terminals and certain self-service terminals (ATMs, ticketing and
check-in machines, interactive information terminals), consumer terminal equipment for electronic
communications or for audiovisual media services, and e-readers. A mobile app on its own is not one of these
products. A phone maker's preinstalled operating system is.

## Scope: services (where most apps fall)

Art. 2(2) covers these services provided to consumers after 28 June 2025:

| Art. 2(2) | Service | Typical mobile apps |
|---|---|---|
| (a) | Electronic communications services, except transmission services used for machine-to-machine services | Operator apps, calling and messaging services that are electronic communications services under Directive (EU) 2018/1972 |
| (b) | Services providing access to audiovisual media services | Streaming and TV apps, including electronic programme guides |
| (c) | Air, bus, rail and waterborne passenger transport: websites, mobile device-based services including mobile applications, e-tickets and e-ticketing, transport information, interactive self-service terminals | Airline, rail and ferry apps. Urban, suburban and regional transport: only the self-service terminals element (point (v)) applies |
| (d) | Consumer banking services (Art. 3(28): credit agreements, certain investment services, payment services, payment-account services, e-money) | Banking, payment and e-money apps |
| (e) | E-books and dedicated software (Art. 3(41)) | E-book reader apps and stores |
| (f) | E-commerce services (Art. 3(30)) | Shopping apps, marketplaces, apps with an in-app shop or checkout that concludes a consumer contract |

Key points from the text:

- "Consumer" (Art. 3(22)) is a natural person acting outside their trade, business, craft or profession. A
  service offered only to businesses is not a consumer service.
- "E-commerce services" (Art. 3(30)): "services provided at a distance, through websites and mobile
  device-based services by electronic means and at the individual request of a consumer with a view to
  concluding a consumer contract". Recital 43: the e-commerce obligations "should apply to the online sale of
  any product or service".
- Recital 47: the four principles (perceivable, operable, understandable, robust) are those used in
  Directive (EU) 2016/2102. Public sector apps fall under that directive.

### Decision table

| Situation | Typical position | Record as an open question |
|---|---|---|
| Shopping app or marketplace selling to consumers in the EU | E-commerce service, in scope | Which entity is the service provider |
| Mobile banking, payment or e-money app for consumers | Consumer banking service, in scope | - |
| Airline, long-distance rail or ferry app | Passenger transport element, in scope | Whether the operator is a regional or urban service (then only terminals) |
| City public transport app | Urban, suburban and regional transport: only Art. 2(2)(c)(v) terminals apply | Online ticket sales: recital 35 relies on the e-commerce obligations for them |
| Streaming or TV app | Access to audiovisual media services, in scope | - |
| IoT companion app that only controls the user's device | Not a listed service on its face | Does it sell subscriptions, spare parts or services in-app (e-commerce)? |
| Game, fitness or productivity app with in-app purchases | Not listed as such; the purchase flow may be e-commerce | Whether in-app purchases through the store make the publisher an e-commerce service provider |
| Internal or B2B app (employees, fleet, field service) | Not a consumer service | - |
| App of a public sector body | Directive (EU) 2016/2102 | Whether a listed service in the app also falls under the EAA |

Do not decide the open questions. List the facts that bear on them.

## Microenterprises (Art. 3(23), Art. 4(5), Art. 14(4))

- Definition: "an enterprise which employs fewer than 10 persons and which has an annual turnover not exceeding
  EUR 2 million or an annual balance sheet total not exceeding EUR 2 million".
- Art. 4(5): "Microenterprises providing services shall be exempt from complying with the accessibility
  requirements referred to in paragraph 3 of this Article and any obligations relating to the compliance with
  those requirements."
- Recital 53: the enterprise must genuinely fulfil Commission Recommendation 2003/361/EC.
  That Recommendation takes partner and linked enterprises into account, so a small subsidiary of a group may
  not qualify. Not checked here against the Recommendation text; confirm with the legal owner.
- Microenterprises dealing with products are not exempt. They only need not document the Art. 14
  assessment, but must give the facts to the market surveillance authority on request.
- Art. 4(6): Member States provide guidelines and tools to microenterprises.

## What services must do

- Art. 13(1): design and provide the service in line with the accessibility requirements.
- Annex I Section III: accessible information about the service and its accessibility features (more than one
  sensory channel, understandable, text that can be turned into other formats, adequate fonts, contrast and
  adjustable spacing, alternatives for non-text content), accessible websites and mobile apps (point (c)),
  and accessible support services where they exist (point (d)).
- Annex I Section IV adds service-specific requirements, for example:
  - (e) consumer banking: identification methods, electronic signatures, security and payment services that are
    perceivable, operable, understandable and robust; information not more complex than CEFR level B2.
  - (g) e-commerce: accessibility information about the products sold when the responsible operator provides
    it; accessible identification, security and payment functions.
  - (b) audiovisual: accessible programme guides; subtitles, audio description and similar access services
    transmitted with adequate quality and synchronised, with user control.
  - (f) e-books: no blocking of assistive technology, including by digital rights management.
- Art. 13(2) and Annex V: publish the information on how the service meets the requirements in the general
  terms and conditions or an equivalent document, in written and oral format and accessibly; keep it for as
  long as the service is in operation.
- Art. 13(3) and (4): procedures to stay conformant when the service or standards change; corrective measures
  and information to the competent authorities in case of non-conformity.

## Exceptions and transition

- Art. 2(4): content not covered: pre-recorded time-based media and office files published before
  28 June 2025; online maps if essential navigational information is provided accessibly; third-party content
  "neither funded, developed by, or under the control of" the operator; archives not updated after
  28 June 2025.
- Art. 14: requirements apply only where they do not cause a fundamental alteration or a disproportionate burden
  (criteria in Annex VI). The assessment must be documented, kept for five years and, for disproportionate
  burden, renewed at least every five years. Operators that receive funding for improving accessibility cannot
  rely on disproportionate burden. Except for microenterprises, operators relying on Art. 14 inform the
  authorities.
- Art. 32(1): a transitional period until 28 June 2030 for services using products lawfully used before
  28 June 2025; service contracts agreed before 28 June 2025 continue until they expire, at most five years.
  How this applies to a given app release is a legal question; do not use it to rate a finding as acceptable.

## EN 301 549

- Current version: V4.1.1 (2026-09), "Harmonised European Standard", adopted 24 August 2026, latest
  announcement date 30 November 2026, withdrawal of conflicting national standards 31 May 2028 (from the
  standard's foreword; listing at https://www.etsi.org/deliver/etsi_en/301500_301599/301549/).
- Prepared under standardisation request C(2022) 6456 "to provide one voluntary means of conforming to the
  essential requirements of Directive (EU) 2019/882". "Once the present document is cited in the Official
  Journal" under that directive, conformance with the clauses in Tables A.1 to A.5 gives a presumption of
  conformity. Whether and when it has been cited must be checked in the Official Journal; this skill could not
  confirm a citation.
- V3.2.1 (2021-03) was prepared for Directive (EU) 2016/2102 (public sector websites and apps). V4.1.1 has
  clauses 9, 10 and 11 updated to WCAG 2.2.
- Annex ZB maps the standard to the EAA: Tables ZB.1 to ZB.3 for products, ZB.4 for all services, ZB.5 for
  specific services.

### Clause 11 (non-web software) for mobile apps

- Clause 11.0 lists "mobile applications" among the software types covered. Web views inside an app are
  assessed with clause 11, not clause 9 ("Where there is any doubt, clause 11 requirements have precedence").
- Numbering: 11 plus the WCAG number for most criteria (11.1.4.3 Contrast (minimum), 11.2.5.8 Target size
  (minimum), 11.3.3.8 Accessible authentication (minimum), 11.4.1.2 Name, role, value).
- Void for non-web software (no requirement): 2.4.1 Bypass Blocks, 2.4.5 Multiple Ways, 3.1.2 Language of
  Parts, 3.2.3 Consistent Navigation, 3.2.6 Consistent Help, and 4.1.1 (removed). Report these as best
  practice, not as failures, when the target is EN 301 549.
- 11.1.4.4 Resize text is modified: up to 200 percent or, where the platform's text resizing does not reach
  200 percent for all text, up to the platform's text sizing capabilities.
- 11.2.4.2 Non-web software titled: screens have titles that describe their name, topic or purpose where the
  platform supports titles.
- 11.3.3.8 Note 2 lists password manager support and copy and paste as mechanisms that satisfy the criterion.
- 11.5.2 Accessibility services: use the platform accessibility services (11.5.2.3, a recommendation) so that
  name, role, state, value, actions and focus are exposed (11.5.2.5 to 11.5.2.17).
- 11.7 User preferences: follow the platform's user preference settings for accessibility features (text size,
  contrast, reduce motion) unless not following them is essential to the function.
- Clause 4 functional performance criteria (usage without vision, with limited vision, without colour
  perception, without hearing, limited manipulation, limited cognition, privacy, and others) mirror EAA
  Annex I Section VII.

## WCAG 2.2 level A and AA on mobile

All 55 level A and AA success criteria, with the usual mobile check. Use the number and name exactly in
findings.

| SC | Name | Level | Mobile check |
|---|---|---|---|
| 1.1.1 | Non-text Content | A | Icons, images, charts have names; decorative ones hidden |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | Transcript or audio alternative |
| 1.2.2 | Captions (Prerecorded) | A | Captions in the player, user can switch on |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | Audio description or text alternative |
| 1.2.4 | Captions (Live) | AA | Live streams have captions |
| 1.2.5 | Audio Description (Prerecorded) | AA | Audio description track |
| 1.3.1 | Info and Relationships | A | Headings, lists, groups, form labels exposed in semantics |
| 1.3.2 | Meaningful Sequence | A | Screen reader order matches visual order |
| 1.3.3 | Sensory Characteristics | A | No "tap the round button on the right" only instructions |
| 1.3.4 | Orientation | AA | Works in portrait and landscape unless essential |
| 1.3.5 | Identify Input Purpose | AA | Autofill content types on personal data fields |
| 1.4.1 | Use of Color | A | Errors, states and links not colour-only |
| 1.4.2 | Audio Control | A | Auto-playing audio over 3 seconds can be paused or muted |
| 1.4.3 | Contrast (Minimum) | AA | 4.5:1 text, 3:1 large text (18 pt, or 14 pt bold) |
| 1.4.4 | Resize Text | AA | 200 percent (EN 301 549: up to platform maximum) without loss |
| 1.4.5 | Images of Text | AA | No text baked into images |
| 1.4.10 | Reflow | AA | Content reflows at large text and narrow widths, no two-way scrolling |
| 1.4.11 | Non-text Contrast | AA | 3:1 for icons, control borders, focus indicators |
| 1.4.12 | Text Spacing | AA | No clipping when line, letter or word spacing grows |
| 1.4.13 | Content on Hover or Focus | AA | Tooltips and popovers dismissible and persistent |
| 2.1.1 | Keyboard | A | Everything works with an external keyboard and switch access |
| 2.1.2 | No Keyboard Trap | A | Focus can leave every component, including bottom sheets and web views |
| 2.1.4 | Character Key Shortcuts | A | Single-key shortcuts can be turned off or remapped |
| 2.2.1 | Timing Adjustable | A | Session and OTP timeouts can be extended or warned |
| 2.2.2 | Pause, Stop, Hide | A | Carousels and animations over 5 seconds can be paused |
| 2.3.1 | Three Flashes or Below Threshold | A | No flashing more than three times per second |
| 2.4.1 | Bypass Blocks | A | Void in EN 301 549 clause 11 |
| 2.4.2 | Page Titled | A | Each screen has a title (EN 301 549 11.2.4.2) |
| 2.4.3 | Focus Order | A | Focus moves into dialogs and returns after they close |
| 2.4.4 | Link Purpose (In Context) | A | "Learn more" links have context |
| 2.4.5 | Multiple Ways | AA | Void in EN 301 549 clause 11 |
| 2.4.6 | Headings and Labels | AA | Headings and labels describe topic or purpose |
| 2.4.7 | Focus Visible | AA | Keyboard focus indicator visible |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Focused field not hidden by the keyboard, sticky bars or sheets |
| 2.5.1 | Pointer Gestures | A | Pinch, multi-finger and path gestures have single-tap alternatives |
| 2.5.2 | Pointer Cancellation | A | Actions fire on release, can be aborted by sliding off |
| 2.5.3 | Label in Name | A | Accessible name contains the visible text |
| 2.5.4 | Motion Actuation | A | Shake or tilt features have a UI alternative and can be disabled |
| 2.5.7 | Dragging Movements | AA | Reorder, sliders, maps work without dragging |
| 2.5.8 | Target Size (Minimum) | AA | At least 24 by 24 (platform target: 48dp / 44pt) |
| 3.1.1 | Language of Page | A | App and web view language set so the screen reader voice is correct |
| 3.1.2 | Language of Parts | AA | Void in EN 301 549 clause 11 |
| 3.2.1 | On Focus | A | Focus alone does not navigate or submit |
| 3.2.2 | On Input | A | Changing a field does not change context unexpectedly |
| 3.2.3 | Consistent Navigation | AA | Void in EN 301 549 clause 11 |
| 3.2.4 | Consistent Identification | AA | Same function, same name and icon across screens |
| 3.2.6 | Consistent Help | A | Void in EN 301 549 clause 11; still good practice |
| 3.3.1 | Error Identification | A | Errors described in text and announced |
| 3.3.2 | Labels or Instructions | A | Persistent labels, not placeholder only |
| 3.3.3 | Error Suggestion | AA | Error text says how to fix it |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | Review, confirm or undo for payments and contracts |
| 3.3.7 | Redundant Entry | A | No re-entry of data already given in the same flow |
| 3.3.8 | Accessible Authentication (Minimum) | AA | Password managers, paste, passkeys or biometrics allowed |
| 4.1.2 | Name, Role, Value | A | Custom controls expose name, role, state and value |
| 4.1.3 | Status Messages | AA | Toasts, snackbars, loading and result messages announced |

## Accessibility information template (Annex V)

Draft for the compliance owner; the final wording and where it is published are their decision.

```markdown
## Accessibility of <service name>

<Service name> is <general description of the service, in plain language>.

How the service works: <main functions, how to sign in, buy, pay, get help>.

How we meet the accessibility requirements:
- Mobile apps for Android and iOS are designed and tested against EN 301 549 V4.1.1 clause 11 (WCAG 2.2 level AA).
- Supported assistive technologies: TalkBack, Switch Access, VoiceOver, Voice Control, external keyboards.
- The apps follow system text size, bold text, contrast and reduce motion settings.
- Known limitations: <list, with the planned fix date, or the Art. 14 assessment reference>.
- How we keep it conformant: accessibility checks on every release, manual screen reader tests of <journeys>.

Contact for accessibility questions and feedback: <accessible channels: email, phone, relay service>.
Last reviewed: <date>.
```

## Open points this skill could not verify

- Whether EN 301 549 V4.1.1 has been cited in the Official Journal under Directive (EU) 2019/882, and from when.
- Whether in-app purchases processed by an app store make the app publisher an e-commerce service provider.
- National transposition details (enforcement body, penalties, any extensions) for each Member State.
