## Description:

Analyzes images to detect AI generation, extract metadata, identify artifacts, and perform content moderation using local and cloud-based tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi)

### License/Terms of Use:


## Use Case:

Developers and review teams use this skill to configure image-detection workflows that identify likely AI-generated images, inspect metadata and visible artifacts, and choose between privacy-focused local analysis and cloud-based moderation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rely on changing npm packages without pinned versions or a lockfile.

Mitigation: Audit packages before installation, pin dependency versions, and use a lockfile for repeatable installs.

Risk: Hive API and reverse-image-search workflows may send images or metadata to outside services.

Mitigation: Use the privacy-focused configuration for sensitive images and require explicit network and data-flow documentation before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/skills/image-detection)
- [Publisher profile](https://clawhub.ai/user/raghulpasupathi)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and JSON or JavaScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local-only and cloud API configuration options for image analysis workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
