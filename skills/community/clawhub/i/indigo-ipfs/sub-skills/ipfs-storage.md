# IPFS Storage

Store and retrieve data on IPFS for the Indigo Protocol.

## Tools

### store_on_ipfs

Store text content on IPFS. Returns the content identifier (CID) that can be used to retrieve the data later.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | Yes | Text content to store on IPFS |

### retrieve_from_ipfs

Retrieve content from IPFS using a content identifier (CID).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cid` | string | Yes | IPFS content identifier (CID) |

## Examples

### Store governance proposal metadata

Store a governance proposal description on IPFS so it can be referenced immutably on-chain.

**Prompt:** "Store this governance proposal on IPFS: Increase iUSD stability pool rewards by 15%"

**Workflow:**

1. Call `store_on_ipfs` with the proposal text:
   ```
   store_on_ipfs({
     "text": "Proposal: Increase iUSD stability pool rewards by 15%\n\nRationale: Current reward rates are below competitive DeFi yields. Increasing SP rewards will attract more liquidity and strengthen the iUSD peg.\n\nImplementation: Adjust the reward distribution parameter from the current rate to +15%."
   })
   ```
2. Return the CID to the user for on-chain reference.

**Sample response:**

```
Content stored on IPFS
──────────────────────
CID: QmX7b2K9fN3pRtA8vYz1wE4cD6hG5jL0mQ9sU2xW3yBn

This CID is an immutable reference to your proposal text.
You can use it in governance submissions or share it
for others to verify the proposal content.
```

### Retrieve stored content

Fetch previously stored content from IPFS using its CID.

**Prompt:** "Retrieve the content at CID QmX7b2K9fN3pRtA8vYz1wE4cD6hG5jL0mQ9sU2xW3yBn"

**Workflow:**

1. Call `retrieve_from_ipfs` with the CID:
   ```
   retrieve_from_ipfs({
     "cid": "QmX7b2K9fN3pRtA8vYz1wE4cD6hG5jL0mQ9sU2xW3yBn"
   })
   ```
2. Display the retrieved text content.

**Sample response:**

```
IPFS Content Retrieved
──────────────────────
CID: QmX7b2K9fN3pRtA8vYz1wE4cD6hG5jL0mQ9sU2xW3yBn

Content:
Proposal: Increase iUSD stability pool rewards by 15%

Rationale: Current reward rates are below competitive DeFi
yields. Increasing SP rewards will attract more liquidity
and strengthen the iUSD peg.

Implementation: Adjust the reward distribution parameter
from the current rate to +15%.
```

### Store CDP position snapshot

Store a snapshot of CDP positions on IPFS for auditing or record-keeping purposes.

**Prompt:** "Store a snapshot of my CDP data on IPFS for my records"

**Workflow:**

1. First gather CDP data using other tools (e.g., `get_cdps_by_owner`).
2. Format the data as a text snapshot.
3. Call `store_on_ipfs` with the formatted snapshot:
   ```
   store_on_ipfs({
     "text": "CDP Snapshot — 2025-01-15\n\nOwner: addr1q9x...\n\nCDP #1: iUSD\n  Collateral: 5,000 ADA\n  Minted: 1,200 iUSD\n  Ratio: 312%\n\nCDP #2: iBTC\n  Collateral: 15,000 ADA\n  Minted: 0.08 iBTC\n  Ratio: 280%"
   })
   ```
4. Return the CID as a permanent reference to this snapshot.

**Sample response:**

```
CDP Snapshot Stored
───────────────────
CID: QmR4t8Y2nP7aK1wV9xB3dF5gH6jM0sQ8uL2cE4iO7pXn

Your CDP position snapshot has been permanently stored.
Use this CID to retrieve the snapshot at any time for
auditing or comparison purposes.
```

## Example Prompts

- "Store this text on IPFS: ..."
- "Retrieve the IPFS content for CID Qm..."
- "Save my governance proposal to IPFS"
- "Fetch the stored data at this CID"
- "Archive my CDP positions on IPFS"
