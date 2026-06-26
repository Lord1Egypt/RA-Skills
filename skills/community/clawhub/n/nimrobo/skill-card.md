## Description: <br>
Use the Nimrobo CLI for voice screening and matching network operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virang-nimrobo](https://clawhub.ai/user/virang-nimrobo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to get guidance for installing and using the Nimrobo CLI for voice screening workflows, matching-network operations, organization and post management, applications, messaging, and JSON-based automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-backed CLI commands can perform sensitive organization, hiring, messaging, onboarding, export, and batch operations. <br>
Mitigation: Require explicit user confirmation before destructive or consequential actions, including deletes, role or member changes, message sends, application decisions, transcript or audio exports, onboarding, and batch operations. <br>
Risk: Nimrobo usage depends on trusting the Nimrobo service, npm CLI package, and locally stored API key. <br>
Mitigation: Install only from trusted sources, protect the API key file, and prefer least-privileged credentials when available. <br>
Risk: Saved Net context can cause commands using current to target the wrong organization, post, channel, or user. <br>
Mitigation: Review saved context before write actions and clear or reset context when switching tasks. <br>


## Reference(s): <br>
- [Nimrobo Skill Overview](artifact/SKILL.md) <br>
- [Installation & Setup](artifact/installation.md) <br>
- [Nimrobo CLI Documentation](artifact/core.md) <br>
- [Nimrobo CLI Command Reference](artifact/commands.md) <br>
- [Voice Commands - Detailed Reference](artifact/voice-commands.md) <br>
- [Net Commands - Detailed Reference](artifact/net-commands.md) <br>
- [Nimrobo CLI Workflow Guide](artifact/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce human-readable text or machine-readable JSON when the --json flag is used.] <br>

## Skill Version(s): <br>
0.17.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
