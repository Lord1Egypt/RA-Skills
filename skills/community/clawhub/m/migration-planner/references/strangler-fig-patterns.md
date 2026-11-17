# Strangler Fig Patterns — .NET Edition

The Strangler Fig pattern (Martin Fowler) gradually replaces a legacy system by building new functionality around it until the old system can be decommissioned. This reference adapts each pattern to concrete .NET seam implementations.

Four governing activities (Cartwright, Horn, Lewis):

1. Establish clear desired outcomes with organizational alignment.
2. Identify seams to decompose the system into manageable pieces.
3. Replace isolated components at acceptable risk.
4. Evolve team practices alongside the system.

Key principle: **transitional architecture** — temporary code that lets legacy and .NET coexist. Its cost is justified by the risk avoided versus a big-bang rewrite.

## Pattern 1: API Gateway Strangler (YARP)

Use when HTTP routes must be split between the legacy app and new ASP.NET Core services.

**.NET implementation:**

1. Stand up a [YARP](https://microsoft.github.io/reverse-proxy/) reverse proxy in front of the legacy app (or beside it).
2. Add route config per migrated slice — matched on path prefix, method, or host:

```csharp
// Program.cs — route /api/invoices to the new Billing service, everything else to legacy
builder.Services.AddReverseProxy().LoadFromMemory(
    routes: new[]
    {
        new RouteConfig { RouteId = "billing", ClusterId = "new",
            Match = new RouteMatch { Path = "/api/invoices/{**catch-all}" } },
        new RouteConfig { RouteId = "legacy", ClusterId = "legacy",
            Match = new RouteMatch { Path = "{**catch-all}" } }
    },
    clusters: new[]
    {
        new ClusterConfig { ClusterId = "new",
            Destinations = { { "d1", new DestinationConfig { Address = "https://new-api/" } } } },
        new ClusterConfig { ClusterId = "legacy",
            Destinations = { { "d1", new DestinationConfig { Address = "https://legacy-app/" } } } }
    });
```

3. Combine with `Microsoft.FeatureManagement` for percentage/flag-based routing inside a transform.
4. Decommission legacy routes once the new implementation is validated.

**Applies to:** monolith → ASP.NET Core services; ASP.NET Framework → ASP.NET Core; any web-backend rewrite where the URL surface must stay stable (important when Blazor WASM clients already target those URLs).

**Rollback:** point the YARP route back to the legacy cluster, or set the routing flag to 0%. Instant, no redeploy of business code.

## Pattern 2: Service Extraction with Adapter (DI seam)

Use when extracting a bounded context from a monolith into a separate ASP.NET Core service — or absorbing a service back into a modular monolith.

**.NET implementation:**

1. **Extract interface** — `IBillingService` capturing the capability.
2. **Legacy adapter** — `LegacyBillingService : IBillingService` delegating to the in-process legacy code (or HTTP client against the legacy endpoint).
3. **New implementation** — `BillingService : IBillingService` in the new service.
4. **Select via DI + feature flag**:

```csharp
services.AddScoped<LegacyBillingService>();
services.AddScoped<BillingService>();
services.AddScoped<IBillingService>(sp =>
    sp.GetRequiredService<IFeatureManager>().IsEnabledAsync("Migration.Billing").GetAwaiter().GetResult()
        ? sp.GetRequiredService<BillingService>()
        : sp.GetRequiredService<LegacyBillingService>());
```

**Applies to:** monolith → services; services → modular monolith; swapping a WCF/remoting dependency for an HTTP client.

**Key considerations:** adapters must translate protocol differences (sync↔async, exception models, DTO shapes); both implementations must satisfy the same contract/parity tests (`testing-safety-nets.md`); the interface IS the seam — keep it free of legacy types.

## Pattern 3: Database Strangler (Dual-Write with EF Core)

Use when the data store changes: schema redesign, engine change (SQL Server ↔ PostgreSQL, → NoSQL), or splitting a shared DB.

**.NET implementation:**

1. New writes go to the **new** EF Core `DbContext` (source of truth).
2. Async sync to legacy — background service, `IDistributedEventBus` handler, or outbox message; failures are logged/retried, never block the operation.
3. Reads try new first, fall back to legacy repository.
4. **Lazy migration** — on a legacy read, copy the row to the new store before returning.
5. Backfill job migrates cold data; then stop dual-write and decommission.

**Critical safeguards:**

- The new store is ALWAYS the write source of truth once dual-write starts.
- Keep both `DbContext` types in the same deployable during transition; isolate them behind repository interfaces.
- Run continuous data-consistency validation (`testing-safety-nets.md`).
- Prefer **expand-contract** for same-DB schema changes: add new columns → dual-write → backfill → switch reads → drop old.

## Pattern 4: UI Component Strangler (Blazor/MAUI islands)

Use when migrating the UI: WebForms/MVC/jQuery/AngularJS/Angular → **Blazor WebAssembly**, or desktop → **.NET MAUI**.

**Web — page/route level (preferred):**

1. Keep the legacy app serving its routes.
2. Stand up the Blazor WASM app for migrated routes; YARP (Pattern 1) or the legacy router sends users to the right app per URL.
3. Share auth via OIDC cookie/token bridge so users never re-login between apps.
4. Migrate one route/feature at a time — NOT component-by-component inside a page.

**Web — component level (only when pages are too big):**

1. Embed Blazor components in legacy pages via the custom-element/`blazor` component registration, or an isolated `<iframe>`/JS-interop island as a last resort.
2. Bridge state with DOM events or a small JS pub-sub; keep the bridge temporary — it dies with the legacy page.
3. Namespace CSS (scoped CSS in Blazor, BEM or CSS isolation for legacy) to avoid bleed.

**Desktop:**

- WinForms/WPF → MAUI: wrap legacy screens behind a shell/navigation seam; reuse business services via DI interfaces first, then port screen-by-screen.
- To share UI between web and desktop targets, extract Razor components into a Razor Class Library consumed by both the WASM app and a MAUI Blazor Hybrid shell.

**Key considerations:**

- Blazor WASM cannot touch the DB or server internals — plan the API surface first; a screen blocked on missing API endpoints is a backend task disguised as UI work.
- Two runtimes on one page are heavy — prefer route-level migration.
- Auth/session is the hardest seam: solve it once (Pattern + auth bridge in `dotnet-target-strategies.md`) before the first UI migration.

## Pattern 5: Event Interception

Use when the legacy system emits/consumes messages (MSMQ, RabbitMQ, Service Bus, in-process events) and handlers must migrate.

**.NET implementation:**

1. Intercept at the producer — wrap legacy dispatch to also publish to the new bus (e.g., via MassTransit / `IDistributedEventBus` on ABP).
2. Old and new consumers both receive events during transition.
3. New consumers process the modern contract; decommission legacy consumers after validation.

**Key considerations:** define and test the old→new message mapping; document ordering differences; ensure idempotency — during transition some events will be processed twice.

## Pattern 6: Branch by Abstraction

Use for large internal replacements that can't be extracted: custom ORM → EF Core, legacy HTTP stack → `HttpClientFactory`, custom auth → ASP.NET Core Identity/OIDC, report engine, vendor SDK.

**.NET implementation:**

1. Create an interface for the component being replaced.
2. Redirect all call sites to the interface (DI).
3. Wrap the legacy implementation behind it; build the new one beside it.
4. Switch with `Microsoft.FeatureManagement` flags (config or runtime toggles).
5. Remove the legacy implementation once validated.

**Difference from Pattern 2:** same deployment unit — nothing becomes a service.

## Migration Phase Management

Every migration passes through:

| Phase | Traffic to new | Duration | Validation | Rollback trigger |
| --- | --- | --- | --- | --- |
| **Setup** | 0% | until infra ready | smoke tests pass | — |
| **Shadow** | 0% (dual-run, compare) | 1–2 weeks | parity > 99% | mismatch > 5% |
| **Canary** | 5–10% | 1–2 weeks | error rate < baseline +0.1% | error rate > baseline +1% |
| **Ramp** | 25→50→75% | 2–4 weeks/step | performance parity | latency > 2× baseline |
| **Full** | 100% | ≥30 days | all metrics green | any degradation |
| **Cleanup** | 100% (legacy removed) | 1–2 weeks | legacy unused 30 days | — (no rollback) |

**Critical rule:** never advance before the current phase's validation passes. A fired rollback trigger reverts ONE phase — not to zero.

## Choosing the Right Pattern

| Situation | Primary pattern | Supporting |
| --- | --- | --- |
| HTTP routes split legacy/new | API Gateway Strangler (YARP) | Service Extraction per endpoint group |
| Module → separate ASP.NET Core service | Service Extraction + DI adapter | Branch by Abstraction for internal deps |
| Shared DB must split/change | Database Strangler (EF Core dual-write) | Expand-contract; API reads for non-owners |
| WebForms/MVC/Angular → Blazor WASM | UI Component Strangler (route-level) | YARP routing; auth bridge |
| WinForms/WPF → .NET MAUI | UI Strangler (screen-level) + DI seams | Shared RCL for Blazor reuse |
| Internal library replacement | Branch by Abstraction | — |
| MSMQ/RabbitMQ → new bus | Event Interception | DB Strangler if events drive writes |
| ASP.NET Boilerplate → ABP | Branch by Abstraction per module | `migrate-aspnetboilerplate-to-abp` skill when installed |
