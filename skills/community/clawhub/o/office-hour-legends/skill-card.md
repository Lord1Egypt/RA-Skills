## Description: <br>
Office Hour Legends runs YC-style office hours and transcript reviews by loading a selected founder or operator persona and guiding the agent through focused startup or builder feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prodigalson](https://clawhub.ai/user/prodigalson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, builders, and startup operators use this skill to run simulated YC-style office hours, sharpen startup ideas, review pitches or meeting transcripts, and produce concise next-step guidance or session notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Fathom meeting metadata and full transcripts after a meeting is selected. <br>
Mitigation: Use transcript review only for meetings where participants consent and where the operator is comfortable exposing the transcript to the agent session. <br>
Risk: Full mode may save derived session notes or transcript review notes locally without a strong retention gate. <br>
Mitigation: Prefer no-save or manual-save handling for sensitive calls, and review or remove generated notes after the session. <br>
Risk: Optional Bookface research and credential-backed integrations may expose private-source context or require additional credentials. <br>
Mitigation: Review Bookface availability, Fathom credential setup, and any private-source research behavior before enabling those optional paths. <br>


## Reference(s): <br>
- [Office Hour Legends ClawHub listing](https://clawhub.ai/prodigalson/office-hour-legends) <br>
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills) <br>
- [Bookface Search optional integration](https://github.com/voska/bookface-search) <br>
- [HN CLI optional integration](https://github.com/voska/hn-cli) <br>
- [Fathom settings for API key setup](https://fathom.video/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown notes with optional timestamped transcript feedback and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch Fathom meeting metadata and transcripts when configured, and may save local Markdown session notes in full mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
