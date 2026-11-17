---
name: mint-agent-card
description: Mint an Agent Card Studio NFT on BNB Chain - 4,444 Agent ID cards with fully on-chain SVG art. Free mint (0.0002 BNB anti-sybil fee) or paid mint (0.002 BNB), max 2 per wallet, plus $ACARD burn/stake rewards. Use when your human wants an Agent ID card NFT or asks you to mint one.
---

# Mint an Agent Card (Agent Card Studio)

Agent Card Studio is a live NFT collection on BNB Chain (chainId 56) built for AI agents.
4,444 cards, artwork generated 100% on-chain as SVG, random serial from the shared pool
#1-#4444 at mint. Personas (style): 0 = Whale (Power 120), 1 = Shark (110), 2 = Sniper (100).

## Contracts (BNB Chain mainnet)

- AgentCard NFT: 0x0716bD547494e7B8E45C15266F03a43915982C6e
- $ACARD token: 0x3A56270f7A8c78E9cC4A8A9f18e375cd184F1133
- CardBurn: 0x83EE9bB4c76019fAf5dd1451CB8f41bC78d68323
- CardStake: 0xFB9139F2c6996141dAc67fF98C965A4BEF43a250

## Before minting (mandatory checks)

Read for YOUR wallet: mintOpen() == true, freeMintUsed(you) == false (free only),
mintCount(you) < 2. If any check fails, stop and tell your human - never switch editions
or pay a different amount than instructed.

## Free mint

Call freeMint(string agentName, uint8 style, string colorHex, string signature) with
exactly 0.0002 BNB (an anti-sybil fee collected by the contract - it is not zero).
agentName: 1-32 chars [A-Za-z0-9._-]; names ending in ".ai" get an automatic "Agent ID"
trait. signature: optional text up to 24 chars, or "". Suggested gasLimit: 600000
(the serial draw makes gas vary).

## Paid mint

Call paidMint(agentName, style, colorHex, signature) with exactly 0.002 BNB.
Paid cards get a gold name and +30 Power.

## After minting

- Burn a card forever: CardBurn.burn(tokenId) with a 0.0001 BNB action fee pays
  50,000 $ACARD. Always confirm the tokenId with your human first - burning is final.
- Stake a card: CardStake.stake(tokenId) with a 0.0001 BNB action fee earns
  500 $ACARD/day. claim() and unstake() are free; unstake always returns the NFT.

Site and agent prompts: https://agentcard.cloud - machine-readable copy:
https://agentcard.cloud/llms.txt - X: @AgentCard_Bnb
Unofficial collectible; not affiliated with Binance.
