<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Security Compliance — Derivation Logic

## Purpose

Derives security compliance rules from `security-rules.md` and `observability-sensitive.md`. This is a HYBRID category: built-in baseline provides universal security floor; steering enriches with project-specific security decisions.

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS activity, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Apply defense-in-depth thinking: baseline security is the floor, steering enrichment adds project-specific layers
- Treat every security rule as Tier A (immediate enforcement) unless explicitly advisory — security violations in intermediate state ARE dangerous
- Think in attack surfaces: endpoints without auth, secrets in code, unmasked PII — each is an exploitable vector
- Assign severity based on blast radius: auth bypass (🔴) > PII exposure (🔴) > CORS misconfiguration (🟠) > naming (🟡)
- Ensure file patterns for security hooks cover ALL entry points, not just controllers

### Anti-Patterns for This Activity
- Do NOT generate security rules with weak language ("should secure") — security is always MUST/NEVER
- Do NOT defer security hooks to agentStop — secrets in code are dangerous at every intermediate state
- Do NOT assume security-rules.md covers everything — built-in baseline applies regardless of steering content

### Quality Check
A good output from this activity sounds like:
- "SEC-BASELINE-01: No hardcoded secrets. Pattern: `**/*.ts`, `**/*.json`, `**/*.yaml`. Event: fileEdited (Tier A). sessionDedup: true. This fires immediately because a committed secret is exploitable from the moment it exists."
- "security-rules.md specifies RS256 → SEC-01 generated. HS256 in any JWT config is a Critical violation."

---

## Source Steering Files

| File | What to Extract |
|------|----------------|
| `security-rules.md` | Auth model, token strategy, RBAC, encryption, OWASP mitigations, audit logging |
| `observability-sensitive.md` | PII categories, masking rules, what NEVER to log, data classification |

## Built-in Baseline (Always Generated)

These rules exist regardless of steering content:

| Rule ID | Statement | Source |
|---------|-----------|--------|
| SEC-BASELINE-01 | No hardcoded secrets in source code (API keys, passwords, tokens, connection strings) | Built-in: Universal security |
| SEC-BASELINE-02 | Every API endpoint MUST have explicit auth declaration (`[Authorize]` or `[AllowAnonymous]`) | Built-in: No accidental exposure |
| SEC-BASELINE-03 | Credentials MUST be in environment variables or secret manager — never in committed files | Built-in: Secret management |

---

## Steering-Enriched Rules

### From `security-rules.md` → Auth Model Section

| Steering Content | Generated Rule |
|-----------------|---------------|
| "JWT Bearer tokens with RS256 signing" | SEC-01: All auth tokens MUST use RS256 signing (no HS256 in production) |
| "Role-based access: Admin, Manager, User" | SEC-02: Every endpoint MUST declare minimum required role |
| "Token expiry: 15 minutes access, 7 days refresh" | SEC-03: Access token TTL MUST NOT exceed 15 minutes |

### From `security-rules.md` → OWASP Section

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Input validation on all API endpoints" | SEC-10: All request DTOs MUST have validation rules |
| "SQL injection prevention: parameterized queries only" | SEC-11: NEVER use string concatenation for queries |
| "CORS: explicit origin whitelist" | SEC-12: CORS must list explicit origins (no wildcard `*` in production) |

### From `observability-sensitive.md`

| Steering Content | Generated Rule |
|-----------------|---------------|
| "NEVER log: passwords, tokens, credit card numbers, SSN" | SEC-20: Log sanitization MUST mask all PII categories |
| "Email addresses: mask middle portion" | SEC-21: Email masking format: `a***@domain.com` |
| "Financial amounts: OK to log; account numbers: NEVER" | SEC-22: Account numbers MUST be masked in all outputs |

---

## Tier Progression

| Tier | Security Rules Active |
|:----:|----------------------|
| 1 | SEC-BASELINE-01/02/03 + basic rules from security-rules.md (auth model, no secrets) |
| 2 | + Full SEC-* set from steering (OWASP, encryption, PII masking) |
| 3 | + SOX internal controls (if applicable), GDPR data rules (if applicable), full audit trail |

### Tier 3 Enrichment (SOX/GDPR — Conditional)

If `project-governance.md` or `scope-and-risks.md` mentions SOX, GDPR, PCI-DSS, or similar:
- Generate additional rules: SOX-01 through SOX-06, GDPR-01 through GDPR-06
- These are Tier 3 — only activated at pre-release
- Source: derived from security-rules.md compliance section + built-in framework knowledge

---

## Hook Mapping

| Hook | Event | Debounce | Rules Enforced |
|------|-------|:--------:|----------------|
| `security-gate-check.json` | fileEdited | Tier A 🔴 | SEC-01/02/03, SEC-BASELINE-02 |
| `sensitive-data-check.json` | fileEdited | Tier A 🔴 | SEC-BASELINE-01, SEC-20/21/22 |

Both hooks are 🔴 Essential — NEVER remove.

---

## File Pattern Derivation

Security hooks watch presentation/controller files (where endpoints are defined):

| Technology | Pattern for security-gate-check |
|-----------|--------------------------------|
| NestJS | `src/modules/*/presentation/**/*.controller.ts` |
| Django | `**/views.py`, `**/viewsets.py` |
| ASP.NET | `src/Modules/*/Presentation/**/*Controller.cs` |
| Spring Boot | `src/main/java/**/controller/*Controller.java` |

Sensitive-data-check watches ALL code files:

| Technology | Pattern for sensitive-data-check |
|-----------|--------------------------------|
| NestJS | `**/*.ts`, `**/*.json`, `**/*.yaml` |
| Django | `**/*.py`, `**/*.json`, `**/*.yaml` |
| ASP.NET | `**/*.cs`, `**/*.json`, `**/*.yaml` |
| Spring Boot | `**/*.java`, `**/*.json`, `**/*.yaml`, `**/*.properties` |
