---
name: ipfs-content-gateway
description: "IPFS Content Gateway: Fetch content from IPFS by CID with automatic failover across 7 gateways. Upload files up to 10MB with pinning. List upload history. Use when an agent needs ipfs content gateway, ipfs content retrieval, decentralized storage access, cid content lookup, ipfs gateway access, list, retrieve, cid through AgentPMT-hosted remote tool calls. Discovery terms: ipfs content gateway, ipfs content retrieval, decentralized storage access, cid content lookup, ipfs gateway access, list."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/ipfs-content-gateway
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/ipfs-content-gateway"}}
---
# IPFS Content Gateway

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
IPFS Content Gateway provides access to the InterPlanetary File System, a decentralized peer-to-peer network for storing and sharing content using content-addressed identifiers. The retrieval function fetches data from IPFS by CID (Content Identifier) with automatic failover across seven public gateways including ipfs.io, Cloudflare IPFS, and Pinata, ensuring high availability even when individual gateways are slow or unavailable. Content retrieval automatically detects whether the response is text or binary data and returns appropriate previews with full metadata including content type, size, and response headers. The upload function accepts base64-encoded files up to 10MB and pins them to IPFS through pinning services that ensure content remains available on the network. Users can provide their own API credentials for Pinata, Web3.Storage, or NFT.Storage, or use shared infrastructure for convenience. Each upload returns the permanent CID along with multiple gateway URLs for immediate access. The list function provides a complete history of uploads including filenames, sizes, upload dates, and ready-to-use gateway links, with aggregate statistics on total storage used.

## Product Instructions
### IPFS Content Gateway

Store and retrieve files on the InterPlanetary File System (IPFS) -- a decentralized, content-addressed storage network. Upload files up to 10MB, retrieve content by CID, and list your upload history.

#### Actions

##### retrieve

Fetch content from IPFS by its Content Identifier (CID). Supports both CIDv0 (`Qm...`) and CIDv1 (`bafy...`) formats. Multiple gateways are tried automatically for reliability.

**Required fields:**
- `action` — `"retrieve"`
- `cid` — The IPFS Content Identifier to retrieve

**Example:**
```json
{
  "action": "retrieve",
  "cid": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG"
}
```

**Response includes:** content (text preview up to 10,000 chars or binary indicator), content_type, content_length, gateway_url, and ipfs_url.

---

##### upload

Upload a file to IPFS. The file is pinned so it remains available on the network. Maximum file size is 10MB.

**Required fields:**
- `action` — `"upload"`
- `content` — Base64-encoded file content
- `filename` — Original filename with extension (e.g., `"report.pdf"`)

**Optional fields:**
- `pinning_api_key` — Your own pinning service API key for unlimited uploads
- `pinning_service` — Which service your API key is for. Required when `pinning_api_key` is provided. One of: `"pinata"`, `"web3storage"`, `"nftstorage"`

**Example (using shared service):**
```json
{
  "action": "upload",
  "content": "SGVsbG8gV29ybGQh",
  "filename": "hello.txt"
}
```

**Example (using your own Pinata key):**
```json
{
  "action": "upload",
  "content": "SGVsbG8gV29ybGQh",
  "filename": "hello.txt",
  "pinning_api_key": "your-pinata-jwt-token",
  "pinning_service": "pinata"
}
```

**Response includes:** cid, filename, file_size_bytes, file_size_mb, ipfs_url, and multiple gateway_urls for accessing the content.

---

##### list

List all files you have previously uploaded through this tool, sorted by most recent first.

**Required fields:**
- `action` — `"list"`

**Example:**
```json
{
  "action": "list"
}
```

**Response includes:** array of uploads (each with cid, filename, file_size, upload_date, ipfs_url, gateway_url), plus totals for upload count and combined size.

---

#### Common Workflows

##### Store a document permanently
1. Base64-encode your file content
2. Use `upload` with the encoded content and filename
3. Save the returned CID -- this is the permanent address of your content

##### Retrieve previously stored content
1. Use `retrieve` with the CID you received from an upload or found elsewhere
2. Text content is returned directly; binary content is identified by type

##### Review your upload history
1. Use `list` to see all files you have uploaded
2. Each entry includes the CID and gateway URL for easy access

#### Important Notes
- **File size limit:** 10MB maximum per upload
- **Content encoding:** Files must be base64-encoded before uploading
- **CID formats:** Both CIDv0 (`Qm...`) and CIDv1 (`bafy...`) are supported for retrieval
- **Persistence:** Uploaded content is pinned to IPFS, meaning it will remain available as long as the pinning service maintains it
- **Gateway fallback:** Retrieval automatically tries multiple gateways if the first one fails
- **Own credentials:** For heavy usage, provide your own API key from Pinata, Web3.Storage, or NFT.Storage to avoid shared service limits

## When To Use
- Use this skill for `IPFS Content Gateway` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: ipfs content gateway, ipfs content retrieval, decentralized storage access, cid content lookup, ipfs gateway access, list, retrieve, cid.
- Supported action names: `list`, `retrieve`, `upload`.

## Use Cases
- IPFS content retrieval
- decentralized storage access
- CID content lookup
- IPFS gateway access
- content-addressed file retrieval
- distributed file download
- IPFS file upload
- decentralized file hosting
- permanent content storage
- immutable file storage
- NFT metadata hosting
- NFT asset storage
- Web3 content storage
- blockchain data storage
- decentralized application storage
- dApp file hosting

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `list` (action slug: `list`): List all files previously uploaded through this tool, sorted by most recent first. Returns upload history with CIDs, filenames, sizes, dates, and gateway URLs. Price: `20` credits. Parameters: none.
- `retrieve` (action slug: `retrieve`): Fetch content from IPFS by its Content Identifier (CID). Supports both CIDv0 (Qm...) and CIDv1 (bafy...) formats. Multiple gateways are tried automatically for reliability. Price: `20` credits. Parameters: `cid`.
- `upload` (action slug: `upload`): Upload a file to IPFS. The file is pinned so it remains available on the network. Maximum file size is 10MB. Files must be base64-encoded before uploading. Price: `20` credits. Parameters: `content`, `filename`, `pinning_api_key`, `pinning_service`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "ipfs-content-gateway"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "ipfs-content-gateway"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "ipfs-content-gateway"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "ipfs-content-gateway"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "ipfs-content-gateway"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "ipfs-content-gateway"
  }
}
```

## Call This Tool
Product slug: `ipfs-content-gateway`

Marketplace page: https://www.agentpmt.com/marketplace/ipfs-content-gateway

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "IPFS-Content-Gateway",
    "arguments": {
      "action": "list"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "ipfs-content-gateway",
  "parameters": {
    "action": "list"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `list` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/ipfs-content-gateway
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
