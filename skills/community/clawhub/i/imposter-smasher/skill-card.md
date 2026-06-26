## Description: <br>
Prepares users for upcoming meetings or events by selecting a next-day calendar event, researching the topic and participants, producing an executive summary, and generating a 3-5 minute audio briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sourishkrout](https://clawhub.ai/user/sourishkrout) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external-facing teams use this skill to prepare for customer, investor, executive, partner, or event meetings with concise research, participant notes, recommended questions, and an audio briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may use calendar metadata and selected meeting details. <br>
Mitigation: Use pasted or sanitized event summaries for confidential meetings and limit attendee details to what is needed for preparation. <br>
Risk: Research and audio generation may involve external services. <br>
Mitigation: Use Contextual.ai and the selected audio provider only when their data handling is acceptable for the meeting contents. <br>
Risk: Participant or topic research can become misleading if claims are weakly sourced. <br>
Mitigation: Ground material claims in credible sources, label low-confidence inferences, and avoid unsupported speculation or rumor-based profiling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sourishkrout/imposter-smasher) <br>
- [Workflow Rubric](references/workflow-rubric.md) <br>
- [Source Credibility Rubric](references/source-credibility-rubric.md) <br>
- [Executive Summary Template](references/executive-summary-template.md) <br>
- [Audio Brief Template](references/audio-brief-template.md) <br>
- [Implementation Notes](references/implementation-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, audio] <br>
**Output Format:** [Markdown executive summaries, plain-text narration scripts, JSON audio manifests, MP3 or WAV audio artifacts, and artifact paths or links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets a 3-5 minute spoken runtime and includes source citations and confidence labels where evidence is weak.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
