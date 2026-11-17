# GoDaddy CLI, MCP, and agent platform

Verified 2026-09-05 using the checksum-verified official gddy v0.2.12 release, its default and experimental command trees, API catalog, and the public Domains MCP handshake. Re-run discovery when using a newer release. Coverage here means workflow guidance, not that every product is enabled on the user's account.

## Select the surface

| Task | Surface |
| --- | --- |
| Public domain search and availability | Public Domains MCP, or gddy domain |
| Account domains, quotes, purchase, DNS, nameservers | Authenticated gddy domain / dns |
| Commerce stores, catalogs, orders, payments, taxes, subscriptions | gddy api REST/GraphQL catalog; inspect operation scopes and schemas |
| Node.js apps, source, jobs, deployments, secrets, logs | Beta gddy hosting nodejs |
| Mailbox list/get/create/eligibility | Beta gddy email |
| Platform apps, extensions, actions, subscriptions, releases | Experimental gddy platform |
| Agent identity, discovery, verification, certificates, events | ANS official REST reference and SDKs |

## Official agent integrations

Source: https://github.com/godaddy/cli

The official CLI skill can also be installed for a supported agent:

```bash
npx skills add godaddy/cli --skill gddy --agent <agent>
```

Claude Code integration:

```bash
claude plugin marketplace add godaddy/cli
claude plugin install gddy@godaddy
```

These are optional host installations. Choose the user's actual agent and inspect installer help before changing host configuration. The older TypeScript `godaddy` CLI lives on the repository's `original` branch; do not mix its command syntax with gddy.

## Public Domains MCP

Documentation: https://developer.godaddy.com/en/docs/api-users/mcp

Configure the host's Streamable HTTP MCP connection using this documented example; adapt transport syntax to that host:

```json
{
  "mcpServers": {
    "godaddy": {
      "url": "https://api.godaddy.com/v1/domains/mcp",
      "transport": "streamable-http"
    }
  }
}
```

No authentication is needed or accepted for account access. Initialize the connection and discover tools with tools/list; inspect their actual input schemas. The server is read-only public discovery, not DNS editing, purchase, transfer, or account administration. Route those operations to gddy. Recheck availability before buying.

The former godaddy/ai and godaddy/commerce-agent-plugin GitHub URLs returned 404 during this release audit. Do not install them or infer a working Commerce MCP endpoint from stale search snippets. Use the current authenticated Commerce CLI/API catalog until an accessible official MCP contract is verified.

## Complete CLI discovery, including staged features

```bash
gddy --version
gddy tree
gddy guide
gddy flags list
gddy api domain list
GDDY_MIN_STAGE=beta gddy tree
GDDY_MIN_STAGE=experimental gddy tree
```

Use the minimum stage required by the requested feature and keep the environment variable scoped to that command. Stage visibility does not grant account access. Inspect command --help before execution; a listed command is not proof the remote service is enabled.

The v0.2.12 tree covers auth, API/schema/GraphQL discovery and calls, DNS, domains, environments, PATs, payment setup, updates, flags, guides, search, and completion. Beta adds Email and Hosting; experimental adds Platform.

### Hosting and Email

```bash
GDDY_MIN_STAGE=beta gddy hosting nodejs --help
GDDY_MIN_STAGE=beta gddy email --help
```

Hosting groups: app list/get/create/update/delete; creation job get; source upload/status and git/git-status; GitHub status/repos/branches; deployment list/publish; secrets list/update; status and logs. Follow create → poll job → upload/import → poll source → inspect preview → publish when requested → verify live status. Keep secret values out of output. Preserve preview versus live distinction.

Email supports list, get, create, and check-eligibility. Inspect eligibility and the creation contract before provisioning a mailbox; confirm any price/account effect from the current response.

### Platform apps (experimental)

```bash
GDDY_MIN_STAGE=experimental gddy platform app --help
GDDY_MIN_STAGE=experimental gddy platform actions --help
GDDY_MIN_STAGE=experimental gddy platform webhook --help
```

App commands cover init, list, info, update, local config validate, remote validate, enable/disable, archive, release, and deploy. Manifest additions include embed/checkout/blocks extensions, actions, webhook subscriptions, and settings. Discover action contracts with actions list/describe and event types with webhook events. Validate godaddy.toml locally and remote state before releasing; inspect deploy progress and resulting state. Do not equate local manifest edits with a deployed or store-enabled app.

## Agent Name Service (ANS)

Start with https://developer.godaddy.com/en/docs/references/rest/ans/registration and the official reference navigation for resolution, search, validation, agents, certificate management, events, and revocation. The open-source implementation and SDK links live at https://github.com/agentnameservice/ans.

ANS concerns agent names, identity certificates, domain ownership, discovery, and verifiable lifecycle history. It is separate from installing an agent skill or connecting the Domains MCP. Use the exact production authentication and schema for the chosen API/SDK; do not assume a Domains PAT or local development API key is accepted. Keep private keys local, send only required CSRs/public material, complete returned DNS/ACME challenges, then verify registry/certificate status. A submitted registration is not a verified identity. Never promote local demo defaults, no-op DNS verification, or development keys to production.

## Coverage limits

The CLI catalog currently exposes 22 API domains including Commerce and Hosting, but it is not every GoDaddy REST API. For Certificates, Aftermarket, Shoppers, Agreements, Countries, Abuse, Parking, or ANS absent from that catalog, open https://developer.godaddy.com/en/docs/references/rest and inspect the exact current contract. An empty CLI search is not proof the product has no API. Do not invent paths or reuse the obsolete custom MCP server from skill v1.
