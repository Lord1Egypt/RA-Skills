## Description:

A ClawHub wrapper that standardizes publishing, installation, governance, and backup workflows for custom user-created agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage personal my_ skills for OpenClaw and ClawHub. It helps publish backups, install skills, and keep agent skill bindings in configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can upload local skill contents, including accidental secrets or unintended files.

Mitigation: Publish only intended my_ skill directories under ~/.openclaw/skills and inspect contents for secrets before upload.

Risk: Installing an unpinned or unknown third-party skill can add untrusted instructions or code.

Mitigation: Install only trusted publishers and versions; pin the version when reproducibility matters.

Risk: Agent skill binding changes can enable capabilities for the wrong agent.

Mitigation: Review skills.json changes and enable only the expected my_ skill for the intended agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-skill-management-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose ClawHub publish/install commands and skills.json configuration changes for review.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
