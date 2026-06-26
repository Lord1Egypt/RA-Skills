# Feature Gating Thresholds

Partner apps should use both score and confidence.

| Feature | Minimum Score | Required Confidence |
|---|---:|---|
| Public profile visible | 500 | low |
| Basic verified badge | 600 | moderate |
| Creator payment trust badge | 675 | moderate |
| Trusted seller badge | 700 | moderate |
| Escrow fast-lane | 725 | moderate or high |
| Partner API trusted label | 725 | high |
| Elite profile badge | 800 | high |
| Manual review bypass | 750 | high |
| High-value transaction recommendation | 775 | high |

## Rules

1. Never use score alone for high-value or high-risk decisions.
2. Low-confidence wallets should not receive elite partner labels.
3. Severe unresolved risk flags override normal feature gates.
4. Partners may choose stricter thresholds.
5. GwapScore should return explanations for gating decisions.
