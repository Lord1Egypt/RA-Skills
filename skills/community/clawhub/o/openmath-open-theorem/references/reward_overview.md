# OpenMath Reward System

## Reward Calculation
*   **Base Reward**: The initial amount set by the theorem proposer when the bounty is created.
*   **Complexity Multiplier**: Rewards may increase if a theorem remains unproven for a long period.
*   **Currency**: Rewards are denominated in **uctk** (micro-CTK on the Shentu chain). Precision: 1 CTK = 1,000,000 uctk.

## Reward Buckets
An address can accumulate two independent reward buckets:
*   `imported_rewards`: Earned when a theorem you created is imported or referenced by other theorems.
*   `proof_rewards`: Earned when you submit a proof that passes on-chain verification.

An address may have only one bucket, both, or neither. A single `withdraw-rewards` transaction withdraws all available buckets together.

## Reward Lifecycle
1.  **Submission**: Proofs are submitted via the two-stage process (proof-hash then proof-detail) on the Shentu chain.
2.  **Verification**: The system automatically verifies the proof in a sandbox environment.
3.  **Accumulation**: Once the theorem reaches `THEOREM_STATUS_PASSED`, the reward is credited to the prover's address as `proof_rewards`.
4.  **Withdrawal**: The prover broadcasts a `withdraw-rewards` transaction to transfer rewards to their wallet. Rewards are claimed per address, not per theorem.

## Claiming Details
For the full on-chain withdrawal commands and operational flow, use the `openmath-claim-reward` skill.
