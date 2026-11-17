<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: tech-stack.md

## Template Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Technology Stack + ADRs | date: {generation-date} -->

# Technology Stack

## Stack Identity

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Language | {language} | {version} | Primary development language |
| Runtime | {runtime} | {version} | Server runtime |
| Framework | {framework} | {version} | Application framework |
| Database | {database} | {version} | Primary data store |
| Cache | {cache} | {version} | Caching and session store |
| Search | {search-engine} | {version} | Full-text search |
| Queue | {queue} | {version} | Background jobs |
| Message Broker | {broker} | {version} | Inter-service messaging |
| UI Framework | {ui-framework} | {version} | Frontend |
| ORM | {orm} | {version} | Database access |
| Testing | {test-framework} | — | Testing |
| Linter | {linter} | — | Code quality |
| Formatter | {formatter} | — | Code style |
| Containerization | {container-tool} | {version} | Dev and deploy |
| Orchestration | {orchestration} | {version} | Multi-container |
| Observability | {obs-stack} | — | Monitoring |

<!-- begin: AP-sourced -->

## Rules

### DO (Required)

1. Use ONLY the technologies listed above. Any addition requires an ADR and team approval.
2. Pin major versions in package manifests.
3. Use the ORM for ALL database operations.
4. Use official framework patterns.
5. All containers defined in docker-compose.yml for local development.
{additional rules from AP}

### DO NOT (Forbidden)

1. DO NOT introduce alternative frameworks without an ADR.
2. DO NOT use deprecated APIs.
3. DO NOT upgrade major versions without team agreement.
4. DO NOT use technology-specific features that break portability.
{additional prohibitions from AP}

<!-- end: AP-sourced -->

## Architecture Decisions

| ADR | Decision | Impact |
|-----|----------|--------|
| ADR-{NNN} | {title} | {impact} |
| ... | ... | ... |

## Version Policy

- **Major upgrades:** Require ADR + team discussion
- **Minor upgrades:** Allowed if tests pass
- **Patch upgrades:** Allowed freely
- **Security patches:** Apply immediately
```

## Filling Instructions

Refer to `mapping/techstack-to-config.md` (Target 1 section).
