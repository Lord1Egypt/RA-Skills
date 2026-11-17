## Description:

Helps agents use the gurkerlcli command-line tool for Austrian online grocery shopping through gurkerl.at.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasogott](https://clawhub.ai/user/pasogott)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search groceries, inspect and modify a gurkerl.at shopping cart, manage shopping lists, and review order history for Austrian grocery delivery.

### Deployment Geography for Use:

Austria

## Known Risks and Mitigations:

Risk: The skill can lead users to expose or persist Gurkerl account passwords through command-line arguments, environment variables, or ~/.env.local.

Mitigation: Prefer interactive login or an OS credential manager, and avoid storing the Gurkerl password in shell history, environment variables, or local env files.

Risk: Cart and shopping-list commands can make authenticated changes to a user's grocery account.

Mitigation: Review proposed commands before execution and require clear confirmation for cart clearing, item removal, or list deletion.

Risk: The skill installs and invokes an external gurkerlcli package.

Mitigation: Verify the external package source and version before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pasogott/skills/gurkerlcli)
- [gurkerl.at](https://gurkerl.at)
- [GitHub Repository](https://github.com/pasogott/gurkerlcli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated cart, list, search, and order-history command guidance for gurkerlcli.]

## Skill Version(s):

0.1.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
