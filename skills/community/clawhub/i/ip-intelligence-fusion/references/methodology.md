# Fusion methodology

## Evidence boundaries

Separate factual consensus, numeric reputation estimates, unscored reputation signals, and
contextual network exposure. A provider failure never becomes negative evidence. Provider
meanings and refresh times differ, so preserve source identity and disagreement.

Country geolocation is not registry country. RDAP allocation prefix is not BGP route prefix.
Hosting, VPN, proxy, Tor, and bot classifications describe exposure or context and do not by
themselves prove malicious activity.

## Facts

Group normalized country, region, city, ASN, organization, ISP, network type, allocation prefix,
route prefix, and reverse DNS values. Call a leading value consensus only when at least two sources
support it without a tie. Otherwise label it single-source or disputed and retain alternatives.

## Numeric reputation risk

Only an upstream numeric risk, fraud, abuse, or trust score participates in the composite.
`ipdata` trust is converted explicitly as `100 - trust_score` and marked
`derived-from-trust-score`; all other accepted numbers are marked `native`.

Never convert `is_abuser`, `recent_abuse`, `is_bot`, crawler, blacklist, proxy, VPN, Tor, hosting,
or other booleans into invented numeric scores. Preserve direct abuse and bot booleans as
`unscored_signals`:

- `single-source`: exactly one positive source and no negative source;
- `corroborated`: at least two positive sources and no negative source;
- `disputed`: positive and negative sources both exist.

Unscored signals do not change the composite, confidence, or numeric corroboration uplift. Show
them in the risk signal area, conflicts, and provider detail.

Numeric relevance weights are:

| Source | Weight |
|---|---:|
| IPQualityScore | 1.00 |
| Scamalytics, AbuseIPDB | 0.95 |
| ipdata | 0.90 |
| proxycheck.io | 0.85 |
| ipapi.is | 0.80 |
| IPinfo | 0.75 |
| Ping0.cc | 0.70 |
| IP-API | 0.60 |

Official public-page numeric evidence receives 90% of the source's API weight. Compute the
reliability-weighted mean, then add 8 for two numeric estimates at least 70 or 15 for three or
more. Cap the result at 100. One source cannot create numeric consensus.

Risk levels are low (0-29), guarded (30-49), elevated (50-69), high (70-84), and critical
(85-100). With no numeric estimate, score and level are `unknown` even when unscored signals exist.

## Confidence and action

Use low confidence for one numeric source; normally medium for two; use high for at least three
that broadly agree. Lower confidence as dispersion grows. Missing keyed sources reduce coverage
but do not increase risk.

- Low or guarded: say the successful scored set returned no strong numeric risk evidence.
- Elevated: recommend contextual verification or step-up controls.
- High or critical: recommend blocking or manual investigation according to the user's threat model.
- Unknown: obtain more scored evidence before a numeric decision.
- Any material conflict: avoid irreversible automation based only on the composite.

## Presentation states

Never collapse distinct non-numeric outcomes into a generic zero-like row. Keep not collected,
unavailable, failed, successful without a numeric field, and boolean-only signal states explicit.
None receives a numeric bar, and none is interpreted as zero risk.
