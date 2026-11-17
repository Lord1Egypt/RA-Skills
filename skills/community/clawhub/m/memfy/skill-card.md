## Description:

Capture durable user-approved memory when the user says memfy, without storing secrets or transient chatter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwithenoch](https://clawhub.ai/user/aiwithenoch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Memfy to ask an agent to persist concise, durable memory for future sessions while avoiding raw secrets, unsupported guesses, and transient conversation noise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory entries can persist across sessions and may later influence agent behavior.

Mitigation: Use the skill only for user-approved memory, keep entries concise and review the chosen memory file periodically.

Risk: Secrets or sensitive personal data could be stored if the user asks the agent to remember inappropriate details.

Mitigation: Do not save raw credentials, tokens, private keys, cookies, recovery codes, or sensitive personal data unless the user clearly permits necessary non-secret context.

Risk: The memory file location may be ambiguous when MEMFY_MEMORY_FILE or local instructions do not define it.

Mitigation: Ask the user where to save memory before writing when no durable memory target is discoverable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiwithenoch/skills/memfy)
- [ClawHub publisher profile](https://clawhub.ai/user/aiwithenoch)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown memory entries and brief text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append concise dated bullets to a durable memory file selected from MEMFY_MEMORY_FILE, local instructions, or user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
