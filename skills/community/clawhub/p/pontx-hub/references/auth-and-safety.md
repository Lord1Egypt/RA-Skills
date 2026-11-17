# Authentication and mutation safety

## Credentials

The Hub catalog declares the environment variable expected by each API. Set the
secret in the user's shell or secret manager before calling the CLI. Do not
write the value into source files, generated examples, chat messages, or CLI
arguments.

Supported v1 schemes:

- API Key in an approved header or query parameter
- Bearer token
- Existing OAuth2 access token
- Basic Auth credentials

The Web Playground can run approved OAuth 2.0 Authorization Code/PKCE and
Client Credentials flows declared by the catalog. Browser access and refresh
tokens stay in session storage; client secrets are used only for the current
exchange and are never persisted by Hub. The CLI and Agent Skill still accept
only an existing access token from the declared environment variable and never
collect client secrets.

## Mutations

POST, PUT, PATCH, and DELETE are mutations even when their names sound
read-only. Always:

1. Inspect the Endpoint metadata in the current PontxSpec.
2. Run `pontx-hub <api-collection> preview [controller] <api-name>`.
3. Present the resolved method, host, path, query, redacted headers, and body.
4. State the expected side effect.
5. Ask the user to confirm that exact request.
6. Run the unchanged request with `pontx-hub <api-collection> call [controller] <api-name> --yes`.

If confirmation is missing, ambiguous, or applies to different parameters, stop
without sending the request.
