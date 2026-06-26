---
name: micro-frontend-arch
description: "Micro-frontend architecture design and implementation guide. Use when: designing micro-frontend architecture, choosing between Module Federation/qiankun/single-spa/wujie, splitting monolith into sub-apps, implementing style isolation, setting up inter-app communication, or deploying micro-frontends independently."
---

# Micro-Frontend Architecture

## Framework Selection

| Scenario | Recommended |
|----------|-------------|
| New project, Webpack 5 | Module Federation |
| Legacy jQuery/Vue2 migration | qiankun |
| Multi-framework coexistence | single-spa |
| Need JS sandbox + style isolation | wujie |

## Core Workflow

1. **Design** → Define app boundaries, shared dependencies, routing strategy
2. **Setup** → Configure main app shell + sub-apps (see framework-specific refs)
3. **Communication** → Choose communication pattern (see references/communication.md)
4. **Style Isolation** → Prevent CSS conflicts (see references/style-isolation.md)
5. **Deploy** → Independent CI/CD per sub-app (see references/deployment.md)

## References

- **references/module-federation.md** — Webpack Module Federation config & patterns
- **references/qiankun.md** — qiankun registration, sandbox, lifecycle hooks
- **references/single-spa.md** — single-spa root config & app registration
- **references/communication.md** — Props, CustomEvent, shared store patterns
- **references/style-isolation.md** — Shadow DOM, CSS Modules, scoped strategies
- **references/deployment.md** — Independent deploy, CDN, versioning strategy
