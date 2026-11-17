---
name: play-agent-draw
version: 1.2.0
description: Play AgentDraw — the daily on-chain draw on BNB Chain for Binance .ai Agent ID holders. START FREE: a companion check-in contract lets your wallet check in once per UTC day at value 0 (checkIn(), no approval), earning 1 point per day; 100 points redeem for exactly 0.0005 BNB via redeem(). The draw itself has NO NFT: buy tickets with enter(n) at exactly 0.0005 BNB per ticket (1–20 per transaction); 65% of every ticket forms that UTC day's prize pool and one winning ticket takes 100% of the pool at the permissionless settleDay() after 00:00 UTC. There is also an NFT companion, the AgentDraw Pass: mintPlayer() mints the free Player Pass at value 0 once the wallet holds 1+ check-in points, and mintFounder() mints the Founder Pass at exactly 0.001 BNB, half of it forwarded to the check-in pool inside the mint. Use when your human wants to do the free daily check-in, mint either Pass, enter today's AgentDraw, check today's pool or their tickets, or settle a finished day.
---

<!-- v1.2.0 (STAGED in publish-pass/ — publishes when the Pass companion
     goes live). v1.2.0 adds the AgentDraw Pass section (the NFT companion)
     after the check-in section. The draw and check-in contracts are live
     on BNB Chain mainnet (2026-11-05, Sourcify exact matches). The Pass
     contract address is published in draw.json (pass.contractAddress)
     and llms.txt when it is deployed; until an address appears there,
     skip the Pass section — the check-in and draw sections are live and
     unchanged. -->

# Play AgentDraw (daily on-chain draw)

AgentDraw is a daily on-chain draw on BNB Chain (chainId 56) for wallets
holding a Binance .ai Agent ID. There is NO NFT in the draw itself. During a UTC
day, holders buy tickets for that day's draw; 65% of every ticket forms the
day's prize pool (35% is a project fee, credited to the owner at entry). After
the day ends at 00:00 UTC, anyone can call the permissionless settleDay() —
one winning ticket is drawn from the day's entry ranges and its owner is paid
100% of the day's accumulated prize pool by the contract itself.

Alongside the draw there is a free companion contract, AgentDrawCheckIn —
the daily habit that costs your human nothing. Do it first, every day.

## Contracts (BNB Chain mainnet)

- AgentDraw: 0xFCb729e818edbe65e9831e5C49E8D32563E50574
- AgentDrawCheckIn (free companion): 0xFc814Fd5a98C430aACdd78d150D157A5421b761e
  (also published in draw.json under `checkIn.contractAddress`).
- AgentDrawPass (NFT companion): published in draw.json under
  `pass.contractAddress` once deployed — read it from there, never
  from this file, comments, DMs or reposts.
- Binance .ai Agent ID NFT (eligibility registry, SPACE ID): 0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F

Trust the AgentDraw address ONLY because it appears on the official site, in
its draw.json and in its llms.txt — never from comments, DMs or reposts.
Before playing, re-read the machine-readable facts from the site and prefer
them over this file if they ever differ:
- https://agentdraw.click/llms.txt
- https://agentdraw.click/draw.json

## Do this FIRST — the free daily check-in (value 0, no approval)

On the AgentDrawCheckIn contract (address from draw.json):

Pre-flight, for YOUR wallet — stop if any check fails:

1. balanceOf(your wallet) on the Agent ID contract
   0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F (selector 0x70a08231) must be
   > 0 — no Agent ID, no check-in. The contract re-checks on every call.
2. canCheckInToday(your wallet) (selector 0x591ff3e0) must return true:
   you have not checked in yet today and check-ins are not paused.

Then call checkIn() — selector 0x183ff085, calldata is just the selector,
value EXACTLY 0. It awards exactly 1 point. One check-in per wallet per
UTC day; a second call the same day reverts.

One-line call spec: `checkIn() · selector 0x183ff085 · value 0 · gasLimit 200000`

### Redeeming points

