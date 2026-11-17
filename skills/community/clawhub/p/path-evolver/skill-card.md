## Description:

Path Evolver tracks skill success rates, discovers better tools, and prompts the user before changing tool choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyzlove](https://clawhub.ai/user/wyzlove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Path Evolver to track tool success across repeated tasks, cache effective paths, and discover alternative skills while keeping tool changes under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local workflow cache may contain task-related metadata or parameters.

Mitigation: Review or clear ~/.openclaw/workspace/.path-evolver/workflow-cache.json periodically and avoid caching sensitive parameters.

Risk: Discovery searches contact ClawHub and GitHub with task-type information.

Mitigation: Send only the task category, not user input or task parameters, and confirm network use is acceptable for the environment.

Risk: Suggested tool changes may be incorrect or unsuitable for a specific workflow.

Mitigation: Review recommendations manually before changing tool priority or adopting an alternative skill.

## Reference(s):

- [Path Evolver on ClawHub](https://clawhub.ai/wyzlove/skills/path-evolver)
- [Design decisions](references/design-decisions.md)
- [Declared ClawHub endpoint](https://clawhub.ai)
- [Declared GitHub API endpoint](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local workflow cache at ~/.openclaw/workspace/.path-evolver/workflow-cache.json.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
