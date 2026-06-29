---
name: openapi-docs-generator
description: >-
  Generate, repair, and validate OpenAPI or Swagger documentation for REST APIs from routes, handlers, schemas, examples, and observed behavior. Use when a user asks for OpenAPI, Swagger, REST API, API docs, schema, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# OpenAPI Docs Generator

## Purpose

Use this skill when an API lacks an OpenAPI spec, the current spec drifts from implementation, examples are missing, or docs fail downstream SDK, gateway, or contract-test tooling.

Audience: backend engineers, platform teams, SDK maintainers, and developer-experience teams responsible for accurate REST API documentation.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Inventory base URLs, auth, routes, controllers, schema validators, request samples, response samples, and existing OpenAPI fragments.
2. Map each operation to method, path, parameters, request body, responses, errors, auth, idempotency, pagination, and rate limits.
3. Draft or patch the OpenAPI document with reusable components for schemas, security schemes, errors, and shared parameters.
4. Add realistic examples that match production constraints while redacting secrets and customer data.
5. Validate with an OpenAPI parser or linter, then note contract mismatches that require code or docs changes.
6. Return the spec changes, validation command, and follow-up tasks for SDK generation, docs publishing, or CI enforcement.

## Expected Outputs

- A new or patched OpenAPI YAML/JSON fragment.
- Endpoint-by-endpoint documentation gaps and proposed fixes.
- Validation commands for linting, bundling, SDK generation, or contract tests.
- Examples for success, validation failure, authorization failure, and rate limits.

## Validation

- Every operation has method, path, auth, parameters, request body, responses, and examples where relevant.
- Schemas reuse components instead of duplicating incompatible shapes.
- The spec is parseable by standard OpenAPI tooling and does not include secrets.
- Known implementation/spec drift is called out clearly.

## Triggers

Keywords: `OpenAPI`, `Swagger`, `REST API`, `API docs`, `schema`, `SDK`, `contract testing`

Example trigger sentences:

- `Use $openapi-docs-generator to create an OpenAPI spec from these Express routes.`
- `Patch this Swagger file so it matches the handler responses.`
- `Review our API docs for missing schemas and examples.`
