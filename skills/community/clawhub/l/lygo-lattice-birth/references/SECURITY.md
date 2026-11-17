# Security — lygo-lattice-birth

**Signature:** Δ9Φ963-LYGO-LATTICE-BIRTH-SECURITY-v1

## Trust boundary

- `LYGO_STACK_ROOT` must be the operator's trusted `lygo-protocol-stack` clone.
- Skill scripts read stack tools in-process only; **no subprocess**, **no network**.
- Live writes require human `--i-consent` on submit and steward ingest.

## Secrets

| Secret | Where | Never |
|--------|-------|-------|
| `consent_bundle` | Local vault, `meta_private` in accepted/ | Pages JSON, git public |
| `family_bind_salt` | Steward accepted/, offline share | Public chart, issues |
| Real name / social | Human memory only | `node.name`, public tags |

## Steward vault

`data/haven_star_chart/submissions/accepted/` holds full submissions. Do not sync this folder to untrusted mirrors without reviewing contents.

## Family bind salt sharing

Share only through encrypted or in-person channels. Rotating salt requires new family fork submissions — old proofs invalid.

## Pair with

`lygo-haven-star-chart` SECURITY.md for portal-wide policies.