# Character-Fit Dialogue

## Aim

Generate and audit dialogue that belongs to this character in this situation.
Keep speakers distinguishable without reducing a profession, class, region, or
temperament to a catchphrase.

## Activation Gate

Use in fiction drafting when the task requests a spoken exchange or directed
interpersonal action. Use in review for sustained dialogue, directed interaction
(including wordless exchanges), or the explicit `voice` profile. A solitary action
or scenery passage does not need this module.

## Evidence Hierarchy

Build from strongest to weakest evidence:

1. Explicit character sheets, continuity ledger, prior chapters, and user instructions.
2. Repeated behavior and speech already established on the page.
3. The current scene's goal, audience, pressure, knowledge, and power balance.
4. Role or cultural priors only as tentative constraints, never as proof of voice.

Do not infer speech style directly from occupation, status, class, region, or one
temperament label. These factors may shape knowledge, incentives, duties, risks,
social options, and code-switching pressure, but they do not define personality.

## Speaker Model

For each important speaker, record only scene-relevant dimensions:

- stable baseline: diction, directness, abstraction, turn length, politeness,
  humor, profanity, titles, discourse particles, fillers, contractions, and taboo wording
- response habits: answer, evade, counterquestion, bargain, teach, test, flatter,
  threaten, joke, quote, correct, or stay silent
- disclosure habits: what is stated, implied, coded, delayed, or never named
- competence boundary: what the person can know, explain, notice, or misunderstand
- role constraints: duties, institutional incentives, dependencies, liabilities,
  and what outcome counts as success
- audience shift: how the person changes with superiors, subordinates, intimates,
  strangers, rivals, witnesses, or possible overhearers

Treat traits as tendencies, not quotas. A blunt person can rehearse one elegant
sentence; a restrained person can speak plainly under urgency. Repeated departure
needs a visible reason.

## Scene Speech Contract

Before writing or judging the exchange, identify:

```text
speaker -> listener / audience
topic -> why it matters now
speaker goal -> desired listener action or belief
speaker constraint -> what cannot be admitted, promised, or understood
tactic -> wording and silence chosen for this turn
result -> what changes in knowledge, leverage, permission, risk, or emotion
```

The declared topic is not always the real transaction. A practical meeting should
reflect the parties' actual incentives and constraints, but it may detour when the
scene gives a motive such as testing, stalling, face-saving, seduction, intimidation,
misunderstanding, or concealment.

## Common Ground And Subtext

For an important exchange, distinguish:

```text
known to both -> known only to speaker -> known only to listener -> disputed or false
surface statement -> hidden aim -> protected information -> intended listener update
```

- Do not make characters explain facts both already know unless the line accuses,
  reframes, rehearses, performs for an audience, or tests a disputed interpretation.
- Let subtext come from a gap between wording and aim, not from random vagueness.
- Check whether a line changes information, leverage, permission, risk, commitment,
  or interpretation. Greetings and texture may remain socially functional.
- Flag narration that immediately paraphrases an already legible line or gesture.
- Preserve direct speech when urgency, intimacy, rank, ritual, or deliberate candor
  makes directness the meaningful choice.

## Response Obligation And Interaction Debt

A pressure-bearing utterance or action opens a response obligation when it asks for
information, changes terms, tests a boundary, offers or withholds something, reveals
knowledge, assigns blame, makes contact, or otherwise demands adjustment from someone
present. Before the prose changes topic, viewpoint, time, or scene, show one form of
uptake:

- a verbal answer, refusal, evasion, counter, clarification, or acknowledgment
- a chosen action that accepts, resists, redirects, approaches, withdraws, or delays
- a visible bodily or sensory response that changes the beat
- deliberate silence made legible through timing, attention, or the speaker's reaction
- an interruption or external event that clearly prevents a response
- explicit deferral recorded as open interaction debt for a later beat

The response need not be immediate, cooperative, or verbal. Do not force mechanical
ping-pong after greetings, incidental remarks, self-talk, rhetorical lines, or turns
whose uptake is already obvious. The failure is an important stimulus abandoned with
no reception, consequence, or deliberate deferral.

### Bidirectional Action And Response

Check every materially affected recipient, including the viewpoint character.
Ordinary gestures qualify when completion or the next beat depends on reception.

- Identify initiator, recipient, perceptible stimulus, and proposed state change.
  A bystander's reaction cannot settle the intended recipient's part.
