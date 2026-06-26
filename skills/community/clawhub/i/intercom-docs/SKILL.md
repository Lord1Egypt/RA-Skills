---
name: intercom
description: Create, update, improve, and review Intercom help-center and support documentation. Use when writing new Intercom articles, revising existing docs, auditing a help center for gaps, turning product or codebase context into customer-facing documentation, or working with Intercom workspace content via the Intercom API using a private workspace access token.
---

# intercom

Create and maintain Intercom documentation that is clear, accurate, concise, and useful.

## Scope

Use this skill for:
- drafting new Intercom help articles
- improving existing articles for clarity, structure, and consistency
- converting product, support, and codebase knowledge into user-facing documentation
- reviewing documentation gaps, duplication, stale content, and missing troubleshooting guidance
- interacting with Intercom workspace content via the Intercom API when a private workspace access token is available

## Core workflow

1. Identify the audience: end user, admin, internal support, or mixed.
2. Confirm the source of truth: product behavior, code, support knowledge, screenshots, existing docs, or direct guidance.
3. State uncertainty clearly instead of inventing behavior.
4. Prefer improving existing documentation over creating duplicates.
5. Write for task completion first: strong headings, short paragraphs, numbered steps, concise troubleshooting.
6. If an Intercom API token is available, inspect current content before proposing replacements.

## Writing rules

- Write for someone trying to complete a task quickly.
- Prefer concrete steps over abstract explanation.
- Use simple language and avoid marketing fluff.
- Keep terminology consistent with the product UI and existing docs.
- Call out prerequisites, permissions, limitations, and common failure cases.
- If behavior is inferred from code, mark it as needing verification when appropriate.
- Default to short, scannable sections rather than dense prose.

## Recommended article structure

Use this structure when it fits:

1. Title
2. Short summary of what the article helps with
3. Who this is for / prerequisites
4. Step-by-step instructions
5. Expected result
6. Troubleshooting / common issues
7. Related articles or next steps

## Review checklist

When reviewing an existing Intercom article or help center area, check for:
- outdated UI labels or navigation paths
- unclear audience or prerequisites
- missing permissions/role requirements
- missing edge cases or limitations
- weak troubleshooting coverage
- duplicate or overlapping articles
- inconsistent terminology across related docs
- too much implementation detail for end users

## Common doc tasks

### Draft a new article

When asked to create a new Intercom doc:
- define the user problem the article solves
- choose a clear task-based title
- write only the context needed to complete the task
- include exact steps and expected outcomes
- add edge cases and troubleshooting when relevant

### Update an existing article

When asked to revise docs:
- preserve the original intent if still valid
- remove stale steps and outdated UI references
- tighten wording and improve scanability
- keep terminology and formatting consistent with neighboring docs
- note any product ambiguity that should be verified

### Turn code/product context into docs

When the source material is code, tickets, or notes:
- extract actual user-visible behavior
- ignore implementation detail unless it affects setup, troubleshooting, limits, or expected outcomes
- translate technical behavior into user-facing language
- separate confirmed behavior from assumptions

### Gap review

When reviewing an Intercom knowledge base:
- identify missing onboarding docs
- identify missing troubleshooting articles
- identify duplicate or overlapping articles
- identify confusing naming or inconsistent terminology
- suggest the smallest useful set of changes first

## Intercom API usage

Use the Intercom API only when an access token for the user's own workspace is available.

### Authentication

Intercom private workspace access uses a bearer token in the Authorization header.

Example:

```bash
curl -s https://api.intercom.io/help_center/collections \
  -H 'Authorization: Bearer <access_token>' \
  -H 'Accept: application/json'
```

Notes:
- Treat the access token like a password.
- Do not write the token into docs, commits, or skill files.
- Prefer read-only inspection first, then propose changes before writing.
- For public third-party apps, Intercom expects OAuth rather than asking users for access tokens.

### API-first doc review workflow

If an Intercom access token is available:

1. List current help-center collections and articles.
2. Sample the relevant article bodies before rewriting.
3. Identify stale content, overlap, and missing coverage.
4. Draft the improved content.
5. Show the proposed delta clearly before applying changes unless the user explicitly asks for direct updates.

### Minimum output when reviewing live Intercom docs

Provide:
- article or collection reviewed
- what is working
- what is unclear/outdated/missing
- proposed improved title if needed
- proposed revised body
- assumptions / items to verify

## Output preference

Unless asked otherwise, provide:
- a suggested article title
- the article body in publishable markdown/plain text
- a short review summary
- a short note listing assumptions or items to verify
