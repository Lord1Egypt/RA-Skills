## Description:

记忆秘书 helps agents analyze local memory files to check quality, find similar past tasks, extract successful cases, identify work patterns, generate reminders, and create shareable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhm2084](https://clawhub.ai/user/yhm2084)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill in an OpenClaw workspace to maintain local memory directories, reduce duplicated work, and surface reusable experience before or during tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed security summary says the test suite can execute Python files outside the reviewed package.

Mitigation: Review or disable the included tests in CI until the external script paths are fixed.

Risk: The reviewed security summary says derived memory reports may be persisted under the workspace memory directory.

Mitigation: Run the skill only in workspaces where report persistence is acceptable and review generated reports before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhm2084/skills/memory-secretatry)
- [Publisher profile](https://clawhub.ai/user/yhm2084)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Python dictionaries, JSON report files, Markdown share reports, and human-readable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against workspace memory files and may persist derived reports under the workspace memory directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
