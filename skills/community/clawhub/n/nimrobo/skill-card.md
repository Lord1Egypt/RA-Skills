## Description:

Use the Nimrobo CLI for voice screening and matching network operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virang-nimrobo](https://clawhub.ai/user/virang-nimrobo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to work with Nimrobo CLI workflows for voice interviews, screening sessions, user research, job posts, applications, organization management, and messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous global CLI installation can lead users to install the wrong package or version.

Mitigation: Verify the official Nimrobo npm package and release version before installing or running commands.

Risk: API keys may be exposed through shell history, logs, or the local `~/.nimrobo/config.json` file.

Mitigation: Avoid pasting keys into shell history, protect the config file, and rotate credentials if exposure is suspected.

Risk: The documented CLI workflows include high-impact operations such as deletes, membership changes, role changes, messages, applicant decisions, and bulk actions.

Mitigation: Require explicit human confirmation before executing account, organization, applicant, messaging, or bulk operations.

Risk: Transcripts, evaluations, and signed audio URLs may contain confidential personal data.

Mitigation: Handle voice session outputs as confidential data and avoid sharing or storing them outside approved systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/virang-nimrobo/skills/nimrobo)
- [Installation & Setup](artifact/installation.md)
- [Nimrobo CLI - Command Reference](artifact/commands.md)
- [Voice Commands - Detailed Reference](artifact/voice-commands.md)
- [Net Commands - Detailed Reference](artifact/net-commands.md)
- [Nimrobo CLI - Workflow Guide](artifact/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may propose authenticated Nimrobo CLI operations and JSON input/output patterns.]

## Skill Version(s):

0.17.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
