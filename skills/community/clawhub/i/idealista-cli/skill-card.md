## Description:

Use the idealista CLI to search Idealista listings by location, fetch listing details, and format command output for table or JSON workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjtf93](https://clawhub.ai/user/pjtf93)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to form idealista-cli commands for searching Idealista real estate listings by location, applying filters, requesting JSON output, and fetching listing details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to run idealista-cli commands that make network requests to Idealista and rely on API-related environment variables.

Mitigation: Use it only when the user already intends to use idealista-cli for Idealista data, review command flags before execution, and avoid exposing API credentials in prompts or logs.

Risk: The skill itself contains only usage instructions, so actual results depend on the installed idealista-cli package and Idealista service responses.

Mitigation: Verify the installed CLI behavior, inspect command output, and check non-zero exit codes when scripting JSON workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pjtf93/skills/idealista-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe idealista-cli table or JSON output expectations and non-zero exit code handling.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
