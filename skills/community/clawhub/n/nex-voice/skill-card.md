## Description:

Voice note transcription and intelligent action item extraction for capture and organization of verbal communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, busy professionals, meeting attendees, and business owners use Nex Voice to transcribe Dutch and English voice notes or meeting recordings, extract action items, search prior transcripts, and manage pending or overdue follow-ups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM extraction can send full transcripts to the configured provider endpoint.

Mitigation: Use --use-llm only for audio that may be shared with the chosen provider, and confirm api_base and model settings before enabling LLM extraction.

Risk: API keys may be stored in local configuration as plaintext.

Mitigation: Prefer environment variables or a credential manager, and review permissions on ~/.nex-voice/config.json if nex-voice config set-api-key is used.

Risk: Recordings, transcripts, action items, configuration, and exports are stored locally under ~/.nex-voice.

Mitigation: Install only where local storage of voice data is acceptable, and protect the ~/.nex-voice directory according to the sensitivity of the audio and transcripts.

Risk: The skill invokes local external commands including whisper, ffmpeg, and curl.

Mitigation: Use an isolated Python environment and reviewed dependency versions before processing sensitive recordings.

## Reference(s):

- [Nex AI homepage](https://nex-ai.be)
- [ClawHub Nex Voice skill page](https://clawhub.ai/nexaiguy/skills/nex-voice)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands; transcript exports may be text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output includes transcript summaries, action item records, search results, status updates, statistics, and export content.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
