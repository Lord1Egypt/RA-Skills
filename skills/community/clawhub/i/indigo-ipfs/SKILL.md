---
name: indigo-ipfs
description: "Store and retrieve data on IPFS and query collector UTXOs for the Indigo Protocol."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# Indigo IPFS & Collector

Store and retrieve data on IPFS and query collector UTXOs for the Indigo Protocol on Cardano.

## MCP Tools

### store_on_ipfs

Store text content on IPFS.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | Yes | Text content to store on IPFS |

**Returns:** The IPFS content identifier (CID) for the stored content.

---

### retrieve_from_ipfs

Retrieve content from IPFS by CID.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cid` | string | Yes | IPFS content identifier (CID) |

**Returns:** The text content stored at the given CID.

---

### get_collector_utxos

Get collector UTXOs for fee distribution.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `length` | number | No | Maximum number of UTXOs to return |

**Returns:** A list of collector UTXOs with their values and assets.

## Sub-Skills

- [IPFS Storage](sub-skills/ipfs-storage.md) — Store and retrieve data on IPFS
- [Collector](sub-skills/collector.md) — Query collector UTXOs for fee distribution

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [Concepts](references/concepts.md) — IPFS content addressing and collector fee distribution
