## Description:

Coordinates independent coding workers across parallel tasks, from dispatch and monitoring through review, pull requests, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate separate coding tasks to multiple workers, monitor their progress, verify results, and coordinate delivery. It is not intended for a single short task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous workers can modify repositories and run terminal commands beyond the intended task.

Mitigation: Authorize each task explicitly, constrain worker scope, and review code changes and command effects before acceptance.

Risk: Remote dispatch and provider sessions can expose access to configured machines or credentials.

Mitigation: Enable only trusted remote nodes and provider sessions; keep real tokens and personal routing files out of published packages.

Risk: Auto-accept, pull-request cleanup, and background Autopilot or night-watch runs may cause unwanted persistent changes.

Mitigation: Review these features before enabling them and require explicit authorization for Git changes and unattended execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cat-xierluo/skills/multi-agent-orca)
- [Publisher-listed homepage (not verified import provenance)](https://github.com/cat-xierluo/legal-skills)
- [Orchestration reference](references/14-pm-orchestrate.md)
- [Remote dispatch reference](references/25-remote-node-dispatch.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with commands and task status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate worker-produced code changes, review evidence, and pull requests.]

## Skill Version(s):

3.0.1 (source: ClawHub release metadata, skill frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
