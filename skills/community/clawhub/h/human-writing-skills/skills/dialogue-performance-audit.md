# Dialogue Performance And Landing

## Aim

Make consequential dialogue feel enacted between particular people, rather than
alternating lines decorated with generic gestures. A spoken turn, its reception,
and any physical beat should alter what the people can know, ask, refuse, risk,
or do next.

## Activation Gate

Use only alongside `dialogue-voice-audit`: in drafting when a fiction or webnovel
task explicitly asks for dialogue or a character-interaction scene, and in review
through the `voice` profile or detection of a spoken or wordless interpersonal exchange.
Do not load for solitary narration, generic proofreading, news interviews,
academic prose, or formal documents.

## Interaction Map

`dialogue-voice-audit` owns response obligation and interaction debt. Use its
speaker/response map rather than rebuilding it. This module owns whether a selected
visible beat earns its place in that established exchange.

For a consequential beat, trace only the links the scene needs:

```text
established uptake -> chosen visible beat (if needed) -> changed option or residue
```

- A visible beat earns its place when it accepts, resists, conceals, tests,
  repositions, interrupts, grants, withdraws, reveals, or delays something.
- A line does not need an action after it. Greetings, banter, a clean answer, and
  deliberately spare exchanges may stay unadorned.
- A scene does not need every link on the page. Keep the unstated link only when
  the reader can still infer who received the pressure and what remains open.

## Drafting Mode

1. Before the exchange, identify the current pressure, each person's immediate
   aim, what either person is willing to show, and the scene's usable objects,
   distance, witnesses, exits, and physical limits from the context.
2. Use the listener uptake already established by `dialogue-voice-audit`.
   For mixed speech and action, preserve each unresolved part of that map; a spoken
   answer alone may not complete the physical exchange. Check visible consequences
   for the viewpoint character as well as the other participants.
3. Choose one concrete performance beat only when it changes the interaction.
   A hand staying on a door, a chair left empty, a phone turned face-down, or a
   step withheld can do work; a low voice, a faint smile, weather, clothing, or
   a stock glance does not automatically do work.
4. Let the beat inherit from the scene ledger. Do not invent a prop, bodily
   position, clothing detail, intimacy level, or access that the scene has not
   established merely to make dialogue feel vivid.
5. Vary the landing: sometimes use direct speech, sometimes a purposeful action,
   sometimes a timed silence, and sometimes stop on the earned line. Do not turn
   every turn into `line -> gesture -> narrator explanation`.
6. Let narration add what speech cannot: timing, competing attention, a withheld
   choice, a material constraint, or a consequence. Do not paraphrase a line that
   already makes its meaning clear.

## Audit Mode

For each obligated exchange identified by the response owner, map:

```text
turn -> established uptake -> performance beat -> changed state
```

Flag only evidence-backed issues:

- a consequential line, touch, offer, accusation, or refusal with no readable
  reception before the prose abandons it
- an adjacent reply that changes topic while ignoring the actual pressure without
  a motive such as evasion, misunderstanding, interruption, or strategic refusal
- stage direction that could be removed with no change to leverage, access,
  attention, information, distance, permission, or emotional choice
- a repeated `said/asked + stock gesture` rhythm used in place of turn-taking
- narration that explains the already legible emotional meaning of a line or action
- a bodily beat that contradicts the current space, props, clothing, injury,
  relationship boundary, or consent/permission state in the supplied context
- a decorative scenic dissolve or reflection inserted instead of the listener's
  uptake or the scene's actual next consequence

Do not flag a concise exchange merely for being concise. Do not require touching,
movement, scenery, or reaction labels after every line. Treat omission as a problem
only when it leaves a consequential interaction unreceived or makes the scene's
state impossible to follow.

## Output

```text
Dialogue Performance Audit
- Scene pressure and usable physical context:
- Turn and listener:
- Inherited uptake and actual performance beat:
- Confirmed problem: cosmetic beat / tag rhythm / explained subtext / continuity conflict
- Evidence and confidence:
- Minimal repair and insertion point:
```

Prefer the smallest repair: remove a decorative beat, replace it with a specific
uptake, add one consequence, or preserve a deliberate silence with enough timing
to be legible. Do not add gestures merely to make the prose look more cinematic.
