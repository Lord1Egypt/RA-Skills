# `verify_data_provenance`

Compares a snapshot **CID** to on-chain `maxSnapshotsCid` for `(data_market, project_id, epoch_id)` via the Powerloom protocol state contract.

**Inputs:** `cid` (string), `epoch_id` (integer), `project_id` (string). Optional `data_market` override.

**Hosted MCP** runs the `eth_call` on the server (configured RPC is **not** included in the tool response). If the server’s RPC is unset, the tool returns a clear configuration error — not a silent pass. For a **local** second check, use the same `cid` / `epoch_id` / `project_id` with your own provider **`POWERLOOM_EVM_RPC_URL`** (e.g. public Powerloom JSON-RPC) and the documented ProtocolState / DataMarket addresses — do not expect MCP to echo an RPC URL.

**Metering** `GET /credits/plans` exposes **`chains[].rpc_url`** only as an optional **public** hint; it can be empty.

**In alerts:** only print verification lines when `cid`, `epoch_id`, and `project_id` are all known from the API response. Do not substitute block numbers for epoch IDs.
