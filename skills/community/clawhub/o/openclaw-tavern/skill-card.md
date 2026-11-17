## Description:

SillyTavern-compatible roleplay plugin with character cards, long memory, multimodal output (TTS/image), and Generative-Agents-style companion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garfeildma](https://clawhub.ai/user/garfeildma)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and operators use this skill to run command-driven roleplay sessions with SillyTavern character cards, presets, lorebooks, long memory, TTS, image generation, and companion-style proactive interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported cards, URLs, and local files may contain untrusted prompt content or unsafe data.

Mitigation: Install only in a trusted, administrator-controlled OpenClaw environment and restrict /rp import access until URL and file import limits are enforced.

Risk: Roleplay conversations, persona instructions, summaries, and embeddings may persist in SQLite.

Mitigation: Review retention expectations with users and configure storage, deletion, and access controls before deployment.

Risk: Persona synchronization and image configuration changes can affect shared agent behavior.

Mitigation: Require administrator preview and approval for persona sync, and make global image configuration changes authorized and auditable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/garfeildma/skills/openclaw-tavern)
- [Project Homepage](https://github.com/garfeildma/openclaw-tavern)
- [OpenClaw RP Plugin Architecture](docs/ARCHITECTURE.md)
- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chat responses, command output, Markdown guidance, JSON configuration snippets, and optional generated media references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist imported assets, roleplay turns, summaries, and embeddings when SQLite storage is enabled.]

## Skill Version(s):

0.1.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
