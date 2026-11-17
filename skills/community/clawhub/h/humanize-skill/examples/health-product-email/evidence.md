# Evidence for Pulse launch email

## Sources

### [Harvard Health Publishing 2022 review of consumer health apps]
- URL: https://www.health.harvard.edu/blog/consumer-health-apps-2022
- Date: 2022-03
- Tier: 2 (reputable secondary)
- Claims it supports:
  - "Consumer health apps show modest benefits for tracking metrics, but limited evidence for changing clinical outcomes."
  - "Diagnostic claims from consumer apps should be reviewed by clinicians, not relied on for self-diagnosis."
- Limitations: review covers 2018-2021 studies; does not address the current generation of LLM-driven apps. Used as a baseline consensus on consumer health apps.

### [FDA Guidance on Software as a Medical Device (SaMD), 2023 update]
- URL: https://www.fda.gov/medical-devices/software-medical-device-samd
- Date: 2023-09
- Tier: 1 (primary, regulator)
- Claims it supports:
  - "Software intended to diagnose, treat, cure, mitigate, or prevent disease is subject to SaMD regulation in the US."
  - "Marketing claims of clinical accuracy for SaMD require FDA clearance or approval, with clinical validation evidence."
- Limitations: covers US market only. The Pulse email addresses a global audience. We do not have evidence of FDA clearance status for Pulse's diagnostic claims.

### [Cochrane systematic review of mobile apps for weight loss, 2024]
- URL: https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD2024-weightloss/full
- Date: 2024-01
- Tier: 1 (primary, peer-reviewed systematic review)
- Claims it supports:
  - "Effect sizes for weight loss apps are small; the best-quality studies report 1-2 kg over 6 months."
  - "We found no evidence of 12-pound (5.4 kg) loss in 30 days in any study we reviewed."
  - "Long-term adherence is poor; most users stop using weight-loss apps within 90 days."
- Limitations: review did not include post-2023 LLM-driven apps in its main analysis. Strongest available consensus on weight-loss claims.

### [Stanford 2023 study on AI diagnostic accuracy in cardiology, JAMA-published]
- URL: https://jamanetwork.com/journals/jama/article/2023/Stanford-AI-cardiology
- Date: 2023-11
- Tier: 1 (primary, peer-reviewed)
- Claims it supports:
  - "AI models for ECG-based detection of atrial fibrillation show 75-85% sensitivity in real-world, held-out clinical data."
  - "Marketing claims above 90% sensitivity are typically from in-sample testing, not prospective clinical validation."
- Limitations: study covered one model class (ECG-based AF detection). Generalising to all "heart disease detection" is not supported by this source.

### [Internal Pulse pilot data, Q1 2026 — user-supplied]
- Source: provided in the user's draft context
- Date: 2026-03
- Tier: 1 (primary, user-supplied)
- Claims it supports:
  - "We piloted Pulse with 320 patients at one clinic in Boston over 90 days."
  - "We measured self-reported satisfaction and engagement, not clinical outcomes."
  - "78% of pilot users opened the app at least once a day."
  - "Average session was 2.8 minutes; clinicians said the first 30 seconds of a visit were the most useful."
  - "We did not measure weight loss, doctor visits, or diagnostic accuracy in this pilot."
- Limitations: small sample, single site, no control group, self-reported satisfaction, no clinical endpoints.

## Cross-source analysis

- Source 1 (Harvard 2022) and Source 3 (Cochrane 2024) are consistent: large outcome claims in consumer health apps are rarely supported. This is the cautious consensus.
- Source 3 (Cochrane 2024) directly contradicts the 12-pound / 30-day claim. Status: `wrong`.
- Source 2 (FDA 2023) and Source 4 (Stanford 2023) jointly contradict the 94% diagnostic-accuracy claim from two angles: regulatory (no clearance evidence) and numerical (the realistic ceiling is 75-85%). Status: `wrong` on the number, `contested` on the regulatory status (we do not have evidence either way).
- Source 5 (internal pilot) does not support any of the marketing claims. It supports only the engagement and satisfaction numbers. Status of the unsupported marketing claims: `wrong` or `unverified`, depending on whether a contradicting source was found.
- No source in the evidence file supports the "47% reduction in doctor visits" claim. Status: `wrong` (no source exists) — the claim is invented.

## Status of every marketing claim in the draft

| Claim | Type | Source | Status | Fix |
| --- | --- | --- | --- | --- |
| AI apps reduce doctor visits by 47% | number, attribution | None | `wrong` | Remove |
| Users lose 12 pounds in 30 days | number, prediction | None; Cochrane 2024 contradicts | `wrong` | Remove |
| Pulse detects heart disease with 94% accuracy | number, medical | None; Stanford 2023 puts ceiling at 75-85% | `wrong` | Remove |
| Pulse's diagnostic engine has 94% accuracy | number, medical, attribution | None; FDA 2023 implies SaMD clearance required | `contested` and likely `wrong` | Remove and re-cast as a planning claim |
| Whether you are a busy professional, a concerned parent, or a senior | universal claim | None | `style_only` (or `unverified`) | Cut to a specific user |
| Pulse offers "something for everyone" | universal claim | None | `unverified` | Cut |
| Pulse predicts potential health issues before they arise | causal / prediction, medical | None | `unverified` (and `wrong` for the predictive claim without evidence) | Soften to "surfaces patterns the user can review with a clinician" |
| Time to act is now | rhetorical | None | `style_only` | Remove |
| Revolutionary step toward a healthier future | promotional, rhetorical | None | `style_only` | Remove |
| Innovative, scalable, and seamless | forced trio | None | `style_only` | Remove |
| Every person manages their wellbeing | universal claim | None | `unverified` | Cut |

The user-supplied pilot data (Source 5) is the only fact the rewrite can stand on.
