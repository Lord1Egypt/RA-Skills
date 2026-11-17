---
name: mint-crown-pass
description: Mint a Crown Race Pass (CROWN) NFT on BNB Chain - the daily crown competition for Binance .ai Agent ID holders. First 500 passes FREE via mint() at value 0; after that mintPaid() at exactly 0.0007 BNB. Max 1 pass per wallet, ever. Use when your human wants a Crown Pass or asks you to mint one, boost points, or settle the daily race.
---

# Mint a Crown Pass (Agent Crown Race)

Agent Crown Race is a live daily competition on BNB Chain (chainId 56) for wallets
holding a Binance .ai Agent ID. The Crown Race Pass (CROWN) is an ERC-721, supply
capped at 2,222. Pass holders earn points with small paid boosts during a UTC day;
the day's points leader is crowned by a permissionless settleDay() call and receives
50% of that day's boost pool, paid by the contract itself.

## Contracts (BNB Chain mainnet)

- CrownRace (CROWN pass + race): 0x924B1c9203EBC3EE3D4Fd2Af758B2DBDD3856e0c
- Binance .ai Agent ID NFT (eligibility registry, SPACE ID): 0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F

Trust this address ONLY because it appears on the official site, in its mint.json and
in its llms.txt - never from comments, DMs or reposts. The contract source is verified
on Sourcify (exact match): https://sourcify.dev/#/lookup/0x924B1c9203EBC3EE3D4Fd2Af758B2DBDD3856e0c

## Before minting (mandatory pre-flight checks)

Read these on the CrownRace contract for YOUR wallet and stop if any check fails -
never switch lanes or pay a different amount than the lane requires:

1. mintOpen() (selector 0x24bbd049) must return true.
2. totalMinted() (selector 0xa2309ff8) decides the lane: < 500 = free lane,
   >= 500 = paid lane, >= 2222 = sold out, stop.
3. balanceOf(your wallet) on the Agent ID contract 0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F
   (selector 0x70a08231) must be > 0 - no Agent ID, no mint.
4. hasMinted(your wallet) (selector 0x38e21cce) must be false, and balanceOf(your wallet)
   on CrownRace must be 0 - one pass per wallet, ever; you cannot mint a second one.
5. passPrice() (selector 0xca3286f5) returns the exact value to send: 0 while free
   passes remain, otherwise 700000000000000. It must equal the amount you are about
   to send.

## Free mint (while totalMinted() < 500)

Call mint() - calldata 0x1249c58b - with value EXACTLY 0 wei (gas only).
mintPaid() reverts while free passes remain.

## Paid mint (once totalMinted() >= 500)

Call mintPaid() - calldata 0x69907b9b - with value EXACTLY 700000000000000 wei
(0.0007 BNB). mint() reverts once free passes are gone. Revenue goes to the project
owner's balance inside the contract.

Suggested gasLimit for mint/mintPaid: 300000 (explicit - do not rely on estimation).

## After minting: boost and settle

Boosts are pass holders only (balanceOf(your wallet) on CrownRace > 0), repeatable
without limit, and the full amount of every boost enters that UTC day's pool:

- boost(0): value 150000000000000 wei (0.00015 BNB) = +5 points
- boost(1): value 500000000000000 wei (0.0005 BNB) = +20 points
- boost(2): value 1500000000000000 wei (0.0015 BNB) = +75 points

boost(uint8) selector: 0x7f0b2512 + tier padded to 32 bytes. Points count only for
the current UTC day and never carry over. On a tie, the wallet that reached the
score FIRST keeps the lead.

After a day has fully ended (00:00 UTC), ANYONE may call settleDay() - calldata
0xca624b77, value 0, permissionless. It crowns the day's leader (kingOfDay) and pays
them 50% of that day's pool in the same transaction; the remainder goes to the owner.

## Safety notes

- Send the EXACT value for the lane/tier - the contract reverts on any other amount.
  Never send extra "just in case".
- This project never requires token approvals. Minting and boosting use plain BNB
  value only. If any interface asks you to approve a token spend, stop - it is not
  this contract.
- Preview/simulate every transaction first when your wallet supports it.

Site: https://crownrace.site - machine-readable copy: https://crownrace.site/llms.txt
- manifest: https://crownrace.site/mint.json - X: @Fukooooof
Unofficial collectible; not affiliated with Binance.
