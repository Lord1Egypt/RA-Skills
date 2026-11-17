# How to Choose Architecture Extensions

**Purpose:** Practical guide for deciding which AI-ADLC extensions to activate — the decision criteria, common mistakes, composition rules, and downstream impact of each extension choice.

---

## Who This Is For

Architects and tech leads running AI-ADLC who reach the extension opt-in points and need to decide: "Does my architecture actually need this pattern? What are the consequences of activating it? Can I combine multiple extensions?"

---

## The Six Extensions

| Extension | Pattern | One-Line Decision Criteria |
|-----------|---------|---------------------------|
| **DDD Tactical** | Domain-Driven Design (aggregates, entities, value objects, events) | Complex domain logic with multiple bounded contexts |
| **Microservices** | Independently deployable services | ≥3 services with separate deployment lifecycles |
| **BFF Pattern** | Backend-for-Frontend | Multiple frontend channels needing different API shapes |
| **Event Sourcing / CQRS** | Event store + command/query separation | Audit-critical data or temporal query requirements |
| **Resilience Patterns** | Circuit breakers, bulkheads, retries, fallbacks | ≥3 external integrations or high-availability requirement |
| **Feature Flags** | Controlled rollout, trunk-based delivery | Gradual rollout, A/B testing, or decoupled deployment/release |

---

## Decision Framework

For each extension, ask three questions:

### Question 1: "Does the architecture REQUIRE this pattern?"

| Extension | Required When | NOT Required When |
|-----------|--------------|-------------------|
| DDD Tactical | Domain has complex business rules spanning multiple entities; multiple teams own different domains | Simple CRUD; single domain; thin business logic layer |
| Microservices | Services need independent scaling, deployment, or technology choices | All components deploy together; single team owns everything |
| BFF Pattern | Mobile app needs different data than web; partner API needs different auth | Single frontend; all consumers need same API shape |
| Event Sourcing | Legal requirement to reconstruct past states; "what happened when" queries | Current-state-only queries; simple update-in-place sufficient |
| Resilience | SLA requires >99.9% uptime; cascade failure is a realistic risk | Internal tool; occasional downtime acceptable; few integrations |
| Feature Flags | Trunk-based development; need to deploy without releasing; A/B experiments | Feature branches with traditional release; no gradual rollout need |

**Key rule:** Activate because architecture DEMANDS it, not because it would be "nice to have." Each extension adds constraints, complexity, and cognitive overhead.

### Question 2: "Can the team deliver this pattern?"

| Extension | Team Capability Needed |
|-----------|----------------------|
| DDD Tactical | Strong domain modeling experience; ability to identify aggregates and boundaries |
| Microservices | DevOps maturity; CI/CD per service; distributed tracing understanding |
| BFF Pattern | API design experience; understanding of client-specific optimization |
| Event Sourcing | Event modeling skill; eventual consistency tolerance; projection management |
| Resilience | Chaos engineering awareness; monitoring infrastructure; fallback design |
| Feature Flags | Flag lifecycle management; test complexity management; release coordination |

**If the team doesn't have the capability:** Consider whether the project timeline allows for learning, or whether a simpler pattern achieves 80% of the benefit with 20% of the complexity.

### Question 3: "What's the downstream impact?"

Each extension affects AI-DWG generation and AI-GCE governance:

| Extension | AI-DWG Impact | AI-GCE Impact |
|-----------|--------------|---------------|
| DDD Tactical | Domain-based folder structure; bounded context separation | Domain boundary enforcement; aggregate integrity rules |
| Microservices | Per-service folders; service mesh config; distributed tracing setup | Inter-service contract rules; deployment independence checks |
| BFF Pattern | BFF layer in container structure; per-client API routing | API versioning enforcement; BFF-specific security rules |
| Event Sourcing | Event store infrastructure; projection services; command/query separation | Event immutability rules; projection consistency checks |
| Resilience | Circuit breaker configs; health check endpoints; fallback implementations | Resilience pattern verification; SLA compliance rules |
| Feature Flags | Flag management service; evaluation endpoints; cleanup lifecycle | Flag hygiene rules (no stale flags); testing-with-flags requirements |

---

## When Extensions Are Presented

AI-ADLC presents each extension at the stage where the decision is architecturally relevant:

