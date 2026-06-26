# Example Conversation Flows

## ERC-20 Token with Staking

**User**: "Build me an ERC-20 token with staking rewards"

**Claude with Pentagonal**:
1. Call `pentagonal_generate` with prompt "ERC-20 token with staking rewards", chain "ethereum"
2. Present the generated code to the user
3. Call `pentagonal_audit` on the code
4. If findings: "I found 2 issues — a reentrancy risk in `claimRewards()` and a gas optimization. Let me fix the critical one."
5. Call `pentagonal_fix` for the reentrancy issue
6. Call `pentagonal_audit` again to verify the fix
7. Call `pentagonal_compile` for the clean code
8. Present ABI + bytecode + deployment instructions

---

## Multi-Sig Wallet

**User**: "Create a multi-signature wallet that requires 3 of 5 approvals"

**Claude with Pentagonal**:
1. Call `pentagonal_generate` with prompt "Multi-signature wallet requiring 3 of 5 owner approvals for transactions", chain "ethereum"
2. Present code
3. Call `pentagonal_audit` — expect findings around owner management and transaction execution
4. Fix any critical/high findings
5. Re-audit until clean
6. Compile and present deployment instructions

---

## Solana Token

**User**: "I need an SPL token on Solana with 1 billion supply"

**Claude with Pentagonal**:
1. Clarify: "Would you like a simple SPL token configuration, or a full Anchor program with custom logic?"
2. Call `pentagonal_generate` with prompt "SPL token with 1 billion supply", chain "solana"
3. Present the token configuration
4. Call `pentagonal_audit` on the output
5. Present deployment commands using `spl-token` CLI

---

## DeFi Vault

**User**: "Build a yield vault that auto-compounds staking rewards on Base"

**Claude with Pentagonal**:
1. Call `pentagonal_generate` with prompt "ERC-4626 yield vault with auto-compounding staking rewards", chain "base"
2. Present code
3. Call `pentagonal_audit` — DeFi vaults typically have findings around flash loan attacks, price manipulation, and reentrancy
4. Fix all critical/high findings (likely 3-5 fixes needed)
5. Re-audit until clean
6. Compile with `pentagonal_compile`
7. Present deployment instructions for Base network
