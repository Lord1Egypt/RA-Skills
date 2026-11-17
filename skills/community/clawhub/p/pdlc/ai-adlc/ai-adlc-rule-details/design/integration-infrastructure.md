<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Integration & Infrastructure

## Stage: 11 of 13
## Phase: 🟢 DESIGN
## Execution: ALWAYS

---

## Purpose

Define how the system connects to external systems (integration architecture) and how it is deployed, scaled, monitored, and kept available (infrastructure architecture). This is a combined stage because integrations often drive infrastructure requirements (queue capacity, network topology, failover).

**CTO Mindset:** "A brilliant design that can't be deployed, monitored, and scaled by a real ops team is a failure. Architecture includes operations."

---

## MANDATORY: Stage Sub-Role — API Designer

During THIS stage, ALSO adopt the mindset of an **API Designer**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- For each external integration, define the full contract: protocol, direction, auth, data format, frequency, failure handling
- Classify each integration as sync (tight coupling, latency budget) vs. async (decoupled, eventual)
- Design resilience per integration — circuit breaker, timeout, retry, fallback — proportional to its criticality
- Think about the deployment topology from an operations lens: how is this monitored, scaled, and recovered?

### Anti-Patterns for This Stage
- Do NOT design integration in isolation from infrastructure — integrations drive infrastructure requirements (queue capacity, network, failover)
- Do NOT assume all external systems are reliable — define degraded-mode behavior for each

### Quality Check
A good output at this stage sounds like:
- "6 external integrations: 2 sync (REST, <500ms budget each), 4 async (events via queue); per-integration circuit breaker + fallback defined; deployment: 3 AZs, auto-scale on queue depth..."

---

## Depth Adaptation

| Depth | Integration & Infrastructure Behavior |
|-------|--------------------------------------|
| **Minimal** | Integration pattern per external system (sync/async). Basic deployment topology. Scaling approach (horizontal/vertical). Monitoring strategy (what to watch). |
| **Standard** | Full integration architecture per external system (pattern, adapter, failure handling). Deployment topology with container strategy. HA and failover design. Observability stack (metrics, logs, traces, alerts). Backup and DR approach. ADRs for key infrastructure decisions. |
| **Comprehensive** | Detailed integration with sequence diagrams per external system. Circuit breaker and retry policy design. Event schema versioning strategy. Network topology diagram. Capacity planning with scaling triggers. Observability with SLI/SLO definitions. Disaster recovery with RTO/RPO targets and runbook outline. Chaos engineering considerations. Multiple ADRs. |

---

## Part A: Integration Architecture

### Step 1: Load External Systems

From Stage 4 (System Context), load the full list of external systems and their relationships with our system.

---

### Step 2: Define Integration Pattern Per External System

For EACH external system identified in C4 L1:

```markdown
## Integration: {External System Name}

| Aspect | Design |
|--------|--------|
| **Direction** | {Inbound / Outbound / Bidirectional} |
| **Pattern** | {Sync REST / Async Queue / Event-Driven / File Transfer / Polling / Webhook} |
| **Protocol** | {HTTPS, LDAP, SMTP/IMAP, AMQP, WebSocket, syslog, custom} |
| **Authentication** | {API key / OAuth / mTLS / Basic Auth / Certificate / None (internal)} |
| **Data format** | {JSON / XML / CSV / Binary / Protocol-specific} |
| **Frequency** | {Per-request / Batch (schedule) / Event-triggered / Continuous stream} |
| **Latency tolerance** | {Real-time (<1s) / Near-real-time (<30s) / Deferred (minutes/hours)} |
| **Failure handling** | {Retry with backoff / Circuit breaker / Dead letter queue / Manual intervention} |
| **Tenant scoping** | {Per-tenant config (credentials, endpoints) / Shared / N/A} |
| **Criticality** | {Critical — system fails without / Important — degraded without / Optional — enhances} |
```

---

### Step 3: Define Integration Patterns Catalog

Document the patterns used across all integrations:

