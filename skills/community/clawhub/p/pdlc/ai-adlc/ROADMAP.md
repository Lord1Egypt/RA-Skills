# AI-ADLC — Extension Roadmap

**Version:** 1.1.0
**Status:** Core workflow complete. v1.1 extensions (High Priority) delivered. v1.2 extensions planned.

---

## Current Coverage (v1.0)

The core AI-ADLC workflow covers solution architecture design for the **80% common case**: modular monolith through service-oriented systems, standard data models, REST APIs, typical infrastructure, and common security patterns.

---

## Planned Extensions

Extensions follow the opt-in model — activated during the workflow when a user's system requires a specific pattern. Each extension adds dedicated design guidance, decision frameworks, and templates for its pattern.

### ✅ Delivered — v1.1 (High Priority)

| Extension | Pattern | Status | Rules |
|-----------|---------|:------:|:-----:|
| `ddd-tactical/` | DDD Tactical Patterns (Aggregates, Domain Events, ACL, Value Objects) | ✅ Complete | DDD-01 → DDD-12 |
| `microservices/` | Microservices Deep-Dive (service mesh, distributed tracing, saga/choreography, schema registry) | ✅ Complete | MS-01 → MS-12 |
| `bff-pattern/` | Backend-for-Frontend (aggregation, client-specific shaping, gateway vs. BFF) | ✅ Complete | BFF-01 → BFF-10 |
| `event-sourcing-cqrs/` | Event Sourcing + CQRS (event store, projections, read models, snapshots) | ✅ Complete | ES-01 → ES-12 |
| `resilience-patterns/` | Resilience Catalog (circuit breaker, bulkhead, graceful degradation, timeout policies) | ✅ Complete | RES-01 → RES-12 |
| `feature-flags/` | Feature Flags & Progressive Delivery (flag architecture, rollout strategies, flag lifecycle) | ✅ Complete | FF-01 → FF-11 |

---

### Medium Priority (v1.2)

| Extension | Pattern | When Needed |
|-----------|---------|-------------|
| `serverless/` | Serverless / FaaS Architecture (Lambda patterns, event-driven, cold starts, cost modeling) | Cloud-native event-driven systems; pay-per-invocation models |
| `ai-ml-integration/` | AI/ML Integration Patterns (model serving, RAG, feature stores, async inference, agent architecture) | Systems with intelligent features, LLM integration, or ML pipelines |
| `micro-frontends/` | Micro-Frontend Architecture (composition strategies, shared shell, independent deployment, routing) | Large teams with independent frontend delivery per domain |
| `graphql-federation/` | GraphQL Federation (schema stitching, federated gateway, subgraph ownership, type resolution) | Multi-team API evolution with GraphQL as primary style |
| `multi-region/` | Multi-Region & Geo-Distribution (data replication, latency routing, conflict resolution, regional compliance) | Global systems with latency requirements or regional data residency |

---

### Lower Priority (v1.3+)

| Extension | Pattern | When Needed |
|-----------|---------|-------------|
| `zero-trust/` | Zero Trust Security Architecture (never trust, always verify; micro-segmentation; identity-based access) | High-security environments; regulated industries |
| `kubernetes-native/` | Kubernetes-Native Patterns (operators, CRDs, Helm charts, service mesh, GitOps, observability) | Systems deployed on Kubernetes with cloud-native operations |
| `edge-computing/` | Edge Computing Architecture (edge nodes, sync strategies, offline capability, edge-to-cloud) | IoT, retail, or systems requiring compute at the edge |
| `data-mesh/` | Data Mesh Architecture (domain data ownership, data products, self-serve platform, federated governance) | Large organizations with multiple data-producing domains |
| `chaos-engineering/` | Chaos Engineering (failure injection, game days, steady-state hypothesis, resilience verification) | Production systems requiring proven fault tolerance |
| `supply-chain-security/` | Supply Chain Security (SBOM, dependency signing, container scanning, provenance attestation) | Regulated environments; compliance-heavy deployments |
| `offline-first/` | Offline-First / PWA Architecture (local-first data, sync protocols, conflict resolution, service workers) | Mobile or field applications requiring disconnected operation |
| `real-time-streaming/` | Real-Time Streaming Architecture (event streams, Kafka patterns, windowing, exactly-once processing) | High-throughput event processing systems |
| `plugin-ecosystem/` | Plugin/Extension Ecosystem Architecture (plugin API, sandboxing, lifecycle, marketplace) | Platforms that support third-party extensions |

---

## Extension Structure

Each extension follows this structure:

```
ai-adlc-rule-details/
└── extensions/
    └── {extension-name}/
        ├── {extension-name}.md              ← Design rules and guidance (full enforcement)
        └── {extension-name}.opt-in.md       ← Opt-in prompt (shown during workflow)
```

**Activation:** During Stage 5 (Container Design) or Stage 6 (Technology Stack), the workflow presents opt-in prompts for applicable extensions. User opts in → extension rules loaded and enforced in subsequent stages.

**v1.1 Delivery Note:** All six high-priority extensions now have complete rule files with numbered rules, verification criteria, anti-patterns, ADR triggers, and templates. Enforcement is structured — once a user opts in, rules are blocking constraints verified at stage completion.

---

## Contributing Extensions

If you create an extension for your own use case:

1. Follow the structure above (`{name}.md` + `{name}.opt-in.md`)
2. Reference core AI-ADLC stages where the extension applies
3. Include ADR triggers specific to the pattern
4. Provide a quality checklist for the pattern
5. Keep it general — no project-specific content

---

*Last Updated: June 2026 — v1.1 extensions delivered*
