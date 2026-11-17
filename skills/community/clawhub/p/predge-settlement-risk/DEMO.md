# Demo transcript

Recorded 2026-10-05T08:28Z against the live API (https://api.predge.io). Real Polymarket markets, real UMA state on Polygon.

## 1. Live check: a market disputed twice, a clean market, a resolved market

```
$ python settlement_risk_check.py 4424722 will-luiz-incio-lula-da-silva-win-the-2026-brazilian-presidential-election 555793
Will Iran target an Arab country by September 30, 2026? (market 4424722)
  risk_level: caution  ->  gate: SKIP (contested_resolution, size x0.0)
  caution: disputed twice, the outcome goes to a UMA token-holder vote, second dispute 8.2 h ago; median 88.5 h from a second dispute to on-chain resolution (Polymarket, 2026-01-01 to 2026-10-02). Latest bulletin-board update (clarification) 8.5 h ago.
  UMA state: disputed, disputes: 2, open dispute: True, sent to UMA vote: True
  dispute: 2026-10-03T22:03:52Z (disputed proposal: Yes) tx 0xff35ff880b5b0f3a54629e84f9ff83782a5bea9cdf96ffd355edcb692ca29101
  dispute: 2026-10-05T00:13:41Z (disputed proposal: Yes) tx 0x13ca1f6774cac8be7b1b126a0ebe95e28b9b83b6f66aff6d19f84463950f968e
  latest bulletin-board update: clarification at 2026-10-05T00:00:02Z (question_creator)
  signature: verified (Predge key 13fa3d18)
  checked at 2026-10-05T08:27:32Z 

Will Luiz Inácio Lula da Silva win the 2026 Brazilian presidential election? (market 601819)
  risk_level: ok  ->  gate: ALLOW (ok, size x1.0)
  ok: no proposal, dispute or recent bulletin-board update on chain.
  UMA state: requested, disputes: 0, open dispute: False, sent to UMA vote: False
  signature: verified (Predge key 13fa3d18)
  checked at 2026-10-05T08:27:35Z 

Will Cardi B perform during the Super Bowl LX halftime show? (market 555793)
  risk_level: resolved  ->  gate: SKIP (already_resolved, size x0.0)
  resolved: the on-chain resolution is final (Yes); nothing is left to settle.
  UMA state: settled, disputes: 2, open dispute: False, sent to UMA vote: False
  dispute: 2026-02-09T02:34:47Z (disputed proposal: Yes) tx 0x64b1f22afeda4494120e780e53f197704482c138e872dd8090cd5e9aca1b682f
  dispute: 2026-02-09T03:35:15Z (disputed proposal: Yes) tx 0x0a60ff27a995641059c5b986997833041fb9724e03cab44ff94d389f8f0852ff
  latest bulletin-board update: clarification at 2026-02-09T04:18:27Z (question_creator)
  on-chain resolution: Yes
  signature: verified (Predge key 13fa3d18)
  checked at 2026-10-05T08:27:36Z 

```

## 2. Bundled records, including a proposal in its challenge window (no network)

```
$ python settlement_risk_check.py --demo
Will Luiz Inácio Lula da Silva win the 2026 Brazilian presidential election? (market 601819)
  risk_level: ok  ->  gate: ALLOW (ok, size x1.0)
  ok: no proposal, dispute or recent bulletin-board update on chain.
  UMA state: requested, disputes: 0, open dispute: False, sent to UMA vote: False
  signature: verified (Predge key 13fa3d18)
  checked at 2026-10-05T08:26:04Z 

Will Iran target an Arab country by September 30, 2026? (market 4424722)
  risk_level: caution  ->  gate: SKIP (contested_resolution, size x0.0)
  caution: disputed twice, the outcome goes to a UMA token-holder vote, second dispute 8.2 h ago; median 88.5 h from a second dispute to on-chain resolution (Polymarket, 2026-01-01 to 2026-10-02). Latest bulletin-board update (clarification) 8.4 h ago.
  UMA state: disputed, disputes: 2, open dispute: True, sent to UMA vote: True
  dispute: 2026-10-03T22:03:52Z (disputed proposal: Yes) tx 0xff35ff880b5b0f3a54629e84f9ff83782a5bea9cdf96ffd355edcb692ca29101
  dispute: 2026-10-05T00:13:41Z (disputed proposal: Yes) tx 0x13ca1f6774cac8be7b1b126a0ebe95e28b9b83b6f66aff6d19f84463950f968e
  latest bulletin-board update: clarification at 2026-10-05T00:00:02Z (question_creator)
  signature: verified (Predge key 13fa3d18)
  checked at 2026-10-05T08:25:58Z 

CE Sabadell FC vs. FC Andorra: CE Sabadell FC O/U 3.5 Corners (market 4748114)
  risk_level: watch  ->  gate: ALLOW (watch, size x0.5)
  watch: "Over" proposed, challenge window ends 2026-10-05T10:25:59Z; no dispute yet.
  UMA state: proposed, disputes: 0, open dispute: False, sent to UMA vote: False
  proposal: Over at 2026-10-05T08:25:59Z, challenge window ends 2026-10-05T10:25:59Z
  signature: verified (Predge key 13fa3d18)
  checked at 2026-10-05T08:26:28Z 

Will Cardi B perform during the Super Bowl LX halftime show? (market 555793)
  risk_level: resolved  ->  gate: SKIP (already_resolved, size x0.0)
  resolved: the on-chain resolution is final (Yes); nothing is left to settle.
  UMA state: settled, disputes: 2, open dispute: False, sent to UMA vote: False
  dispute: 2026-02-09T02:34:47Z (disputed proposal: Yes) tx 0x64b1f22afeda4494120e780e53f197704482c138e872dd8090cd5e9aca1b682f
  dispute: 2026-02-09T03:35:15Z (disputed proposal: Yes) tx 0x0a60ff27a995641059c5b986997833041fb9724e03cab44ff94d389f8f0852ff
  latest bulletin-board update: clarification at 2026-02-09T04:18:27Z (question_creator)
  on-chain resolution: Yes
  signature: verified (Predge key 13fa3d18)
  checked at 2026-10-05T08:26:05Z 

```

## 3. Bad input fails closed

```
$ python settlement_risk_check.py 0x1234
0x1234: SKIP (state_unavailable): HTTP 400: bad_market Pass a Polymarket condition id (0x + 64 hex), a numeric market id, or a market slug.

```

## 4. Raw call, no SDK

```
$ curl -s https://api.predge.io/v1/settlement-risk/4424722 | jq "{risk_level, dispute_count, sent_to_uma_vote, recommendation}"
{
  "risk_level": "caution",
  "dispute_count": 2,
  "sent_to_uma_vote": true,
  "recommendation": "caution: disputed twice, the outcome goes to a UMA token-holder vote, second dispute 8.2 h ago; median 88.5 h from a second dispute to on-chain resolution (Polymarket, 2026-01-01 to 2026-10-02). Latest bulletin-board update (clarification) 8.5 h ago."
}
```
