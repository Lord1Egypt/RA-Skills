## Description: <br>
Converts user-provided text into AI speech, voiceover, or text-to-audio through the Giggle.pro TTS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate speech, voiceover, or text-to-audio from user-provided text through Giggle.pro, choosing a voice, emotion, and speaking rate before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text is sent to Giggle.pro and may include private, confidential, or regulated content. <br>
Mitigation: Review text before conversion and avoid submitting material that should not be processed by the external Giggle.pro service. <br>
Risk: Submitted prompts are stored locally in ~/.openclaw/skills/giggle-generation-speech/logs/ for task tracking. <br>
Mitigation: Periodically delete the local logs directory when prompt retention is not desired. <br>
Risk: Returned signed audio links may provide access to generated audio. <br>
Mitigation: Treat signed audio URLs as sensitive and share them only with intended recipients. <br>
Risk: The skill depends on a Giggle API key for external API access. <br>
Mitigation: Use a dedicated, revocable GIGGLE_API_KEY rather than a broadly shared credential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/giggle-generation-speech) <br>
- [Publisher profile](https://clawhub.ai/user/patches429) <br>
- [Giggle.pro](https://giggle.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status messages, JSON task status, shell commands, and signed audio links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, and GIGGLE_API_KEY; writes task state and prompt logs under ~/.openclaw/skills/giggle-generation-speech/logs/.] <br>

## Skill Version(s): <br>
0.0.10 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
