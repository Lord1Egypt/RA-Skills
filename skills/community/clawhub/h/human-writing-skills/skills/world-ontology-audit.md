# World Ontology Audit

## Aim

Keep objects, institutions, technology, customs, and available actions compatible
with the story's declared world. This is a constraint check, not a request to add
decorative period detail.

## Activation Gate

Use only when the draft or supplied context establishes an era, place, speculative
system, institutional setting, or material limit. Do not load for generic narration,
casual answers, or scenes whose world assumptions are not at issue.

## World Contract

Extract only dimensions used by the current passage:

```text
time and place
technology and infrastructure
institutions, law, and authority
economy, transport, and communication
social customs and information access
speculative rules, powers, and costs
capability tiers, permissions, resources, counters, and transition costs
```

For every challenged detail, record the on-page claim, the governing world rule,
and one of these verdicts:

- compatible
- compatible after an established exception or adaptation
- possible but unsupported
- contradictory
- unknown and requiring research

## Audit

- Flag an object, procedure, title, unit, institution, or communication method that
  requires a world condition the text has denied or never supplied.
- Flag modern assumptions imported into historical or invented settings without a
  translation layer.
- Flag powers, laws, markets, travel speeds, or social permissions that change only
  to make the current scene convenient.
- For detailed individual power, skill, equipment, injury, or resource transitions,
  load `capability-state-audit`; this module owns the governing world rule only.
- Distinguish a deliberate anachronism, hybrid culture, hidden technology, unreliable
  narrator, or local exception from an accidental mismatch.
- Do not treat genre convention or general world knowledge as stronger than the
  user's ledger and the text's explicit rules.

## Repair

Prefer the smallest repair: replace one incompatible detail, add one enabling rule,
show one exception cost, change the available action, or mark the fact for research.
Do not rebuild the whole world to save one sentence.

```text
World Ontology Audit
| Passage | Detail/action | Governing rule evidence | Verdict | Confidence |
| --- | --- | --- | --- | --- |

- Confirmed incompatibility:
- Unsupported but possible detail:
- Valid exception:
- Minimal repair or research question:
```
