<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Microservices Deep-Dive

## When This Extension Applies

Your system likely needs this extension if:

- You chose "Microservices" or "Service-Oriented" decomposition (Stage 5)
- More than 5 independently deployable services
- Multiple teams owning different services
- Need for independent deployment cadence per service
- Complex inter-service communication patterns

## Opt-In Question

```
### Would you like to apply Microservices Deep-Dive patterns?

This extension adds detailed guidance for:
- Service mesh architecture (sidecar proxies, traffic management, mTLS)
- Distributed tracing design (correlation IDs, span propagation, trace sampling)
- Saga patterns (choreography vs. orchestration for distributed transactions)
- Schema registry (event schema evolution, compatibility rules)
- Service discovery and routing
- Per-service data ownership enforcement
- Contract testing between services

(a) Yes — Apply microservices patterns to the architecture
(b) No — Service-level decomposition in core workflow is sufficient

Recommended for: >5 services, multiple teams, independent deployment needs
Skip if: Modular monolith, 2-3 coarse services, single team ownership
```

## Status: ✅ Available (v1.1)
