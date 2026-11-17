# Relationship Stance Audit

## Aim

Prevent dialogue and narration from violating the established relationship graph.
Characters should speak as if they remember alliances, hostility, secrecy, loyalty,
public posture, private leverage, and who is allowed to know what.

This module is about social logic, not morality. A character may break a rule, lie,
flatter an enemy, expose a secret, or praise a rival, but the draft must give a
reason on the page.

## Core Model

Track every important relationship as a directed edge:

```text
Person A -> Person B
- public stance: respectful / hostile / neutral / intimate / subordinate / superior
- private stance: loyal / resentful / attracted / afraid / exploiting / hiding
- knowledge: knows / suspects / misreads / must not know
- mention policy: praise allowed / criticism allowed / avoid mention / coded mention only
- exposure risk: low / medium / high
- leverage: what A can gain, lose, reveal, or threaten by mentioning B
```

Relationships are directional. A may trust B while B is using A. A may publicly
respect B while privately undermining B.

## Dialogue Triangle Test

For every line of dialogue or important thought, extract:

```text
speaker -> listener/audience -> referenced third party/topic
```

Then ask:

1. Does the speaker know the relationship between listener and referenced party?
2. Would this speaker normally mention that party in this audience?
3. Is the tone compatible with the speaker's public stance and private aim?
4. Does the line leak information the listener should not have?
5. If the line violates the rule, is there a visible motive: provocation, report,
   manipulation, cover story, loyalty test, bargaining, panic, ignorance, or mistake?

Flag the line if the answer is unclear.

## Common Contradictions

### Hostile or Rival Factions

- A character praises a known rival in front of someone who hates that rival.
- A subordinate casually cites the enemy faction without fear, calculation, or cover.
- Someone reveals a strategic weakness to the wrong side.
- A narrator treats two hostile parties as socially interchangeable.

Repair by adding motive, caution, coded language, visible discomfort, or a different
comparison target.

### Secret Affair or Multi-Relationship Plot

- A person talks about one secret partner to another secret partner without reason.
- A hidden relationship is treated as public knowledge.
- The wrong spouse, lover, rival, or witness is used as the comparison target.
- Jealousy appears without knowledge; acceptance appears without discovery.

Repair by tracking who knows, who suspects, who must not know, and which names are
forbidden in which room.

### Sect, Court, Family, Office, or Hierarchy

- A disciple insults an allied sect leader in front of their own master without
  status consequences.
- A manager praises a rival executive to an opposed chairperson without tactical purpose.
- A family member reveals private shame to an outsider despite established taboo.
- Honorifics, titles, nicknames, and levels of directness ignore rank and intimacy.

Repair by adjusting address form, adding consequences, changing audience, or making
the line a deliberate social move.

## Mention Policy Ledger

For complicated scenes, maintain this compact table:

| Speaker | Audience | Referenced Person/Group | Allowed Tone | Forbidden Leak | Exception Motive |
| --- | --- | --- | --- | --- | --- |
| A | B | C | avoid / coded / praise / criticize / report only | secret, affair, alliance, debt | provoke, test, bargain |

## Audit Output

```text
Relationship Stance Audit
- Dialogue triangle: speaker -> listener -> referenced party
- Established relationship rule:
- Draft line or summary:
- Conflict type: audience mismatch / stance mismatch / secret leak / rank mismatch / knowledge mismatch
- Could be intentional? yes/no
- Required repair: add motive / change audience / change target / code the mention / add consequence / update ledger
```

## Revision Check

Before finalizing a scene, answer:

- Who is in the room or likely to hear?
- Which names, topics, comparisons, and praises are dangerous in this audience?
- Which relationships are public, private, suspected, or concealed?
- Which line changes someone's knowledge, leverage, or suspicion?
- Does every social breach have a motive or consequence?

If not, revise the dialogue before polishing the prose.
