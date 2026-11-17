<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Resilience Patterns

## When This Extension Applies

Your system likely needs dedicated resilience design if:

- Distributed system with multiple services communicating over network
- External system integrations where failures are expected
- High availability requirements (99.9%+)
- Partial failure must not cascade to total system failure
- Users expect graceful degradation (not hard errors)

## Opt-In Question

```
### Would you like to apply Resilience Patterns?

This extension adds detailed guidance for:
- Circuit Breaker design (thresholds, half-open state, fallback behavior)
- Bulkhead pattern (resource isolation, thread pool separation, queue limits)
- Timeout policies (per-integration timeouts, global request budgets)
- Retry strategies (exponential backoff, jitter, idempotency requirements)
- Graceful degradation catalog (what degrades, what stops, what falls back)
- Health check architecture (liveness vs. readiness vs. startup probes)
- Failure mode analysis (per-component: what fails, impact, detection, recovery)
- Dead letter queues and poison message handling

(a) Yes — Design resilience patterns into the architecture
(b) No — Basic retry + timeout in integration patterns is sufficient

Recommended for: Microservices, heavy integration, 99.9%+ SLA, user-facing systems
Skip if: Monolith with few external dependencies, lower availability tolerance
```

## Status: ✅ Available (v1.1)
