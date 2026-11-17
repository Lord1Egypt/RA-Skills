<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Backend-for-Frontend (BFF)

**Extension ID:** bff-pattern
**Version:** 1.1.0
**Rule Prefix:** BFF
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 5 (Container Design)
- **Secondary Stages:** Stage 7 (API Architecture), Stage 11 (Integration Architecture)

These rules apply to the design of client-specific backend layers that aggregate, shape, and optimize data delivery for distinct consumer types.

---

## MANDATORY: Extension Sub-Role — API Designer

When this extension is active, ALSO adopt the mindset of an **API Designer**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of BFF rule enforcement.

### Behavioral Shifts
- Think consumer-first — the BFF exists because a specific client type needs data shaped differently than the backend provides
- Separate gateway concerns (routing, auth, CORS) from BFF concerns (aggregation, shaping, client-specific logic)
- One BFF per client type — web, mobile, third-party get their own; a "universal BFF" becomes a monolith
- Shield clients from knowing backend service topology — the BFF is the single aggregation point

### Anti-Patterns for This Extension
- Do NOT create a BFF that only proxies without aggregating — that's an unnecessary hop; use the gateway
- Do NOT serve multiple divergent client types from a single BFF with conditional logic

### Quality Check
A good output with this extension sounds like:
- "3 BFFs: web (aggregates 4 services), mobile (optimized payloads, offline-first), partner-API (stable, versioned); gateway handles auth + rate-limiting only..."

---

## Rules

### Rule BFF-01: BFF vs. Gateway Decision

**Statement:** The architecture must explicitly document why a BFF is needed instead of (or in addition to) an API gateway. A BFF is justified only when clients require client-specific aggregation, shaping, or business logic beyond simple routing and cross-cutting concerns.

**Verification:**
- [ ] Decision rationale is documented (why gateway alone is insufficient)
- [ ] Responsibilities of gateway vs. BFF are clearly separated
- [ ] Gateway handles: routing, auth, rate limiting, CORS (cross-cutting only)
- [ ] BFF handles: aggregation, response shaping, client-specific logic
- [ ] No duplication of responsibility between gateway and BFF

**Anti-Pattern:** Creating a BFF that only proxies requests to backend services without any aggregation or shaping — this is just an unnecessary extra hop (use the gateway instead).

**ADR Trigger:** Yes — When deciding whether to use BFF, API gateway, or both. This is a foundational architectural decision.

---

### Rule BFF-02: One BFF per Client Type

**Statement:** Each distinct client type (web, mobile, third-party, internal tooling) must have its own BFF instance. A single BFF must not serve multiple client types with divergent needs.

**Verification:**
- [ ] BFF instances are enumerated per client type
- [ ] Each BFF serves exactly one client type (or a family with identical data needs)
- [ ] Data shape returned by each BFF is optimized for its specific consumer
- [ ] No "shared BFF" serving both mobile and web with conditional logic
- [ ] BFF boundaries align with client team boundaries

**Anti-Pattern:** "Universal BFF" — a single BFF trying to serve all client types with if/else branching per client, eventually becoming a coupled monolith.

**ADR Trigger:** Yes — When deciding how many BFFs to create and how to draw the boundary between client types.

---

### Rule BFF-03: Aggregation Responsibility

**Statement:** Each BFF is responsible for aggregating data from multiple backend services into a single response optimized for its client. The BFF shields the client from knowing backend service topology.

**Verification:**
- [ ] BFF aggregates calls to multiple backend services into unified responses
- [ ] Client makes one call to BFF instead of multiple calls to backend services
- [ ] Backend service topology is hidden from the client (client depends only on BFF API)
- [ ] Aggregation logic handles partial failures gracefully (one backend down ≠ total failure)
- [ ] Response shape matches what the client view/screen actually needs (no over-fetching)

**Anti-Pattern:** Client directly calling multiple backend services and stitching responses together, duplicating aggregation logic across client platforms.

**ADR Trigger:** No

---

### Rule BFF-04: BFF Ownership Model

