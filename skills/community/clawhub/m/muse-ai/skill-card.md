## Description:

Muse AI helps an agent guide users through conversational creation of original songs, instrumentals, BGM, lyrics, and arrangements using the Muse cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a64307410](https://clawhub.ai/user/a64307410)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill in supported agent CLIs to create original songs, instrumentals, background music, and lyrics through a short guided conversation. Developers can install it as an AgentSkill-compatible music creation assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Muse cloud service receives song prompts, account activity, a bearer token, and a persistent device-linked identifier.

Mitigation: Install only when this data handling is acceptable, treat Muse tokens as passwords, avoid sharing tokens in chats, and remove ~/.muse/token and ~/.muse/device_id when no longer using the skill.

Risk: The release includes an installer command that clones and runs shell code.

Mitigation: Inspect or pin the installer before allowing an agent to run it automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a64307410/skills/muse-ai)
- [Muse registration page](https://skills.muse.top/)
- [Register guide](assets/register-guide.md)
- [Style catalog](references/style-catalog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with inline shell commands and JSON API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include song metadata, audio links, cover links, authentication prompts, and progress updates.]

## Skill Version(s):

1.0.6 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
