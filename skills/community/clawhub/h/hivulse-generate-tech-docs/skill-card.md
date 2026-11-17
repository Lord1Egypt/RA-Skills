## Description:

Hivulse蜂巢 AI generates structured technical documents for software projects by uploading a selected code directory to Hivulse's documentation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mojo-bo-coder](https://clawhub.ai/user/mojo-bo-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate requirements, design, test, and security assessment documentation from an existing software project directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected project directories may be uploaded broadly to Hivulse's cloud service.

Mitigation: Run the skill only on directories intended for upload, and remove secrets, private configuration, and unrelated sensitive files before use.

Risk: API key handling and local configuration may expose credential material.

Mitigation: Use a dedicated low-privilege Hivulse API key and check local config and log files for plaintext or exposed key material.

Risk: Project directories containing symlinks may expose files outside the intended upload scope.

Mitigation: Review or remove symlinks that point outside the selected project before running the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mojo-bo-coder/skills/hivulse-generate-tech-docs)
- [Hivulse website](https://www.hivulse.com)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown documents and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Hivulse API key; generated documents are produced through Hivulse's cloud service.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
