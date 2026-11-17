## Description:

Converts uploaded meeting audio into structured meeting minutes using ASR transcription, transcript cleanup, LLM summarization, and optional TTS voice summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cows21](https://clawhub.ai/user/cows21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn meeting recordings into structured minutes with topics, discussion points, decisions, action items, cleaned transcript text, and an optional voice-summary file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting recordings and derived text may contain sensitive information and are sent to configured ASR, LLM, and optional TTS providers.

Mitigation: Use approved enterprise endpoints and API keys, and avoid sensitive meetings unless provider retention and compliance terms are acceptable.

Risk: Generated minutes may misstate decisions, action items, or responsibilities.

Mitigation: Review generated minutes before relying on decisions or action items.

Risk: The optional voice summary can create an additional local audio artifact containing meeting content.

Mitigation: Store generated outputs only in approved locations and delete files when they are no longer needed.

## Reference(s):

- [Output Schema](references/output_schema.md)
- [Prompt Templates](references/prompts.md)
- [ClawHub skill page](https://clawhub.ai/cows21/skills/meeting-record-analysis)

## Skill Output:

**Output Type(s):** [JSON, Text, Files]

**Output Format:** [JSON object printed to stdout and saved as a local JSON file; optional MP3 voice-summary file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes topic, discussion_points, decisions, action_items, cleaned_transcript, and voice_summary_path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
