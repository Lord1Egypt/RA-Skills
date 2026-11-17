# Relationship Stance Continuity

Physical continuity asks whether a character can be in a place. Relationship
stance continuity asks whether a character would say this about that person in
this audience.

Long-form drafts often drift because the model forgets:

- who is hostile to whom
- who is publicly friendly but privately opposed
- who knows a secret and who only suspects it
- who must not know another person exists
- whose name can be praised, criticized, compared, or avoided in a given room

## Core Method: Dialogue Triangle

For every line of dialogue, extract:

```text
speaker -> listener/audience -> referenced third party/group/secret
```

Then check:

- Does the speaker know the listener's relationship to the referenced party?
- Is this party safe to mention in this audience?
- Does the tone fit the public stance and private motive?
- Does the line leak forbidden information?
- If the line breaks the rule, does the draft provide motive or consequence?

## Relationship Ledger Fields

| Field | Purpose |
| --- | --- |
| public stance | respect, hostility, neutrality, intimacy, rank |
| private stance | loyalty, resentment, use, fear, concealment |
| knowledge | knows, suspects, misreads, must not know |
| mention policy | avoid, code, praise, criticize, compare, report only |
| exposure risk | low, medium, high |
| leverage | what the speaker can gain, lose, reveal, or threaten |

## Common Failure Modes

### Hostile or Rival Parties

If the chairperson and general manager are enemies, a protagonist should not casually
praise one in front of the other unless the scene gives a motive: reporting, testing,
provoking, bargaining, pleading, or pretending neutrality.

### Secret Affair or Multi-Relationship Plot

If one character has two hidden partners, they should not casually tell one partner
about the other unless the draft shows discovery, intent, coded speech, a slip, or
a public change in the relationship state.

### Sect, Family, Office, or Faction

If two sect leaders are close, insulting one in front of the other's disciple should
carry a cost. If they are enemies, praising one in front of the other should read
as strategy, risk, ignorance, or provocation.

The same logic works for companies, courts, families, teams, schools, offices, and
any group with hierarchy or faction pressure.

## Recommended Commands

`--deep-review` includes `relationship-stance-audit`; it can also be selected directly with `--module relationship-stance-audit`:

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --deep-review `
  --context examples/relationship-stance-ledger.zh-CN.md `
  --task "Continue the banquet scene. Mentions of rival factions and hidden relationships must respect the audience."
```

Audit an existing draft:

```powershell
python -m humanwriting.cli audit `
  --draft examples/problem-car-scene-draft.md `
  --context examples/relationship-stance-ledger.zh-CN.md `
  --profile relationship
```

## Minimal Repairs

When a stance contradiction appears, prefer a small repair:

- change the audience
- change the comparison target
- use coded speech or a title instead of a name
- add motive
- add consequence
- update the ledger if the relationship has become public
