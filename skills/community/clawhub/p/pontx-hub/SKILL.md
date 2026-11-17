---
name: pontx-hub
description: Discover, compare, inspect, preview, call, and integrate curated public APIs with Pontx Hub. Use whenever a user asks to find a public API for a task, identify which Endpoint or Schema returns a field, inspect PontxSpec or OpenAPI documentation, install provider-specific Skills, preview a request safely, confirm a mutation, or generate code with a published Pontx SDK.
---

# Pontx Hub

Use `pontx-hub` as the authoritative interface to the curated API catalog. Keep
API metadata out of long-lived context by searching and loading only the
product, endpoint, or schema needed for the current task.

This universal Skill owns catalog-wide discovery and request safety. A
`pontx-<apiSlug>` product Skill adds only provider-specific integration flows,
best practices, and caveats; it does not replace the current PontxSpec.

## Workflow

1. Search before choosing an API. Natural-language capability, request, and
   response questions are supported:

   ```bash
   pontx-hub search "<capability>" --json
   pontx-hub search "创建任务的入参" --locale zh --json
   pontx-hub search "返回 dueDate 的接口" --locale zh --json
   ```

   Narrow the result type when useful:

   ```bash
   pontx-hub search "<field-or-model>" --type schema --json
   ```

2. Inspect the selected stable resource ID:

   ```bash
   pontx-hub show endpoint:<api>/<endpoint>
   pontx-hub show schema:<api>/<schema>
   ```

3. When provider-specific guidance would help, check the available product
   Skills. Explain the benefit and install one only when the user requests or
   approves the installation:

   ```bash
   pontx-hub skill list
   pontx-hub skill install <apiSlug>
   ```

   Use that product Skill for provider-specific sequencing and caveats, then
   return to `pontx-hub show` for current Endpoint, Schema, and auth details.

4. For an Endpoint, build and review the exact request without sending it:

   ```bash
   pontx-hub <api-collection> preview <api-name> --parameter value --body '<json>'
   pontx-hub <api-collection> preview <controller> <api-name> --parameter value --body '<json>'
   ```

5. For GET or HEAD, call only when the user requested execution:

   ```bash
   pontx-hub <api-collection> call <api-name> --parameter value
   pontx-hub <api-collection> call <controller> <api-name> --parameter value
   ```

6. For POST, PUT, PATCH, or DELETE, show the dry-run result and obtain explicit
   user confirmation. Then pass `--yes` without changing parameters:

   ```bash
   pontx-hub <api-collection> call <controller> <api-name> --parameter value --body '<json>' --yes
   ```

7. Generate application code after the request shape is verified. Use the
   package and exports reported by the Hub instead of inventing a package or
   pinning a stale version:

   ```bash
   pontx-hub sdk <api>
   pnpm add @pontx/<apiSlug>
   ```

## Safety

- Never infer approval for a write from a request to inspect, explain, or
  preview an API.
- Never print, echo, log, or place credentials directly in command arguments.
- Read credentials from the environment variables named by `show`.
- Never call an arbitrary URL or an Endpoint outside the Hub catalog.
- Never treat a product Skill as the source for Endpoint, parameter, Schema,
  authentication, package-version, or server metadata; inspect the current
  PontxSpec through the Hub.
- Never bypass the separate `preview` step for a mutation.
- Treat a changed parameter, body, server, or Endpoint as a new request that
  requires another dry-run and confirmation.
- Read [references/auth-and-safety.md](references/auth-and-safety.md) when
  configuring credentials, diagnosing authentication, or executing a mutation.

## Output

Prefer `--json` when consuming CLI output programmatically. Preserve the CLI
exit code and machine-readable error code when reporting failures. Use the
result's `match.mode` and `match.fields` to explain whether product, parameter,
request, response, schema, or property metadata produced the match. Use the
Endpoint's published `@pontx/<apiSlug>` package when generating application
code.
