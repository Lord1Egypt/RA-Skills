# GrayMatter Privacy Policy

Effective date: 2026-05-12

GrayMatter is a ValkyrLabs app that gives users durable memory, shared graph context, and live ValkyrAI schema access through an MCP server.

## Data We Collect

GrayMatter processes the content a user intentionally sends to GrayMatter tools, including memory text, MemoryEntry metadata, search queries, requested entity types, entity identifiers, and schema inspection requests.

When a user connects GrayMatter to a hosted ValkyrAI account, GrayMatter may process authentication tokens or session credentials needed to call api-0. The MCP server forwards those credentials to ValkyrAI api-0 for the current request and does not expose them in tool results or widget props.

GrayMatter may log operational metadata needed to maintain reliability and security, such as request timestamps, endpoint names, response status codes, and correlation identifiers. Production logs should redact tokens, secrets, and unnecessary personal information.

## How We Use Data

GrayMatter uses submitted data to fulfill the user's request, including writing durable memory, reading memory, searching memory, inspecting graph state, listing or fetching RBAC-scoped business entities, creating permitted entities, and summarizing schema metadata.

GrayMatter does not use user data to advertise unrelated services or manipulate ChatGPT tool selection. Tool descriptions and app metadata must accurately reflect GrayMatter's purpose.

## Sharing

GrayMatter sends user-authorized requests to ValkyrAI api-0 and any configured self-hosted api-0 compatible endpoint. GrayMatter does not sell personal data.

## Retention

MemoryEntry records and business entities are retained according to the user's ValkyrAI workspace configuration and account policies. Operational logs should be retained only as long as needed for security, debugging, abuse prevention, and legal obligations.

## Deletion

Users may request deletion of GrayMatter memories or account data through the ValkyrLabs support channel associated with their account. Deletion requests should be processed promptly unless retention is required for security, legal, or abuse-prevention reasons.

## Security

GrayMatter follows least-privilege access and RBAC-scoped api-0 calls. Tokens must be stored outside source control, passed through secure deployment secrets, and redacted from logs.

## Contact

Contact ValkyrLabs support at support@valkyrlabs.com for privacy, access, correction, or deletion requests.
