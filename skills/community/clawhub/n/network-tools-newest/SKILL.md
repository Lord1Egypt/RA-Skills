---
name: network-tools
description: "Network Tools: Network utilities: IP conversion/validation, subnet calculator, CIDR ranges, MAC formatting, port lookup, DNS resolution, private IP detection. Use when an agent needs network tools, ipv4 to binary conversion, ip address binary representation, binary to ipv4 conversion, ip to integer conversion, network binary to ipv4, input, network cidr to range through AgentPMT-hosted remote tool calls. Discovery terms: network tools, ipv4 to binary conversion, ip address binary representation."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/network-tools
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/network-tools"}}
---
# Network Tools

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A utility for IP address manipulation, subnet calculations, and network-related operations commonly needed in network administration, security analysis, and infrastructure automation. IP address conversion functions translate between IPv4 dotted decimal notation, 32-bit binary representation, and integer formats for low-level network programming and analysis. The subnet calculator takes CIDR notation and returns comprehensive network information including network address, broadcast address, netmask, wildcard mask, first and last usable addresses, total and usable host counts, and IP class classification. CIDR to range conversion lists all IP addresses within a subnet block with sample addresses for large ranges. IP range membership checking determines whether a specific address falls within a given CIDR block. MAC address formatting converts hardware addresses between colon-separated, dash-separated, Cisco dot notation, and plain formats. Port validation identifies well-known service associations for common ports and classifies numbers as well-known, registered, or dynamic ranges. DNS lookup resolves hostnames to IP addresses with support for multiple A records, while reverse DNS finds hostnames associated with IP addresses. IP information analysis identifies address class, private versus public status, loopback, multicast, and reserved designations. Additional utilities include random IPv6 generation, private IP range detection with specific range identification, and CIDR notation validation with automatic correction suggestions.

## Product Instructions
### Network Tools

Perform IP address conversions, subnet calculations, MAC address formatting, port validation, DNS lookups, and other networking utilities.

#### Actions

##### network-ipv4-to-binary
Convert an IPv4 address to its binary representation.

**Required:** `input` - IPv4 address

```json
{"action": "network-ipv4-to-binary", "input": "192.168.1.1"}
```

Returns: binary string (continuous and dotted), bit length.

---

##### network-binary-to-ipv4
Convert a 32-bit binary string back to an IPv4 address.

**Required:** `input` - 32-bit binary string (dots/spaces allowed)

```json
{"action": "network-binary-to-ipv4", "input": "11000000101010000000000100000001"}
```

Returns: the corresponding IPv4 address.

---

##### network-ipv4-to-integer
Convert an IPv4 address to its integer and hexadecimal representations.

**Required:** `input` - IPv4 address

```json
{"action": "network-ipv4-to-integer", "input": "192.168.1.1"}
```

Returns: integer value and hex value.

---

##### network-integer-to-ipv4
Convert an integer (0-4294967295) back to an IPv4 address.

**Required:** `input` - integer as a string

```json
{"action": "network-integer-to-ipv4", "input": "3232235777"}
```

Returns: the corresponding IPv4 address and hex value.

---

##### network-subnet-calculator
Calculate full subnet details from CIDR notation.

**Required:** `input` - CIDR notation (e.g., `192.168.1.0/24`)

```json
{"action": "network-subnet-calculator", "input": "10.0.0.0/16"}
```

Returns: network address, broadcast address, netmask, wildcard mask, first/last usable host, total addresses, usable addresses, prefix length, IP class.

---

##### network-cidr-to-range
Convert CIDR notation to a start/end IP range with sample IPs.

**Required:** `input` - CIDR notation

```json
{"action": "network-cidr-to-range", "input": "192.168.1.0/28"}
```

Returns: start IP, end IP, total IPs, and up to 10 sample IPs.

---

##### network-ip-in-range
Check whether an IP address falls within a given CIDR range.

**Required:** `input` - IPv4 address to check
**Required:** `input2` - CIDR notation to check against

