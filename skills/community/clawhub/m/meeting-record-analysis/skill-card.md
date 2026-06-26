## Description: <br>
Converts meeting audio into structured meeting minutes using speech recognition, transcript cleanup, LLM summarization, and optional voice-summary generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cows21](https://clawhub.ai/user/cows21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to turn uploaded meeting recordings into concise structured minutes with topics, discussion points, decisions, action items, and a cleaned transcript. It is useful when a meeting needs a JSON record and, optionally, an audio summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting audio, transcripts, and optional summary text are sent to configured external ASR, LLM, and TTS providers. <br>
Mitigation: Use only approved providers for the meeting data involved, use dedicated API keys, and avoid highly confidential or regulated recordings unless those providers are cleared. <br>
Risk: Generated minutes and optional MP3 summaries are saved locally and may contain sensitive meeting content. <br>
Mitigation: Store outputs in an approved location, restrict access, and delete JSON or MP3 files when they are no longer needed. <br>
Risk: LLM-generated summaries may omit context or state uncertain points too confidently. <br>
Mitigation: Review the generated decisions and action items against the cleaned transcript before using them as an official meeting record. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cows21/meeting-record-analysis) <br>
- [Output Schema](references/output_schema.md) <br>
- [Prompt Templates](references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, audio] <br>
**Output Format:** [JSON object with optional MP3 voice-summary file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns topic, discussion_points, decisions, action_items, cleaned_transcript, and voice_summary_path; also saves a local JSON output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