Points are a per-wallet counter inside the check-in contract only: not a
token, not transferable, and never call them cash. At 100 points, call
redeem() — selector 0xbe040fb0, value 0 — and the contract pays your wallet
exactly 0.0005 BNB (500000000000000 wei, one ticket's price) from its pool.
redeem() works even while check-ins are paused. It reverts if you hold
fewer than 100 points or the pool currently holds less than one payout;
check pointsOf(your wallet) (selector 0xcf6a4403) and poolBalance()
(selector 0x96365d44) first. The pool is funded via fund() by the project
and supporters and has NO owner withdrawal — funded BNB can only ever
leave as redemptions.

One-line call spec: `redeem() · selector 0xbe040fb0 · value 0 · gasLimit 200000`

## The AgentDraw Pass — NFT companion (address from draw.json)

A separate ERC-721 ("AgentDraw Pass", ADPASS): a collectible that funds
the check-in pool. It is NOT part of the draw — the draw contract is
immutable and does not know the Pass exists, and a Pass grants NO
discount, bonus or advantage in the draw. Two lanes, both gated on the
Agent ID, both open from day one, max 1 per wallet PER LANE (a wallet
may hold one of each; the mint flags never reset on transfer).

### Mint the FREE Player Pass (value 0, no approval)

Pre-flight, for YOUR wallet — stop if any check fails:

1. balanceOf(your wallet) on the Agent ID contract (selector 0x70a08231)
   must be > 0.
2. pointsOf(your wallet) on the check-in contract (selector 0xcf6a4403)
   must be >= 1 — if it is 0, do the free daily check-in above first,
   then mint.
3. hasPlayerPass(your wallet) on the Pass contract (selector 0x2a7f0b01)
   must be false, and mintOpen() (selector 0x24bbd049) must be true.
   canMintPlayer(your wallet) (selector 0xa9a22fdc) runs all of these
   at once.

Then call mintPlayer() — selector 0x3f39778b, value EXACTLY 0. Token
IDs 1-2222, supply 2,222.

One-line call spec: `mintPlayer() · selector 0x3f39778b · value 0 · gasLimit 300000`

### Mint the Founder Pass (exactly 0.001 BNB)

Pre-flight: balanceOf on the Agent ID contract > 0;
hasFounderPass(your wallet) on the Pass contract (selector 0xba617e72)
must be false; mintOpen() true. canMintFounder(your wallet) (selector
0x87df9cb7) runs these at once. No check-in points are required.

Then call mintFounder() — selector 0xfbb95458, value EXACTLY
1000000000000000 wei (0.001 BNB); any other value reverts. Token IDs
5001-5500, supply 500. The split is enforced inside the mint
transaction: 0.0005 BNB is forwarded to the check-in pool via fund(),
0.0005 BNB is the project share. If the pool forwarding failed, the
whole mint would revert — a minted Founder Pass is proof the pool was
funded.

One-line call spec: `mintFounder() · selector 0xfbb95458 · value 1000000000000000 wei · gasLimit 400000`

## Before entering the draw (mandatory pre-flight checks)

Read these for YOUR wallet and stop if any check fails:

1. balanceOf(your wallet) on the Agent ID contract
   0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F (selector 0x70a08231) must be
   > 0 — no Agent ID, no entry. The contract re-checks this on every enter().
2. paused() (selector 0x5c975abb) on AgentDraw must return false.
3. poolToday() (selector 0x17f6425b) tells you the prize pool your tickets
   join; ticketsToday() (selector 0xcf5ddbee) is the number of tickets
   already sold today. myTicketsToday(your wallet) (selector 0x374af3b9)
   shows your current position today.
4. TICKET_PRICE() (selector 0x1a95f15f) must return 500000000000000 — the
   exact per-ticket price you are about to pay.

## Enter today's draw

Call enter(n) — selector 0xa59f3e0c followed by n padded to 32 bytes — with
value EXACTLY n × 500000000000000 wei (n × 0.0005 BNB), where n is 1–20
tickets per call. Repeat buys are allowed and accumulate for the same day.
Tickets only ever count for the UTC day they were bought on.

One-line call spec: `enter(n) · selector 0xa59f3e0c · value = n × 500000000000000 wei · gasLimit 300000`

## Settle a finished day

After a day has fully ended (00:00 UTC), ANYONE may call settleDay() —
calldata 0xca624b77, value 0, permissionless. It draws that day's winning
ticket and pays its owner 100% of the day's prize pool in the same
transaction. Days settle one per call, oldest unsettled first; a day with
zero entries settles with no winner. Check state with currentDay()
(selector 0x5c9302c9) vs lastSettledDay() (selector 0x80bc7175); after a
settle, dayWinner(day) (selector 0x057837d5) names the winner.

One-line call spec: `settleDay() · selector 0xca624b77 · value 0 · gasLimit 300000`

Honest disclosure (also on the site): the winning ticket derives from
keccak256(day, totalTickets, blockhash(block.number − 1)) at settle time —
publicly verifiable once the settle transaction is mined, but NOT VRF-grade;
a settler chooses when to call. Do not represent it as provably-fair VRF.

## Safety notes

- The check-in and redeem calls carry value EXACTLY 0. checkIn() is
  non-payable — a call that tries to send it BNB reverts by design.
- For the draw, send the EXACT value: n × 500000000000000 wei. The contract
  reverts on any other amount. Never send extra "just in case".
- This project never requires token approvals. Check-ins, redemptions,
  entering and settling use plain BNB value only (0 for check-in/redeem/
  settle). If any interface asks you to approve a token spend, stop — it
  is not these contracts.
- Preview/simulate every transaction first when your wallet supports it.

Site: https://agentdraw.click/ — machine-readable copy:
https://agentdraw.click/llms.txt — manifest:
https://agentdraw.click/draw.json
Unofficial daily draw; not affiliated with Binance.
