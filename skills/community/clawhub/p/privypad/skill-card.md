## Description:

Interact with the PrivyPad.com API to read, create, update, delete, and organize encrypted notes and groups on behalf of a user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aididmyhomework](https://clawhub.ai/user/aididmyhomework)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage their PrivyPad notes and groups through the PrivyPad API, including search, filtering, tagging, pinning, updates, and deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive PrivyPad notes and bearer tokens.

Mitigation: Use only tokens the user is comfortable providing to an agent, and do not place real pp_ tokens in source files or logs.

Risk: The skill can delete notes, including permanent deletion when requested.

Mitigation: Require explicit user confirmation before deletion, especially before using permanent deletion.

Risk: The evidence notes conflicting guidance about the encryption/API model and plaintext examples.

Mitigation: Clarify PrivyPad's encryption and API behavior before sending confidential note content through examples or generated requests.

## Reference(s):

- [PrivyPad API base URL](https://www.privypad.com/api/v1/)
- [ClawHub skill page](https://clawhub.ai/aididmyhomework/skills/privypad)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration]

**Output Format:** [Markdown with REST endpoint examples and JavaScript/Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP request patterns that use a user-supplied PrivyPad bearer token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
