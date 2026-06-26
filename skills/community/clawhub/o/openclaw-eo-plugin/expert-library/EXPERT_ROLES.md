# Expert Roles (8 Roles)

> Fast-access role layer mapped from 141 category experts.

## Role Overview

| Role | ID Prefix | Count | Primary Source | Command |
|------|----------|-------|----------------|---------|
| **Architect** | ar | 5 | engineering, specialized | `/architect` |
| **Planner** | pl | 4 | marketing, sales, product | `/plan` |
| **Frontend** | fe | 4 | engineering, design | `/frontend` |
| **Backend** | be | 5 | engineering, specialized | `/backend` |
| **QA** | qa | 4 | testing, engineering | `/verify`, `/e2e`, `/tdd` |
| **Security** | sc | 4 | engineering, specialized | `/security-scan` |
| **DevOps** | do | 4 | engineering, specialized | `/deploy`, `/build-fix` |
| **CodeReviewer** | cr | 5 | engineering, specialized | `/code-review` |

## Role Definitions

### Architect (架构师)
```
ID prefix: ar
Maps from: engineering, specialized, product, spatial
Commands: /architect
Tasks: System architecture, tech selection, architecture review
```

### Planner (规划师)
```
ID prefix: pl
Maps from: marketing, sales, product, project-management
Commands: /plan
Tasks: Project planning, task decomposition, milestone creation
```

### Frontend (前端开发)
```
ID prefix: fe
Maps from: engineering, design, game-development
Commands: (direct role access)
Tasks: UI development, component library, responsive design
```

### Backend (后端开发)
```
ID prefix: be
Maps from: engineering, specialized
Commands: (direct role access)
Tasks: API design, database architecture, service development
```

### QA (测试工程师)
```
ID prefix: qa
Maps from: testing, engineering
Commands: /verify, /e2e, /tdd
Tasks: Test planning, automation, quality assurance
```

### Security (安全工程师)
```
ID prefix: sc
Maps from: engineering, specialized
Commands: /security-scan
Tasks: Security audit, vulnerability assessment, penetration testing
```

### DevOps (运维工程师)
```
ID prefix: do
Maps from: engineering, specialized
Commands: /deploy, /build-fix
Tasks: CI/CD, deployment, monitoring, infrastructure
```

### CodeReviewer (代码审查)
```
ID prefix: cr
Maps from: engineering, specialized
Commands: /code-review
Tasks: Code quality review, refactoring suggestions, pattern enforcement
```

## Quick Reference

For **standard tasks** → Use 8 roles (fast path)
For **specialized needs** → Use 13 categories (deep path)

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed two-layer architecture explanation.
