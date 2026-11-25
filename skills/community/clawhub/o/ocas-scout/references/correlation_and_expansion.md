# Scout: Cross-Site Correlation, Recursive Expansion & Domain Verification

Three capabilities that extend Scout from a sweep tool into a graph investigation. All are stdlib-only; Pillow is optional for avatar hashing.

## 1. Cross-site correlation (`correlate_profiles.py`)

Cluster profiles that look like the same person across sites. Operates on the structured profiles from `profile_extract.py` (or a research result JSON), not on raw names.

### Signals

| Signal | Strength | Requires |
|---|---|---|
| Avatar dHash (64-bit, Hamming ≤ 8) | highest | Pillow |
| Shared external URL in bio | highest | bio text |
| Structured name equality | medium | `name_from_profile: true` |
| Bio Jaccard token overlap (≥ 0.5) | low–medium | bio text |

Every edge records which signals produced it, so a brief can state *why* two profiles were joined. Clusters are labeled high/medium/low strength. Avatar hashing degrades gracefully — without Pillow, correlation falls back to link/name/bio signals and notes it.

### Avatar safety

Avatar URLs are scraped from the target page, so they point wherever the page owner chooses. Before any download, the URL host is resolved and every address must be public — cloud metadata endpoints, loopback, and private addresses are refused. `--allow-private` disables this for lab-network scanning on purpose.

```bash
python3 correlate_profiles.py --input research_result.json --format concise
python3 correlate_profiles.py --input research_result.json --no-avatars
python3 correlate_profiles.py --input research_result.json --allow-private
```

## 2. Recursive handle expansion (`recurse_expand.py`)

Mines linked usernames out of profile bios (`@mentions` and profile URLs on handle-bearing hosts) and emits them as a NEW pass of handle candidates. This is the graph step that a linear Sherlock → Maigret sweep cannot do.

### Invariant 9: hard cap of TWO passes

The script structurally enforces a single additional pass. A request to expand pass 2 is refused with `recursion_cap`; it does not emit a third pass even if the bios contain more handles. The cap is safety, not optimization — username chains converge on noise and each pass multiplies cost. Every candidate carries its sources (which bios observed it), and candidates observed in two independent bios are marked `corroborated`.

### Handles are leads, not identities

A handle found in a bio is a *lead*. It enters synthesis only after the identity gate (invariant 7: 2+ independent data points) is satisfied. The script's action guidance always says so.

```bash
# Pass 1: emit pass-2 candidates from found profiles
python3 recurse_expand.py --input result.json --pass 1 --format concise

# Pass 2: stop here — cap reached
python3 recurse_expand.py --input result.json --pass 2
# → refused (recursion cap), actionable_guidance to finish

# Track already-scanned handles to avoid re-reporting
python3 recurse_expand.py --input pass1.json --pass 1 --known oldhandle,mirrorhandle

# Write candidates for the next scan pass
python3 recurse_expand.py --input result.json --pass 1 --out pass2_candidates.json
```

## 3. Domain availability check (`domain_check.py`)

Tests whether `<username>.<tld>` is registered and live, using DNS resolution + HTTP only. No whois API, no key, no rate limit beyond the targets' own patience. Reported separately: a registered-but-not-live domain still means the name is taken; a live one is a stronger identity signal than a profile match alone.

Specific-match domains (uppercase, then lowercase DNS match) are reported first and labeled `confirmed`; permutations follow at lower confidence.

```bash
python3 domain_check.py --username indigokarasu
python3 domain_check.py --username someone --tlds com,io,dev,me
```

## Pipeline integration

```bash
# 1. Research, 2. Extract profiles, 3. Correlate, 4. Expand handles, 5. Check domains
python3 research_person.py --name "Someone" --format detailed
python3 profile_extract.py --input result.json
python3 correlate_profiles.py --input result.json --no-avatars
python3 recurse_expand.py --input result.json --pass 1 --out pass2.json
python3 domain_check.py --username someone
```
