## Description: <br>
Guides new users through OpenClaw setup, capability discovery, persistent memory, skill discovery, and group chat summary workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binson1994](https://clawhub.ai/user/binson1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
New OpenClaw users and the agents assisting them use this skill to run a short onboarding flow. It teaches basic setup, capability discovery, persistent memory, self-service skill installation, and group chat summary prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory examples can save personal, business, or sensitive information in local OpenClaw files. <br>
Mitigation: Avoid storing secrets or sensitive personal or business data, and review saved memory files before relying on or sharing them. <br>
Risk: The onboarding flow teaches skill installation, including confirmation-skipping commands, which can install unreviewed third-party skills. <br>
Mitigation: Review a skill's publisher, source, permissions, and security guidance before installation; avoid confirmation-skipping install flags for new skills. <br>
Risk: Group chat summary examples can process or export conversation content that the user may not be authorized to access or share. <br>
Mitigation: Use chat-summary and document-export features only for conversations and destinations where the user has authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binson1994/openclaw-onboarding) <br>
- [Publisher profile](https://clawhub.ai/user/binson1994) <br>
- [README](artifact/README.md) <br>
- [OpenClaw quickstart training](artifact/references/training/quickstart.md) <br>
- [Find Skills reference](artifact/references/find-skills/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with example prompts, tables, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes onboarding scripts and examples that may write local OpenClaw configuration and memory files when followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
