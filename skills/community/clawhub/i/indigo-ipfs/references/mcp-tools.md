# MCP Tools Reference — Indigo IPFS & Collector

Detailed reference for all MCP tools in the `indigo-ipfs` skill package.

## store_on_ipfs

Store text content on IPFS and receive an immutable content identifier.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Text content to store on IPFS |

**Returns:**

| Field | Type | Description |
|-------|------|-------------|
| `cid` | string | IPFS content identifier (CID) for the stored content |

**Notes:**
- Content is stored as plain text
- The returned CID is a permanent, immutable reference
- CIDs follow the IPFS content-addressing standard (typically Qm... or bafy... format)
- Stored content can be retrieved at any time using `retrieve_from_ipfs`

---

## retrieve_from_ipfs

Retrieve previously stored content from IPFS using a content identifier.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cid` | string | Yes | IPFS content identifier (CID) |

**Returns:**

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | The text content stored at the given CID |

**Notes:**
- Retrieval requires a valid CID that references existing content
- Content is returned as plain text
- IPFS content is immutable — the same CID always returns the same content

---

## get_collector_utxos

Query collector UTXOs that hold accumulated protocol fees available for distribution.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `length` | number | No | All | Maximum number of UTXOs to return |

**Returns:**

Array of UTXO objects, each containing:

| Field | Type | Description |
|-------|------|-------------|
| `txHash` | string | Transaction hash of the UTXO |
| `outputIndex` | number | Output index within the transaction |
| `value` | object | ADA and native token values held in the UTXO |

**Notes:**
- Collector UTXOs accumulate protocol fees from CDP operations, liquidations, and redemptions
- Omitting `length` returns all available collector UTXOs
- UTXOs may contain ADA, iAssets (iUSD, iBTC, iETH, iSOL), and INDY tokens
- Fee distribution is a separate protocol operation that consumes these UTXOs