**Statement:** BFF ownership must be explicitly assigned. The team that owns the client experience should own the BFF (frontend team model) or a clear API team owns it with a defined contract with frontend consumers.

**Verification:**
- [ ] Ownership of each BFF is documented (which team maintains it)
- [ ] Ownership model is consistent across all BFFs (same pattern for all)
- [ ] The owning team can deploy the BFF independently
- [ ] Change requests to BFF have a clear process (who approves, who implements)
- [ ] No "orphaned" BFF without a clear owner

**Anti-Pattern:** BFF owned by the backend team that doesn't understand client needs, or BFF owned by nobody, becoming stale and misaligned with client requirements.

**ADR Trigger:** Yes — When deciding the ownership model (frontend-team-owned vs. backend-team-owned vs. dedicated API team).

---

### Rule BFF-05: Client-Specific Authentication Flow

**Statement:** Each BFF must handle the authentication and session management pattern appropriate for its client type. Token formats, session lifetimes, and refresh strategies may differ per BFF.

**Verification:**
- [ ] Authentication flow is documented per BFF (OAuth flow, token type, session strategy)
- [ ] BFF manages token exchange with backend services (client tokens → internal tokens)
- [ ] Session lifetime matches client type expectations (e.g., mobile = long-lived, web = shorter)
- [ ] Token refresh strategy is defined per BFF
- [ ] BFF does not expose internal service tokens to the client

