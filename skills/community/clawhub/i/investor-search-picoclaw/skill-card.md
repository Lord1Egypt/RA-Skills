## Description:

Builds sourced investor lists for a market in PicoClaw, separating investors from advisers, preserving source links, and delivering a workbook plus local run files for future continuation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chainleo](https://clawhub.ai/user/chainleo)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and business development teams using PicoClaw use this skill to build sourced investor prospect lists, enrich existing investor files, and resume later market runs without duplicating prior work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores investor-research files in the agent workspace, which may expose lead-research history in shared deployments.

Mitigation: Use a separate workspace per team or user, and limit workspace access to people authorized to see the investor list and research history.

Risk: The skill can attach the generated workbook to the active chat, including group or channel conversations.

Mitigation: Run it only in chats where all participants should receive the workbook, and avoid public/shared channels for sensitive investor research.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/chainleo/skills/investor-search-picoclaw)
- [README](README.md)
- [Environment](references/environment.md)
- [Lists](references/lists.md)
- [Why each rule exists](references/why.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown instructions with inline shell commands; completed runs produce an XLSX workbook and supporting CSV/ledger files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, web search/fetch tools, and workspace file persistence for resumable runs.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
