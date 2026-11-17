<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Observability Steering Templates

> **Purpose:** Used by the project-init-agent to generate observability-related steering files
> in the target project's `rules/` folder. These templates encode logging standards,
> tracing conventions, and sensitive data protection rules derived from `observability-logging.md`
> and `observability-sensitive.md`.

---

## observability-logging.md (Always)

**Generates**: `rules/observability-logging.md`
**Derived From**: observability-logging.md + tech-stack.md

```markdown
---
inclusion: always
---

# Logging Standards

## Message Format
- ALL log messages MUST use {logging_framework} {message_format_type} with named properties
- CORRECT: {correct_log_example}
- WRONG: {wrong_log_example}
- Property names MUST be {property_naming_convention}

## Log Levels
- Fatal: System cannot continue ({fatal_examples})
- Error: Operation failed, needs attention ({error_examples})
- Warning: Unexpected but handled ({warning_examples})
- Information: Business events on happy path ({info_examples})
- Debug: Technical details ({debug_examples})

## Required Logging Points
- ALL entity state transitions MUST be logged at Information
- ALL external service calls MUST be logged with service, endpoint, duration, status
- ALL {domain_critical_operation_type} operations MUST be logged with {domain_log_fields}
- ALL security events MUST be logged (login, failed auth, permission denied)
- ALL errors MUST be logged with full exception
- ALL background job start/complete MUST be logged with duration and result count

## Context (automatic via {context_enrichment_mechanism})
- {auto_context_fields} are added automatically
- Use {scoped_context_mechanism} for operation-scoped context

## Performance
- NEVER log inside tight loops — log batch summary instead
- Use {log_level_check_pattern} before expensive log message construction
- Debug level MUST be disabled in production
```

---

## observability-tracing.md (Conditional — IF tracing configured)

**Generates**: `rules/observability-tracing.md`
**Condition**: Generated IF `observability-tracing.md` exists in workspace OR tracing tool specified in tech-stack
**Derived From**: observability-tracing.md + tech-stack.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{application_and_infrastructure_pattern}"
---

# Tracing Standards

## Custom Spans
- ALL command handlers MUST create a span: {span_creation_pattern}
- ALL cross-module service calls MUST create a span: {cross_module_span_pattern}
- ALL external HTTP calls are auto-instrumented (do not create duplicate spans)
- ALL database calls are auto-instrumented (do not create duplicate spans)

## Span Attributes
- Business operations MUST include: {business_span_attributes}
- NEVER include sensitive data in span attributes (passwords, tokens, PII)
- Use semantic conventions: {semantic_attribute_examples}

## Span Naming
- API: "{api_span_naming}" (automatic)
- Application: "{application_span_naming}"
- Domain: "{domain_span_naming}"
- External: "{external_span_naming}"

## Error Handling in Spans
- {span_error_status_pattern} when operation fails
- {span_exception_recording_pattern} for unhandled exceptions
- Add error event with reason for business failures
```

---

## observability-sensitive-data.md (Always)

**Generates**: `rules/observability-sensitive-data.md`
**Derived From**: observability-sensitive.md + security-rules.md

```markdown
---
inclusion: always
---

# Sensitive Data Protection in Observability

## NEVER log, trace, or include in metrics:
- Passwords, password hashes, or password reset tokens
- JWT tokens, API keys, or secrets
- {sensitive_identifier_types}
- Personal addresses or phone numbers
- Full request/response bodies containing PII
- Connection strings or database credentials
- Encryption keys or certificates

## Masking Rules
{for_each_sensitive_field_type}
- {field_type}: {masking_pattern} → "{masked_example}"
{end_for_each}

## Safe to Log
- Entity IDs ({safe_id_examples})
- {safe_value_examples} (not PII)
- Status values and state transitions
- Timestamps and durations
- Error codes and messages (not stack traces with secrets)
```
