# Workflow Rubric

## Step 1: List Next-Day Events
- Resolve user timezone explicitly.
- Pull events for tomorrow only.
- Include: title, start/end, organizer, attendee count, and virtual meeting links if available.
- If >8 events, show top 8 and allow `show more`.

## Step 2: Confirm Event Selection
- Ask user to select by number.
- Confirm chosen event details before researching.
- If event data is sparse, ask for missing context (goal, relationship, sensitivity).

## Step 3: Build Research Plan
- Topic lane:
  - Company/product/domain state.
  - Recent developments relevant to meeting objective.
- Participant lane:
  - Role, seniority, remit, likely priorities.
  - Publicly attributable context only.
- Risk lane:
  - Potential objections, unknowns, and decision blockers.

## Step 4: Delegate By Capability
- Calendar-specific operations: calendar integration/tooling.
- Web research and source retrieval: Contextual.ai.
- Voice rendering and mastering: ElevenLabs or Chatterbox.

## Step 5: Synthesize Outputs
- Executive summary: 300-600 words.
- Participant snapshots: 2-4 bullets each.
- Suggested talking points: max 7 bullets.
- Question bank: max 8 questions.

## Step 6: Produce Audio Briefing
- Use audio template and runtime estimator.
- Spoken target: 180-300 seconds.
- Tone: calm, direct, senior-operator style.
- Include explicit confidence labels for contested claims.

## Step 7: Final Delivery Package
- `executive_summary.md`
- `audio_script.txt`
- `audio_manifest.json`
- `briefing.mp3` or `briefing.wav`

## Guardrails
- No impersonation instructions.
- No outreach actions (email, DM, booking changes).
- No fabrication when evidence is absent.
