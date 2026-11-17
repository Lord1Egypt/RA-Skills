## Description:

Meeting Analyzer turns Tencent Meeting or Feishu meeting links into structured transcript analysis JSON, drawio summary diagrams, and Markdown/HTML meeting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team operators use this skill to analyze Tencent Meeting or Feishu transcripts from meeting links, extract key points, decisions, action items, and participant context, and produce shareable reports and diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive meeting transcripts, reports, and optional screenshots.

Mitigation: Use only with authorized meetings and keep generated reports, JSON files, and screenshots in access-controlled storage.

Risk: The release evidence flags mutable, unaudited npm-based tooling as a review concern.

Mitigation: Review before installing, use an isolated project or container, and pin and verify npm packages before running them.

Risk: Transcript and summary quality depends on upstream meeting transcripts, optional recordings, and LLM configuration.

Mitigation: Review extracted key points, decisions, action items, and snapshots before relying on or sharing the generated reports.

## Reference(s):

- [Source repository](https://github.com/samonysh/meeting-analyzer)
- [ClawHub skill page](https://clawhub.ai/samonysh/skills/meeting-analyzer)
- [Publisher profile](https://clawhub.ai/user/samonysh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, drawio, Markdown, HTML, and optional JPEG snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to a local output directory and may include meeting-derived sensitive content.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
