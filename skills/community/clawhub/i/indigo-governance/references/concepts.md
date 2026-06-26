# Governance Concepts

Key concepts for understanding governance on the Indigo Protocol.

## Governance Process

Indigo Protocol governance follows a two-stage process:

### 1. Temperature Check
- **Purpose:** Gauge community sentiment before a formal vote
- **How:** Community members discuss and vote on a preliminary proposal
- **Duration:** Typically 3-7 days
- **Requirement:** Must reach a support threshold to advance to formal poll

### 2. Formal Poll
- **Purpose:** Binding on-chain vote for protocol changes
- **How:** INDY stakers vote on-chain with their staked balance as voting power
- **Duration:** Typically 7 days
- **Quorum:** Minimum percentage of staked INDY must participate
- **Result:** If passed, the change is implemented by the protocol team

## Voting Power

Voting power is determined by staked INDY balance:
- 1 staked INDY = 1 vote
- Unstaked INDY has no voting power
- Voting power is snapshot at the start of each poll

## Protocol Parameters

Key configurable parameters that governance can change:

| Category | Parameters |
|----------|-----------|
| Collateral | Minimum ratios per iAsset |
| Fees | Minting fee, redemption fee, liquidation bonus |
| Governance | Proposal threshold, voting period, quorum requirement |
| Rewards | INDY emission rates, stability pool incentives |
| Oracle | Feed frequency, bias time, operator settings |
