---
name: Error Writer
description: Rewrites bad error messages into clear, actionable ones. Paste your error strings, exception messages, or an entire errors file and get back a full rewrite following the "what happened / why it happened / what to do next" pattern — with separate variants for log output, user-facing UI text, and API response bodies. Also audits for anti-patterns: vague generics ("Something went wrong"), leaked internals (stack traces in user-facing messages), wrong audience (developer jargon in end-user messages), and missing context. Works across any language. Zero external API. Triggers on "rewrite error messages", "fix error messages", "bad error message", "improve errors", "error message audit", "/error-writer".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - error-messages
    - ux-writing
    - developer-experience
    - api-design
    - logging
    - user-experience
    - developer-tools
    - code-quality
---

# Error Writer

Bad error messages are the #1 cause of unnecessary support tickets and debugging dead ends. Good error messages tell you what broke, why, and exactly what to do next.

Paste your existing error strings and get a complete rewrite — one version for users, one for logs, one for your API response body.

**Works on any language. No config. No API keys.**

---

## Trigger Phrases

- "rewrite error messages", "fix error messages", "improve error messages"
- "bad error message", "this error is confusing", "make errors clearer"
- "error message audit", "audit my errors", "review error strings"
- "write better errors", "improve UX of errors"
- "/error-writer"

---

## How to Provide Input

```
# Option 1: Paste error strings directly
/error-writer
"Something went wrong"
"Invalid input"
"Error: 500"
"Cannot read property 'id' of undefined"

# Option 2: Paste a code file with error messages
/error-writer
[paste errors.ts / errors.py / constants.js etc.]

# Option 3: Provide file path
/error-writer src/errors.ts

# Option 4: Specify audience
/error-writer --audience end-user
"User not found in database at line 42 of UserService.java"

# Option 5: Full audit mode
/error-writer --audit src/
(scans all source files for error message patterns)
```

---

## Step 1: Classify Each Error Message

Before rewriting, classify every error by two dimensions:

### Dimension 1: Audience

| Audience | Who Reads It | Channel |
|----------|-------------|---------|
| **End user** | Non-technical: customer, student, patient | UI toast, modal, page text |
| **Developer** | Integrating your API | API response body, SDK exception |
| **Ops/SRE** | Running your service | Server logs, monitoring alerts |
| **Internal dev** | Debugging locally | Console, test output |

### Dimension 2: Error Category

| Category | Examples | What the message needs |
|----------|---------|----------------------|
| **Validation** | Bad input format, missing required field | What field, what's wrong, what format is expected |
| **Auth/Permission** | Unauthorized, forbidden | What was attempted, what permission is needed |
| **Not Found** | Missing resource | What resource, what ID, what to check |
| **Rate Limit** | Too many requests | Limit, window, when to retry |
| **Upstream/Dependency** | Third-party service down | Which service, whether it's transient, what to do |
| **Internal/Bug** | Unexpected server error | User: reassurance + reference ID. Dev: full context |
| **Conflict** | Duplicate resource, state mismatch | What already exists, how to resolve |
| **Timeout** | Request too slow | What timed out, suggested next action |

---

## Step 2: Audit for Anti-Patterns

Flag every error message that matches these patterns:

### 🔴 Critical Anti-Patterns

**1. Vague Generics** — Tells the reader nothing actionable
```
❌ "Something went wrong"
❌ "An error occurred"
❌ "Operation failed"
❌ "Invalid request"
❌ "Error 500"
❌ "Unexpected error"
```

**2. Leaked Internals** — Internal details visible to end users
```
❌ "NullPointerException at UserService.java:42"
❌ "Error: Cannot read property 'id' of undefined"
❌ "SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry"
❌ "Connection refused: 127.0.0.1:5432"
❌ Stack traces in API responses
```

**3. Wrong Audience** — Developer speak in end-user messages
```
❌ "JWT token expired" (end-user message)
❌ "Invalid UUID format" (end-user message)
❌ "HTTP 422 Unprocessable Entity" (end-user message)
❌ "Database constraint violation" (end-user message)
```

**4. Missing Context** — No information about what went wrong or what to do
```
❌ "Email invalid" — which email? what format is valid?
❌ "Not found" — what wasn't found?
❌ "Access denied" — what requires access? how to get it?
❌ "Please try again" — when? how many times? is it transient?
```

### 🟠 High Anti-Patterns

**5. Fear-inducing language** — Overstates severity for end users
```
❌ "FATAL ERROR: system failure"
❌ "CRITICAL: data corruption detected"
❌ "WARNING: your account may be compromised"
   (when it's just a session timeout)
```

**6. Blame language** — Implicit or explicit blame
```
❌ "You provided an invalid email address" → "The email address doesn't match the expected format"
❌ "You must be logged in" → "Sign in to continue"
❌ "User error: ..." → just describe what happened
```

**7. No recovery path** — Error with no next step
```
❌ "Payment declined." (end)
   Better: "Payment declined. Check that your card number and expiry date are correct, then try again."
```

### 🟡 Medium Anti-Patterns

**8. Inconsistent capitalization/punctuation**
```
❌ Mix of: "Email is required." / "password required" / "Phone Required!"
```

**9. All-caps for non-critical errors**
```
❌ "ERROR: EMAIL NOT FOUND"
```

**10. Numeric codes without explanation**
```
❌ "Error code: 10042" with no description
```

---

## Step 3: Rewrite Each Message

Apply the **3-part formula** to every error:

```
[What happened] + [Why it happened] + [What to do next]
```

### Rules by Output Channel

#### UI / End-User Facing
- Plain language, no technical terms
- Short: 1-2 sentences max
- Reassuring tone — not scary
- Clear next action in the same sentence or as a button label
- Never expose: exception names, file paths, line numbers, SQL, IDs

