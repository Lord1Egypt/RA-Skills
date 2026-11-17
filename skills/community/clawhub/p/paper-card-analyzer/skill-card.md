## Description:

Analyze `paper-parse` outputs and generate a research-oriented paper card directly in natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-li-17](https://clawhub.ai/user/chen-li-17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill after parsing a paper to produce a structured research summary covering contributions, methods, results, limitations, reproducibility notes, and future work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite paper-card.md and paper-card.json in the selected paper folder.

Mitigation: Keep backups or rename existing paper-card files before running the skill on a folder with prior work.

Risk: The skill appends revision history to paper-card-feedback.md.

Mitigation: Review the feedback log before sharing outputs if user feedback may include sensitive notes.

Risk: Paper summaries can become misleading if source evidence is incomplete or weak.

Mitigation: Follow the skill's evidence protocol by marking missing sections as not clearly stated and reviewing generated claims against the parsed paper content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen-li-17/skills/paper-card-analyzer)
- [ClawHub publisher profile](https://clawhub.ai/user/chen-li-17)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown and JSON files with a revision feedback log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes paper-card.md, paper-card.json, and paper-card-feedback.md in the selected paper folder.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
