---
name: multi-protocol-bridge
description: "Multi-Protocol Bridge: HTTP gateway to FTP, SSH, and MQTT protocols. Execute file transfers, remote commands, and IoT messaging via HTTP requests. Use when an agent needs multi protocol bridge, ftp file upload automation, ftp file download, secure ftps file transfer, remote directory listing, ftp delete, url, options through AgentPMT-hosted remote tool calls. Discovery terms: multi protocol bridge, ftp file upload automation, ftp file download, secure ftps file transfer."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/multi-protocol-bridge
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/multi-protocol-bridge"}}
---
# Multi-Protocol Bridge

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Protocol Bridge is an HTTP gateway that enables AI agents, automation workflows, and modern applications to interact with traditional network protocols without native protocol support. It translates simple HTTP requests into FTP, SSH, and MQTT operations, making it easy to integrate file transfers, remote command execution, and IoT messaging into any system that can make web requests. The tool supports secure connections including FTPS, SSH key authentication, and MQTTS with TLS, ensuring enterprise-grade security for sensitive operations. Connection details can be passed via intuitive URL strings or explicit parameters, giving developers flexibility in how they configure each action. Protocol Bridge is ideal for building automation pipelines, connecting legacy infrastructure to modern APIs, orchestrating DevOps tasks, and enabling large language models to perform real-world actions across diverse systems. For email sending workflows, use the dedicated SMTP Mailer tool which provides a streamlined interface specifically optimized for email delivery.

## Product Instructions
### Multi-Protocol Bridge

Access FTP, SSH, and MQTT protocols through a unified HTTP interface. All actions use a URL-first approach where connection details (host, port, credentials, path) are encoded in the URL.

#### URL Format

All actions require a protocol URL:
```
scheme://username:password@hostname:port/path
```

Supported schemes:
- `ftp://` / `ftps://` (FTP with optional TLS)
- `ssh://` (SSH remote commands)
- `mqtt://` / `mqtts://` (MQTT with optional TLS)

---

#### Actions

##### ftp_upload

Upload a file to an FTP/FTPS server.

**Required fields:**
- `action`: `"ftp_upload"`
- `url`: FTP URL with path to the destination file (scheme must be `ftp://` or `ftps://`)
- `content`: File content to upload (text or base64-encoded)

**Optional fields:**
- `content_encoding`: `"text"` (default) or `"base64"` for binary files

**Example:**
```json
{
  "action": "ftp_upload",
  "url": "ftp://myuser:mypass@ftp.example.com:21/uploads/report.txt",
  "content": "Monthly report data here..."
}
```

**Example (binary file):**
```json
{
  "action": "ftp_upload",
  "url": "ftps://myuser:mypass@ftp.example.com:21/images/logo.png",
  "content": "iVBORw0KGgoAAAANSUhEUg...",
  "content_encoding": "base64"
}
```

**Limits:** Maximum file size is 100 MB.

---

##### ftp_download

Download a file from an FTP/FTPS server.

**Required fields:**
- `action`: `"ftp_download"`
- `url`: FTP URL with path to the file to download (scheme must be `ftp://` or `ftps://`)

**Optional fields:**
- `options.return_base64` (boolean): Return file content as base64 instead of text. Default: `false`. Use this for binary files.

**Example:**
```json
{
  "action": "ftp_download",
  "url": "ftp://myuser:mypass@ftp.example.com:21/reports/q1.csv"
}
```

**Example (binary download):**
```json
{
  "action": "ftp_download",
  "url": "ftps://myuser:mypass@ftp.example.com:21/images/photo.jpg",
  "options": { "return_base64": true }
}
```

**Limits:** Maximum file size is 100 MB. Non-text files that fail UTF-8 decoding are automatically returned as base64.

---

##### ftp_list

List the contents of a directory on an FTP/FTPS server.

**Required fields:**
- `action`: `"ftp_list"`
- `url`: FTP URL with path to the directory (scheme must be `ftp://` or `ftps://`)

**Optional fields:**
- `options.recursive` (boolean): List subdirectories recursively. Default: `false`

**Example:**
```json
{
  "action": "ftp_list",
  "url": "ftp://myuser:mypass@ftp.example.com:21/documents/"
}
```

**Example (recursive):**
```json
{
  "action": "ftp_list",
  "url": "ftp://myuser:mypass@ftp.example.com:21/project/",
  "options": { "recursive": true }
}
```

**Limits:** Results are capped at 1,000 entries.

---

##### ftp_delete

Delete a file on an FTP/FTPS server. Requires explicit confirmation.

**Required fields:**
- `action`: `"ftp_delete"`
- `url`: FTP URL with path to the file to delete (scheme must be `ftp://` or `ftps://`)
- `options.confirm_delete`: Must be the string `"DELETE"` to confirm deletion

**Example:**
```json
{
  "action": "ftp_delete",
  "url": "ftp://myuser:mypass@ftp.example.com:21/old-files/archive.zip",
  "options": { "confirm_delete": "DELETE" }
}
```

---

##### ssh_execute

Execute a shell command on a remote server via SSH.

**Required fields:**
- `action`: `"ssh_execute"`
- `url`: SSH URL (scheme must be `ssh://`)
- `content`: The shell command to execute

**Optional fields:**
- `options.timeout` (integer): Command timeout in seconds. Default: `30`
- `options.private_key` (string): SSH private key in PEM format for key-based authentication. When provided, password in the URL can be omitted.
- `options.known_hosts` (string): SSH known hosts entry for host verification

**Example (password auth):**
```json
{
  "action": "ssh_execute",
  "url": "ssh://deploy:s3cret@server.example.com:22",
  "content": "df -h && uptime"
}
```