```markdown
## Integration Patterns Used

### Synchronous Request-Response

| When Used | For integrations requiring immediate response |
|-----------|----------------------------------------------|
| **Pattern** | Caller sends request → waits → receives response |
| **Error handling** | Timeout → retry (max {n}) → fallback / error state |
| **Circuit breaker** | Open after {n} consecutive failures; half-open retry after {n}s |
| **Examples** | {List which integrations use this} |

### Asynchronous (Queue-Based)

| When Used | For work that can be deferred; decouples caller from processor |
|-----------|--------------------------------------------------------------|
| **Pattern** | Producer enqueues message → Consumer processes independently |
| **Delivery guarantee** | {At-least-once / At-most-once / Exactly-once} |
| **Dead letter queue** | After {n} failed attempts → move to DLQ for manual inspection |
| **Examples** | {List which integrations use this} |

### Event-Driven (Publish-Subscribe)

| When Used | For broadcasting state changes to multiple consumers |
|-----------|-----------------------------------------------------|
| **Pattern** | Publisher emits event → N subscribers react independently |
| **Event schema** | {Envelope: event_type, timestamp, tenant_id, payload} |
| **Ordering** | {Per-tenant ordered / Global unordered / Partition-ordered} |
| **Examples** | {List which integrations use this} |

### Polling / Scheduled Sync

| When Used | When external system has no push mechanism |
|-----------|-------------------------------------------|
| **Pattern** | Scheduler triggers periodic pull from external source |
| **Frequency** | {Configurable per integration — e.g., every 5 min} |
| **Idempotency** | {Watermark-based / Last-modified tracking / Deduplication} |
| **Examples** | {List which integrations use this} |

### File/Batch Transfer

| When Used | Bulk data exchange (import/export) |
|-----------|-------------------------------------|
| **Pattern** | Generate file → transfer → process |
| **Format** | {CSV / Excel / JSON / XML} |
| **Transfer** | {SFTP / Shared storage / API upload} |
| **Examples** | {List which integrations use this} |
```

---

### Step 4: Define Adapter/Connector Architecture

```markdown
## Connector Architecture

### Design Principle

Each external integration is accessed through an **adapter layer** that:
- Encapsulates the external system's API/protocol details
- Provides a consistent internal interface
- Handles authentication, retry, and error translation
- Is replaceable without affecting business logic

### Adapter Structure

```
Business Logic (Service Layer)
       │
       ▼
┌─────────────────────────┐
│   Integration Interface  │  ← Internal contract (stable)
├─────────────────────────┤
│   Adapter Implementation │  ← External-specific code (changeable)
├─────────────────────────┤
│   External System SDK    │  ← Library/HTTP client
└─────────────────────────┘
       │
       ▼
   External System
```

### Per-Tenant Configuration (if multi-tenant)

| Configuration | Scope | Storage |
|--------------|:-----:|---------|
| Endpoint URL | Per-tenant | Tenant config (encrypted) |
| Credentials (API keys, passwords) | Per-tenant | Secrets store (encrypted at rest) |
| Feature toggles (enabled/disabled) | Per-tenant | Tenant config |
| Rate limits (external system's limits) | Per-tenant or global | Config |
```

---

### Step 5: Define Internal Event Architecture (if applicable)

```markdown
## Internal Event Bus

### Purpose
Decouple modules within the system for async communication without external infrastructure dependency.

### Design

| Aspect | Decision |
|--------|----------|
| **Technology** | {In-process event emitter / Queue-backed (BullMQ) / Dedicated broker} |
| **Scope** | {Within application container / Cross-container} |
| **Event naming** | `{domain}.{entity}.{action}` — e.g., `tickets.ticket.created` |
| **Payload** | {Minimal reference (ID + tenant) / Full entity snapshot} |
| **Consumers** | {Synchronous subscribers / Async queue workers / Both} |

### Event Catalog (Key Events)

| Event | Producer | Consumer(s) | Purpose |
|-------|----------|-------------|---------|
| `{domain}.{entity}.{action}` | {Module} | {Module(s)} | {What triggers downstream} |
```

---

### Step 5b: Legacy Integration Patterns (IF MODE D ACTIVE)

**Execute IF:** Requirements Ingestion detected brownfield input (Mode D) AND existing system interactions are required.
**Skip IF:** Greenfield project OR brownfield with full replacement (no coexistence needed).

