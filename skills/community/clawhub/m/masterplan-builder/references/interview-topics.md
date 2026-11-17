# Interview Topics — ask in this order, one at a time

Go topic by topic. Don't ask everything at once. Every topic below applies to every category unless marked otherwise. Category-specific notes are under each topic where relevant (Website/Web App = WEB, Mobile App = MOBILE, Local AI Assistant/Agent = AI, Desktop App = DESKTOP, Backend/API = API, Browser Extension = EXT, CLI Tool = CLI).

## 1. Identity & purpose
- Project name (working name is fine, can change later)
- One-line pitch: what does it do, in one sentence
- What problem does it solve, and for whom — what happens today without it
- Is this commercial (sold/marketed), internal/personal, or open source — this changes licensing, monetization, and compliance questions later

## 2. Target users
- Who uses this — primary persona(s), and any secondary ones
- Technical level of the users (affects UX complexity, onboarding, error messaging)
- Expected scale at launch and in year one (10 users? 10,000? 10 million?) — this drives infra and architecture decisions later, don't skip it
- MOBILE/WEB: which platforms/devices/browsers must be supported, minimum OS/browser versions
- AI: does the assistant run fully local (no cloud calls) or hybrid — this is a hard architectural constraint, get it explicit

## 3. Definition of done
- What does "100% finished and ready to launch/use" mean specifically for this project — get a concrete list, not a feeling
- Is there a hard launch date or event driving scope
- What would make this a failure even if technically working (e.g. too slow, not accessible, not secure enough)

## 4. Features
- Ask for a full feature brain-dump first, unfiltered
- Then sort together into: MVP (must exist for v1) vs later/nice-to-have — be explicit, don't let this stay implicit
- For every MVP feature, get it down to acceptance-criteria level: what does "this feature works" mean exactly, what are the edge cases, what happens on error/empty state/invalid input
- Any feature that depends on a third-party service (payments, maps, notifications, LLM API, etc.) — identify the specific provider now, not "a payment provider," because that decision cascades into architecture

## 5. Tech stack (research each before presenting options)
- Frontend framework/library (WEB, MOBILE, DESKTOP, EXT) — search current recommendations for this category before offering choices
- Backend language/framework (WEB, API, AI if it has a backend)
- Database(s) — relational, document, vector (if AI/search features), cache layer — search current recommendations, don't default to what's familiar from training data without checking it's still the right current call
- Mobile: native (Swift/Kotlin) vs cross-platform (React Native/Flutter/etc.) — search current state of each before asking
- AI: which model/runtime (local model via what inference engine, or API-based), and if local — hardware constraints (RAM/GPU) the user's target machines actually have
- Hosting/infra target (cloud provider, self-hosted, serverless, on-device) — search current pricing/limits, don't assume old tier structures still apply
- Auth approach (build vs third-party auth provider, session vs token-based) — search current recommended practice
- For every choice: get the specific version/edition being targeted, not just the name of the tool

## 6. Data model
- List every entity/object the system needs to store, in plain language first
- For each entity: fields, types, which are required, which are unique, relationships to other entities (one-to-many, many-to-many, etc.)
- Any data that's sensitive (PII, payment info, health data, credentials) — flag now, it drives the security section
- Expected data volume and growth rate — affects indexing/partitioning decisions later

## 7. Architecture & integration
- How do frontend and backend communicate (REST, GraphQL, RPC, WebSocket, IPC for desktop) — pick one and be specific about the contract style
- API design conventions (resource naming, versioning strategy, pagination, error format) — don't leave this implicit
- Every third-party integration named in step 4/5: how is it called, is it synchronous or via webhook/background job, what happens if it's down
- Background jobs/queues needed (emails, scheduled tasks, long-running AI inference, etc.) and what runs them
- Caching strategy if any — what's cached, invalidation approach
- EXT: what browser APIs/permissions are needed, manifest version, content-script vs background-script boundaries
- CLI: argument/flag design, config file format, how it's distributed/installed, update mechanism

## 8. Non-functional requirements
- Performance targets — specific numbers where possible (page load, API response time, app cold-start time), not "should be fast"
- Accessibility requirements (WEB/MOBILE especially) — target standard (e.g. WCAG level) if applicable
- Internationalization/localization — needed at launch or not, which languages
- Security requirements beyond auth — encryption at rest/in transit, rate limiting, input sanitization, secrets management approach
- Compliance considerations if relevant (GDPR, HIPAA, PCI, etc.) — ask, don't assume it doesn't apply
- Offline behavior (MOBILE/DESKTOP/EXT especially) — does it need to work without network at all

## 9. Environments & deployment
- Environments needed (local/dev, staging, production at minimum) — how do they differ
- CI/CD: what triggers a deploy, what gates it (tests passing, manual approval)
- Deployment target specifics (which region, which service tier) — tie back to the hosting choice in step 5
- Monitoring/logging/alerting — what tool, what gets alerted on, who gets paged
- Backup and rollback strategy — for the database and for deploys
- Config/secrets management — how environment-specific values and credentials are handled (must never be hardcoded — flag this explicitly in the plan)

