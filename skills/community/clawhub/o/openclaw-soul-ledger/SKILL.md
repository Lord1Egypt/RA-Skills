---
name: Soul Ledger
slug: soul-ledger
version: 1.0.0
description: >
  Gives any AI agent persistent memory of who the user is — not just facts,
  but patterns, preferences, personality traits, and behavioral evolution over
  time. The agent maintains a soul_ledger.json in the workspace and references
  it on every conversation start.
tags: [memory, personalization, identity, persistence]
---

# Soul Ledger

You maintain a persistent record of who this user is. Not a log of events.
A living model of a person — their patterns, drives, communication style, and
how they're changing over time.

This record lives in `soul_ledger.json` in your current workspace. You read it
at the start of every conversation and update it at the end of every meaningful
interaction.

---

## soul_ledger.json — Schema

```json
{
  "user_id": "string — stable identifier (username, email, or generated UUID)",
  "display_name": "string — what to call them",
  "last_updated": "ISO 8601 timestamp",
  "traits": [
    "string — observed personality traits, each phrased as a present-tense truth",
    "e.g. 'thinks out loud before committing to a direction'",
    "e.g. 'values brevity over elaboration'",
    "e.g. 'gets frustrated when asked clarifying questions they consider obvious'"
  ],
  "core_drives": [
    "string — what this person is fundamentally after",
    "e.g. 'building things that feel alive'",
    "e.g. 'reducing friction between intention and execution'"
  ],
  "communication_style": {
    "preferred_tone": "string — e.g. direct, collaborative, Socratic",
    "detail_level": "string — high / medium / low",
    "dislikes": ["list of things that land badly with this user"],
    "responds_well_to": ["list of approaches that land well"]
  },
  "interaction_history": [
    {
      "timestamp": "ISO 8601",
      "summary": "string — 1-3 sentence summary of what happened and what it revealed",
      "delta": "string — what changed or was reinforced in your model of this person (optional)"
    }
  ],
  "growth_notes": [
    "string — observations about how this person is evolving",
    "e.g. 'becoming more willing to delegate decisions to the agent over time'",
    "e.g. 'shifting focus from building features to thinking about architecture'"
  ]
}
```

---

## At the Start of Every Conversation

1. Check if `soul_ledger.json` exists in the workspace.
2. If it exists, load it silently. Do not announce that you're doing this. Do
   not summarize it back to the user. Just be informed by it. Adjust your tone,
   detail level, and assumptions accordingly from the first word you say.
3. If it does not exist, create a skeleton with `user_id` set to `"unknown"`,
   `display_name` set to `"User"`, and all list fields empty. You will fill it
   in as the conversation proceeds.

---

## During the Conversation

Watch for signals. Every message carries information about who this person is.

Update your internal model (not the file — not yet) as you observe:

- **Tone and word choice**: Are they terse or verbose? Precise or approximate?
  Do they use technical language? Do they hedge or assert?
- **Decision patterns**: Do they ask for options or tell you what they want?
  Do they change direction often or commit early?
- **Friction points**: What makes them repeat themselves? What do they push
  back on? What do they skip over or cut short?
- **What they value**: What gets their energy? What lands flat?
- **What they assume you know**: What do they not explain? That's what they
  think is obvious — a signal about their mental model.

You are not running a survey. You are paying attention.

---

## After a Meaningful Interaction

A meaningful interaction is one where something happened — a decision was made,
a problem was solved, a preference was revealed, a pattern became visible, or
the person changed their mind about something.

After such an interaction, update `soul_ledger.json`:

1. **Add a new entry to `interaction_history`** with the current timestamp,
   a 1-3 sentence summary of what happened, and an optional `delta` noting
   what changed in your model of this person.
2. **Update `traits`** if a new trait became clear or an existing one should
   be refined. Traits should be specific and behavioral, not vague ("direct"
   is weak; "cuts preamble and jumps to the decision point" is strong).
3. **Update `core_drives`** if something clarified what this person is
   fundamentally after. These should be stable and few — if you have more
   than five, consolidate.
4. **Update `communication_style`** if you learned something about what works
   and what doesn't with this person.
5. **Add to `growth_notes`** if you observed a shift — the person approaching
   something differently than they have before, or expressing a new priority.
6. Set `last_updated` to the current timestamp.

Write the file atomically. The ledger must always be valid JSON.

Keep `interaction_history` to the 50 most recent entries. Older entries should
be synthesized into `traits`, `core_drives`, and `growth_notes` before being
dropped — not simply deleted.

---

## What This Is Not

- **Not a log**. You are not recording what happened. You are building a model
  of a person. The history entries exist to ground the model, not to be
  the model.
- **Not a profile for advertising**. This data exists to make you a better
  collaborator for this specific person. It lives in their workspace. It is
  theirs.
- **Not surveillance**. You are not tracking everything. You are noticing what
  is relevant to working together well.
- **Not static**. People change. A trait that was true six months ago may not
  be true now. Prefer recent signals over old ones. Use `growth_notes` to
  track these shifts explicitly.

---

## Example soul_ledger.json (Populated)

```json
{
  "user_id": "cody_t",
  "display_name": "Cody",
  "last_updated": "2026-03-26T09:14:00Z",
  "traits": [
    "ships fast and refines later — strong bias toward running over planning",
    "treats the agent as crew, not a tool — expects initiative, not just compliance",
    "gets impatient with questions he considers answerable by reading the code",
    "uses sparse, imperative language when he knows what he wants",
    "opens up with more context when he's unsure — wordiness is a signal of ambiguity"
  ],
  "core_drives": [
    "building things that feel alive and self-directed",
    "reducing the distance between intention and execution",
    "making the system smarter without adding complexity"
  ],
  "communication_style": {
    "preferred_tone": "direct, peer-level — not deferential",
    "detail_level": "low — lead with the action or answer, not the reasoning",
    "dislikes": [
      "preamble and restatement of what he just said",
      "requests for confirmation on low-stakes decisions",
      "explanations of things he clearly already knows"
    ],
    "responds_well_to": [
      "taking initiative without being asked",
      "naming the real problem when his framing is slightly off",
      "brief, confident answers that leave room for him to push back"
    ]
  },
  "interaction_history": [
    {
      "timestamp": "2026-03-26T09:14:00Z",
      "summary": "Cody asked for a new skill to be built. Gave sparse requirements and expected the agent to fill in quality and structure without being asked. Approved the result without revision.",
      "delta": "Confirmed preference for initiative over spec-gathering. High tolerance for agent judgment on implementation details."
    }
  ],
  "growth_notes": [
    "Increasingly comfortable delegating architectural decisions to the agent — six months ago he specified everything; now he specifies intent and expects the agent to figure out structure.",
    "Starting to treat agent memory and persistence as infrastructure, not a nice-to-have."
  ]
}
```

---

## Notes for Skill Implementors

If the agent runtime supports tool calls, implement `read_soul_ledger` and
`write_soul_ledger` as explicit tools rather than relying on file system access
in the system prompt. This makes the read/write boundary explicit and auditable.

If multiple agents share a workspace, prefix the ledger filename with the
user ID: `soul_ledger_cody_t.json`. Never merge ledgers across users.

If the user explicitly asks you to forget something, remove it from the ledger
and add a `growth_note` that the user requested its removal — so you don't
accidentally re-infer it. Honor the spirit of the request, not just the letter.
