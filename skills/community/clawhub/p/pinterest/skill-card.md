## Description:

Search and browse Pinterest pins, get pin details, and send actual images to the user via Telegram/messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xs4m1337](https://clawhub.ai/user/0xs4m1337)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find visual inspiration on Pinterest, inspect pin details, and send image media directly in chat. Developers can also use the included OAuth-based commands to read their own Pinterest boards and pins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse Pinterest and send external images where that behavior is not intended.

Mitigation: Use it only in workflows where Pinterest browsing and external image delivery are expected, and review image results before forwarding them.

Risk: Pinterest access tokens and app secrets can expose account data if pasted into chats or logs.

Mitigation: Treat PINTEREST_ACCESS_TOKEN and OAuth secrets as sensitive credentials, store them outside shared transcripts, and limit scopes to the required read permissions.

Risk: The script can install an unpinned httpx dependency at runtime if it is missing.

Mitigation: Run the skill in a controlled environment with dependencies preinstalled from pinned versions instead of allowing runtime package installation.

## Reference(s):

- [Pinterest OAuth Setup](references/oauth-setup.md)
- [Pinterest API v5 Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, images, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser/message commands, shell command examples, and optional JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send Pinterest image media directly through the agent's messaging tool; API commands require PINTEREST_ACCESS_TOKEN.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
