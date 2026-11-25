---
name: maverick-docusign-mcp
description: Read DocuSign accounts, envelopes, recipients, templates, and signing status, and create, send, update, void, or remind on signature envelopes through DocuSign's official developer MCP server. Use when the user asks to inspect or manage DocuSign signing workflows.
metadata:
  openclaw:
    emoji: '✍️'
    homepage: https://developers.docusign.com/platform/mcp-server/
    requires:
      bins:
        - mcporter
      env:
        - MAVERICK_DOCUSIGN_MCP_ACCESS_TOKEN
        - MAVERICK_DOCUSIGN_MCP_REFRESH_TOKEN
        - MAVERICK_DOCUSIGN_MCP_CLIENT_ID
        - MAVERICK_DOCUSIGN_MCP_CLIENT_SECRET
    primaryEnv: MAVERICK_DOCUSIGN_MCP_REFRESH_TOKEN
    setup:
      script: scripts/setup.sh
    install:
      - id: node
        kind: node
        package: mcporter@0.16.1
        bins:
          - mcporter
        label: Install mcporter (node)
---

# DocuSign

## How to use this skill

This skill is a thin pass-through to DocuSign's official developer MCP server at `https://mcp-d.docusign.com/mcp`. The bundle exposes a bounded set of eSignature read and write tools. The live server remains the source of truth for their current schemas and server-published instructions.

Discover the live tool schemas with Maverick's managed tool before calling a tool:

```json
{ "provider": "docusign" }
```

Pass that input to `list_integration_tools`. Read the returned schemas and server instructions, then use `call_integration_tool` with the exact discovered tool name and JSON arguments:

```json
{ "provider": "docusign", "tool": "getUserInfo", "args": {} }
```

Use the managed tools for connection-health checks, credential isolation, and reconnect recovery. Do not run mcporter in a shell or start an OAuth flow yourself. Deferred tool schemas can be found with `tool_search` and `tool_describe`.

The allowed tools are exactly:

- `getUserInfo`
- `getAccount`
- `getEnvelopes`
- `getEnvelope`
- `listRecipients`
- `getTemplates`
- `getEnvelopeVsAgreementSkill`
- `listEnvelopeDocuments`
- `createEnvelope`
- `resolveEnvelopeSendMethod`
- `updateEnvelope`
- `updateEnvelopeRecipients`
- `updateEnvelopeTabs`
- `sendReminder`

## Authorized writes

Carry out the user's clear request when the envelope or template, recipients, content, and intended change are known. Their request authorizes that action: do not add a confirmation step or stop at a draft when they asked you to send. Reuse authorization in the conversation or scheduled job instructions. Ask only for missing essentials or a materially changed action. A request to prepare a draft authorizes a draft only; never send it without an instruction to send.

For templates, read the discovered `resolveEnvelopeSendMethod` schema and its workflow instructions, then use the template the user selected. This helper provides orchestration guidance; it does not itself prove that an envelope was created or sent. Follow the live `getTemplates` and `createEnvelope` schemas for the selected template and recipients. Never substitute a different template. For a draft-only request, use the discovered draft status (`created`), stop before any send step, and verify the saved envelope remains a draft. When the user asked you to send, complete the send and verify the resulting status.

For documents, follow the discovered `createEnvelope` schema. Use inline document content only if that schema supports it. If it requires a publicly reachable HTTPS URL, use only an already-approved URL; never publish a private attachment to make it reachable. If the available tools cannot accept the user's private attachment, explain the limitation and use an authorized existing template or approved URL. The separate `createEnvelopeWithDocuments` MCP App upload widget is outside this integration; do not try to invoke it through another configuration.

Read envelope status, documents, and recipients before updating or voiding it. Inspect pending recipients before sending reminders. Use `listEnvelopeDocuments` and `updateEnvelopeTabs` only when live discovery exposes them; inspect the document or recipient fields before changing tabs.

After a timeout or ambiguous provider result, inspect the envelope before attempting another write. Never automatically replay a send, reminder, or other potentially completed write.

## Tool and scope boundary

The `allowedTools` list in `mcporter.json` permits only the tools above. Agreement Manager, Maestro, CLM, account administration, and Data Verification app installation are outside this integration. Do not bypass the allowlist with direct API calls or another MCP configuration, including when provider guidance mentions an excluded tool.

This release requests the eSignature `signature` OAuth scope for both reads and writes, plus `extended` so each successful refresh renews the refresh token's lifetime. It does not request Agreement Manager or workflow scopes. A connected DocuSign user's account permissions still govern which writes the provider accepts.

## Authentication

Credentials are provisioned at setup time by `scripts/setup.sh` (a thin delegator to `scripts/init-mcporter-oauth.sh`) and stored in mcporter's local vault. The setup hook requires these credential env vars:

- `MAVERICK_DOCUSIGN_MCP_REFRESH_TOKEN`
- `MAVERICK_DOCUSIGN_MCP_CLIENT_ID`
- `MAVERICK_DOCUSIGN_MCP_CLIENT_SECRET`
- `MAVERICK_DOCUSIGN_MCP_ACCESS_TOKEN`

For refresh-aware seeding, setup also reads optional expiry metadata env vars when the provisioner supplies them:

- `MAVERICK_DOCUSIGN_MCP_EXPIRES_AT`
- `MAVERICK_DOCUSIGN_MCP_EXPIRES_IN`
- `MAVERICK_DOCUSIGN_MCP_REFRESH_TOKEN_EXPIRES_AT`

mcporter sends the refreshed bearer token to DocuSign's hosted MCP server and refreshes expired access tokens through DocuSign's demo token endpoint. Access-token expiry normally refreshes automatically. Follow the managed tool's structured result: request reconnection only when it reports `reauthorization-required`; a timeout, network failure, or provider outage does not prove that authorization ended.

## Data flow

Tool arguments and results travel over HTTPS to DocuSign's hosted developer MCP server. DocuSign sees the account, envelope, recipient, template, and signing-status data referenced by each call. Use this skill only with a DocuSign developer/demo account and do not pass unrelated sensitive content through these tools. Production endpoint promotion is outside this bundle's scope.

## Dependencies

- **`mcporter`** ([github.com/openclaw/mcporter](https://github.com/openclaw/mcporter)) — MCP CLI used to discover and call the hosted MCP server. If it is missing from `PATH`, the frontmatter installs the exact `mcporter@0.16.1` package with npm install scripts disabled.

## References

- DocuSign MCP overview: <https://developers.docusign.com/platform/mcp-server/>
- DocuSign developer MCP endpoint: <https://mcp-d.docusign.com/mcp>
