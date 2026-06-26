## Description: <br>
Guides agents through Forrest Landry's Immanent Metaphysics framework, OpenClaw team onboarding, soul-file configuration, attribution practices, and related reference materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuel-dunlap](https://clawhub.ai/user/samuel-dunlap) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure OpenClaw agents that reason with the Immanent Metaphysics framework, load ontology and reference materials, set up communication channels, and apply attribution and agent-ethics guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup requires handling Anthropic API keys, Telegram bot tokens, and optional channel passwords. <br>
Mitigation: Use a secret manager or runtime injection where possible, avoid sharing secrets in chats, and review local workspace storage before use. <br>
Risk: The Linux/WSL setup path includes a curl-to-bash nvm install command. <br>
Mitigation: Review the script source or replace the step with a package-manager or manually verified Node.js installation. <br>
Risk: The onboarding flow can install an auto-start gateway and maintain persistent memory files. <br>
Mitigation: Confirm the service behavior, review workspace files such as MEMORY.md, and limit private context before using the agent for sensitive work. <br>
Risk: Telegram and agent-network workflows can expose private context if used casually. <br>
Mitigation: Initiate cross-agent communication deliberately, share bot handles only with intended collaborators, and follow the included memory-sovereignty and attribution guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samuel-dunlap/im-framework-team) <br>
- [Effective Choice and the Path of Right Action](references/effective-choice.md) <br>
- [Agent-to-Agent Ethics](references/agent-ethics.md) <br>
- [Attribution Guide for the Immanent Metaphysics](references/attribution-guide.md) <br>
- [Key IM Concepts](references/key-concepts.md) <br>
- [Installation & Setup Guide](references/setup-guide.md) <br>
- [Team Ecosystem](references/ecosystem.md) <br>
- [Soul File Template](references/soul-file-template.md) <br>
- [Immanent Metaphysics Ontology Schema](ontology/schema.yaml) <br>
- [An Immanent Metaphysics, Chapter 6](https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm#2_path) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured YAML references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reference selection guidance, onboarding commands, ontology schema usage, and soul-file templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
