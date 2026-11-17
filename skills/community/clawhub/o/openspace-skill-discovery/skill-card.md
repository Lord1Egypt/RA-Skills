## Description:

Searches for reusable skills across OpenSpace's local registry and cloud community so agents can find relevant reusable capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search local and cloud skill registries, evaluate matching skills, and decide whether to follow, import, or delegate to a discovered skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud skill results may be automatically imported and followed without clear user approval or provenance checks.

Mitigation: Review cloud results before import or use, and prefer disabling automatic import unless the registry, publisher, version, and downloaded contents are trusted and the agent has limited permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/openspace-skill-discovery)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown guidance with tool-call examples and a decision flow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search accepts query, source, limit, and auto_import controls; cloud results may include a local_path when imported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
