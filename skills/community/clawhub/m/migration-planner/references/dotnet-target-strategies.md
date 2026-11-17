# .NET Target Strategies

Stack-specific strategies for migrating INTO the .NET ecosystem — Blazor WebAssembly / Blazor Web App for web, .NET MAUI for desktop/mobile, ASP.NET Core for backends, EF Core for data. This is the target-side playbook; legacy-side seams live in `strangler-fig-patterns.md`.

> **Scope:** this reference applies only when the migration target is .NET (the default). When the user chooses a different target stack, do not load this file — instead produce equivalent target-strategy guidance inside `research/stack-research.md`, reusing the same seam patterns conceptually.

Always verify versions and APIs via web search / Microsoft Learn / Context7 before writing them into a plan — the ecosystem moves fast and this file is a map, not a version authority.

## Choosing the .NET Target

| Legacy source | Preferred target | When to deviate |
| --- | --- | --- |
| WebForms / MVC / Razor Pages | **Blazor Web App** (Server or WASM per interactivity needs) | SEO-heavy public site → SSR + streaming; consider keeping Razor Pages for pure-static areas |
| AngularJS / Angular / jQuery SPA / React | **Blazor WebAssembly** | Team/enterprise mandate for Angular → then `design` + Angular skills, not Blazor |
| Silverlight | **Blazor WebAssembly** (closest mental model: XAML → Razor, same .NET on client) | — |
| WinForms / WPF | **.NET MAUI** (cross-platform) | Windows-only → WinUI 3 acceptable; pure service backend → headless + Blazor frontend |
| Xamarin.Forms | **.NET MAUI** (direct successor — namespaces/handlers map almost 1:1) | — |
| Console/Windows Service, scheduled jobs | **.NET Worker Service** (`BackgroundService`), Hangfire, or ABP background jobs | — |
| ASP.NET Boilerplate / EAF monolith | **ABP Framework** (modular monolith → microservices path) | pair with `migrate-aspnetboilerplate-to-abp` when installed |
| Non-.NET backend (PHP, Java, Node, Python) | **ASP.NET Core Web API** (minimal APIs or controllers) | ABP when modular DDD/multi-tenancy is required |

### Web UI: WASM vs Server vs Web App

- **Blazor WebAssembly** (default preference): runs in the browser, no per-user server circuit, CDN-friendly, works offline-capable paths. Requires a clean API surface — plan it first.
- **Blazor Server**: intranet apps, low-latency LAN, legacy browsers, when WASM download size is a problem.
- **Blazor Web App (.NET 8+)**: SSR + islands — pick when SEO/first-paint matters or a gradual Server→WASM path is wanted.
- **MAUI Blazor Hybrid**: desktop/mobile shell reusing the SAME Razor components (share via a Razor Class Library) — the standard answer when the migration must ship web + desktop/mobile.

## Target Solution Layout

