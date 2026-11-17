## Description:

Nex Deliverables helps agents manage local client deliverable records, deadlines, workload summaries, status emails, and CSV or JSON exports for agency and freelance projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External agency operators, freelancers, and developers use this skill to track client deliverables, update project status, identify overdue work, summarize workload, and generate client-facing status updates from local data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer has a path-handling code-injection risk when run from an unsafe directory path.

Mitigation: Install only from a trusted, plainly named directory and avoid paths containing quotes or unusual shell or Python metacharacters.

Risk: The local client database may be created with weak permissions on shared machines.

Mitigation: After setup, verify ~/.nex-deliverables is mode 700 and that the SQLite database is not readable by other users.

Risk: CSV or JSON exports may expose sensitive client deliverable data at the selected output path.

Mitigation: Treat exports as sensitive records and write them only to protected locations with appropriate access controls.

## Reference(s):

- [Nex Deliverables ClawHub page](https://clawhub.ai/nexaiguy/skills/nex-deliverables)
- [Nex AI homepage](https://nex-ai.be)
- [Artifact README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Plain text CLI output, generated email text, and optional CSV or JSON export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite storage under ~/.nex-deliverables; exported files can contain sensitive client deliverable data.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