## 10. Testing strategy
- What gets unit tested, what gets integration/e2e tested
- Any manual QA step before release, and by whom
- How is "ready to ship" verified — checklist, staging soak time, etc.

## 11. Build roadmap
- Break the whole build into phases, each of which ends in something genuinely working (not just "backend done" with nothing runnable) — this is what makes the plan buildable incrementally rather than only usable at the very end
- Order phases by dependency, not by preference — a phase should never assume something from a later phase
- For each phase: what's built, what "done" looks like for that phase specifically, roughly how it depends on prior phases
- For any phase that replaces or makes obsolete something from an earlier phase (a temporary implementation, a placeholder integration, an earlier data model): state explicitly what gets removed/deleted in that phase, not just what gets added — a roadmap that only ever adds without ever removing leaves dead code behind by construction

## 12. Adaptive / environment-aware behavior
- Get explicit about the fact that the system must not be hard-coded to the assumptions made during this interview (a specific device, a specific network condition, a specific screen size, a specific hardware tier) — it must detect and adapt to the actual runtime environment it finds itself in
- What can vary at runtime for this project: device capability (RAM/CPU/GPU/storage), network condition (offline/slow/fast), screen size/input method, locale/timezone/language, OS/platform, load/concurrent users — ask which of these actually apply to this category, don't assume
- For each that applies: what should the system do differently under each condition (e.g. lower-spec device → smaller model/lower quality asset; offline → cached/local fallback; slow network → progressive/lazy loading; high load → auto-scale or shed gracefully)
- Is there a minimum viable environment (a floor below which the system explicitly refuses to run / degrades to a stated fallback) rather than failing unpredictably

## 13. Risk register
- What are the top risks that could derail this project — technical (a chosen tech turns out not to fit), scope (creep), resourcing (key person dependency), external (a vendor/API changes terms) — get at least the top 5
- For each: likelihood, impact, and a concrete mitigation or contingency — not just "we'll deal with it if it happens"

## 14. Cost & budget
- Expected infrastructure cost at launch and at the stated year-one scale (hosting, database, CDN, third-party APIs — especially per-call AI/LLM API costs if applicable)
- Any one-time costs (app store fees, domain, certificates, design assets, licenses)
- Who's paying, is there a hard budget ceiling that constrains earlier tech-stack choices — if so, revisit step 5 with that constraint in mind

## 15. Security threat modeling
- Walk through the system's trust boundaries: what's exposed to the public internet, what talks to what, where does user input enter
- For each boundary, ask what an attacker would try (spoofing identity, tampering with data, repudiation of actions, information disclosure, denial of service, elevation of privilege — STRIDE) and what stops them
- Is a third-party security audit or pen test expected before launch, and does that gate the release

## 16. Reliability targets
- Target uptime/availability (e.g. "99.9%") if this is a service that needs to stay up — or explicitly "no formal target" if it's not that kind of project
- Recovery objectives if there's a database/stateful component: RTO (how fast must it be back up) and RPO (how much data loss is tolerable in a disaster)
- What counts as an incident, and is there an on-call/response expectation

## 17. Versioning & release policy
- Semantic versioning or another scheme — and what counts as a breaking change for this project
- Backward-compatibility policy for the API/data format if external consumers exist
- Deprecation policy — how much notice before removing something

## 18. Team & roles
- Solo project or team — if team, who owns which layer (frontend/backend/infra/design/QA), enough to assign the build roadmap phases to someone
- Skip this topic entirely (don't force it) if it's clearly a solo/personal project

## 19. Post-launch maintenance & support
- What happens after "done" — who fixes bugs, who handles user support requests, how often are dependencies updated
- Is there a maintenance budget/time allocation, or does this ship and get abandoned (get an honest answer, it affects earlier architecture choices like how much automation vs manual ops is worth building)

## 20. Vendor lock-in / exit strategy
- For every major third-party dependency (cloud provider, auth provider, payment provider, model API): what would it cost (time/money/rework) to switch away from it later
- Is that an acceptable risk given the project's stage, or does it justify an abstraction layer now

## 21. Infrastructure as code
- Should infra be defined as code (Terraform, Pulumi, CloudFormation, etc.) or managed manually through a provider's console — get an explicit answer, don't default to manual by omission
- If IaC: which tool, and does it match what the hosting choice from step 5 actually supports well

## 22. Analytics & KPI tracking
- What metrics define success post-launch (activation, retention, conversion, error rate, latency, whatever's relevant) — not just "we'll check analytics"
- What tool captures them, and is instrumenting these metrics itself part of the build roadmap (it should be, not an afterthought)

## 23. Market & competitive context (commercial projects only)
- Skip entirely for internal/personal/non-commercial projects
- Who are the closest existing alternatives, and what does this do differently or better
- Any positioning decision that should influence feature prioritization in step 4

## Wrap-up
- Anything the user wants to explicitly rule out (a technology they don't want, a pattern they've been burned by before)
- Any existing code, brand assets, or constraints (existing infra, existing user base, existing brand) the plan must work within
