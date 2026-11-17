## Description:

Lark Contact helps agents look up Lark/Feishu users by name, email, or open_id and return identifiers and profile fields needed before messaging, scheduling, or displaying contact details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu2003li](https://clawhub.ai/user/gu2003li)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace agents use this skill to resolve Lark/Feishu contact names, email addresses, and open_id values before sending messages, adding people to meetings or groups, or presenting contact profile details to a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query Lark directory data visible to the current user account, which may include workplace personal data.

Mitigation: Install and use it only for legitimate workplace tasks, and handle returned profile details according to organizational data policies.

Risk: Ambiguous contact matches could lead an agent to message, invite, or schedule with the wrong person.

Mitigation: Show multiple plausible matches to the user and ask for confirmation before taking actions with side effects.

Risk: Broad filter-only searches can enumerate contact data within the user's permission scope.

Mitigation: Avoid broad filter-only searches unless there is a valid business reason and prefer specific name, email, or open_id lookups.

## Reference(s):

- [+get-user reference](references/lark-contact-get-user.md)
- [+search-user reference](references/lark-contact-search-user.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Lark CLI commands, contact lookup constraints, disambiguation guidance, and permission or visibility cautions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
