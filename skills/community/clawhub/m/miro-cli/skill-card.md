## Description:

Miro CLI tool for board/team/org management via command line. Use when querying boards, exporting data, viewing teams/organizations, or automating Miro workflows from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and operations teams use this skill to query Miro boards, teams, organization details, logs, and board exports from a terminal-based workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned community CLI that handles Miro OAuth credentials and organization data.

Mitigation: Review or pin the CLI before use, avoid elevated npm installs, and test with a non-production tenant first.

Risk: Board exports and CSV inventories can contain sensitive organization data.

Mitigation: Store generated files only in access-controlled locations and treat CSV output as untrusted before opening it in spreadsheet software.

Risk: Broad Miro OAuth permissions can expose more data than a workflow requires.

Mitigation: Use least-privilege Miro scopes for the OAuth app and avoid using production credentials until the workflow is reviewed.

## Reference(s):

- [Miro CLI Command Reference](references/commands.md)
- [Miro CLI Scripts Reference](references/scripts.md)
- [mirocli npm package](https://www.npmjs.com/package/mirocli)
- [mirocli source repository](https://github.com/davitp/mirocli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and helper shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local board exports and CSV or JSON inventories when the documented commands or helper scripts are run.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
