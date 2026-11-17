<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Multi-Tenancy Architecture

**Document Status:** {Draft / Review / Approved}
**Version:** {n.n}
**Date:** {YYYY-MM-DD}
**Author:** {Role}

---

## 1. Isolation Model

**Chosen:** {Shared DB Row-Level / Schema-per-Tenant / DB-per-Tenant / Hybrid}
**Rationale:** {Why — ADR-{nnn}}

---

## 2. Tenant Context Propagation

### Resolution

| Entry Point | Method |
|-------------|--------|
| {entry point} | {how tenant is identified} |

### Enforcement (Defense in Depth)

| Layer | Mechanism |
|-------|-----------|
| {layer} | {how isolation is enforced} |

---

## 3. Tenant Lifecycle

### Provisioning

| Step | Action | Automated? |
|:----:|--------|:----------:|
| 1 | {action} | {Yes/No} |

### Deactivation & Deletion

| Action | Behavior | Retention |
|--------|----------|:---------:|
| {action} | {what happens} | {period} |

---

## 4. Cross-Tenant Access

| Role | What They See | How |
|------|-------------|-----|
| {role} | {scope} | {mechanism} |

### Safety Rules
1. {Rule 1}
2. {Rule 2}

---

## 5. White-Label Architecture (if applicable)

### Branding Resolution

| Touchpoint | Branded Element | Method |
|-----------|----------------|--------|
| {touchpoint} | {what's branded} | {how resolved} |

---

*Multi-Tenancy Architecture v{version} | {date} | Status: {status}*