When integrating with or migrating from a legacy system, standard integration patterns (Step 2-4) apply but additional patterns are needed to manage the transition boundary. These are distinct from "external system integrations" because the legacy system is OURS — we control (or will control) both sides.

**Legacy-specific integration patterns:**

```markdown
## Legacy Integration Patterns

### Anti-Corruption Layer (ACL)

| When Used | New system interacts with legacy system that has a different domain model |
|-----------|-------------------------------------------------------------------------|
| **Purpose** | Translate between legacy concepts and new domain model at the boundary |
| **Pattern** | New system defines its own interfaces → ACL adapter translates → Legacy system |
| **Direction** | New → ACL → Legacy (and reverse for queries) |
| **Ownership** | ACL belongs to the new system (it protects the new model from legacy pollution) |
| **Lifecycle** | Exists during transition; removed when legacy component is decommissioned |

**Structure:**
```
┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  New System      │     │  Anti-Corruption │     │  Legacy System   │
│  (clean model)   │────►│  Layer (ACL)     │────►│  (legacy model)  │
│                  │◄────│                  │◄────│                  │
└──────────────────┘     └─────────────────┘     └──────────────────┘
         │                        │
         │  Domain events         │  Translated calls
         │  Clean contracts       │  Legacy protocols
```

**Rules:**
- New system NEVER imports legacy data types/models directly
- ACL handles ALL translation (data format, naming, semantics)
- ACL is stateless (no business logic — pure translation)
- ACL is tested with contract tests on BOTH sides
- When legacy is decommissioned: replace ACL with direct implementation

---

### Strangler Fig Routing

| When Used | Gradually migrating functionality from legacy to new system |
|-----------|--------------------------------------------------------------|
| **Purpose** | Route requests to either legacy or new system based on feature/endpoint |
| **Pattern** | Facade/proxy sits in front → routes based on rules → legacy OR new |
| **Routing criteria** | By feature flag, by endpoint, by tenant, by user cohort |
| **Lifecycle** | Routes shift from legacy→new over time; removed when migration complete |

**Structure:**
```
┌──────────────┐     ┌──────────────────────────────────────────┐
│   Clients    │────►│  Routing Layer (Reverse Proxy / Gateway)  │
└──────────────┘     └────────────┬──────────────┬──────────────┘
                                  │              │
                          ┌───────▼──────┐ ┌────▼───────────┐
                          │ New System   │ │ Legacy System  │
                          │ (migrated    │ │ (not yet       │
                          │  features)   │ │  migrated)     │
                          └──────────────┘ └────────────────┘
```

**Rules:**
- Routing is transparent to clients (same URL, same contracts)
- Feature flags or configuration drive routing decisions (not code changes)
- Both systems return compatible response formats (or router transforms)
- Monitoring on BOTH paths — compare latency, error rate, response shape
- Rollback = flip routing back to legacy (instant)

---

### Data Synchronization Patterns

| Pattern | When to Use | Trade-offs |
|---------|-------------|-----------|
| **Shared Database** | Short transition; same technology; tight coupling acceptable | Fast; no sync delay. BUT: couples releases; schema changes risky |
| **Event-Based Sync** | Loose coupling preferred; eventually consistent acceptable | Decoupled; resilient. BUT: eventual consistency; event schema maintenance |
| **Dual-Write** | Must keep both systems consistent; transition period is long | Both always up-to-date. BUT: failure modes complex; transaction boundaries unclear |
| **Change Data Capture (CDC)** | Legacy has no event capability; can't modify legacy code | Non-invasive; reads DB changelog. BUT: ties to DB internals; schema-dependent |
| **ETL/Batch Sync** | Acceptable delay; large data volumes; clean transformation needed | Simple; well-understood. BUT: stale data between runs; missed real-time changes |

**Selection criteria:**

| If... | Use... |
|-------|--------|
| Transition < 3 months AND same DB technology | Shared Database |
| Both systems have event infrastructure | Event-Based Sync |
| Legacy cannot be modified AT ALL | Change Data Capture (CDC) |
| Data freshness SLA > 1 hour | ETL/Batch Sync |
| Real-time consistency required AND both systems modifiable | Dual-Write (with saga/compensation) |

---

### Characterization Testing at Integration Points

| What | Why | How |
|------|-----|-----|
| Record existing system behavior at API boundaries | You can't safely replace what you don't understand | Capture request/response pairs from production traffic (sanitized) |
| Document undocumented protocols | Legacy systems often have implicit contracts | Instrument or intercept; build contract from observations |
| Build assertion suite | Verify new system produces same outputs for same inputs | Golden master tests; shadow traffic comparison |
| Map failure modes | Legacy may have quirky error handling clients depend on | Chaos testing on legacy; document which errors clients handle |

**Rule:** NEVER begin replacing or modifying a legacy integration point without characterization tests covering its observed behavior. "It seems to work" is not sufficient — you need proof that your understanding matches reality.
```

