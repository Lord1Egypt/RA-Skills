## Description:

Open Hugging Face in the user's Brave browser and take the user to the Hugging Face homepage while reusing an existing Hugging Face tab or session when possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill as a browser shortcut to open Hugging Face in Brave, reuse an existing matching tab or authenticated session when present, and verify that the Hugging Face homepage is loaded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reuse an existing logged-in Brave session for Hugging Face.

Mitigation: It instructs the agent not to handle credentials, authentication codes, API keys, account settings, or content changes, and to stop at the login page if authentication is required.

Risk: A browser automation shortcut could land on an unexpected page if navigation or tab reuse is wrong.

Mitigation: It verifies that the expected Hugging Face destination is visibly loaded before reporting success.

## Reference(s):

- [Hugging Face Homepage](https://huggingface.co/)
- [ClawHub Skill Page](https://clawhub.ai/ruchir17-cmd/skills/open-huggingface)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with browser automation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Brave, prefers an existing matching tab, verifies the destination, and stops at login without handling credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
