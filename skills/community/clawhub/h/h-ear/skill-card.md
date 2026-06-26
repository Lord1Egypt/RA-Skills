## Description: <br>
H-ear lets agents classify environmental audio, inspect jobs and usage, manage webhooks, and retrieve audio analysis artifacts through the H-ear API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[badajoz95](https://clawhub.ai/user/badajoz95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to classify audio from files or URLs, list supported sound classes, review H-ear jobs and usage, retrieve analysis artifacts, and manage webhook delivery for audio events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires H-ear credentials and may send selected audio, audio URLs, job metadata, and webhook callback data to the H-ear service. <br>
Mitigation: Install only when that data sharing is acceptable, use least-privileged credentials, and avoid private or regulated audio unless H-ear data handling terms have been reviewed. <br>
Risk: The security evidence reports an under-disclosed live RTSP capture command that can invoke ffmpeg and submit captured audio for classification. <br>
Mitigation: Require explicit user approval before live capture or listen workflows, confirm the RTSP source and duration, and disable or block capture where continuous audio collection is not intended. <br>
Risk: Webhook create, update, and delete actions can change callback delivery behavior, and webhook deletion is permanent. <br>
Mitigation: Require explicit confirmation for webhook changes and retain webhook IDs and signing secrets according to the user's operational process. <br>


## Reference(s): <br>
- [H-ear World](https://h-ear.world) <br>
- [ClawHub Skill Page](https://clawhub.ai/badajoz95/h-ear) <br>
- [Publisher Profile](https://clawhub.ai/user/badajoz95) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text CLI responses with job metadata, sound classifications, tables, temporary URLs, and webhook results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires H-ear credentials and environment selection; some commands may return temporary audio/report URLs or one-time webhook signing secrets.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
