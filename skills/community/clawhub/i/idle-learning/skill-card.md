## Description:

AI持续学习系统让 an agent periodically collect GitHub trend and arXiv paper signals, summarize them, and store the results as local learning records for later memory workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freak30](https://clawhub.ai/user/freak30)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to give an OpenClaw-style agent an idle-time learning loop that gathers public GitHub and arXiv signals, summarizes them, and saves concise local learning logs for review or memory distillation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended collection can persist untrusted public internet content into local learning files.

Mitigation: Scope allowed sources and topics, review saved records, and apply explicit retention limits before using the data in later agent workflows.

Risk: Fetched GitHub or arXiv content may contain prompt-injection text or misleading claims.

Mitigation: Treat collected content as untrusted data, summarize it with prompt-injection defenses, and require human review before promotion into long-term memory.

Risk: The artifact uses plain HTTP arXiv query URLs.

Mitigation: Require HTTPS arXiv URLs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freak30/skills/idle-learning)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Console text plus JSON learning records and Markdown study logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores recent learning entries in learnings.json and appends brief topic summaries to study_log.md.]

## Skill Version(s):

1.0.0 (source: server release evidence, target metadata, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
