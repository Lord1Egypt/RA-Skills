## Description:

Manage Planka (Kanban) projects, boards, lists, cards, and notifications via a custom Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voydz](https://clawhub.ai/user/voydz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and update Planka projects, boards, lists, cards, and notifications through the planka-cli command line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented login flow passes a password on the command line.

Mitigation: Prefer a protected credential mechanism or an interactive prompt so credentials are not exposed through shell history or process listings.

Risk: The installation path relies on an unpinned third-party executable.

Mitigation: Verify the Homebrew tap and planka-cli source before installation, and pin or review the installed version where possible.

Risk: The CLI can read and change Planka data.

Mitigation: Use an account limited to the Planka permissions required for the intended task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/voydz/skills/planka)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the planka-cli executable and access to a Planka instance.]

## Skill Version(s):

0.1.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