**Anti-Pattern:** Forcing all client types to use the same authentication flow (e.g., requiring mobile apps to use browser-redirect OAuth flows that don't fit mobile UX).

**ADR Trigger:** No

---

### Rule BFF-06: BFF Must Not Contain Domain Logic

**Statement:** BFFs must contain only aggregation, shaping, and client-adaptation logic. Business rules, domain logic, and data persistence must remain in backend services.

**Verification:**
- [ ] No business rules are implemented in the BFF
- [ ] BFF does not own any persistent data store
- [ ] BFF logic is limited to: aggregation, filtering, sorting, formatting, caching
- [ ] If business logic starts creeping in, it is a signal to move it to a backend service
- [ ] BFF tests are primarily integration tests (does it aggregate correctly?) not unit tests of domain logic

**Anti-Pattern:** BFF becoming a "fat middle tier" that accumulates business rules, eventually becoming the hardest component to maintain and the source of most bugs.

**ADR Trigger:** No

---

### Rule BFF-07: BFF Resilience and Partial Response

**Statement:** When a BFF aggregates from multiple backends, it must define partial response behavior — which backend failures degrade the response vs. which are critical failures that block the response entirely.

**Verification:**
- [ ] Each backend dependency of a BFF is classified (critical vs. optional)
- [ ] Partial response strategy is documented (degrade gracefully vs. fail fast)
- [ ] Client receives an indication of degraded data (e.g., null fields, metadata flags)
- [ ] Timeout budget is defined per BFF request (total budget allocated across backends)
- [ ] Caching or fallback values are defined for non-critical backend failures

**Anti-Pattern:** BFF failing entirely because one of five aggregated backends is slow or down, even though the client could render 80% of the page without that data.

**ADR Trigger:** No

---

### Rule BFF-08: BFF Caching Strategy

**Statement:** Each BFF must define its caching strategy independently, based on client access patterns. Caching at the BFF layer reduces backend load and improves client-perceived latency.

**Verification:**
- [ ] Caching strategy is documented per BFF (what is cached, TTL, invalidation)
- [ ] Cache scope is appropriate for the client type (per-user, per-tenant, shared)
- [ ] Cache invalidation mechanism is defined (time-based, event-driven, manual)
- [ ] Stale-while-revalidate or equivalent pattern is considered for availability
- [ ] Cache hit ratio targets are established and monitored

**Anti-Pattern:** No caching at the BFF level, causing every client request to fan out to all backends even for data that rarely changes, creating unnecessary load and latency.

**ADR Trigger:** No

---

### Rule BFF-09: BFF API Versioning and Evolution

**Statement:** Each BFF exposes its own versioned API contract to its client. BFF API versions evolve independently of backend service versions and independently of other BFFs.

**Verification:**
- [ ] BFF API has its own versioning scheme (independent of backend APIs)
- [ ] BFF can absorb backend API changes without breaking its own client contract
- [ ] Deprecation policy is defined per BFF API (how long old versions are supported)
- [ ] Multiple BFF API versions can run simultaneously during migration
- [ ] Client teams are notified of BFF API deprecations through documented process

**Anti-Pattern:** BFF API versions tightly coupled to backend versions, forcing client updates whenever any backend service updates its API.

**ADR Trigger:** Yes — When defining the BFF API versioning strategy (URL-based, header-based, or GraphQL schema evolution).

---

### Rule BFF-10: BFF Scaling Independence

**Statement:** Each BFF must be independently scalable based on its client's traffic patterns. BFF scaling must not be coupled to backend service scaling or other BFF instances.

**Verification:**
- [ ] Each BFF can scale horizontally independent of other BFFs
- [ ] Scaling triggers are based on client traffic to that specific BFF
- [ ] BFF does not share compute resources with other BFFs (no single process serving multiple BFFs)
- [ ] Backend services scale based on their own load (not BFF count)
- [ ] Traffic spikes from one client type (e.g., mobile push notification) don't affect other clients

**Anti-Pattern:** Running all BFFs in the same process/deployment, where a traffic spike for mobile clients causes degradation for web clients.

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with BFF rules active, verify:

- [ ] BFF vs. gateway decision is documented with clear rationale
- [ ] One BFF per distinct client type (no universal BFF)
- [ ] Aggregation responsibilities are defined per BFF
- [ ] Ownership model is explicit and documented
- [ ] Authentication flows are designed per client type
- [ ] No domain logic resides in any BFF
- [ ] Partial response behavior is defined for backend failures
- [ ] Caching strategy is documented per BFF
- [ ] BFF API versioning is independent of backend versions
- [ ] Each BFF is independently deployable and scalable

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| BFF-01 | Deciding whether to use BFF, API gateway, or both |
| BFF-02 | Deciding how many BFFs and boundary between client types |
| BFF-04 | Selecting BFF ownership model (frontend vs. backend vs. dedicated team) |
| BFF-09 | Defining BFF API versioning strategy |

---

## Templates

### BFF Design Card

```
## BFF: {Client Type} BFF

**Client Type Served:** {Web SPA / Mobile / Third-Party / Internal}
**Owning Team:** {Team name}
**Authentication Flow:** {OAuth2 PKCE / API Key / Session-based / etc.}
**Backend Services Aggregated:** {List of backend services called}
**Caching Strategy:** {Per-user / Per-tenant / Shared | TTL | Invalidation method}
**Partial Response Policy:**
| Backend | Critical? | Fallback on Failure |
|---------|-----------|---------------------|
| {Service A} | Yes | Fail entire request |
| {Service B} | No | Return null / cached |
**Scaling Trigger:** {Metric + threshold}
**API Version:** {Current version}
```

### BFF vs. Gateway Responsibility Matrix

```
| Concern | API Gateway | BFF |
|---------|-------------|-----|
| Routing | ✅ | ❌ |
| Authentication | ✅ | Token exchange only |
| Rate Limiting | ✅ | ❌ |
| Response Aggregation | ❌ | ✅ |
| Data Shaping | ❌ | ✅ |
| Client-Specific Logic | ❌ | ✅ |
| Caching (client-aware) | ❌ | ✅ |
| Protocol Translation | ✅ (edge) | ❌ |
```

### BFF Aggregation Flow

```
## Endpoint: {BFF Endpoint}

**Client Request:** {What the client sends}
**Backend Calls:**
1. {Service A} — {endpoint} — {purpose}
2. {Service B} — {endpoint} — {purpose}
3. {Service C} — {endpoint} — {purpose} [optional, fallback: null]

**Response Shape:** {What the client receives — fields, structure}
**Total Timeout Budget:** {e.g., 2000ms, split as: A=500ms, B=800ms, C=400ms + overhead}
```
