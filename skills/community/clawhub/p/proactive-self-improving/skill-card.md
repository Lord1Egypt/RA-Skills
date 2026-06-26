## Description: <br>
Helps an agent capture failures, corrections, feature requests, and task reviews into local learning records, then promote repeated lessons into durable guidance with anti-drift checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lygjoey](https://clawhub.ai/user/lygjoey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give an agent a structured way to record lessons from failures, corrections, missing capabilities, and completed tasks. It is intended for workspaces where persistent local learning notes and manually reviewed promotions are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local learning notes may capture task details, sensitive personal data, credentials, or proprietary information. <br>
Mitigation: Install only in workspaces where persistent local notes are acceptable, and add redaction, retention, and deletion controls before using it around sensitive data. <br>
Risk: Promoting learnings into long-term files or generated skills can change future agent behavior without clear approval. <br>
Mitigation: Require manual review and approval before promotions or new skill creation, and regularly review .learnings/, AGENTS.md, TOOLS.md, SOUL.md, and generated skills. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lygjoey/proactive-self-improving) <br>
- [Publisher profile](https://clawhub.ai/user/lygjoey) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown instructions with file templates, shell examples, and JSONL log examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local learning records and promotion guidance when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
