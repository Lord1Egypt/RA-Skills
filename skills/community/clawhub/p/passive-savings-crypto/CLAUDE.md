# SYT Skill — Claude Context

## About autoHODL

autoHODL is a passive savings app for crypto users, inspired by Acorns/Stash but built natively for Web3. It rounds up on-chain purchases and automatically deposits the spare change into Aave to earn yield. Example: spend 7.38 USDC → 0.62 USDC goes to Aave immediately.

- Supports any EVM wallet
- Live on Base and Linea, with native MetaMask Card support
- Launched production December 2025 after winning 1st place at a MetaMask hackathon
- Website: autohodl.money | GitHub: github.com/locker-labs/autohodl.money
- On-chain stats: https://dune.com/locker_money/autohodl

Current distribution channels in development: Telegram bot (memecoin community partnerships), OpenClaw skill (this repo), expanded token/chain support.

## About Spendable Yield Tokens (SYTs)

SYTs are a novel token primitive that makes yield actually spendable. Reference: https://hackmd.io/@locker/autohodl-syts

**The core insight:** wrapped yield tokens like aUSDC are not spendable — when you send aUSDC, the recipient receives aUSDC (a yield token they can't use everywhere). SYTs fix this.

- `sUSDC` (spendable USDC) earns yield like aUSDC
- When you *spend* sUSDC, the recipient receives **regular USDC** — not a wrapped token
- Yield stays liquid and usable at any time
- autoHODL distributes earnings to users as sUSDC

## This Skill

This OpenClaw skill manages the lifecycle of sUSDC for a user:

- **Minting:** Convert idle USDC into sUSDC to earn yield
- **Balance tracking:** Report both nominal sUSDC balance and underlying USDC value (rebasing logic means these differ)
- **Spending:** Route transfers via `transferSYT.js` so recipients get USDC, not sUSDC

## Stack

- Node.js scripts in `scripts/`
- Requires env vars: `AGENT_PRIVATE_KEY`, `RPC_URL`

## Key scripts

- `node scripts/getSYTBalance.js` — get sUSDC balance + underlying USDC value
- `node scripts/transferSYT.js <address> <amount>` — send USDC via sUSDC (recipient gets USDC)

## Important concepts

- **Rebasing:** sUSDC balance changes over time as yield accrues. Always report both nominal sUSDC and claimable underlying USDC.
- **Smart spending:** Always use `transferSYT.js` for sends — never raw USDC transfers. The script handles the unwrap so the recipient gets USDC.
