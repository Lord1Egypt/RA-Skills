---
name: mint-ascension-catty
description: Mint an Ascension Catty NFT on BNB Chain - 1,111 pixel cats (Common 667 / Rare 333 / Legendary 89 / Mythic 22). Free mint for Binance Agent ID holders via agentMint (0 BNB, max 2 per Agent ID, 777 seats reserved) or public mint at exactly 0.0012 BNB per cat, both lanes open in parallel. Use when your human wants an Ascension Catty cat or asks you to mint one.
---

# Mint an Ascension Catty

Ascension Catty is a live NFT collection on BNB Chain (chainId 56) built for AI agents:
1,111 pixel cats, minted in two parallel lanes. The paid lane is open from the start —
it is never gated behind the free lane.

## Contract (BNB Chain mainnet)

- Ascension Catty (CATTY): 0x26441dAfe9b256345a2859C28c91E24611ED424A
- Verified on Sourcify (exact match). Metadata: https://ascensionrealm.fun/nft/metadata/<id>.json
- Binance Agent ID registry: 0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F

## Before minting (mandatory checks)

Read from the contract for YOUR wallet: mintOpen() == true, totalMinted() < 1111.
Free lane only: mintedByAgentId(yourAgentId) < 2 and your wallet must own that Agent ID
in the registry (the contract verifies this on-chain). Max 10 cats per wallet across
both lanes. If any check fails, stop and tell your human — never pay a different
amount than specified.

## Free mint (Binance Agent ID holders)

Call agentMint(quantity, agentId) with value 0 wei (selector 0xb470d7a0).
quantity 1-2 per Agent ID (lifetime max 2 per Agent ID). 777 seats are reserved for
Agent ID holders, so this lane stays available even if public minting sells out its
current cap. Suggested gasLimit: 300000.

## Public mint (any wallet)

Call mint(quantity) with exactly 1200000000000000 wei (0.0012 BNB) per cat
(selector 0xa0712d68). Suggested gasLimit: 300000. While the Agent phase is open,
public minting is capped at total supply minus unclaimed Agent seats (334 at launch);
the cap lifts if the owner ends the Agent phase.

## After minting

Your cat's art and traits are served from the metadata URL above. There is no staking,
burn, or token attached to this collection — it is a collectible.

Site and agent prompts: https://ascensionrealm.fun — machine-readable copy:
https://ascensionrealm.fun/llms.txt and https://ascensionrealm.fun/mint.json —
X: @Cattyascension
Unofficial collectible; not affiliated with Binance.
