<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Backend-for-Frontend (BFF)

## When This Extension Applies

Your system likely needs BFF patterns if:

- Multiple distinct client types (web SPA, mobile app, third-party, internal tools)
- Clients need different data shapes from the same backend services
- Need to aggregate multiple backend calls into one client call
- API gateway alone is insufficient (need client-specific business logic)
- Different authentication or rate-limiting per client type

## Opt-In Question

```
### Would you like to apply Backend-for-Frontend (BFF) patterns?

This extension adds detailed guidance for:
- BFF vs. API Gateway decision framework (when BFF, when gateway is enough)
- Per-client BFF design (aggregation rules, response shaping, caching)
- BFF ownership model (frontend team owns BFF vs. backend team)
- GraphQL as BFF (federation, schema stitching for client flexibility)
- Authentication flow per BFF (token exchange, session handling)
- BFF scaling and deployment (coupled vs. independent from frontend)

(a) Yes — Design BFF layer for my multi-client system
(b) No — Single API serving all clients is sufficient

Recommended for: Mobile + Web + third-party consumers; different data needs per client
Skip if: Single SPA consuming a single API; uniform client requirements
```

## Status: ✅ Available (v1.1)