| Extension | Presented At | Why |
|-----------|-------------|-----|
| DDD Tactical | Stage 4 (System Context) | Bounded contexts are a system-level concern |
| Microservices | Stage 5 (Container Design) | Service decomposition is a container decision |
| BFF Pattern | Stage 5 (Container Design) | BFF is an additional container |
| Event Sourcing / CQRS | Stage 9 (Data Architecture) | Fundamentally changes data model |
| Resilience Patterns | Stage 11 (Integration) | Applies to distributed communication |
| Feature Flags | Stage 12 (Component Design) | Affects component behavior implementation |

**You can decline now and activate later** — but activating later means re-running from the relevant stage (rules apply retroactively to prior decisions).

---

## Extension Composition (Combining Multiple)

Extensions are designed to compose without conflict:

### Common Combinations

| Combination | Use Case | Composition Notes |
|-------------|----------|-------------------|
| DDD + Microservices | Bounded contexts mapped to services | DDD defines boundaries; Microservices defines deployment |
| Microservices + Resilience | Distributed services needing fault tolerance | Natural pair — distributed = needs resilience |
| Microservices + BFF | Multi-service backend with multiple frontends | BFF sits in front of the service mesh |
| Event Sourcing + DDD | Domain events as the core data model | Events ARE the domain model — deep synergy |
| Feature Flags + any | Gradual rollout for any architecture style | Purely additive — no conflicts with other patterns |

### Composition Rules

1. **Maximum active:** No formal limit, but >3 active extensions means very high complexity. Question whether the project truly needs all of them.
2. **No conflicts by design:** Each extension adds rules in its own namespace (DDD-*, MICRO-*, BFF-*, ES-*, RES-*, FF-*). No rule from one extension contradicts another.
3. **Additive only:** Extensions add constraints on top of core workflow. They never relax or remove core rules.
4. **Override triggers:** Some extensions force conditional generation in AI-DWG regardless of normal triggers. Example: Microservices forces `resilience-standards.md` generation even if <3 integrations.

---

## The Activation Decision Record

When you activate (or decline) an extension, AI-ADLC records it:

**In `adlc-state.md`:**
```yaml
Enabled Extensions:
  - DDD Tactical (activated Stage 4)
  - Resilience Patterns (activated Stage 11)
Declined Extensions:
  - Microservices (declined Stage 5 — single deployable unit)
  - Event Sourcing (declined Stage 9 — current-state queries sufficient)
  - BFF Pattern (declined Stage 5 — single frontend)
  - Feature Flags (declined Stage 12 — branch-based release)
```

**In ADR (for activated extensions):**
```markdown
# ADR-{N}: Activate {Extension Name}

## Decision
Activate {extension} because {rationale}.

## Consequences
- Adds {N} blocking rules to architecture stages
- AI-DWG will generate {additional steering files}
- AI-GCE will derive {additional rules}
- Team must be familiar with {pattern concepts}
```

---

## Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|-------------|-----------------|
| "We might need microservices later" | Extensions add constraints NOW — activating "just in case" adds complexity without benefit | Decline. Activate when architecture demands it. |
| Activating DDD without domain expertise | DDD rules require aggregate identification, bounded context mapping | Build team capability first, or use simpler module patterns |
| All 6 extensions active on a small project | Overwhelming constraint set; most rules won't apply | Match extensions to actual complexity — most projects need 0-2 |
| Declining resilience with 5+ integrations | External dependencies WILL fail; no resilience = cascading outages | If you integrate heavily, resilience is not optional |
| Activating Event Sourcing for "audit logging" | ES is a fundamental data model change, not just an audit trail | Use append-only audit log instead — much simpler |

---

## Quick Decision Matrix

Answer Yes/No for your project:

| Question | Yes → Consider |
|----------|---------------|
| Multiple business domains with different rules? | DDD Tactical |
| Services that must deploy independently? | Microservices |
| Mobile + Web + Partner needing different API shapes? | BFF Pattern |
| Must reconstruct historical state at any point in time? | Event Sourcing |
| ≥3 external services or 99.9%+ SLA requirement? | Resilience Patterns |
| Trunk-based delivery with gradual rollout needed? | Feature Flags |
| All No? | No extensions — core workflow is sufficient |

---

## Related Documents

| Document | Location |
|----------|----------|
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| How ADLC Progressive Decomposition Works | `knowledge_docs/HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| Why Architecture Before Code Matters | `knowledge_docs/WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