#### API Response Body (for developer integrating your API)
- Include: `error` (machine-readable code), `message` (human-readable), `details` (optional array)
- Machine-readable codes should be `SCREAMING_SNAKE_CASE`
- Include: request ID for tracing, documentation link if complex
- Can include: field names, constraint names, allowed values

```json
{
  "error": "VALIDATION_ERROR",
  "message": "The request body contains invalid fields.",
  "details": [
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "Must be a valid email address (e.g., user@example.com)"
    },
    {
      "field": "age",
      "code": "OUT_OF_RANGE",
      "message": "Must be between 13 and 120"
    }
  ],
  "request_id": "req_7f3a9b"
}
```

#### Server Logs / Ops
- Include ALL context: user ID, request ID, timestamp, trace ID
- Include exception type and stack trace
- Structured (JSON) preferred
- No sanitization — ops team needs raw details

```json
{
  "level": "error",
  "timestamp": "2026-03-18T10:42:00Z",
  "message": "Payment processing failed",
  "error_type": "StripeConnectionError",
  "user_id": "usr_abc123",
  "request_id": "req_7f3a9b",
  "stripe_error_code": "connection_error",
  "retry_count": 3,
  "stack": "..."
}
```

---

## Step 4: Output Report

```markdown
## Error Writer Report
Input: [N] error messages analyzed | [M] anti-patterns found

### Audit Summary

| Severity | Count | Category |
|----------|-------|---------|
| 🔴 Critical | 4 | Vague generics (3), Leaked internals (1) |
| 🟠 High | 2 | Missing recovery path (2) |
| 🟡 Medium | 1 | Inconsistent formatting (1) |

---

### Rewrites

---

**❌ BEFORE:** `"Something went wrong"`
**Category:** Validation | **Audience:** End user | **Anti-pattern:** Vague generic

**✅ AFTER:**

*UI message:*
> "We couldn't save your changes. Check that all required fields are filled in and try again."

*API response:*
```json
{
  "error": "SAVE_FAILED",
  "message": "Unable to save changes. Ensure all required fields are populated.",
  "request_id": "req_{{id}}"
}
```

*Log entry:*
```
ERROR [UserService.save] Failed to persist user update | user_id={{id}} | validation_errors={{errors}} | request_id={{id}}
```

---

**❌ BEFORE:** `"Cannot read property 'id' of undefined"`
**Category:** Internal bug | **Audience:** Leaked to end user | **Anti-pattern:** Leaked internals

**✅ AFTER:**

*UI message (what the user sees):*
> "Something unexpected happened on our end. Your data is safe. Please try again or contact support if this persists. [Reference: {{request_id}}]"

*Ops log (what engineers see):*
```
ERROR [UserController.getUser] Null reference: user object was undefined when accessing .id
Expected: User object from DB lookup
Got: undefined (possible cache miss or deleted user)
user_id_param={{param}} | request_id={{id}} | stack={{trace}}
```

*Action required:* Add null check before accessing `.id`. Investigate why DB lookup returned undefined for valid-format ID.

---

**❌ BEFORE:** `"Invalid input"`
**Category:** Validation | **Anti-pattern:** Missing context + Vague

**✅ AFTER:**

*UI:* "Please check the highlighted fields — some information is missing or in the wrong format."

*API:*
```json
{
  "error": "VALIDATION_ERROR",
  "message": "One or more input fields are invalid.",
  "details": [
    {"field": "{{field_name}}", "message": "{{specific constraint}}"}
  ]
}
```

*Log:* `WARN [Validator] Input validation failed | fields={{fields}} | rules_violated={{rules}} | request_id={{id}}`

---

### Copy-Paste Constants File

```typescript
// errors.ts — generated by phy-error-writer
export const Errors = {
  SAVE_FAILED: {
    code: "SAVE_FAILED",
    ui: "We couldn't save your changes. Check that all required fields are filled in and try again.",
    log: "Failed to persist entity update",
  },
  VALIDATION_ERROR: {
    code: "VALIDATION_ERROR",
    ui: "Please check the highlighted fields — some information is missing or in the wrong format.",
    log: "Input validation failed",
  },
  INTERNAL_ERROR: {
    code: "INTERNAL_ERROR",
    ui: "Something unexpected happened on our end. Your data is safe — please try again or contact support.",
    log: "Unhandled internal error",
  },
} as const;
```

---

### Error Message Style Guide (project-specific, generated)

Based on the messages analyzed, your project should follow these conventions:
- Sentence case, ending with a period
- End-user messages: present tense, active voice, no technical terms
- Include recovery action in every end-user message
- API error codes: SCREAMING_SNAKE_CASE
- Log entries: include request_id and user_id as structured fields on every error
```

---

## Quick Mode

For a single error message:

```
Input: "User not found in database at UserService.java:42"

Quick Rewrite:
UI: "We couldn't find your account. Double-check your email address, or sign up if you're new."
API: {"error": "USER_NOT_FOUND", "message": "No account found with that identifier."}
Log: ERROR [UserService] User lookup returned null | query_param={{id}} | request_id={{id}}

Anti-patterns fixed: Leaked internals (Java file path), Wrong audience (database mention)
```

---

## Why This Matters

A study of developer productivity found that **unclear error messages are the #1 cause of unnecessary support tickets** and the **#2 cause of debugging time wasted** (after missing logs). For an API, bad error messages mean:

- Integrators file support tickets for things they could self-serve
- Developers spend hours on errors that a good message would resolve in minutes
- Security information leaks via stack traces in production responses
- End users abandon flows that could be recovered with a clear next step

This skill turns error message improvement from a "someday" task into a 5-minute audit.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
