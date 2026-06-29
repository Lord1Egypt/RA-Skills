# OpenAPI Docs Generator

## What It Does

Generate, repair, and validate OpenAPI or Swagger documentation for REST APIs from routes, handlers, schemas, examples, and observed behavior.

This package was generated from demand signals in run `20260623-040526` and then rewritten for publication with domain-specific workflow guidance instead of generic task scaffolding.

## Best For

Backend engineers, platform teams, sdk maintainers, and developer-experience teams responsible for accurate rest api documentation.

## Workflow Summary

1. Inventory base URLs, auth, routes, controllers, schema validators, request samples, response samples, and existing OpenAPI fragments.
2. Map each operation to method, path, parameters, request body, responses, errors, auth, idempotency, pagination, and rate limits.
3. Draft or patch the OpenAPI document with reusable components for schemas, security schemes, errors, and shared parameters.
4. Add realistic examples that match production constraints while redacting secrets and customer data.
5. Validate with an OpenAPI parser or linter, then note contract mismatches that require code or docs changes.
6. Return the spec changes, validation command, and follow-up tasks for SDK generation, docs publishing, or CI enforcement.

## Deliverables

- A new or patched OpenAPI YAML/JSON fragment.
- Endpoint-by-endpoint documentation gaps and proposed fixes.
- Validation commands for linting, bundling, SDK generation, or contract tests.
- Examples for success, validation failure, authorization failure, and rate limits.

## Quality Bar

- Every operation has method, path, auth, parameters, request body, responses, and examples where relevant.
- Schemas reuse components instead of duplicating incompatible shapes.
- The spec is parseable by standard OpenAPI tooling and does not include secrets.
- Known implementation/spec drift is called out clearly.

## Trigger Examples

- `Use $openapi-docs-generator to create an OpenAPI spec from these Express routes.`
- `Patch this Swagger file so it matches the handler responses.`
- `Review our API docs for missing schemas and examples.`

## Files

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing guide.
- `README.zh-CN.md`: Chinese user-facing guide.
- `references/requirement-plan.md`: Demand evidence and scoring details.
- `agents/openai.yaml`: Default invocation metadata.
