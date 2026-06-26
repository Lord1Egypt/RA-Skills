---
name: imposter-smasher
description: Prepare a user for an upcoming meeting or event by listing next-day calendar events, prompting for a selection, researching the topic and participants, producing an executive summary, and generating a fully produced 3-5 minute audio briefing. Use when the user asks to prep for meetings, get ready for an event, research attendees before a call, or receive an audio meeting brief.
---

# Imposter Smasher

## Purpose
Imposter Smasher is an orchestrator skill for high-stakes meeting prep. It compiles next-day meetings, lets the user pick one, researches the topic and participants with credible sources, then delivers:
1. A concise executive summary.
2. A fully produced 3-5 minute audio briefing.

## Use This Skill When
- The user wants prep for a meeting happening tomorrow.
- The user wants a confidence-boosting brief before a customer, investor, executive, or partner call.
- The user wants both text and audio output.

## Hard Dependencies
- Calendar access (to list and inspect next-day events).
- Web research via Contextual.ai.
- Audio generation via ElevenLabs or Chatterbox.

## Out Of Scope
- Sending emails/messages on behalf of the user.
- Booking, modifying, or cancelling meetings.
- Unsupported speculation or rumor-based profiling.
- Long dossiers beyond prep needs.
- Live in-meeting copilot behavior.
- Research that cannot be grounded in credible sources.

## Inputs To Collect
- Timezone (if unclear).
- Target date (default: next day in user timezone).
- Preferred audio engine (`ElevenLabs` or `Chatterbox`).
- Optional persona/tone for briefing voice.

## Orchestration Workflow
1. Fetch next-day calendar events.
2. Present a numbered shortlist with title, start time, organizer, and attendees.
3. Ask user to choose one event.
4. Extract research targets:
   - Meeting topic and company/domain context.
   - Participants and their roles.
   - Strategic risks, opportunities, and likely questions.
5. Delegate specialized subtasks where possible:
   - Calendar retrieval/parsing to calendar-capable tooling.
   - Web research and source collection to Contextual.ai.
   - Audio rendering to ElevenLabs/Chatterbox integration.
6. Synthesize an executive summary using `references/executive-summary-template.md`.
7. Build final audio script with `references/audio-brief-template.md`.
8. Generate a produced 3-5 minute audio file and return artifact paths/links.
9. Return concise prep package:
   - Executive summary.
   - Top participant notes.
   - Risks/questions checklist.
   - Audio file location and duration.

## Quality Bar
- Cite only credible, attributable sources.
- Distinguish facts vs inferences.
- Keep briefing actionable and concise.
- Target spoken runtime between 180 and 300 seconds.
- If evidence is weak, explicitly say so and reduce confidence.

## Failure Handling
- If no calendar access: ask for pasted event details and continue.
- If research fails: provide a minimal brief with explicit gaps and retry options.
- If audio generation fails: provide final narration script and engine-specific retry command.

## Detailed References
- Workflow rubric: `references/workflow-rubric.md`
- Source credibility rules: `references/source-credibility-rubric.md`
- Executive summary template: `references/executive-summary-template.md`
- Audio script template: `references/audio-brief-template.md`
- Concise implementation notes: `references/implementation-notes.md`

## Helper Scripts
- `scripts/build_briefing_packet.py`: compile event + research notes into summary and narration draft.
- `scripts/estimate_runtime.py`: estimate spoken duration and validate 3-5 minute target.
- `scripts/validate_skill.sh`: basic scaffold validation.
