## Description:

Skill for interacting with OurGroceries.com to manage shopping lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poedenon](https://clawhub.ai/user/poedenon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation agents use this skill to add, retrieve, remove, and synchronize OurGroceries shopping-list items from voice or text workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify a real OurGroceries account using an email and password.

Mitigation: Provide credentials through a secure environment or vault, avoid plaintext env files in shared workspaces, and run commands only against the intended account.

Risk: The vendored client logs an authenticated session cookie at debug level.

Mitigation: Remove or redact session-cookie logging before use, and keep debug logs out of shared or persistent log stores.

Risk: Removal and deletion operations can change shopping lists destructively.

Mitigation: Require explicit confirmation for destructive actions and verify the target list and item names before execution.

Risk: The browser DevTools monitor can print private request data while observing a real account.

Mitigation: Use the monitor only for controlled debugging and avoid running it on accounts or sessions containing private data.

## Reference(s):

- [OurGroceries API Reference](references/api_reference.md)
- [OurGroceries](https://www.ourgroceries.com)
- [py-our-groceries](https://github.com/ljmerza/py-our-groceries)
- [ClawHub Skill Page](https://clawhub.ai/poedenon/skills/ourgroceries)
- [Publisher Profile](https://clawhub.ai/user/poedenon)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from or modify a live OurGroceries account when credentials are configured.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
