## Description:

MetaBot Basic helps agents create MetaID-based MetaBots, set avatar images, and send Buzz messages on the MVC network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newfish](https://clawhub.ai/user/newfish)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to create and manage MetaID-based MetaBot identities, attach avatar metadata, and publish Buzz messages through the MVC network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real wallet authority and stores recovery phrases and API keys in plaintext account files.

Mitigation: Use only in a constrained workspace with no valuable wallet funds; do not commit or share account.json; rotate any API key written there.

Risk: Avatar, name, and Buzz operations may submit on-chain actions and fees.

Mitigation: Require explicit confirmation of the selected account, content, fee, destination, network, and avatar file before executing any transaction.

## Reference(s):

- [Account Management](references/account-management.md)
- [Buzz Protocol](references/buzz-protocol.md)
- [ClawHub release page](https://clawhub.ai/newfish/skills/metabot-basic)
- [Metalet service](https://www.metalet.space)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update account.json and userInfo.json and may broadcast MVC transactions when the user approves execution.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
