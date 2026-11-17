# Reference Map: Conditional Generation Triggers

**Purpose:** Complete lookup table of all conditional generation triggers in AI-DWG — which output files are generated conditionally, what their trigger condition is, and where to check.

---

## All Conditional Triggers

| # | Output File | Trigger Condition | Where to Check | Extension Override? |
|---|------------|-------------------|----------------|:-------------------:|
| 1 | `multi-tenancy.md` | AP contains multi-tenancy architecture (§7 or §10) | Scan AP for "tenant", "multi-tenancy", "isolation" | ❌ |
| 2 | `event-sourcing.md` | Event Sourcing/CQRS extension active | `adlc-state.md` → Enabled Extensions | ✅ (extension) |
| 3 | `resilience-standards.md` | ≥3 external integrations OR Resilience extension active | AP §11 integration count + `adlc-state.md` | ✅ (Microservices also forces) |
| 4 | `feature-flags.md` | Feature Flags extension active | `adlc-state.md` → Enabled Extensions | ✅ (extension) |
| 5 | `frontend-standards.md` | AP contains frontend containers | AP §3 container types | ❌ |
| 6 | `microservices.md` | Microservices extension active | `adlc-state.md` → Enabled Extensions | ✅ (extension) |
| 7 | `ddd-patterns.md` | DDD Tactical extension active | `adlc-state.md` → Enabled Extensions | ✅ (extension) |
| 8 | `bff-patterns.md` | BFF Pattern extension active | `adlc-state.md` → Enabled Extensions | ✅ (extension) |
| 9 | `graphql-standards.md` | AP API architecture includes GraphQL | AP §10 API style decisions | ❌ |
| 10 | `grpc-standards.md` | AP API architecture includes gRPC | AP §10 API style decisions | ❌ |
| 11 | `message-queue-standards.md` | AP contains async messaging/event bus | AP §11 integration patterns | ❌ |
| 12 | `caching-standards.md` | AP data architecture includes caching layer | AP §9 data architecture | ❌ |
| 13 | `performance-budgets.md` | AP contains quantitative performance NFRs | AP §1 quality attributes | ❌ |
| 14 | `accessibility.md` | AP contains frontend + accessibility NFRs | AP §1 + frontend container | ❌ |

---

## Always-Generated Files (No Trigger — Always Present)

| # | Output File | Why Always |
|---|------------|-----------|
| 1 | `workspace-rules.md` | Every project needs workspace context |
| 2 | `tech-stack.md` | Every project has a technology stack |
| 3 | `api-standards.md` | Most projects have APIs (if truly no APIs, still provides request/response patterns) |
| 4 | `security-rules.md` | Security is never optional |
| 5 | `module-structure.md` | Every project has code organization |
| 6 | `naming-conventions.md` | Every project needs naming consistency |
| 7 | `testing-strategy.md` | Every project should test |
| 8 | `session-governance.md` | Session discipline is universal |
| 9 | `error-handling.md` | Error handling is universal |
| 10 | `logging-observability.md` | Logging is universal |
| 11 | `role-isolation.md` | Team topology applies to any multi-person project |
| 12 | `project-governance.md` | PR/review process is universal |

---

## Extension Override Rules

When an extension is active, it can force conditional generation regardless of normal triggers:

| Extension | Forces Generation Of |
|-----------|---------------------|
| Microservices | `resilience-standards.md` (even if <3 integrations) |
| Microservices | `microservices.md` |
| DDD Tactical | `ddd-patterns.md` |
| DDD Tactical | Enriches `module-structure.md` with bounded context rules |
| Event Sourcing | `event-sourcing.md` |
| Event Sourcing | Enriches `data-standards.md` with event immutability rules |
| BFF Pattern | `bff-patterns.md` |
| BFF Pattern | Enriches `api-standards.md` with BFF routing rules |
| Resilience | `resilience-standards.md` |
| Feature Flags | `feature-flags.md` |

---

## Trigger Evaluation Order

```
1. Check always-generated list → generate these unconditionally
2. Read adlc-state.md → check enabled extensions
3. For each extension → apply override rules (force generation)
4. For remaining conditional files → evaluate trigger against AP content
5. Files that pass trigger → generate
6. Files that fail trigger → skip (don't generate)
```

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Conditional Generation | `knowledge_docs/PATTERN_CONDITIONAL_GENERATION.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| Interaction Between Extensions and Governance | `knowledge_docs/INTERACTION_BETWEEN_EXTENSIONS_AND_GOVERNANCE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