- Separate speech and action obligations: an answer may leave a transfer, invitation,
  or contact pending. Check possession, position, attention, and access as needed.
- Distinguish intention, attempt, and completion. An offer is not acceptance;
  reaching is not contact. Establish completion, resistance, interruption, or a
  legible pending state before relying on a result.
- After a distance or posture change, establish whether the other person follows,
  stays, calls after them, or loses contact when the next beat depends on it.
- For action toward a person or their belongings, use character and relationship
  evidence for awareness, cooperation, resistance, withdrawal, or stillness. Never
  assume gratitude, intimacy, compliance, or an inaccessible internal feeling.
- Same-clause uptake, shared action, or a later consequence may imply completion.
  No extra sentence is needed. Supported unawareness can explain no response.
- Before cutting away, check both directions and all unresolved parts. Carry who
  owes what and the next relevant opportunity; deferral needs evidence in the prose.

Use the smallest fitting continuation, without stock gestures, scenic filler, or
emotional gloss. If the intended response is unknown, offer alternatives, not canon.

## Drafting Mode

When this file is loaded as a `Technique Module`:

1. Build a compact speaker model and scene speech contract before drafting.
2. Give each turn a purpose and make it respond to the preceding turn.
3. Track common ground so speakers do not recite shared history for the reader.
4. After a pressure-bearing turn, land the listener's uptake before shifting focus,
   unless the missing response is deliberately carried as interaction debt.
5. Let expertise appear through what a speaker asks, notices, refuses, corrects,
   or treats as obvious, not through an exposition dump.
6. Keep vocabulary and syntax near the speaker's baseline while allowing motivated
   code-switching for audience, pressure, performance, quotation, or strategy.
   When language, dialect, honorific, or regional evidence matters, load
   `speech-register-continuity` instead of improvising a linguistic profile here.
7. Make important dialogue transact: alter knowledge, leverage, permission, risk,
   commitment, trust, or the next available action.
8. Do not display the hidden model unless the user asks for notes.

## Audit Mode

When this file is loaded as an `Audit Module`:

1. Extract speaker models and the scene speech contract from evidence.
2. Within the assigned text, inspect every directed exchange, including wordless
   actions and the viewpoint character's responses. Map only obligated beats as
   `initiator -> recipient -> speech/action -> evidence of reception -> resolved,
   partly resolved, blocked, or deferred state`. Sampling speaker style must not
   replace interaction coverage. Check neighboring paragraphs before claiming a gap.
3. Remove labels from several lines and test whether they remain attributable.
4. Flag only evidence-backed failures:
   - interchangeable speakers or narrator-shaped exposition
   - topic or incentive drift without a scene motive
   - knowledge, competence, or institutional-constraint mismatch
   - a reply that ignores the preceding turn
   - shared facts restated only for reader exposition
   - on-the-nose lines whose wording, motive, and meaning are identical without cause
   - narration that translates an already legible line or gesture
   - a pressure-bearing line or action abandoned before any uptake or explicit deferral
   - silence treated as a response even though the text gives it no timing or consequence
   - unearned register, politeness, directness, dialect, or profanity shift
   - a colloquial fragment whose intended meaning is not recoverable because a required
     verb, object, complement, name, or referent was accidentally omitted
   - speech incompatible with the current audience, power balance, or emotional load
   - personality reduced to one repeated verbal tic or occupational stereotype
5. Test every deviation for a change gate: audience adaptation, deception,
   performance, quotation, sarcasm, rehearsal, stress, intoxication, panic, intimacy,
   status change, new evidence, or deliberate loss of control.
6. Repair the smallest unit: tactic, wording, address form, omitted fact, silence,
   listener reaction, or one short change-gate beat.

## Output

```text
Character-Fit Dialogue Audit
- Speaker model and evidence source:
- Scene speech contract:
- Common ground and information asymmetry:
- Surface statement, hidden aim, and protected information:
- Turn or line:
- Response obligation: none / immediate / refused / interrupted / deferred
- Actual uptake or missing landing beat:
- Initiator and affected recipient; separate speech/action obligations:
- Evidence span searched, unresolved state, and next relevant opportunity:
- Conflict: baseline / goal / topic / knowledge / role constraint / audience / response
- Confirmed mismatch or uncertain inference:
- Valid change gate, if any:
- Minimal repair and insertion point:
```

Do not invent dialect, jargon, or verbal tics merely to make speakers different.
Do not rewrite a plausible individual into a generic representative of their job.
