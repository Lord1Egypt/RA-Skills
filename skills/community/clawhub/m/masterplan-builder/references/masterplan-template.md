# Masterplan Document Structure

Use this as the section order for `docs/masterplan/masterplan.md`. Every section must be filled with real, specific content gathered in the interview and validated by research — no placeholders.

```
# <Project Name> — Masterplan

## 1. Overview
- One-line pitch
- Problem & who it's for
- Project category
- Definition of done (what "100% ready" means for this project specifically)

## 2. Users & Personas
- Primary/secondary personas
- Expected scale (launch and year one)
- Platform/device/browser support matrix (if applicable)

## 3. Features
### MVP (v1)
For each feature: description, acceptance criteria, edge cases, error/empty states.
### Later / Backlog
List only — not detailed to acceptance-criteria level.

## 4. Tech Stack
Per layer (frontend / backend / database / hosting / auth / model-runtime as applicable):
- Chosen technology + exact version
- Why it was chosen, what the alternatives were
- Source(s) confirming it's current (link or note what was verified)

## 5. Data Model
- Entity list with fields, types, constraints, relationships
- Sensitive data flagged, with handling approach
- Expected volume/growth

## 6. Architecture
- How components communicate (protocol/style, contract conventions)
- API surface (endpoints/methods or equivalent for the category) at a level ready to implement from
- Third-party integrations: how called, sync/async, failure behavior
- Background jobs/queues, caching, offline behavior as applicable

## 7. Non-Functional Requirements
- Performance targets (specific numbers)
- Security requirements
- Accessibility / i18n
- Compliance considerations

## 8. Environments & Deployment
- Environment list and differences
- CI/CD pipeline (triggers, gates)
- Hosting/infra specifics
- Monitoring, logging, alerting
- Backup & rollback strategy
- Config/secrets management approach

## 9. Testing Strategy
- Unit / integration / e2e coverage expectations
- Manual QA / release checklist

## 10. Adaptive System Design
- Which environment dimensions this system must detect and adapt to at runtime (device capability, network, screen/input, locale, load, etc.) and why each does or doesn't apply
- Per dimension: detection method, and the concrete behavior change at each tier (best case → degraded → minimum viable floor)
- The explicit minimum viable environment and what happens below it (stated fallback, not silent failure)

## 11. Production-Readiness Checklist
Concrete, checkable items pulled from references/production-standards.md, tailored to this project — not the generic list, the specific instantiation of it (e.g. "JWT tokens stored in httpOnly secure cookies, 15-min expiry, refresh via rotating token" rather than "secure auth").

## 12. Risk Register
Table or list: risk — likelihood — impact — mitigation. At least top 5.

## 13. Cost & Budget
- Launch-scale and year-one-scale infra/API cost estimate
- One-time costs
- Budget ceiling if any, and confirmation the tech stack fits it

## 14. Security Threat Model
- Trust boundaries and what's exposed where
- STRIDE-style walkthrough per boundary with stated defenses
- Audit/pen-test decision

## 15. Reliability Targets
- Uptime/availability target (or n/a)
- RTO/RPO if stateful
- Incident definition and response expectation

## 16. Versioning & Release Policy
- Versioning scheme, what counts as breaking
- Backward-compatibility and deprecation policy

## 17. Team & Roles
(Omit this section entirely for solo/personal projects.)
- Ownership per layer

## 18. Post-Launch Maintenance & Support
- Who maintains this after launch, update cadence, support channel if any

## 19. Vendor Lock-in / Exit Strategy
- Per major third-party dependency: switching cost, and whether an abstraction layer is justified now

## 20. Infrastructure as Code
- IaC tool decision, or explicit manual-management decision

## 21. Analytics & KPI Tracking
- Success metrics, tool, and where instrumenting them appears in the build roadmap

## 22. Market & Competitive Context
(Commercial projects only — omit entirely otherwise.)
- Nearest alternatives and differentiation

## 23. Build Roadmap
Ordered phases, each ending in a working increment:
### Phase 1 — <name>
- What's built
- Definition of done for this phase
- Dependencies on prior phases (none, for phase 1)
### Phase 2 — <name>
...

## 24. Open Questions / Explicit Exclusions
- Anything genuinely undecided and why (should be rare — most things should be decided by this point)
- Anything explicitly ruled out per the user's request
- Any Minor/Polish-level gap noted during self-audit that didn't block delivery
```
