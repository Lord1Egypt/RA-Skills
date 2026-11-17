## Description:

Helps agents manage Sonatype Nexus Repository 3 artifacts by browsing repositories, searching components, uploading or downloading files, and deleting components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiguang1017](https://clawhub.ai/user/weiguang1017)

### License/Terms of Use:

MIT

## Use Case:

Developers and repository administrators use this skill to find, publish, retrieve, and clean up artifacts in Sonatype Nexus Repository Manager 3.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloading from an arbitrary URL can send Nexus credentials to an external site.

Mitigation: Restrict downloads to trusted Nexus URLs and use a least-privileged account; do not pass external URLs to the download command.

Risk: Component deletion is irreversible and the CLI does not enforce confirmation.

Mitigation: Require a code-enforced confirmation gate in agent workflows, verify the component ID, and grant delete permission only when needed.

Risk: Implicit invocation or overly broad permissions can trigger unintended repository operations.

Mitigation: Review the skill before installing, limit implicit invocation where possible, and default to read-only repository access.

## Reference(s):

- [ClawHub release](https://clawhub.ai/weiguang1017/skills/nexus-repository-skill)
- [Server-resolved source repository](https://github.com/weiguang1017/nexus-repository-skill)
- [Usage guide](references/USAGE.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files]

**Output Format:** [Markdown guidance and shell commands; CLI results in JSON and downloaded asset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Nexus 3.0+ credentials; upload supports raw hosted repositories.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
