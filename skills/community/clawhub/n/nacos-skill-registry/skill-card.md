## Description:

Discover, install, update, merge, and publish AI skills with Nacos for personal or team skill registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzyyj](https://clawhub.ai/user/lzyyj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to find and install skills from a Nacos registry, reconcile local changes with newer versions, and share skills through review and release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploads, reviews, or releases may affect the wrong registry or team namespace.

Mitigation: Confirm the active profile, namespace, and authentication mode before changing or publishing skills.

Risk: Private skill backups in /tmp may be exposed on shared machines.

Mitigation: Store private backups in a restricted directory and remove temporary copies when finished.

Risk: Local profiles and token files may contain sensitive credentials.

Mitigation: Keep credentials in local profiles or token files and avoid including them in shared skill documentation.

## Reference(s):

- [nacos-cli repository (listed skill homepage)](https://github.com/nacos-group/nacos-cli)
- [Nacos documentation](https://nacos.io/)
- [ClawHub skill release](https://clawhub.ai/lzyyj/skills/nacos-skill-registry)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May present skill search results, install options, and version or release status.]

## Skill Version(s):

0.0.8 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
