# Assessment Framework

Methods for mapping dependencies, scoring risks, identifying domains, and evaluating technical debt. Every output must cite `file:line` from the codebase or a verified external source.

## Domain Identification Method

### Step 1: Module Inventory

For each module (directory, `.csproj`, package, or feature folder):

```markdown
| Module Path | Responsibility | Internal Deps | External Deps | Data Stores | LOC |
|-------------|---------------|---------------|---------------|-------------|-----|
| `src/Billing/` | Invoice lifecycle | Auth, Notifications | Stripe API | Invoices, Payments | 1,200 |
```

Every cell references `file:line` evidence. For .NET solutions, a `.csproj` is usually the module boundary — start there, then confirm with code reads.

### Step 2: Affinity Grouping

Group modules by:

1. **Import/reference analysis** — modules referencing each other belong together. In .NET, `ProjectReference` edges in `.csproj` are the strongest signal; `using` directives of sibling namespaces refine it. In TS/JS frontends, import graphs.
2. **Data affinity** — modules reading/writing the same tables.
3. **Business vocabulary** — shared domain terms (`Invoice`, `Payment`, `Policy`).
4. **Co-change analysis** — `git log` files frequently committed together reveal logical coupling invisible to import analysis:

```bash
git log --name-only --pretty=format: | sort | uniq -c | sort -rn | head -50
```

### Step 3: Coupling Metrics

Per candidate domain:

- `cohesion = internal_deps / total_modules_in_domain` (higher is better)
- `coupling = external_deps / (internal + external)` (lower is better)
- `db_coupling = shared_tables / total_tables_accessed` (lower is better)

Interpretation: `coupling < 0.3` good boundary · `0.3–0.5` acceptable, needs facade · `> 0.5` bad boundary — merge or redraw.

### Step 4: Domain Scorecard

```markdown
## Domain Scorecard: {Name}

| Metric | Value | Rating |
|--------|-------|--------|
| Cohesion | 0.85 | Good |
| Coupling | 0.22 | Good |
| DB coupling | 0.10 | Good |
| LOC | 3,200 | Medium |
| Test coverage | 45% | Needs safety net before migration |
| Change frequency | 12 commits/month | Active — high business value |
| Parity surface size | 6 endpoints, 3 screens, 1 job | Medium |

**Verdict**: Ready / Needs boundary adjustment / Too coupled to migrate independently
```

## Risk Assessment Matrix

### Categories

- **Technical** — circular dependencies, shared mutable state, implicit coupling (statics, singletons, global caches), missing tests on critical paths, data-integrity risk in DB migration, Windows-only APIs on the .NET path (e.g., `System.Drawing`, COM interop, IIS-only features).
- **Operational** — downtime at cutover, dual-run performance, monitoring gaps, rollback failure, WASM payload size limits, MAUI store/rollout constraints.
- **Business** — revenue-impacting flows, compliance windows, SLAs constraining migration timing, team .NET/Blazor skill gap.

### Scoring

| Field | Values |
| --- | --- |
| Impact | Critical(4) / High(3) / Medium(2) / Low(1) |
| Probability | High(3) / Medium(2) / Low(1) |
| Score | impact × probability → ≥12 CRITICAL, ≥8 HIGH, ≥4 MEDIUM, <4 LOW |

```markdown
## Risk: {description}
**Category**: Technical | Operational | Business
**Impact**: {level — why, with file:line}
**Probability**: {level — why, with evidence}
**Score**: {n} → **{severity}**
**Mitigation**: {strategy — reference strangler-fig-patterns.md if applicable}
**Residual**: {after mitigation}
**Owner**: {ask user if unclear}
```

Top 3–5 risks must be addressed in roadmap Phase 0 (Safety Net). An unmitigable CRITICAL risk is escalated to the user before the plan proceeds.

## Technical Debt Evaluation

| Category | Indicators | Detection |
| --- | --- | --- |
| Dependency debt | Outdated/EOL packages, `packages.config`, non-SDK `.csproj` | version compare via web search |
| Architecture debt | circular refs, god classes/services, data access scattered in UI | import graph, module size, SQL in code-behind |
| Test debt | low coverage, no integration tests, no parity suite | test-file ratio, coverage config |
| Infrastructure debt | manual deploys, no CI/CD, no containers | Dockerfile/CI config presence |
| Documentation debt | no API docs/diagrams/OpenAPI | docs/, README content |
| Security debt | hardcoded secrets, obsolete crypto, weak authz | `security-debt.md` scan from research-phase §4.3 |

### Debt Impact Classification

- **Blocker** — prevents migration (circular deps) → Phase 0.
- **Amplifier** — makes migration harder (no tests) → Phase 0 or accept + risk entry.
- **Resolved by migration** — fixed naturally by the target (deprecated package dies with the old stack) → document, don't prioritize.
- **Prerequisite** — must exist before migration (parity tests, auth bridge) → Phase 0.

## Component Complexity Scoring

Rate 1–10 per dimension:

| Dimension | 1–3 (Low) | 4–6 (Medium) | 7–10 (High) |
| --- | --- | --- | --- |
| Size | <500 LOC | 500–2000 | >2000 |
| Dependencies | 0–2 external | 3–5 | >5 |
| Data coupling | own tables | 1–2 shared | 3+ shared |
| Test coverage | >70% | 40–70% | <40% |
| Change frequency | <2 commits/mo | 2–10 | >10 |
| Business criticality | internal tools | customer-facing non-critical | revenue/auth/payment |

Composite = average. Order: score 1–3 first (quick wins), 4–6 middle, 7–10 last.

## Integration Point Catalog Format

```markdown
## Integration: {Name}
**Type**: REST | gRPC | WCF/SOAP | Message Queue | Database | File share | Third-party SDK | COM/native
**Location**: `file:line`
**Direction**: Outbound | Inbound | Bidirectional
**Protocol**: HTTP | AMQP | TCP | named pipes | …
**Authentication**: API key | OAuth/OIDC | Windows auth | mTLS | None | Unknown (ASK USER)
**Data format**: JSON | XML | SOAP | Protobuf | CSV | Binary
**Error handling**: `file:line`
**Contract**: OpenAPI at {path} | WSDL at {path} | Proto at {path} | None
**SLA**: {if known — ASK USER for critical integrations}
**Migration impact**: facade-able | contract renegotiation needed | must stay as-is
**.NET client plan**: {HttpClientFactory | Refit | generated client | gRPC client | SDK replacement}
```
