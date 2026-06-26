# Governance MCP Tools Reference

Detailed reference for all governance MCP tools in the Indigo Protocol.

## get_protocol_params

Get the current Indigo Protocol on-chain parameters.

**Parameters:** None

**Returns:** Protocol parameters object including:
- `collateralRatios` — minimum collateral ratios per iAsset
- `fees` — minting fee, redemption fee, liquidation bonus
- `governance` — proposal threshold, voting period, quorum
- `oracleSettings` — oracle feed parameters

---

## get_temperature_checks

Get active governance temperature checks (preliminary community sentiment votes).

**Parameters:** None

**Returns:** Array of temperature check objects:
- `id` — Unique identifier
- `title` — Proposal title
- `description` — Proposal description
- `votesFor` — INDY votes in favor
- `votesAgainst` — INDY votes against
- `status` — "active" | "passed" | "failed"
- `deadline` — Voting deadline timestamp

---

## get_polls

Get formal on-chain governance polls and voting data.

**Parameters:** None

**Returns:** Array of poll objects:
- `id` — Poll number
- `title` — Proposal title
- `description` — Proposal description
- `votesFor` — INDY votes in favor
- `votesAgainst` — INDY votes against
- `status` — "active" | "passed" | "failed" | "expired"
- `startDate` — Voting start timestamp
- `endDate` — Voting end timestamp
