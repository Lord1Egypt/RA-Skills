# Research Phase — Detailed Methodology

This reference contains the step-by-step process for the RESEARCH phase. Every finding must cite `file:line` from the user's codebase or a verified external URL. If you cannot verify something, do not include it — ask the user (in pt-BR) instead.

## Step 0: Source Acquisition

Before anything else, pin down WHERE the legacy code lives:

| Source given | Action |
| --- | --- |
| Current working directory is the legacy repo | Analyze in place — still read-only until the PLAN outputs. |
| Repo URL (GitHub, Azure DevOps, GitLab…) | `git clone <url> "$(mktemp -d)/src"` — **full clone** (co-change analysis in Step 2 needs `git log` history). Treat the clone as strictly read-only: no writes, no builds that mutate the tree, no branches. |
| Private repo, clone fails | Ask the user for access (pt-BR). Never attempt credential handling yourself. |
| Local path to a copy | Use it directly, read-only. |

Always record provenance at the top of every research file:

```markdown
**Source**: {origin URL or local path} @ `{HEAD SHA}` (cloned {date} to {temp path})
```

This makes every `file:line` citation reproducible — the temp clone may be deleted after the run.

If no target repo was provided yet, run in analysis-only mode: write `migration-plan/` into the current directory and defer Phase 3+ (SPECs, Issues) until the user supplies the target.

## Step 1: Environment Visibility and Codebase Deep Analysis

### 1.0 — Visibility Setup (optional but recommended)

Before reading files manually, check whether the environment exposes structured access to the legacy system. Connected sources beat sampled file reads for large systems:

- **Database MCP servers** — if an MCP server exposes the legacy database schema (tables, views, stored procedures, foreign keys), use it to inventory the data layer instead of guessing schema from ORM models.
- **Git/search indexers** — if an MCP or CLI indexes the repository, use it for dependency-graph and co-change queries.
- **Observability MCP** — if the legacy system is instrumented, pull real usage data (which endpoints/screens are actually used) to prioritize domains by traffic, not intuition.
- **Ticket systems** — open issues can reveal known migration blockers.

Record in `stack-research.md` which sources were used. If no MCP/indexer exists, fall back to direct file reading — and note the visibility gap as a risk (incomplete inventory).

Never paste secrets or PII obtained through any connector into output files — reference `path:line` with `<redacted>`.

### 1.1 — Project Structure Scan

Read the root directory and map the top-level structure. Identify:

- **Entry points** — `Program.cs`, `Startup.cs`, `Global.asax`, `main.ts`, `index.html`, `App.xaml.cs`, etc. Cite each as `file:line`.
- **Configuration files** — `.sln`, `*.csproj`/`*.fsproj`/`*.vbproj`, `packages.config`, `web.config`, `appsettings.json`, `package.json`, `requirements.txt`, `docker-compose.yml`, `Makefile`.
- **Build and deploy config** — `Dockerfile`, CI/CD pipelines (`.github/workflows/`, `azure-pipelines.yml`, `Jenkinsfile`), IIS configs, `web.config` transforms, infrastructure as code.
- **Monorepo indicators** — `nx.json`, `turbo.json`, `pnpm-workspace.yaml`, multi-project `.sln` files, `Directory.Build.props`, `nuget.config`.

**.NET legacy signals to detect and record:**

| Signal | Files / pattern | Migration implication |
| --- | --- | --- |
| .NET Framework vs .NET | `<TargetFramework>net4*` in `.csproj`, `packages.config`, non-SDK-style projects | Full rewrite of project files; no direct upgrade for WebForms |
| WebForms | `*.aspx`, `*.ascx`, `*.master`, `Page_Load` lifecycle, ViewState | No incremental in-place path — plan screen-level rewrite to Blazor |
| MVC/Web API (Framework) | `Global.asax`, `RouteConfig`, `ApiController` on `System.Web` | Route-to-endpoint mapping is a natural seam table |
| WPF / WinForms | `.xaml`, `InitializeComponent`, code-behind | MAUI candidate; inventory MVVM vs code-behind coupling |
| Xamarin.Forms | `Xamarin.Forms` package refs | Direct path to .NET MAUI (`UseMauiApp`, handler model) |
| Silverlight / ClickOnce | `.xap`, `.application` manifests | UI is dead platform — full rewrite to Blazor WASM or MAUI |
| Classic AngularJS/jQuery SPA | `angular.module`, `$.ajax`, bundling configs | Route-level UI strangler into Blazor WASM |
| ASP.NET Boilerplate / EAF | `Abp` package refs, `AbpModule`, Dynamic Web Api | Pair with `migrate-aspnetboilerplate-to-abp` skill when installed |

### 1.2 — Dependency Inventory

For each dependency file found (`packages.config`, `.csproj` PackageReference, `package.json`, `requirements.txt`, `pom.xml`...):

