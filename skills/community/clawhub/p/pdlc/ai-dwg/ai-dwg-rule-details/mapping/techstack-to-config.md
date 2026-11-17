<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Technology Stack → tech-stack.md + .gitignore + docker-compose.yml + .editorconfig

## Purpose

This mapping rule transforms the **Technology Stack** document (AP artifact) and its associated ADRs into four workspace artifacts:
1. `rules/tech-stack.md` — Technology reference and constraints
2. `.gitignore` — Stack-appropriate ignore patterns
3. `docker-compose.yml` — Development infrastructure skeleton
4. `.editorconfig` — Code style enforcement

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- tech-stack.md is RESTRICTIVE, not descriptive — it defines what's ALLOWED; unauthorized additions are architecture violations
- Generate docker-compose for infrastructure services only — databases, caches, queues; never application containers (those are AI-DLC v1's domain)
- Match .gitignore patterns to the specific technology stack — better to over-ignore than accidentally commit node_modules or .env files
- Ensure ADR references are included for every major technology choice — "why PostgreSQL and not MongoDB?" should have a documented answer
- Think about version policy as governance — major upgrades require ADR, patches are free, security fixes are immediate

### Anti-Patterns for This Activity
- Do NOT add technologies the AP doesn't specify — if no formatter is mentioned, don't add Prettier
- Do NOT use `latest` tags in docker-compose — pin to the specific version from the AP
- Do NOT generate opinions beyond the AP — if AP says TypeORM, generate TypeORM patterns even if you "prefer" Prisma

### Quality Check
A good output from this activity sounds like:
- "tech-stack.md DO NOT rule: 'DO NOT introduce alternative frameworks (e.g., Express alongside NestJS) without an ADR'. Every technology choice is locked by architecture decision."
- "docker-compose.yml: postgres:16 (port 5432, healthcheck, named volume), redis:7 (port 6379), rabbitmq:3 (management UI on 15672). Infrastructure only — no app containers."

---

## Source (AP Artifact)

**Document:** Technology Stack (typically `04_Technology_Stack.md` or `decisions/technology-stack.md`)

**Sections to extract:**

| Section | Contains | Maps To |
|---------|----------|---------|
| Technology selections per container | Language, framework, DB, cache, queue, etc. | All four output files |
| Selection rationale | Why each technology was chosen | `tech-stack.md` rationale |
| ADR references | ADR-NNN for each major decision | `tech-stack.md` cross-references |
| Version specifications | Minimum/target versions | `tech-stack.md`, `docker-compose.yml` |
| Development tooling | Linters, formatters, test runners | `.editorconfig`, `tech-stack.md` |

---

## Target 1: tech-stack.md

### Role

Technology reference steering file. Developers consult this to know what's allowed, what's not, and what version to target. Prevents technology drift and unauthorized additions.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Technology Stack + ADRs | date: {generation-date} -->

# Technology Stack

## Stack Identity

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Language | {e.g., TypeScript} | {e.g., 5.4+} | Primary development language |
| Runtime | {e.g., Node.js} | {e.g., 20 LTS} | Server runtime |
| Framework | {e.g., NestJS} | {e.g., 10.x} | Application framework |
| Database | {e.g., PostgreSQL} | {e.g., 16.x} | Primary data store |
| Cache | {e.g., Redis} | {e.g., 7.x} | Caching and session store |
| Search | {e.g., Elasticsearch} | {e.g., 8.x} | Full-text search (if applicable) |
| Queue | {e.g., BullMQ} | {e.g., 5.x} | Background jobs and async processing |
| Message Broker | {e.g., RabbitMQ} | {e.g., 3.x} | Inter-service messaging (if applicable) |
| UI Framework | {e.g., React} | {e.g., 18.x} | Frontend (if applicable) |
| ORM / Data Access | {e.g., Prisma} | {e.g., 5.x} | Database access layer |
| Testing | {e.g., Jest + Supertest} | — | Unit and integration testing |
| Linter | {e.g., ESLint} | — | Code quality |
| Formatter | {e.g., Prettier} | — | Code style |
| Containerization | {e.g., Docker} | {e.g., 24+} | Development and deployment |
| Orchestration | {e.g., Docker Compose} | {e.g., 2.x} | Local multi-container setup |
| Observability | {e.g., OpenTelemetry + Grafana} | — | Monitoring and tracing |

<!-- begin: AP-sourced -->

## Rules

### DO (Required)

1. Use ONLY the technologies listed above. Any addition requires an ADR and team approval.
2. Pin major versions in package manifests (lockfile committed).
3. Use the ORM/data access layer for ALL database operations — no raw SQL unless explicitly justified.
4. Use the official framework patterns (e.g., NestJS modules, decorators, DI) — no ad-hoc alternatives.
5. All containers MUST be defined in docker-compose.yml for local development.

### DO NOT (Forbidden)

1. DO NOT introduce alternative frameworks (e.g., Express alongside NestJS) without an ADR.
2. DO NOT use deprecated APIs of any listed technology.
3. DO NOT upgrade major versions without team agreement and an ADR.
4. DO NOT use technology-specific features that break portability (unless AP explicitly permits).
5. DO NOT add client-side state management libraries beyond what's specified (if frontend exists).

<!-- end: AP-sourced -->

## Architecture Decisions

| ADR | Decision | Impact |
|-----|----------|--------|
| ADR-{NNN} | {title} | {brief impact on development} |
| ... | ... | ... |

## Version Policy

- **Major upgrades:** Require ADR + team discussion
- **Minor upgrades:** Allowed if tests pass; note in PR
- **Patch upgrades:** Allowed freely; keep lockfile updated
- **Security patches:** Apply immediately; no ADR needed
```

### Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Technology selection (name + version) | Copy to Stack Identity table | Row in stack table |
| Selection rationale | Compress to ADR reference | ADR link in Decisions table |
| Version specification | Copy to Version column | Stack table version |
| "We chose X over Y because Z" | Reference the ADR | Decisions section |
| Development tooling mentions | Add to appropriate stack row | Linter/Formatter/Testing rows |

---

## Target 2: .gitignore

### Role

Prevent committing generated files, dependencies, secrets, and platform-specific artifacts. Content is technology-specific.

### Generation Logic

Select patterns based on Technology Stack selections:

| Technology Detected | Add Patterns |
|--------------------|-------------|
| Node.js / TypeScript | `node_modules/`, `dist/`, `build/`, `.env`, `.env.*`, `*.js.map`, `coverage/` |
| Python / Django | `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.env`, `db.sqlite3`, `*.egg-info/`, `htmlcov/` |
| .NET / C# | `bin/`, `obj/`, `*.user`, `*.suo`, `.vs/`, `packages/`, `*.nupkg` |
| Java / Spring | `target/`, `*.class`, `.gradle/`, `build/`, `.settings/`, `*.jar` |
| Docker | `.docker/`, `docker-compose.override.yml` |
| IDE (always) | `.idea/`, `.vscode/settings.json`, `*.swp`, `.DS_Store`, `Thumbs.db` |
| Secrets (always) | `.env`, `.env.*`, `*.pem`, `*.key`, `secrets/` |
| Logs (always) | `logs/`, `*.log`, `npm-debug.log*` |
| OS (always) | `.DS_Store`, `Thumbs.db`, `*.tmp` |

### Template Selection

Load the appropriate base template from `templates/config/gitignore/` based on primary technology, then append common patterns (IDE, secrets, logs, OS).

### Structure

```gitignore
# ═══════════════════════════════════════════
# {Project Name} — .gitignore
# Generated by AI-DWG | Stack: {primary technology}
# ═══════════════════════════════════════════

# Dependencies
{technology-specific dependency patterns}

# Build output
{technology-specific build patterns}

# Environment & Secrets
.env
.env.*
*.pem
*.key
secrets/

# IDE
.idea/
.vscode/settings.json
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Test coverage
coverage/
htmlcov/

# Docker (local overrides)
docker-compose.override.yml
```

---

## Target 3: docker-compose.yml

### Role

Development infrastructure skeleton. Defines containers for local development matching the architecture's data stores, caches, queues, and services.

### Generation Logic

Build services from Technology Stack selections:

| Technology | Docker Service |
|-----------|---------------|
| PostgreSQL | `postgres` with volume, port 5432, env vars |
| MySQL | `mysql` with volume, port 3306, env vars |
| MongoDB | `mongo` with volume, port 27017 |
| Redis | `redis` with port 6379 |
| Elasticsearch | `elasticsearch` with volume, ports 9200/9300, memory limits |
| RabbitMQ | `rabbitmq` with management plugin, ports 5672/15672 |
| Kafka | `kafka` + `zookeeper` with ports |
| MinIO (object storage) | `minio` with volume, ports 9000/9001 |
| MailHog / MailPit (dev email) | `mailpit` with ports 1025/8025 |

### Structure

```yaml
# ═══════════════════════════════════════════
# {Project Name} — Development Infrastructure
# Generated by AI-DWG | Source: Infrastructure & Deployment + Technology Stack
# ═══════════════════════════════════════════
#
# Usage: docker compose up -d
# Tear down: docker compose down -v

version: "3.8"

services:
  {service-name}:
    image: {image}:{version-tag}
    container_name: {project-prefix}_{service-name}
    ports:
      - "{host-port}:{container-port}"
    environment:
      {ENV_VAR}: {value}
    volumes:
      - {volume-name}:/path/in/container
    healthcheck:
      test: [{healthcheck-command}]
      interval: 10s
      timeout: 5s
      retries: 3

  # ... repeat for each infrastructure service

volumes:
  {volume-name}:

networks:
  default:
    name: {project-prefix}_network
```

### Rules

1. Include ONLY infrastructure services (databases, caches, queues) — NOT application containers
2. Use specific version tags (not `latest`)
3. Include healthchecks for all services
4. Use named volumes for data persistence
5. Use project-prefix in container names to avoid conflicts
6. Include comments explaining each service's role
7. Set reasonable resource limits for heavy services (Elasticsearch, Kafka)

---

## Target 4: .editorconfig

### Role

Enforce basic code style consistency across all editors and IDEs. Technology-aware formatting rules.

### Generation Logic

| Technology | Indent Style | Indent Size | End of Line | Trim Trailing | Final Newline |
|-----------|:------------:|:-----------:|:-----------:|:-------------:|:-------------:|
| TypeScript/JavaScript | space | 2 | lf | true | true |
| Python | space | 4 | lf | true | true |
| C# / .NET | space | 4 | crlf | true | true |
| Java | space | 4 | lf | true | true |
| Go | tab | 4 | lf | true | true |
| YAML | space | 2 | lf | true | true |
| Markdown | space | 2 | lf | false | true |
| Makefile | tab | 4 | lf | true | true |

### Structure

```ini
# ═══════════════════════════════════════════
# {Project Name} — Editor Configuration
# Generated by AI-DWG | Stack: {primary technology}
# https://editorconfig.org
# ═══════════════════════════════════════════

root = true

# Default for all files
[*]
charset = utf-8
end_of_line = {based on primary tech}
indent_style = {based on primary tech}
indent_size = {based on primary tech}
trim_trailing_whitespace = true
insert_final_newline = true

# {Primary language files}
[*.{extensions}]
indent_size = {tech-specific}

# YAML (always 2-space)
[*.{yml,yaml}]
indent_size = 2

# Markdown (preserve trailing spaces for line breaks)
[*.md]
trim_trailing_whitespace = false

# Makefile (must use tabs)
[Makefile]
indent_style = tab
```

---

## Key Rules for This Mapping

1. **tech-stack.md is restrictive** — it defines what's ALLOWED, not just what exists. Unauthorized additions are prohibited.
2. **docker-compose.yml is infrastructure-only** — no application services; those are for the team to add during development.
3. **.gitignore is comprehensive** — better to over-ignore than under-ignore. Include patterns for all detected technologies.
4. **.editorconfig matches the primary technology** — consistency with ecosystem conventions.
5. **Version numbers come from AP** — if AP specifies "PostgreSQL 16", use `postgres:16` not `postgres:latest`.
6. **ADR references are mandatory** — every major technology choice in tech-stack.md links to its ADR.
7. **No opinions beyond AP** — if AP doesn't specify a formatter, don't add one. If AP says "Prettier", include it.

---

## Depth Adaptation

| Depth | tech-stack.md | docker-compose.yml | .gitignore | .editorconfig |
|-------|--------------|-------------------|-----------|---------------|
| **Minimal** | Stack table + basic rules (5 DO, 3 DON'T) | Core services only (DB + cache) | Standard patterns | Basic config |
| **Standard** | Full structure as defined above | All infrastructure services with healthchecks | Technology-specific + common | Full with language-specific overrides |
| **Comprehensive** | Full structure + version policy + upgrade procedures + compatibility notes | All services + environment profiles (dev/test) + resource limits | Exhaustive (includes CI artifacts, IDE variants) | Full + per-folder overrides if polyglot |

---

## Reconciliation Behavior

When Technology Stack changes:

| Change | Impact | Action |
|--------|--------|--------|
| New technology added | New service in docker-compose, new .gitignore patterns | Add to all four files |
| Technology version changed | Version update in tech-stack, docker image tag | Update references |
| Technology removed | Service removed from docker-compose | Flag for user (may have data in volume) |
| Framework changed | Major restructure | Flag as HIGH IMPACT — affects coding-standards, naming-conventions, and potentially module-structure |
| New ADR for technology | New entry in decisions table | Add to tech-stack.md decisions section |
