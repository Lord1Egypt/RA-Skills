# Fusion methodology

## Evidence boundaries

The report separates factual consensus, numeric reputation estimates, unscored signals, and
contextual network exposure. A provider failure is never negative evidence. Provider definitions and
refresh times differ, so source identity, observation time, and disagreement remain visible.

The public interface accepts one public IP only. It does not ingest customer or account logs,
cookies, device identifiers, or batches. External mode sends the target IP only, after confirmation.

## Facts

The fusion layer compares country, region, city, ASN, organization, ISP, network type, allocation
prefix, route prefix, and registry country. It does not collect personalized hostnames or RDAP
contact fields. A leading value is consensus only when at least two sources support it without a tie;
otherwise it is single-source or disputed and alternatives remain available.

Registry country and allocation prefix are kept separate from geolocation country and observed BGP
route prefix. RDAP output is limited to registration organization, allocation prefix, registry country,
and the fields needed for registry/routing interpretation. It does not retain `fn`, email, or abuse
contacts.

## Numeric reputation risk

Only an upstream numeric risk, fraud, abuse, or trust score enters the composite. `ipdata` trust is
converted explicitly as `100 - trust_score` and marked `derived-from-trust-score`; other accepted
numbers are marked `native`.

Never convert `is_abuser`, `recent_abuse`, `is_bot`, proxy, VPN, Tor, hosting, blacklist, or other
boolean labels into invented numeric scores. Preserve direct abuse and bot booleans as
`unscored_signals`:

- `single-source`: one positive source and no negative source;
- `corroborated`: at least two positive sources and no negative source;
- `disputed`: positive and negative sources both exist.

Unscored signals do not change the composite or numeric confidence.

The current relative weights are:

| Source | Weight |
|---|---:|
| IPQualityScore | 1.00 |
| Scamalytics, AbuseIPDB | 0.95 |
| ipdata | 0.90 |
| proxycheck.io | 0.85 |
| ipapi.is | 0.80 |
| IPinfo | 0.75 |
| Ping0.cc | 0.70 |

Validated official public-page numeric evidence receives 90% of the corresponding source weight.
The weighted mean receives an uplift of 8 for two scores at least 70 or 15 for three or more, then
is capped at 100. One source cannot create numeric consensus.

Risk levels are low (0-29), guarded (30-49), elevated (50-69), high (70-84), and critical (85-100).
With no numeric estimate, score and level are `unknown`, even when contextual flags exist.

## Confidence and action

Use low confidence for one numeric source; normally medium for two; use high for at least three that
broadly agree. Lower confidence as dispersion grows. Missing credentials reduce coverage but do not
increase risk. Material conflicts require human review and should not drive irreversible automation.

## Presentation states

Keep `success`, `skipped`, `not-requested`, `unavailable`, `error`, successful-without-score, and
boolean-only signal states distinct. No state is rendered as a zero score. HTML and Markdown show the
network mode and the `not-requested` count so a local report cannot be mistaken for a completed
external investigation.
