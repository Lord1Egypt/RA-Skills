# Polls & Temperature Checks

Query governance temperature checks and polls for the Indigo Protocol DAO.

## MCP Tools

### get_temperature_checks

Get active governance temperature checks. Temperature checks are preliminary community sentiment votes before formal governance proposals.

**Parameters:** None

**Returns:** Array of temperature check objects with proposal details, vote counts, and status.

### get_polls

Get governance polls and voting data. Polls are formal on-chain governance votes for protocol changes.

**Parameters:** None

**Returns:** Array of poll objects with proposal details, vote tallies, and outcomes.

## Examples

### View active temperature checks

See what governance proposals are in the temperature check phase.

**Prompt:** "Show me the active temperature checks"

**Workflow:**
1. Call `get_temperature_checks()` to retrieve all active temp checks
2. Filter for those with "active" status
3. Present each with title, description, vote counts, and deadline

**Sample response:**
```
Active Temperature Checks:

1. "Reduce iUSD minimum collateral ratio to 140%"
   For: 2.4M INDY (68%) | Against: 1.1M INDY (32%)
   Status: Active — 3 days remaining

2. "Add iSOL stability pool INDY incentives"
   For: 1.8M INDY (82%) | Against: 390K INDY (18%)
   Status: Active — 5 days remaining
```

### Check governance poll results

View the outcome of formal on-chain governance votes.

**Prompt:** "What are the latest governance poll results?"

**Workflow:**
1. Call `get_polls()` to retrieve all polls
2. Sort by most recent first
3. Show vote tallies and whether each passed or failed

**Sample response:**
```
Recent Governance Polls:

1. Poll #47: "Increase INDY staking rewards by 5%"
   Result: PASSED (74% for)
   Votes: 3.1M INDY for / 1.1M INDY against

2. Poll #46: "Update oracle feed frequency to 30s"
   Result: FAILED (41% for)
   Votes: 1.7M INDY for / 2.4M INDY against
```

### Track a proposal through the governance pipeline

Follow a proposal from temperature check through formal poll.

**Prompt:** "What proposals are being voted on right now?"

**Workflow:**
1. Call `get_temperature_checks()` for proposals in the sentiment phase
2. Call `get_polls()` for proposals in the formal voting phase
3. Present both stages together for a complete governance overview

**Sample response:**
```
Governance Pipeline:

Temperature Check Phase (2 active):
  - Reduce iUSD min ratio to 140% — 68% support
  - Add iSOL SP incentives — 82% support

Formal Voting Phase (1 active):
  - Poll #48: Adjust liquidation bonus to 8% — voting ends in 2 days
```

## Example Prompts

- "Show me the active temperature checks"
- "What governance polls are currently open?"
- "List recent Indigo governance proposals"
- "What are the latest voting results?"
- "How much INDY voted on the latest poll?"
