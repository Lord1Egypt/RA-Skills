<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Integration & Infrastructure Architecture

**Document Status:** {Draft / Review / Approved}
**Version:** {n.n}
**Date:** {YYYY-MM-DD}
**Author:** {Role}

---

## Part A: Integration Architecture

### 1. Integration Patterns Used

| Pattern | Description | Used By |
|---------|-------------|---------|
| {pattern} | {description} | {which integrations} |

### 2. Per-System Integration Design

#### {External System Name}

| Aspect | Design |
|--------|--------|
| Direction | {In/Out/Both} |
| Pattern | {Sync/Async/Event/Polling} |
| Protocol | {protocol} |
| Authentication | {method} |
| Failure handling | {retry/circuit-breaker/DLQ} |
| Tenant scoping | {per-tenant config?} |
| Criticality | {Critical/Important/Optional} |

### 3. Adapter Architecture

{Description of adapter/connector design pattern used.}

### 4. Internal Event Architecture

| Event | Producer | Consumer(s) | Purpose |
|-------|----------|-------------|---------|
| {event.name} | {module} | {module(s)} | {what triggers} |

---

## Part B: Infrastructure & Deployment

### 5. Deployment Topology

{ASCII or Mermaid diagram of deployment layout.}

### 6. Container-to-Host Mapping

| Container | Min Instances | Target Instances | Resource Profile |
|-----------|:-------------:|:----------------:|:----------------:|
| {container} | {n} | {n} | {CPU/RAM} |

### 7. High Availability

| Component | Redundancy | Failover | Recovery Time |
|-----------|:----------:|:--------:|:-------------:|
| {component} | {model} | {mechanism} | {time} |

### 8. Scaling Strategy

| Component | Scalable? | Trigger | Max |
|-----------|:---------:|---------|:---:|
| {component} | {H/V/No} | {when} | {n} |

### 9. Observability

| Concern | Tool | Approach |
|---------|------|----------|
| Metrics | {tech} | {method} |
| Logging | {tech} | {method} |
| Alerting | {tech} | {method} |

### 10. Backup & DR

| Metric | Target | Method |
|--------|:------:|--------|
| RPO | {value} | {approach} |
| RTO | {value} | {approach} |

### 11. Network Security Zones

| Zone | Contains | Access Policy |
|------|----------|:-------------:|
| {zone} | {components} | {rules} |

---

*Integration & Infrastructure v{version} | {date} | Status: {status}*
