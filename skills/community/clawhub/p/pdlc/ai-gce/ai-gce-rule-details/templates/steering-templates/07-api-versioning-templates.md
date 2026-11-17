<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# API Versioning Steering Templates

> **Purpose:** Used by the project-init-agent to generate API versioning steering files
> in the target project's `rules/` folder. These templates encode versioning strategy,
> backward compatibility rules, and deprecation management derived from `api-versioning.md`
> (conditional steering file — only generated when API versioning is in scope).

---

## api-versioning.md (FileMatch `{presentation_layer_pattern}`)

**Generates**: `rules/api-versioning.md`
**Condition**: Generated only IF `api-versioning.md` exists in workspace steering
**Derived From**: api-versioning.md + api-standards.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{presentation_layer_pattern}"
---

# API Versioning Standards

## Versioning Strategy
- {versioning_approach}: {versioning_description}
- ALL API endpoints MUST include version identifier: {version_format_example}
- {version_registration_mechanism}
- Deprecated versions MUST be marked with {deprecation_marker}

## Response Headers
- ALL responses MUST include {supported_versions_header} (lists active versions)
- Deprecated endpoints MUST include {sunset_header} and {deprecation_header}
- {version_negotiation_strategy}

## DTOs / Response Models
- Each major version MUST have its own response model namespace: {dto_namespace_pattern}
- Response models MUST NOT be shared across major versions
- Request models MAY be shared if format is unchanged between versions

## Backward Compatibility Rules
- NEVER remove a field from a response without a major version bump
- NEVER add a required field to a request without a major version bump
- New optional fields MAY be added without version bump (non-breaking)
- {additional_compatibility_rules}

## Deprecation Process
- {deprecation_notice_period}
- {deprecation_communication_strategy}
- {migration_support_strategy}
- Deprecated versions MUST remain functional until {sunset_policy}
```