1. Read the file completely.
2. List every dependency with its **pinned or range version**.
3. Web-search each: still maintained? latest version? known CVEs? Is there a .NET/Core-compatible replacement?
4. Flag deprecated, unmaintained, EOL, or Windows-only dependencies (e.g., `System.Drawing`, `Microsoft.Owin` on Framework, WCF client stacks).

Output format for `dependency-map.md`:

```markdown
## Dependencies — {file:line ref to dependency file}

| Dependency | Current Version | Latest / .NET Equivalent | Status | Notes |
|------------|----------------|--------------------------|--------|-------|
| EntityFramework | 6.4.4 | EF Core 9.x | Legacy | Rewrite DbContext; LINQ mostly ports |
| Newtonsoft.Json | 12.0.3 | System.Text.Json (built-in) | Replaceable | Attribute differences: [JsonProperty] etc. |
| jQuery | 3.4.1 | — (Blazor replaces) | Remove | UI rewrite; keep during strangler phase |
```

### 1.3 — Module Responsibility Mapping

For each directory/module/project:

1. Read the main files (entry point, controllers, services, index/barrel files).
2. State the module's **single responsibility** in one sentence.
3. List **internal dependencies** (`ProjectReference`, `using` of sibling namespaces, TS/JS imports).
4. List **exports** (controllers, public services, components consumed elsewhere).
5. Identify **external calls** (HttpClient, WCF clients, raw ADO.NET, message queues, COM interop, file shares).

Do NOT paraphrase code — reference it: "Module `Billing/` (`src/Billing/BillingController.cs:12-88`) generates invoices and posts to the payment gateway (client at `src/Billing/GatewayClient.cs:30`)."

### 1.4 — Database and Data Layer Analysis

Identify all persistence:

- **Connections** — connection strings in `web.config`/`appsettings.json`, ORM configs (EF6 `DbContext`, NHibernate, Dapper, raw ADO.NET, stored-procedure calls).
- **Schema** — entities, migration files, `.edmx`, and (if a DB MCP is available) the actual live schema — tables, views, SPs, triggers, and which modules touch them.
- **Shared tables** — every table accessed by more than one module is a coupling point. Flag each with `file:line`.
- **Data flow** — writes vs reads, reporting queries, ETL/SSIS packages, caches (MemoryCache, Redis), queue-driven writes.
- **Query patterns** — capture representative queries/SPs per domain. The PLAN phase uses them to propose indexing/partitioning under the target stack and to design the EF Core model.

### 1.5 — Parity Surface Inventory

List every **externally observable behavior** the legacy system exposes — this becomes the parity-test surface in PLAN:

- HTTP endpoints (routes, verbs, response shapes) — from route tables/attributes.
- Screens/pages with business logic (WebForms pages, WinForms dialogs, Angular routes).
- Scheduled jobs, background services, message handlers, report generators.
- Public APIs consumed by third parties (check `docs/`, OpenAPI/WSDL, consumers list — ask the user if unknown).

Record per item: location `file:line`, inputs, outputs/side effects, and who calls it.

## Step 2: Domain / Bounded Context Mapping

Load `references/assessment-framework.md` for scoring.

### 2.1 — Candidate Identification

Group modules into candidate bounded contexts: shared business vocabulary, high internal cohesion, low external coupling. For .NET solutions, also respect natural boundaries: `.csproj` per module, namespace roots, `Area` folders, ABP modules.

### 2.2 — Coupling Analysis

Per candidate domain compute internal imports, external imports, shared tables, and `coupling = external / (internal + external)`. Above 0.5 the boundary is wrong — merge or redraw.

For .NET codebases, also compute **project-reference coupling**: cross-`ProjectReference` edges between candidate domains (from `.csproj` files) — a stronger signal than `using` statements.

### 2.3 — Domain Candidate Report

```markdown
## Domain: {Name}

**Modules**: `src/Billing/`, `src/Billing.Web/` (refs: `Billing.csproj:5`, `Billing.Web.csproj:8`)
**Responsibility**: Invoice lifecycle and payment collection.
**Internal cohesion**: 14 internal references
**External coupling**: 4 external references (Auth, Notifications, Reporting)
**Shared tables**: `Invoices`, `Payments` (also read by `Reports/` at `src/Reports/Monthly.cs:67`)
**Coupling ratio**: 0.22 (good)
**Parity surface**: `POST /api/invoices`, `GET /api/invoices/{id}`, `MonthlyCloseJob`
**Migration complexity**: Medium — shared `Payments` table needs facade or dual-write.
```

## Step 3: Stack Research

MANDATORY. Never rely on training data alone.

### 3.1 — Current Stack Research

Per technology: web-search name + docs + current year; check latest stable, LTS/EOL dates, official upgrade/migration paths. For .NET Framework assets, record exact version and Microsoft EOL/support status.

### 3.2 — Target Stack Research (.NET default)

When the user accepts the default .NET target, research:

