## Description:

Legal Brief Drafter helps organize case materials and draft structured Chinese-language legal documents, including post-hearing opinions, agency statements, appeals, answers, rebuttals, and evidence examination comments.

This skill is for research and development only.

## Publisher:

[1126053051-lgtm](https://clawhub.ai/user/1126053051-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

External users working with Chinese-language case materials use this skill to turn hearing records, evidence lists, legal provisions, and oral argument notes into structured draft legal documents. It is suited to administrative litigation, civil litigation, consumer protection, internet platform disputes, and contract disputes, with legal review required before reliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated legal analysis, confidence scores, or legal conclusions may be incorrect, outdated, or overstated.

Mitigation: Treat outputs as drafting assistance only; verify statutes and citations against current law and require review by a qualified legal professional before use.

Risk: The unsandboxed CLI reads input files and can overwrite user-selected output paths that may contain sensitive legal material.

Mitigation: Run the skill in a restricted workspace, redact confidential case details before use, and choose output paths carefully with backups for important files.

Risk: No server-resolved GitHub import provenance is available for this release.

Mitigation: Review the packaged artifact, server-resolved publisher profile, file hashes, and security summary before deployment.

## Reference(s):

- [Legal Brief Drafter on ClawHub](https://clawhub.ai/1126053051-lgtm/skills/legal-brief-drafter)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [CC BY-NC-SA 4.0 License Terms](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.zh-Hans)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Chinese-language Markdown documents, JSON analysis summaries, and CLI status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can write outputs to user-selected paths; generated legal conclusions and confidence scores require independent review.]

## Skill Version(s):

3.0.2 (source: server release metadata, skill.yaml, README, and SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