```json
{"action": "network-ip-in-range", "input": "192.168.1.50", "input2": "192.168.1.0/24"}
```

Returns: boolean `in_range`, plus network and broadcast addresses of the range.

---

##### network-mac-format
Reformat a MAC address into different notation styles.

**Required:** `input` - MAC address in any format
**Optional:** `format` - output style: `colon` (default), `dash`, `dot`, or `plain`

```json
{"action": "network-mac-format", "input": "001A2B3C4D5E", "format": "dash"}
```

Returns: formatted MAC and all four format variants.

---

##### network-port-validate
Validate a port number and identify the associated well-known service.

**Required:** `input` - port number (1-65535) as a string

```json
{"action": "network-port-validate", "input": "443"}
```

Returns: validity, port type (well-known / registered / dynamic), and service name if recognized (e.g., HTTPS, SSH, MySQL).

---

##### network-dns-lookup
Resolve a hostname to its IP address(es).

**Required:** `input` - hostname

```json
{"action": "network-dns-lookup", "input": "google.com"}
```

Returns: primary IP and list of all resolved IPs.

---

##### network-reverse-dns
Perform a reverse DNS lookup on an IP address to find its hostname.

**Required:** `input` - IPv4 address

```json
{"action": "network-reverse-dns", "input": "8.8.8.8"}
```

Returns: hostname if a PTR record exists, or a not-found message.

---

##### network-ip-info
Get detailed classification information about an IPv4 address.

**Required:** `input` - IPv4 address

```json
{"action": "network-ip-info", "input": "10.0.0.1"}
```

Returns: IP version, class (A/B/C/D/E), and boolean flags for private, loopback, multicast, reserved, and global.

---

##### network-generate-ipv6
Generate a random IPv6 address. No input required.

```json
{"action": "network-generate-ipv6"}
```

Returns: full and compressed IPv6 address representations.

---

##### network-private-ip-check
Check whether an IPv4 address belongs to a private, loopback, or link-local range.

**Required:** `input` - IPv4 address

```json
{"action": "network-private-ip-check", "input": "172.16.5.10"}
```

Returns: private/loopback/link-local flags and the matching private range name if applicable.

---

##### network-cidr-validate
Validate CIDR notation and check whether it uses strict network addressing.

**Required:** `input` - CIDR notation

```json
{"action": "network-cidr-validate", "input": "192.168.1.100/24"}
```

Returns: validity, correct network address, prefix length, whether the notation is strict, and the corrected CIDR if needed.

---

#### Common Workflows

**Plan a subnet:** Use `network-subnet-calculator` to get the full breakdown, then `network-cidr-to-range` to see actual host IPs.

**Verify an IP belongs to a network:** Use `network-ip-in-range` with the IP and the CIDR block.

**Audit IP classification:** Use `network-ip-info` for general details, then `network-private-ip-check` to confirm private range membership.

**Resolve and reverse-verify a host:** Use `network-dns-lookup` to get the IP, then `network-reverse-dns` on the result to confirm the PTR record matches.

#### Important Notes

- All IP address inputs must be valid IPv4 dotted-decimal format unless otherwise noted.
- CIDR notation must include the prefix (e.g., `/24`). The tool uses non-strict parsing, so host bits in the address portion are accepted.
- The `input` and `input2` parameters are always strings, even for numeric values like port numbers or integers.
- The `format` parameter only applies to `network-mac-format`.
- `network-generate-ipv6` is the only action that requires no input.

## When To Use
- Use this skill for `Network Tools` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: network tools, ipv4 to binary conversion, ip address binary representation, binary to ipv4 conversion, ip to integer conversion, network binary to ipv4, input, network cidr to range.
- Supported action names: `network-binary-to-ipv4`, `network-cidr-to-range`, `network-cidr-validate`, `network-dns-lookup`, `network-generate-ipv6`, `network-integer-to-ipv4`, `network-ip-in-range`, `network-ip-info`, `network-ipv4-to-binary`, `network-ipv4-to-integer`, `network-mac-format`, `network-port-validate`, `network-private-ip-check`, `network-reverse-dns`, `network-subnet-calculator`.

