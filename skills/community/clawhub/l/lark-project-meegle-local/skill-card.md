## Description:

Connects to Lark Project/Meegle to query and manage work items and todos, detecting login status and guiding Device Code authorization when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to connect an agent to Lark Project/Meegle, authenticate with Device Code flow, query todos and work items, and create or update work item records through the Meegle CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm package during login and work-item changes.

Mitigation: Install only if the npm package and Meegle account scope are trusted, and prefer a pinned reviewed CLI version.

Risk: The skill can create or update Meegle work items after authentication.

Mitigation: Run with least-privilege credentials and review create or update actions before allowing the agent to execute them.

Risk: Device Code authorization could expose the user to the wrong login destination if domains are not checked.

Mitigation: Verify login domains before authorizing access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuliyuan2026/skills/lark-project-meegle-local)
- [@lark-project/meegle npm package](https://www.npmjs.com/package/@lark-project/meegle)
- [MQL syntax reference](artifact/references/mql-syntax.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON output from the Meegle CLI when executing supported operations.]

## Skill Version(s):

0.1.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
