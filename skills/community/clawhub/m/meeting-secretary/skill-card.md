## Description: <br>
Meeting Secretary analyzes completed meeting transcripts or notes and produces structured meeting minutes with key information, viewpoints, consensus, disagreements, action items, risks, and subtle intent signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuzhiguocarter](https://clawhub.ai/user/wuzhiguocarter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and teams use this skill to turn meeting transcripts or notes into structured minutes for review, follow-up, and decision tracking. It is especially suited for decision meetings, discussions, project updates, brainstorming sessions, one-on-one conversations, and training or knowledge-sharing meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts can contain confidential business information, regulated data, or personal information. <br>
Mitigation: Redact secrets and unnecessary personal data before analysis, confirm participant consent, and use only AI environments approved for the meeting's confidentiality level. <br>
Risk: The skill infers tone, intent, hidden concerns, and emotional posture from transcript text, which may be inaccurate or overconfident. <br>
Mitigation: Treat inferred intent and sentiment as review cues, not facts; verify sensitive conclusions with participants before using them for decisions or performance evaluation. <br>
Risk: Reference documentation mentions optional audio and video workflows that are not included in the artifact. <br>
Mitigation: Review and security-check any additional transcription, audio, or video tooling separately before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuzhiguocarter/meeting-secretary) <br>
- [Meeting secretary best practices](references/best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown meeting minutes, structured analysis, action lists, and optional shell commands for transcript splitting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled transcript splitter can write segment text files and a Markdown segment index for long transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
