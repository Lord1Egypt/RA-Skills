## Description: <br>
Nex Voice helps agents transcribe Dutch and English voice notes with Whisper, store searchable local transcripts, and extract or manage action items such as tasks, reminders, meetings, decisions, and deadlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, professionals, meeting attendees, and business owners use this skill to convert voice notes and meeting recordings into local transcripts, searchable records, and tracked action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recordings, transcripts, action items, exports, and possibly an API key are stored under ~/.nex-voice. <br>
Mitigation: Install and use the skill only on systems where local storage of those materials is acceptable; review and protect ~/.nex-voice according to the sensitivity of the recordings. <br>
Risk: When optional LLM extraction is enabled, transcript text can be sent to the configured provider or custom endpoint. <br>
Mitigation: For local-only use, do not configure an API key and do not run --use-llm; if LLM extraction is enabled, treat the full transcript as shared with that provider. <br>


## Reference(s): <br>
- [Nex AI Homepage](https://nex-ai.be) <br>
- [ClawHub Skill Page](https://clawhub.ai/nexaiguy/nex-voice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown guidance with shell command examples; exported transcripts can be text or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output uses section headers, list items, ISO-8601 timestamps, action item fields, and a footer that agents should strip before presenting results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
