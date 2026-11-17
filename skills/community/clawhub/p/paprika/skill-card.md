## Description:

Access recipes, meal plans, and grocery lists from Paprika Recipe Manager. Use when user asks about recipes, meal planning, or cooking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve Paprika Recipe Manager recipes, meal plans, grocery lists, and categories through the Paprika CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a third-party npm CLI package can add supply-chain and local execution risk.

Mitigation: Verify that paprika-recipe-cli is the intended package before installation and avoid running npm with administrator privileges.

Risk: Paprika account credentials can be exposed if environment variables are stored in shell profiles, logs, or shared environments.

Mitigation: Prefer the interactive paprika auth flow and do not commit or persist PAPRIKA_EMAIL or PAPRIKA_PASSWORD in shared locations.

## Reference(s):

- [Paprika Recipe Manager](https://www.paprikaapp.com)
- [ClawHub Paprika skill page](https://clawhub.ai/mjrussell/skills/paprika)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Paprika CLI commands; some commands support JSON output through --json.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
