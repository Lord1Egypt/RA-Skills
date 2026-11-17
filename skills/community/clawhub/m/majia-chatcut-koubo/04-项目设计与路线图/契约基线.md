# Contract baseline

Baseline commit: `4a44f3555a0a80adbd03943a17d128c7c4e1fc27`
Roadmap review baseline: `36baefd5b8ea3ebc5f8d5e26c24ebd358070a4e4`

This document records the contract gaps observed before the v1.3 contract-hardening work. It is evidence for the migration, not an allowlist for release.

| Area | Baseline observation | Required release behavior |
| --- | --- | --- |
| Schema execution | JSON Schemas existed but `npm run verify` did not execute them | Every governed JSON/template/fixture is validated offline in CI |
| Profile inheritance | Runtime accepted `extends`, while the single profile Schema rejected it | Source and resolved contracts are separate; resolved output is complete and has no `extends` |
| Local overlay | Example profiles contained fields rejected by the published Schema | Public examples and an anonymized local-layer fixture resolve and validate |
| Hard policy | Some caption limits could be relaxed by profile or terminology data | Overlays may only preserve or tighten hard policy |
| Text evidence | Comparison discarded punctuation and numeric signs | Decimal, negative, percent, date and unit semantics remain significant |
| Word evidence | Keys only needed to be non-empty; ordering/overlap/integer frames were unchecked | Keys are document-unique and intervals are integer, ordered, non-overlapping and in-page |
| Short cards | Arbitrary whitelist text could bypass the normal minimum | Only policy-conforming ASCII brand/acronym cards may use the narrow exception |
| Theme contrast | Script thresholds were weaker than the documented internal target | Body/secondary/CTA text use 7:1; headline emphasis uses 4.5:1 |
| Asset consistency | Theme/layout/composition relationships had no release gate | IDs, references, required files and canvas geometry are checked |
| Version drift | English README still described five states | Package, skill, changelog, badges and capability counts agree |
| Runtime evidence | Static review did not re-prove live ChatCut behavior | Live adapter claims remain `unverified` until a current capability canary runs |

## V1.3.1 P0 disposition

| Roadmap finding | Release disposition |
| --- | --- |
| C-001 Schema not in `verify` | Closed: offline release scan, meta-schema compilation, positive/negative fixtures and zero baseline debt |
| C-002 tests bypass profile Schema | Closed: source layers, resolved profiles, structured captions and new terminology run through Ajv before domain checks |
| C-003 `extends` conflicts with Schema | Closed: source and resolved contracts are separate; resolved output cannot contain `extends` |
| C-004 local example conflicts with Schema | Closed: public examples and the anonymized layered fixture validate and resolve |
| C-005 profile expands replacement limit | Closed: the hard policy owns the cap; profiles can only reduce it |
| C-006 arbitrary Chinese short-card allowlist | Closed: only policy-shaped ASCII/numeric cards qualify and strict release requires pixel evidence |
| C-007 punctuation-blind text comparison | Closed: number signs, decimals, percentages, dates, units and NFKC boundaries have regression coverage |
| C-008 weak word evidence | Closed: safe integer intervals, document-unique keys, ordering/overlap and explicit source binding are enforced |
| C-009 unbound provenance | Closed: project, timeline and source asset/revision evidence must match the leaf-owned profile maps |
| C-010 unaudited risky correction | Closed: approved correction records, stable term IDs and audio evidence are mandatory for risky changes |
| C-011 warning-only short cards | Closed: `--strict` blocks missing reviewer/pixel evidence |
| C-012 weak contrast thresholds | Closed: body/secondary/CTA use 7:1 and headline emphasis uses 4.5:1 |

Any deferred P0 must fail closed in release mode. A note in this document is never sufficient to waive a release gate.
