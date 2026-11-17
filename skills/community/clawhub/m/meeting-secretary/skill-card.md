## Description:

Meeting Secretary analyzes meeting transcripts or notes and produces structured meeting minutes with key points, decisions, disagreements, action items, sentiment cues, and inferred subtext.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuzhiguocarter](https://clawhub.ai/user/wuzhiguocarter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to turn completed meeting transcripts or notes into structured Markdown minutes for decisions, discussions, project updates, brainstorming sessions, one-on-ones, and training or sharing meetings. For long transcripts, the bundled splitter can divide text into manageable segments before the agent synthesizes the final minutes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts may contain confidential business information, personal data, or sensitive participant statements.

Mitigation: Confirm authorization before processing meeting content and redact confidential information or personal data when appropriate.

Risk: Optional dependency installation or upgrade commands can change the execution environment or introduce unreviewed package versions.

Mitigation: Run optional pip install or upgrade commands only in a dedicated virtual environment with reviewed dependency versions.

Risk: Generated interpretations of tone, sentiment, or subtext may be incorrect or overstate what the transcript proves.

Mitigation: Review generated minutes before sharing or acting on them, and mark uncertain interpretations for confirmation.

## Reference(s):

- [Meeting Secretary README](README.md)
- [Best Practices Guide](references/best_practices.md)
- [ClawHub skill page](https://clawhub.ai/wuzhiguocarter/skills/meeting-secretary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown meeting minutes with optional shell commands for transcript splitting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summaries, participant viewpoints, decisions, consensus and disagreement points, action items, risk notes, sentiment or tone analysis, value-density scoring, and suggested follow-up.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
