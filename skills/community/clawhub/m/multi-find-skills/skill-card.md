## Description:

Multi Find Skills helps an agent search ClawHub, skills.sh, and LobeHub for relevant skills, compare quality signals, recommend candidates, and provide install guidance after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzairong](https://clawhub.ai/user/wangzairong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need to discover, compare, and select installable skills across ClawHub, skills.sh, and LobeHub. It is intended to produce ranked recommendations, quality scores, and installation commands while preserving explicit user preferences in local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill can guide agents toward external registry searches, package-manager-backed CLIs, and local skill-environment changes.

Mitigation: Review the skill before installation, inspect candidate skills before use, and require explicit user confirmation before running any install command.

Risk: The security guidance warns against force installs, global installs, auto-confirm flags, whole-repository installs, and registry-mirror commands without independent verification.

Mitigation: Avoid --force, -g, -y, whole-repository install commands, and registry mirror changes unless the exact source, version, and install scope have been verified.

Risk: Search queries leave the local machine for public registries, and local memory may store explicit preferences and search history.

Mitigation: Use specific but non-sensitive search terms, keep preference memory local, and record only preferences or feedback the user explicitly provides.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzairong/skills/multi-find-skills)
- [Publisher profile](https://clawhub.ai/user/wangzairong)
- [Search sources guide](artifact/sources.md)
- [Quality evaluation guide](artifact/evaluation.md)
- [Troubleshooting guide](artifact/troubleshooting.md)
- [ClawHub](https://clawhub.ai)
- [skills.sh](https://skills.sh)
- [LobeHub skills](https://lobehub.com/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown recommendations with comparison tables, four-factor scores, rationale, and install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and recommendation output can be influenced by local preference memory; live searches require registry CLIs such as clawhub and npx-backed tools.]

## Skill Version(s):

2.8.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
