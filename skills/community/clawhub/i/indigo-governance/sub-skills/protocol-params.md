# Protocol Parameters

Query current Indigo Protocol on-chain parameters and configuration.

## MCP Tools

### get_protocol_params

Get the current Indigo Protocol parameters including collateral ratios, fee structures, and governance settings.

**Parameters:** None

**Returns:** Protocol parameters object with all configurable on-chain settings.

## Examples

### View all protocol parameters

Get a comprehensive view of the current Indigo Protocol configuration.

**Prompt:** "What are the current Indigo protocol parameters?"

**Workflow:**
1. Call `get_protocol_params()` to retrieve all on-chain parameters
2. Group parameters by category (collateral, fees, governance, etc.)
3. Present in a structured format

**Sample response:**
```
Indigo Protocol Parameters:

Collateral Ratios:
  iUSD min ratio: 150%
  iBTC min ratio: 150%
  iETH min ratio: 150%
  iSOL min ratio: 150%

Fee Structure:
  Minting fee: 0.5%
  Redemption fee: 1.0%
  Liquidation bonus: 10%

Governance:
  Proposal threshold: 100,000 INDY
  Voting period: 7 days
  Quorum: 10% of staked INDY
```

### Check collateral requirements for a specific iAsset

Find out the minimum collateral ratio required for an iAsset CDP.

**Prompt:** "What is the minimum collateral ratio for iBTC?"

**Workflow:**
1. Call `get_protocol_params()` to get all parameters
2. Extract the collateral ratio setting for iBTC
3. Present with context about what it means for CDP management

**Sample response:**
```
iBTC Collateral Requirements:
  Minimum ratio: 150%
  For 1 iBTC minted at $42,000:
    Minimum ADA collateral: $63,000 worth
    Recommended (safe): $84,000 worth (200% ratio)
```

### Check fee parameters

Understand the current fee structure for protocol operations.

**Prompt:** "What fees does Indigo charge?"

**Workflow:**
1. Call `get_protocol_params()` to retrieve fee parameters
2. Present all fees with explanations of when they apply

**Sample response:**
```
Indigo Protocol Fees:
  Minting fee: 0.5% (applied when minting iAssets from CDP)
  Redemption fee: 1.0% (applied when redeeming iAssets)
  Liquidation bonus: 10% (premium paid to liquidators)
  Interest rates: Variable per iAsset (set by oracle)
```

## Example Prompts

- "What are the current Indigo protocol parameters?"
- "Show me the collateral ratio settings"
- "What are the current fee parameters?"
- "What's the minimum collateral for iETH?"
- "How much INDY is needed to submit a proposal?"
