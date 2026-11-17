## Description:

PASM Tutor provides an offline learning tutor agent that tracks per-topic mastery, recommends weak topics for practice, responds with encouragement, and exports machine-readable student progress snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building education agents and tutoring experiences use this skill to add offline adaptive practice, encouraging learner feedback, and JSON progress snapshots for profile or reporting systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tutor can persist student progress and mistake history locally, which may include sensitive student data.

Mitigation: Use it only in environments approved for that data, review the upstream pasm-agents package before deployment, and avoid entering unnecessary personal information.

Risk: The artifact documents product limitations, including no built-in forgetting curve and literal rather than semantic mistake retrieval.

Mitigation: Treat mastery snapshots as decision support, validate behavior with educators or domain owners, and add decay or review logic when the deployment requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arronjack/skills/pasm-tutor)
- [PASM agents homepage](https://github.com/arronJack/pasm-agents)
- [PASM skills tutorial](https://github.com/arronJack/pasm-skills/blob/master/docs/TUTORIAL.md)
- [PASM agents Gitee fallback](https://gitee.com/arronzheng/pasm-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks, plus JSON-like progress snapshot examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced tutor agent is offline-runnable and can produce text replies and machine-readable mastery snapshots.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
