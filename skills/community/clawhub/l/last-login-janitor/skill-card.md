## Description:

Scans developer storage for stale repositories, environments, Docker assets, caches, and model files, then proposes size-ranked cleanup candidates for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators audit disk usage across development projects, identify stale assets, and review suggested cleanup commands before reclaiming space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning inherited or untrusted repositories may run Git-controlled helper code under the user's account.

Mitigation: Avoid untrusted repositories or scan them in an isolated environment.

Risk: Executing proposed removal commands could delete valuable files or Docker assets.

Mitigation: Treat commands as suggestions; verify each target, protection reason, and restore cost before running anything.

Risk: A saved manifest can reveal local directory names and project paths.

Mitigation: Store manifests outside shared or sensitive locations and limit access to them.

## Reference(s):

- [Last-Login Janitor release on ClawHub](https://clawhub.ai/voronindenis5/skills/last-login-janitor)
- [Publisher profile on ClawHub](https://clawhub.ai/user/voronindenis5)
- [Dev-Cleanup Playbook](references/cleanup-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Text audit report with suggested shell commands; optional JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Size-ranked candidates include reasons and restore costs; proposed commands require human review and are not run automatically.]

## Skill Version(s):

1.0.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