## Use Cases
- IPv4 to binary conversion
- IP address binary representation
- binary to IPv4 conversion
- IP to integer conversion
- integer to IP conversion
- IP address math
- subnet calculation
- subnet calculator
- CIDR calculator
- network address calculation
- broadcast address calculation
- netmask calculation
- wildcard mask
- usable host count
- subnet planning
- CIDR to IP range

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `15`.
x402 availability: not enabled for this product.

- `network-binary-to-ipv4` (action slug: `network-binary-to-ipv4`): Convert a 32-bit binary string back to an IPv4 dotted-decimal address. Price: `5` credits. Parameters: `input`.
- `network-cidr-to-range` (action slug: `network-cidr-to-range`): Convert CIDR notation to a start/end IP range with sample IPs. Price: `5` credits. Parameters: `input`.
- `network-cidr-validate` (action slug: `network-cidr-validate`): Validate CIDR notation, check whether it uses strict network addressing, and suggest corrections if needed. Price: `5` credits. Parameters: `input`.
- `network-dns-lookup` (action slug: `network-dns-lookup`): Resolve a hostname to its IP address(es) including all A records. Price: `5` credits. Parameters: `input`.
- `network-generate-ipv6` (action slug: `network-generate-ipv6`): Generate a random IPv6 address in both full and compressed notation. No input required. Price: `5` credits. Parameters: none.
- `network-integer-to-ipv4` (action slug: `network-integer-to-ipv4`): Convert an integer (0-4294967295) back to an IPv4 dotted-decimal address. Price: `5` credits. Parameters: `input`.
- `network-ip-in-range` (action slug: `network-ip-in-range`): Check whether a specific IPv4 address falls within a given CIDR range. Price: `5` credits. Parameters: `input`, `input2`.
- `network-ip-info` (action slug: `network-ip-info`): Get detailed classification information about an IPv4 address including class, private/public status, and special designations. Price: `5` credits. Parameters: `input`.
- `network-ipv4-to-binary` (action slug: `network-ipv4-to-binary`): Convert an IPv4 address to its 32-bit binary representation (continuous and dotted notation). Price: `5` credits. Parameters: `input`.
- `network-ipv4-to-integer` (action slug: `network-ipv4-to-integer`): Convert an IPv4 address to its integer and hexadecimal representations. Price: `5` credits. Parameters: `input`.
- `network-mac-format` (action slug: `network-mac-format`): Reformat a MAC address into different notation styles (colon, dash, dot, or plain). Price: `5` credits. Parameters: `input`, `output_format`.
- `network-port-validate` (action slug: `network-port-validate`): Validate a port number and identify the associated well-known service (e.g., HTTP, SSH, MySQL). Price: `5` credits. Parameters: `input`.
- `network-private-ip-check` (action slug: `network-private-ip-check`): Check whether an IPv4 address belongs to a private (RFC 1918), loopback, or link-local range, and identify the specific range. Price: `5` credits. Parameters: `input`.
- `network-reverse-dns` (action slug: `network-reverse-dns`): Perform a reverse DNS lookup on an IPv4 address to find its associated hostname (PTR record). Price: `5` credits. Parameters: `input`.
- `network-subnet-calculator` (action slug: `network-subnet-calculator`): Calculate full subnet details from CIDR notation including network/broadcast addresses, netmask, wildcard, usable hosts, and IP class. Price: `5` credits. Parameters: `input`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "network-tools"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "network-tools"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "network-tools"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "network-tools"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "network-tools"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "network-tools"
  }
}
```

## Call This Tool
Product slug: `network-tools`

Marketplace page: https://www.agentpmt.com/marketplace/network-tools

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
    "name": "Network-Tools",
    "arguments": {
      "action": "network-binary-to-ipv4",
      "input": "example input"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "network-tools",
  "parameters": {
    "action": "network-binary-to-ipv4",
    "input": "example input"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `network-binary-to-ipv4` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/network-tools
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
