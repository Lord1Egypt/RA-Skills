# Safety Guardrails

## 15. SAFETY GUARDRAILS (NON-NEGOTIABLE)

### The Golden Rule: PAUSE, Never Delete

> **Never delete campaigns, ad sets, ads, audiences, or pixels.** Meta's algorithm learns from historical data attached to every object. Deleted objects lose their optimization history forever. Paused objects retain it.

```
CORRECT:  ads_activate_entity(status: PAUSED) on underperforming campaigns/ad sets/ads
INCORRECT: Any delete operation on live or historical campaign entities
```

### Additional Safety Rules

| Rule | Why |
|---|---|
| Always create campaigns in **PAUSED** status | Prevents accidental spend before review |
| Never increase budget by more than **20% at a time** | Larger jumps reset the Learning Phase |
| Never run campaigns without a **verified Pixel** | No conversion data = no optimization |
| Never edit targeting, creative, or budget simultaneously | Isolate variables so you know what changed performance |
| Never touch campaigns in **Learning Phase** (first 7 days / ~50 events) | Edits extend or restart learning |
| Keep **account spending limit** set in billing | Prevents runaway spend from bugs or errors |
| Always **preview ads** before activating | Catches broken URLs, wrong pages, copy errors |
| Never use **personal ad accounts** for business campaigns | No access controls, billing risk |
| **Document every change** in the campaign's Decisions Log | Creates audit trail, enables learning over time |
| For special ad categories (housing, credit, employment, political) — **declare them** | Non-declared special categories can cause account suspension |

### Account Health Rules
- Maintain **ad account policy compliance** — avoid prohibited content in any ad
- If an ad is **rejected**, review the policy reason before resubmitting. Don't just re-upload identical creative.
- If an **account is flagged or restricted**, immediately contact Meta Business Support — do not attempt workarounds
- Keep **payment method verified** and up to date
- **Verify identity** in Business Manager to unlock full capabilities

## Data & privacy (non-negotiable)

- Never upload customer email/phone, or send PII via CAPI, without a documented lawful basis and consent.
- Always SHA‑256 hash email/phone before transmission — never plaintext.
- Minimize data; honor opt-outs and right-to-be-forgotten; maintain suppression lists.
- Operate under Meta's Data Processing Terms; account for EU/UK data-residency.
- Special ad categories (housing, employment, credit, social/political issues) carry extra targeting and privacy restrictions — confirm eligibility and rules before launching.