**Example (key-based auth):**
```json
{
  "action": "ssh_execute",
  "url": "ssh://deploy@server.example.com:22",
  "content": "ls -la /var/log",
  "options": {
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
    "timeout": 60
  }
}
```

**Limits:** Command output (stdout/stderr) is capped at 10 MB each.

---

##### mqtt_publish

Publish a message to an MQTT broker.

**Required fields:**
- `action`: `"mqtt_publish"`
- `url`: MQTT URL with the topic as the path (scheme must be `mqtt://` or `mqtts://`)
- `content`: Message payload (plain text or JSON string)

**Optional fields:**
- `options.qos` (integer): Quality of Service level. `0` = at most once (default), `1` = at least once, `2` = exactly once.
- `options.retain` (boolean): Broker retains the message for future subscribers. Default: `false`
- `options.client_id` (string): MQTT client identifier. Auto-generated if not provided.

**Example:**
```json
{
  "action": "mqtt_publish",
  "url": "mqtt://sensoruser:sensorpass@broker.example.com:1883/sensors/temperature",
  "content": "{\"value\": 22.5, \"unit\": \"celsius\"}"
}
```

**Example (with QoS and retain):**
```json
{
  "action": "mqtt_publish",
  "url": "mqtts://admin:secret@broker.example.com:8883/alerts/critical",
  "content": "Server CPU above 95%",
  "options": { "qos": 2, "retain": true, "client_id": "monitoring-agent" }
}
```

**Limits:** Payload size is capped at 1 MB.

---

#### Common Workflows

##### Deploy a file and verify it exists
1. Use `ftp_upload` to upload the file.
2. Use `ftp_list` on the parent directory to confirm it appears.

##### Remote server health check
1. Use `ssh_execute` with a command like `uptime && free -m && df -h` to get server status.

##### IoT data publishing
1. Use `mqtt_publish` to send sensor readings to a topic with `qos: 1` for guaranteed delivery.

##### Secure file transfer
1. Use `ftps://` scheme for encrypted FTP connections.
2. Use `mqtts://` scheme for encrypted MQTT connections.
3. Use `options.private_key` for SSH key-based authentication.

---

#### Important Notes

- **URL encoding:** Special characters in usernames or passwords must be URL-encoded (e.g., `@` becomes `%40`).
- **Default ports:** FTP uses 21, SSH uses 22, MQTT uses 1883, MQTTS uses 8883. You can omit the port to use the default.
- **FTP anonymous access:** If no username is provided, connections default to anonymous access.
- **Delete safety:** The `ftp_delete` action requires `options.confirm_delete` set to `"DELETE"` as a safeguard.
- **Binary files:** Use `content_encoding: "base64"` for uploading binary files and `options.return_base64: true` for downloading them.
- **SSH authentication:** Provide either a password in the URL or a `private_key` in options, not both.

## When To Use
- Use this skill for `Multi-Protocol Bridge` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: multi protocol bridge, ftp file upload automation, ftp file download, secure ftps file transfer, remote directory listing, ftp delete, url, options.
- Supported action names: `ftp_delete`, `ftp_download`, `ftp_list`, `ftp_upload`, `mqtt_publish`, `ssh_execute`.

## Use Cases
- FTP file upload automation
- FTP file download
- secure FTPS file transfer
- remote directory listing
- automated file deletion
- SSH remote command execution
- server administration automation
- DevOps task orchestration
- IoT MQTT message publishing
- sensor data transmission
- smart home device control
- MQTT broker integration
- AI agent protocol access
- LLM tool integration
- workflow automation
- legacy system integration

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `6`.
x402 availability: not enabled for this product.

- `ftp_delete` (action slug: `ftp-delete`): Delete a file on an FTP or FTPS server. Requires explicit confirmation via options.confirm_delete. Price: `5` credits. Parameters: `options`, `url`.
- `ftp_download` (action slug: `ftp-download`): Download a file from an FTP or FTPS server. Returns file content as text or base64. Price: `5` credits. Parameters: `options`, `url`.
- `ftp_list` (action slug: `ftp-list`): List the contents of a directory on an FTP or FTPS server. Price: `5` credits. Parameters: `options`, `url`.
- `ftp_upload` (action slug: `ftp-upload`): Upload a file to an FTP or FTPS server. Supports text and base64-encoded binary content. Price: `5` credits. Parameters: `content`, `content_encoding`, `url`.
- `mqtt_publish` (action slug: `mqtt-publish`): Publish a message to an MQTT or MQTTS broker. The topic is specified as the URL path. Price: `5` credits. Parameters: `content`, `options`, `url`.
- `ssh_execute` (action slug: `ssh-execute`): Execute a shell command on a remote server via SSH. Supports password and key-based authentication. Price: `5` credits. Parameters: `content`, `options`, `url`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "multi-protocol-bridge"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "multi-protocol-bridge"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "multi-protocol-bridge"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "multi-protocol-bridge"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "multi-protocol-bridge"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "multi-protocol-bridge"
  }
}
```

## Call This Tool
Product slug: `multi-protocol-bridge`

Marketplace page: https://www.agentpmt.com/marketplace/multi-protocol-bridge

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
    "name": "Multi-Protocol-Bridge",
    "arguments": {
      "action": "ftp_delete",
      "options": {
        "confirm_delete": "example confirm delete"
      },
      "url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "multi-protocol-bridge",
  "parameters": {
    "action": "ftp_delete",
    "options": {
      "confirm_delete": "example confirm delete"
    },
    "url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `ftp_delete` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/multi-protocol-bridge
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
