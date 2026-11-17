# Production-Readiness Standards

Every component the masterplan specifies must clear this bar. When writing the plan, don't just say "implement X" — say what makes X's implementation production-grade rather than prototype-grade, using these as the checklist. Anything below is a Blocker-level gap if left unaddressed in the plan.

## Universal (every project, every category)

- **No hardcoded secrets or config** — API keys, credentials, endpoints, feature flags must come from environment variables or a secrets manager, never literals in code. The plan must specify exactly which values are config and how they're supplied per environment.
- **Real error handling everywhere** — every external call (network, database, file system, third-party API) must have specified failure behavior: what error is shown to the user, what's logged, does it retry, does it degrade gracefully. "Handle errors" is not a spec; "on timeout, retry twice with backoff then show X message and log Y" is.
- **Input validation on every boundary** — every place external input enters the system (API request body, form input, CLI args, file upload) must have validation specified: required fields, types, length/size limits, sanitization against injection.
- **No debug/dev-only artifacts in the shipped path** — no console.log-style debug output left in production code paths, no test/mock data reachable in production, no bypassed auth "for now," no commented-out real logic. The plan should explicitly call out where dev-only conveniences (e.g. a local mock API) are separated from the production path, not just present everywhere.
- **No dead code** — no unused functions, variables, imports, or dependencies; no unreachable branches; no commented-out blocks left in place "just in case"; no permanently-off feature flags left in the codebase instead of being removed. If the build roadmap includes a step that's later superseded, the plan must say to remove the superseded code, not layer the new code on top of it.
- **No silent failures** — every catch/error-handling path must either genuinely recover, or surface the failure (log it, alert on it, return a real error to the caller/user) — never swallow an exception with an empty catch block, a bare pass, or a default value that masks a real error as if nothing happened. Every fallback path (cache miss, retry exhausted, degraded mode) must be observable — logged or metriced — so a silent fallback never looks identical to success in the system's own telemetry.
- **Logging that's actually useful in production** — structured logs with enough context to debug an incident, without leaking secrets or full PII into logs.
- **Authentication and authorization specified per resource** — not just "users log in," but which roles/permissions gate which actions, specified per feature.
- **Rate limiting / abuse protection** on any publicly reachable endpoint.
- **Dependency and version discipline** — the plan names specific, current, actively-maintained versions (verified via research, not assumed), not "latest" left undefined.
- **Documentation as a deliverable, not an afterthought** — README/setup docs, API reference if applicable, and inline comments where logic is non-obvious, all named as build-roadmap deliverables, not implied to happen automatically.
- **Accessibility and internationalization decisions made explicitly**, not defaulted to "we'll add it later" if they were flagged as required in the interview.
- **Licensing** — if any third-party library, model, asset, or service has a license that restricts commercial use, redistribution, or requires attribution, the plan must name it.

## Environment Adaptability (Auto-Adapt) — universal

The system must never be hard-coded to the specific device/network/hardware assumed during planning. It must detect its actual runtime environment and adjust behavior accordingly, with a stated, graceful floor rather than an unpredictable failure when conditions are worse than expected.

- **Capability detection, not assumption** — detect actual available RAM/CPU/GPU/storage, network condition, screen size, OS/platform, locale at runtime, and branch behavior on the detected value, not on what was assumed at build time.
- **Graceful degradation path defined** — for every dimension that varies (device tier, network, load), the plan states what "reduced but working" looks like, not just the best-case path. Silent failure on unsupported/weaker environments is a Blocker.
- **Explicit minimum viable environment** — a floor is stated (minimum RAM, minimum OS version, minimum bandwidth, etc.) below which the system gives a clear, honest message instead of crashing or hanging.
- **No fixed resource ceilings baked in as constants** — batch sizes, cache sizes, concurrency limits, model sizes, quality settings, etc. should scale with detected capability, not be a single hardcoded number that was right for one test machine.
- **Adaptation is tested, not assumed** — the testing strategy (masterplan section 9) must include verifying behavior at low-end/degraded conditions, not just the developer's own machine/network.

Category-specific adaptive behavior:
- WEB: responsive layout across real breakpoints, progressive enhancement, network-aware asset loading (adaptive image/video quality, lazy loading on slow connections), offline fallback via cache where relevant.
- MOBILE: adapts UI across real screen sizes/densities, adjusts feature/quality set based on detected device tier and battery state, platform-specific behavior differences (iOS vs Android) handled explicitly rather than one code path assumed to work everywhere.
- AI/local assistant: detects available RAM/VRAM and selects model size/quantization accordingly (or falls back to a cloud path if defined), adjusts context window/streaming behavior to available resources, degrades to a smaller/faster model rather than failing when resources are constrained.
- DESKTOP: adapts to OS differences (paths, shortcuts, notifications) natively per platform rather than a lowest-common-denominator hack; scales resource use (cache, background work) to detected machine capability.
- API/Backend: auto-scales with load (horizontal scaling or equivalent), sheds load gracefully (rate limiting, queueing, backpressure) rather than falling over under spikes; adapts to regional/latency conditions if multi-region.
- EXT: adapts to the host page's actual DOM/context rather than assuming a fixed page structure; degrades gracefully on pages where expected elements are missing.
- CLI: adapts output to actual terminal capability (color support, width, TTY vs piped output) and OS differences (path separators, shell).

## Website / Web App
- HTTPS everywhere, secure cookie flags, CSRF protection on state-changing requests, CSP headers.
- Responsive across the stated device/browser support matrix, not just desktop.
- SEO basics if public-facing (meta tags, sitemap, semantic HTML) — only if relevant to the project's goals.
- Graceful loading/error/empty states specified per screen, not just the happy path.

## Mobile App
- App store submission requirements accounted for (privacy manifest, permissions justification, icons/screenshots) if targeting app stores.
- Offline behavior explicitly specified, not assumed to "just work."
- Push notification handling (permission flow, token refresh, background delivery) if used.
- Battery/performance impact considered for any background work.

## Local AI Assistant / Agent
- Explicit resource budget (RAM/VRAM/disk) matched against the stated target hardware from the interview — a model that doesn't fit isn't a valid plan.
- Data privacy boundary stated explicitly: what, if anything, ever leaves the device, and under what condition.
- Prompt injection / tool-use safety considered if the agent can take actions (file system, shell, network) — least-privilege on what it's allowed to do without confirmation.
- Update/versioning path for the model itself, separate from the app code.
- Fallback behavior when the model is unavailable, overloaded, or produces an invalid/unsafe output.

## Desktop App
- Auto-update mechanism specified (or explicitly decided against, with reasoning).
- OS-specific packaging/signing/notarization requirements per target OS.
- Local data storage location and format specified, with a migration story for schema changes across versions.

## Backend / API service
- API versioning strategy specified so future changes don't break existing consumers.
- Health-check/readiness endpoints for orchestration and monitoring.
- Idempotency specified for any endpoint that can be safely retried (payments, writes).
- Horizontal scaling story — what's stateless vs stateful, what needs sticky sessions or a shared store.

## Browser Extension
- Manifest version and exact permissions requested, each justified — least privilege, no broad host permissions "just in case."
- Content Security Policy and cross-origin behavior specified.
- Store review requirements (privacy disclosure, permission justification text) accounted for if publishing to a store.

## CLI Tool
- Non-interactive mode / scriptability considered (exit codes, machine-readable output option) even if the primary UX is interactive.
- Config file and flag precedence rules specified explicitly.
- Cross-platform behavior (path handling, shell differences) specified if targeting more than one OS.
- Distribution/install/update mechanism specified (package manager, binary release, etc.).