Propose this shape per extracted domain (adapt to the user's conventions — check for existing ABP/layered structure first):

```
src/
  {Product}.Domain/           # entities, enums, domain services (no infra deps)
  {Product}.Application/      # use cases, DTOs, interfaces (ports)
  {Product}.Infrastructure/   # EF Core DbContext, external clients (adapters)
  {Product}.Api/              # ASP.NET Core endpoints/controllers (the seam's far side)
  {Product}.Wasm/             # Blazor WebAssembly client
  {Product}.Maui/             # .NET MAUI app (if desktop/mobile in scope)
  {Product}.Shared.UI/        # Razor Class Library shared by Wasm + Maui Hybrid
tests/
  {Product}.Tests/            # xUnit unit + characterization
  {Product}.Parity/           # logical parity suite (legacy vs new)
  {Product}.E2E/              # Playwright
```

When the organization uses ABP, map instead to the ABP layered/module layout (`*.Domain`, `*.Application`, `*.EntityFrameworkCore`, `*.HttpApi`, `*.Blazor`) — see the `abp-*` skills when installed.

## Backend Strategies

### Legacy monolith → ASP.NET Core service(s)

1. YARP in front; migrate one route group at a time (`/api/billing/*`).
2. New service gets its own EF Core `DbContext` over owned tables; shared tables via owner-service + API reads or dual-write.
3. Inter-service calls: synchronous `HttpClientFactory`/Refit for commands, events (MassTransit / ABP distributed bus) for notifications and data sync.
4. Keep the URL surface stable — external consumers and the Blazor client depend on it. Version new APIs (`/api/v2`, header versioning) only when the contract must change.

### Non-.NET backend → ASP.NET Core

- Port the API contract first (contract tests), then the internals — the contract is the seam.
- Map framework concepts deliberately: middleware↔middleware, filters↔interceptors, DI↔DI, ORM→EF Core (verify provider support for the existing DB engine).
- Watch for impedance gaps: dynamic-typing payloads → DTOs with explicit validation; scoping/lifetime differences; sync→async (`async`/`await` end-to-end; no `.Result`/`.Wait()`).

### ASP.NET Framework → ASP.NET Core (same-language modernization)

- `.csproj` → SDK-style, `TargetFramework` → current .NET LTS.
- `Global.asax`/OWIN startup → `Program.cs` minimal hosting; `web.config` → `appsettings.json` + env vars.
- `System.Web` usages (HttpContext.Current, Server.MapPath, caching) → injected abstractions.
- `ApiController`/`Controller` ports are mostly mechanical; WebForms is NOT portable — it is a UI rewrite (see below).
- WCF server → ASP.NET Core Web API or CoreWCF only when SOAP must be preserved for legacy consumers.

## Frontend Strategies (→ Blazor / MAUI)

### Route-level migration (default)

- Map legacy routes to Blazor routes 1:1 where UX allows; a page is the migration unit.
- YARP or the legacy router splits traffic; shared auth bridge keeps sessions unified.
- Keep a screen inventory (`migration-plan/research/` parity surface) — every legacy screen needs a target disposition: migrate / merge / drop (with user confirmation for drops).

### Component-level (exceptional)

- Only when a page can't move as a unit. Bridge state via JS interop events; kill the bridge with the page.
- Never build a permanent two-framework page — transitional only.

### Desktop (→ .NET MAUI)

- Separate UI from logic first: port code-behind logic into services/viewmodels (MVVM) — the UI layer is then a thin shell.
- Reuse Razor components via MAUI Blazor Hybrid when the web app is also migrating — one component library (`*.Shared.UI`), two shells.
- Inventory platform dependencies early: printing, serial/USB, tray, registry, GDI drawing — each needs a MAUI-compatible plan or stays Windows-only (documented decision).

### Design and UX

- Follow `design` skill conventions for the new UI (it already has Blazor guidance); do not clone legacy pixel-for-pixel unless required — flag UX upgrades as optional scope in the SPEC, not silent scope creep.
- Component library: Fluent UI Blazor / MudBlazor / Radzen per user preference (never build base components from scratch).

## Data Strategies (→ EF Core)

- **Owned tables** → domain's own `DbContext`; legacy reads become API calls.
- **Shared tables** → dual-write (Pattern 3) or pick an owner service + API reads for others.
- **Schema modernization** → expand-contract: add new columns → dual-write → backfill → switch reads → drop old.
- **EF6 → EF Core gaps to check**: lazy-loading proxies (opt-in in EF Core), `Include` patterns, stored-proc mapping, spatial/UDT support, `GroupBy` translation — research each against the EF Core version chosen.
- **Stored procedures**: decide per-SP — port logic to domain services (preferred for business rules) or keep as mapped EF Core procs (reporting-heavy SPs).
- **Non-deterministic legacy columns** (encrypted per-row, computed triggers): document as migration risks with reconciliation queries.

## Auth & Session Bridging

The first seam to solve — everything else depends on it:

- **Prefer**: move both systems to a shared OIDC identity (Entra ID / OpenIddict / existing IdP). Legacy app validates the same token/cookie or accepts a bridge token minted by the gateway.
- **Transitional**: YARP transform that exchanges the legacy session cookie for a JWT (or vice-versa) — document it as throwaway with a decommission date.
- **Windows-auth-only legacy**: keep Windows auth on the legacy side during transition; issue tokens at the gateway after validating the Windows identity.
- Never port Forms auth ticket formats or custom password hashes — redesign per `security-debt.md` (PasswordHasher, OIDC, short-lived tokens).

## Observability During Migration

- Tag every request/log with `migration_path: legacy|new` (YARP header → Activity tag → Serilog property → OpenTelemetry attribute).
- Dashboard comparing old vs new: error rate, p50/p95/p99 latency, throughput, business metrics.
- Alerts: error-rate delta >1%, latency >2×, business metric delta >5%.
- `Traceparent`/`W3C` propagation through YARP so a request's legacy↔new hops appear in one trace.
- ASK THE USER which observability stack exists — never assume.

## Legacy Decommission Criteria

A domain's legacy path may be removed only when ALL hold:

- 100% traffic on the new path for ≥30 days.
- Parity suite green; contract tests green in CI.
- Data consistency validation clean for the agreed window.
- Feature flags/routes kept ≥60 days post-removal (documented in the roadmap).

## Common .NET Pitfalls to Check in Every Plan

| Pitfall | Why it matters |
| --- | --- |
| Blazor WASM calling legacy endpoints cross-origin | CORS + auth must be designed; prefer same-origin via YARP/static hosting |
| Blocking async (`.Result`, `.GetAwaiter().GetResult()` in ported code) | Deadlocks and thread starvation — plan code-review rule |
| EF Core tracking differences vs EF6/ADO.NET | Silent perf regressions and stale reads — parity suite must cover read paths |
| Culture/locale differences in ported formatting/parsing | Number/date formats change silently — include in golden masters |
| Assembly/binary serialization (`BinaryFormatter`, remoting) | Removed/obsolete in modern .NET — requires redesign, flagged in security-debt |
| Windows-only APIs (Registry, EventLog, `System.Drawing`) | Break on Linux containers — flag for replacement |