- **Blazor WebAssembly** — current .NET LTS, hosting model (ASP.NET Core hosted vs static), AOT, trimming, limitations (no direct DB access — everything via API).
- **.NET MAUI** — supported OS targets, Blazor Hybrid option for sharing Razor components with the WASM app.
- **ASP.NET Core** — minimal APIs vs controllers, versioning, OpenAPI.
- **EF Core** — provider match for the existing database engine, migration tooling, features missing vs EF6 (e.g., some stored-proc mapping patterns).
- **YARP** — for the strangler routing layer.
- **ABP Framework** — when the source is ASP.NET Boilerplate/EAF or the user wants modular DDD.

When the user chooses a **non-.NET target**, apply the same rigor to that stack: official migration guides, framework equivalents for the legacy pieces (UI framework, ORM/data layer, auth, DI, background jobs), ecosystem maturity of equivalent libraries, deployment fit, and community migration experience. Document the resulting target-strategy recommendations in `stack-research.md`.

Use Context7 / Microsoft Learn for API-accurate details; cite every claim with a URL.

### 3.3 — Compatibility Matrix

```markdown
## Current Stack

| Technology | Version in Use | Latest Stable | EOL | Source |
|------------|---------------|---------------|-----|--------|
| .NET Framework | 4.7.2 | — | supported but frozen | [learn.microsoft.com](url) |
| Angular | 12.x | 20.x | 2024-11 | [angular.dev](url) |

## Target Stack

| Technology | Recommended | Justification | Source |
|------------|------------|---------------|--------|
| .NET | 10 (LTS) | LTS, current Blazor/MAUI baseline | [dotnet.microsoft.com](url) |
| Blazor WebAssembly | net10.0 | Preferred web target; wasm AOT for heavy pages | [learn.microsoft.com](url) |
```

## Step 4: Risk, Dependency, and Security-Debt Mapping

Load `references/assessment-framework.md` for the risk matrix.

### 4.1 — Integration Point Catalog

For every external integration record: protocol, auth, data format, error handling, contract availability, `file:line`. Add **migration impact**: wrappable in facade / needs contract renegotiation / must stay as-is.

### 4.2 — Circular Dependency Detection

Trace import/project-reference chains for cycles (A→B→C→A). Every cycle is an extraction blocker — document the full chain with `file:line`.

### 4.3 — Security-Debt Scan → `security-debt.md`

Blog-driven addition: legacy code carries security patterns that must be **redesigned**, not ported. Scan for and flag:

| Pattern to find | Typical locations | Target direction |
| --- | --- | --- |
| Hardcoded secrets / connection strings with passwords | `web.config`, `appsettings.json`, `.cs` literals | User Secrets / env vars / Key Vault; rotate exposed secrets |
| Custom crypto, MD5/SHA1 password hashing | `*Helper.cs`, `Crypto*` classes | ASP.NET Core Identity hasher / `Rfc2898DeriveBytes` / `PasswordHasher<T>` |
| Forms/Windows auth only | `web.config <authentication>` | OIDC / Entra ID / OpenIddict; bridge during transition |
| Missing authz checks / role checks in code-behind | `Page_Load`, controllers without `[Authorize]` | Policy-based authorization in ASP.NET Core |
| SQL string concatenation | raw ADO.NET calls | EF Core parameterized queries |
| Unvalidated redirects/inputs, missing CSRF | WebForms/MVC handlers | Blazor antiforgery, `[ValidateAntiForgeryToken]`, input validation |

Format:

```markdown
## Finding: {Short description}
**Severity**: Critical | High | Medium | Low
**Evidence**: `file:line` (redacted for secrets)
**Redesign direction**: {target pattern — never "port as-is"}
**Migration phase**: Phase 0 prerequisite | per-domain | post-migration
```

### 4.4 — Risk Assessment

```markdown
## Risk: {Description}
**Category**: Technical | Operational | Business
**Impact**: Critical | High | Medium | Low
**Probability**: High | Medium | Low
**Evidence**: {file:line or external ref}
**Mitigation**: {strategy — reference strangler-fig-patterns.md when applicable}
**Residual risk**: {after mitigation}
```

## Research Completion Checklist

- [ ] Source provenance recorded (origin URL/path + HEAD SHA) in every research file
- [ ] Source analyzed read-only (temp clone when URL was given; nothing written into it)
- [ ] Every module read and mapped with `file:line` citations
- [ ] MCP/indexer visibility assessed and recorded (or its absence noted as risk)
- [ ] Every dependency checked against current versions via web search
- [ ] Bounded contexts identified with coupling ratios
- [ ] Target stack (.NET default, or the user-chosen stack) researched with cited sources — versions verified, not assumed
- [ ] Parity surface inventory written (all externally observable behaviors)
- [ ] Integration points cataloged; circular dependencies identified
- [ ] `security-debt.md` written (or explicitly empty with justification)
- [ ] `dependency-map.md`, `domain-candidates.md`, `stack-research.md`, `risk-assessment.md` written
- [ ] No unverified claims in any output file
