<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: naming-conventions.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Technology Stack + Component Design + Domain Context | date: {generation-date} -->

# Naming Conventions

## Files & Folders
<!-- begin: AP-sourced -->
| Item | Convention | Example |
|------|-----------|---------|
| Module folder | kebab-case | `incident-management/` |
| Service file | {tech-convention} | `{example}` |
| Controller | {tech-convention} | `{example}` |
| Repository | {tech-convention} | `{example}` |
| DTO | {tech-convention} | `{example}` |
| Test file | {tech-convention} | `{example}` |
| Migration | {convention} | `{example}` |
| Constant file | {convention} | `{example}` |
<!-- end: AP-sourced -->

## Classes & Interfaces
<!-- begin: AP-sourced -->
| Item | Convention | Example |
|------|-----------|---------|
| Class | PascalCase | `IncidentService` |
| Interface | {I-prefix or not — tech choice} | `{example}` |
| Enum | PascalCase | `IncidentStatus` |
| Type alias | PascalCase | `CreateIncidentDto` |
<!-- end: AP-sourced -->

## Functions & Variables
<!-- begin: AP-sourced -->
| Item | Convention | Example |
|------|-----------|---------|
| Function/method | camelCase, verb-first | `createIncident()` |
| Variable | camelCase | `incidentCount` |
| Constant | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Boolean | is/has prefix | `isActive`, `hasAttachment` |
| Private | {tech-convention} | `{example}` |
<!-- end: AP-sourced -->

## Database (cross-ref database-rules.md)
<!-- begin: AP-sourced -->
| Item | Convention | Example |
|------|-----------|---------|
| Table | plural snake_case | `incidents` |
| Column | snake_case | `created_at` |
| FK | {ref}_id | `incident_id` |
| Index | idx_{table}_{columns} | `idx_incidents_tenant_status` |
<!-- end: AP-sourced -->

## API (cross-ref api-standards.md)
<!-- begin: AP-sourced -->
| Item | Convention | Example |
|------|-----------|---------|
| URL path | kebab-case, plural | `/service-requests` |
| Query param | camelCase | `?pageSize=20` |
| JSON field | camelCase | `createdAt` |
| Error code | UPPER_SNAKE_CASE | `VALIDATION_FAILED` |
<!-- end: AP-sourced -->

## Domain Terms (cross-ref domain-context.md)
<!-- begin: AP-sourced -->
Use EXACT terms from domain-context.md. NEVER use synonyms.
| Domain Term | Use In Code | NEVER Use |
|-------------|-------------|-----------|
| {term} | `{ClassName}` | {synonyms} |
| ... | ... | ... |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 4).