**Document per integration:**

For each legacy system interaction (from the Brownfield Strategy ADR's "Integration During Transition" table), define:

| Aspect | What to Specify |
|--------|----------------|
| Pattern | ACL / Strangler Route / Shared DB / Event Sync / CDC |
| Data flow direction | Legacy→New / New→Legacy / Bidirectional |
| Consistency model | Strongly consistent / Eventually consistent / Best-effort |
| Failure handling | Retry + DLQ / Fallback to legacy / Circuit breaker + manual |
| Decommission trigger | When is this integration removed? (which phase?) |
| Characterization tests | Yes/No — exist before any modification |

---

## Part B: Infrastructure & Deployment Architecture

### Step 6: Define Deployment Topology

```markdown
## Deployment Architecture

### Deployment Model: {Docker Compose / Kubernetes / Bare Metal / Hybrid}

### Topology Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     NETWORK BOUNDARY                              │
│                                                                   │
│  ┌──────────────┐     ┌──────────────────────────────────────┐  │
│  │ Load Balancer │────►│          Application Tier             │  │
│  │  (Nginx/HAP) │     │  ┌────────┐ ┌────────┐ ┌────────┐  │  │
│  └──────────────┘     │  │ App 1  │ │ App 2  │ │Worker  │  │  │
│                        │  └────────┘ └────────┘ └────────┘  │  │
│                        └──────────────────────────────────────┘  │
│                                         │                         │
│                        ┌──────────────────────────────────────┐  │
│                        │          Data Tier                    │  │
│                        │  ┌──────┐ ┌───────┐ ┌────────┐     │  │
│                        │  │  DB  │ │ Cache │ │ Search │     │  │
│                        │  └──────┘ └───────┘ └────────┘     │  │
│                        └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Container-to-Host Mapping

| Container | Instances (Min) | Instances (Target) | Host Affinity | Resource Profile |
|-----------|:---------------:|:------------------:|:-------------:|:----------------:|
| {Container name} | {n} | {n} | {Any / Dedicated / Co-located with X} | {CPU/RAM estimate} |
```

---

### Step 7: Define High Availability

```markdown
## High Availability

### Redundancy Per Component

| Component | Redundancy Model | Failover Mechanism | Recovery Time |
|-----------|:----------------:|:------------------:|:-------------:|
| Application nodes | {N active / Active-passive} | {Load balancer health check → remove unhealthy} | {Seconds} |
| Database | {Primary + replica / Active-standby / Cluster} | {Automatic failover / Manual promotion} | {Seconds / Minutes} |
| Cache | {Cluster / Replica / None (reconstructible)} | {Auto-reconnect / Fallback to DB} | {Seconds} |
| Queue/Broker | {Cluster / Persistent / Reconstructible} | {Failover / Retry from producers} | {Seconds} |
| Load Balancer | {Redundant pair / Single (risk accepted)} | {Keepalived / DNS failover} | {Seconds} |

### Single Points of Failure

| Component | SPOF? | Mitigation |
|-----------|:-----:|-----------|
| {Component} | {Yes/No} | {How mitigated or risk accepted} |

### Health Checks

| Level | What's Checked | Frequency | Action on Failure |
|-------|---------------|:---------:|:-----------------:|
| Load balancer → App | HTTP health endpoint | {5-10s} | Remove from pool |
| App → Database | Connection test | {30s} | Alert; failover if replica available |
| App → Cache | Ping | {10s} | Alert; degrade gracefully (bypass cache) |
| App → Queue | Connection test | {30s} | Alert; retry queue reconnection |
```

---

### Step 8: Define Scaling Strategy

```markdown
## Scaling

### Horizontal Scaling (Add Instances)

| Component | Horizontally Scalable? | Scaling Trigger | Max Instances |
|-----------|:---------------------:|:---------------:|:-------------:|
| Application | {Yes — stateless} | {CPU > 70% / Request queue > threshold} | {n} |
| Background workers | {Yes} | {Queue depth > threshold} | {n} |
| Database read replicas | {Yes} | {Read load / Replica lag} | {n} |
| Cache | {Yes — cluster mode} | {Memory usage / Eviction rate} | {n} |

### Vertical Scaling (Add Resources)

| Component | When to Scale Vertically | Limit |
|-----------|-------------------------|-------|
| Database primary | {Write bottleneck; can't shard easily} | {Hardware max} |
| Search index | {Index size exceeds RAM} | {Hardware max} |

### Statelessness Requirements

| Component | Stateless? | What Makes It Stateless |
|-----------|:----------:|------------------------|
| Application | {Yes} | {No local session; externalized cache; no local file deps} |
| Workers | {Yes} | {Job state in queue; no local memory between jobs} |
| Database | No | Stateful by nature — scaled via replication |
```

---

### Step 9: Define Observability Stack

```markdown
## Observability

### Metrics

| Aspect | Decision |
|--------|----------|
| **Tool** | {Prometheus / StatsD / Custom} |
| **Collection** | {Pull (Prometheus scrape) / Push (StatsD)} |
| **Dashboards** | {Grafana / Custom} |
| **Key metrics** | Request rate, error rate, latency (p50/p95/p99), queue depth, DB connections, cache hit ratio |
| **Per-tenant metrics** | {Yes — labeled by tenant_id / No} |

### Logging

| Aspect | Decision |
|--------|----------|
| **Format** | {Structured JSON / Plaintext} |
| **Aggregation** | {Loki / ELK / Fluentd → storage} |
| **Retention** | {n days hot / n days cold} |
| **Correlation** | {Request ID in all log lines; tenant_id as field} |
| **Sensitive data** | {PII masked/excluded from logs} |

### Tracing (if applicable)

| Aspect | Decision |
|--------|----------|
| **Tool** | {Jaeger / Zipkin / OpenTelemetry / None for v1} |
| **Scope** | {All requests / Sampled (n%) / On-demand} |

### Alerting

| Aspect | Decision |
|--------|----------|
| **Tool** | {Alertmanager / Grafana alerts / Custom} |
| **Channels** | {Email / Slack / PagerDuty / SMS} |
| **Key alerts** | Error rate spike, latency degradation, disk >80%, DB replication lag, health check failure |
| **Escalation** | {Auto-escalate after {n} minutes unacknowledged} |
```

---

### Step 10: Define Backup & Disaster Recovery

```markdown
## Backup & Disaster Recovery

### Backup Schedule

| Data | Method | Frequency | Retention | Location |
|------|--------|:---------:|:---------:|----------|
| Database | {pg_dump / WAL archiving / Snapshot} | {Daily full + continuous WAL} | {n days} | {On-site + off-site} |
| File storage | {rsync / Snapshot / Replication} | {Daily} | {n days} | {location} |
| Configuration | {Git / Backup script} | {On change} | {Indefinite} | {Repository} |
| Secrets | {Vault backup / Export} | {On change} | {n copies} | {Secure off-site} |

### Recovery Targets

| Metric | Target | How Achieved |
|--------|:------:|:-------------|
| RPO (max data loss) | {From requirements} | {WAL shipping / replication frequency} |
| RTO (max downtime) | {From requirements} | {Standby infrastructure + documented runbook} |

### DR Testing

| Aspect | Approach |
|--------|----------|
| Frequency | {Quarterly / Semi-annual} |
| Scope | {Full failover / Component recovery / Tabletop exercise} |
| Documentation | {Runbook maintained and versioned} |
```

---

### Step 11: Define Network & Security Zones

```markdown
## Network Architecture

### Security Zones

| Zone | Contains | Access From | Access To |
|------|----------|:----------:|:---------:|
| DMZ / Edge | Load balancer, reverse proxy | Internet | Application zone |
| Application | API servers, web apps, workers | DMZ, Data zone | Data zone, External integrations |
| Data | Database, cache, search, queue | Application zone only | — (no outbound) |
| Management | Monitoring, logging, backup | All zones (read) | — |

### Firewall Rules (Conceptual)

| Source | Destination | Port | Purpose |
|--------|-------------|:----:|---------|
| Internet | Load balancer | 443 | HTTPS traffic |
| Load balancer | App nodes | {app port} | Proxy to application |
| App nodes | Database | {db port} | SQL queries |
| App nodes | Cache | {cache port} | Cache operations |
| App nodes | External systems | 443/various | Outbound integrations |
```

---

### Step 12: Produce ADR(s)

Possible integration/infrastructure ADRs:

| ADR | Decision |
|-----|----------|
| ADR-{nnn} | Container orchestration (Compose vs. K8s vs. bare metal) |
| ADR-{nnn} | Observability stack selection |
| ADR-{nnn} | Internal event/messaging approach |
| ADR-{nnn} | Backup/DR strategy |

---

### Step 13: Assemble Document

Compile into one or two documents:

**Option A (single document):** `Integration_Infrastructure.md` — both parts combined
**Option B (two documents):** `Integration_Architecture.md` + `Infrastructure_Deployment.md`

Choose based on document length. If combined exceeds 40 pages → split.

Contents:
1. Integration patterns catalog
2. Per-system integration design
3. Adapter/connector architecture
4. Internal event architecture
5. Deployment topology diagram
6. High availability design
7. Scaling strategy
8. Observability stack
9. Backup & DR
10. Network security zones
11. ADR references

---

### Step 14: Present for Review

```markdown
## Review: Integration & Infrastructure — {system_name}

**Integration:**
- External integrations: {n} systems
- Patterns used: {sync REST: n, async: n, event-driven: n, polling: n}
- Adapter architecture: {approach}
- Internal events: {n} key events defined

**Infrastructure:**
- Deployment: {model — e.g., "Docker Compose, 10-12 containers"}
- HA: {summary — e.g., "2+ app nodes, DB primary + replica, redundant LB"}
- Scaling: {approach — e.g., "Horizontal app + workers; vertical DB"}
- Observability: {stack — e.g., "Prometheus + Grafana + Loki"}
- DR: RPO {value}, RTO {value}

**ADRs produced:** {n}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Integration and infrastructure design is complete; proceed
- (b) **Add integration** — Missing external system connection
- (c) **Adjust infrastructure** — Topology or sizing needs revision
- (d) **Change observability** — Different monitoring approach
- (e) **Strengthen HA/DR** — Need more resilience
```

---

### Step 15: Log and Transition

1. Update state: Stage 11 = ✅ Done; Current Stage = 12
2. Update ADR register
3. Update Architecture Workbook

Display:

```
✅ Stage 11: Integration & Infrastructure — Complete

🔌 Integrations: {n} | 🖥️ Deployment: {model} | 📊 Observability: {stack}
📄 Saved to: {file_path}

Next → Stage 12: Component Design (C4 Level 3)

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/09_Integration_Architecture.md` + `{output_root}/10_Infrastructure_Deployment.md` (split)
- Phase folders: `{output_root}/design/Integration_Infrastructure.md` (combined or split)

---

## Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| All externals covered | Every system from C4 L1 has an integration pattern defined |
| Failure handling | Every integration has retry/circuit breaker/fallback defined |
| Tenant-aware | Per-tenant credentials and configuration supported (if multi-tenant) |
| No SPOF | All critical components have redundancy or risk-accepted justification |
| Scaling clear | Every container has scaling model defined |
| Observable | Metrics, logs, and alerts cover all critical paths |
| DR tested | Backup targets (RPO/RTO) achievable with stated strategy |
| Constraint compliant | Deployment model respects on-prem/cloud/network constraints |
| Principle aligned | Infrastructure simplicity matches team operational capability |
