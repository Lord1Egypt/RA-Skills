## Description: <br>
Enables AI agents to maintain session continuity, develop self-identity, and manage file-based long-term memory anchored by human partners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a local file-based continuity framework for personal, team, or autonomous agents. It provides templates and operating guidance for persistent identity notes, layered memory files, and session-start context loading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory files may contain sensitive configuration or personal context. <br>
Mitigation: Keep SOUL.md, MEMORY.md, and memory/*.md in a trusted workspace and review them regularly. <br>
Risk: Raw conversation dumps, secrets, credentials, private keys, mnemonic phrases, or regulated personal data could be loaded into future agent sessions if stored in memory files. <br>
Mitigation: Do not store secrets or sensitive personal data in the generated memory files. <br>
Risk: Installing the framework changes how an agent preserves and reloads local context. <br>
Mitigation: Install only when persistent local agent memory is intended and review the files before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/mupengism) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [MEMORY-SYSTEM.md](artifact/MEMORY-SYSTEM.md) <br>
- [SOUL-TEMPLATE.md](artifact/SOUL-TEMPLATE.md) <br>
- [PRINCIPLES.md](artifact/PRINCIPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory and identity setup guidance; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
