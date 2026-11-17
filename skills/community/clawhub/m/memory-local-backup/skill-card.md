## Description:

Infinite organized memory that complements your agent's built-in memory with unlimited categorized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[12357851](https://clawhub.ai/user/12357851)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and maintain a durable local memory folder for long-term project, contact, decision, knowledge, and collection records outside the agent's built-in memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates durable local records under ~/memory/, which can retain private information longer than the user expects.

Mitigation: Review what is written, avoid storing secrets or highly sensitive personal data, and periodically delete or archive entries that should no longer be retained.

Risk: Local memory entries can become hard to find or misleading if indexes are missing or stale.

Mitigation: Maintain INDEX.md files for each category and run periodic checks for unlisted files or dead links.

Risk: Optional sync from built-in memory can duplicate information and confuse which memory source is authoritative.

Mitigation: Keep sync one-way from built-in memory into ~/memory/, preserve separation from the agent's own MEMORY.md and workspace memory folder, and store detailed records locally while keeping only summaries in built-in memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/12357851/skills/memory-local-backup)
- [Publisher Profile](https://clawhub.ai/user/12357851)
- [Setup Guide](artifact/setup.md)
- [Memory Templates](artifact/memory-template.md)
- [Organization Patterns](artifact/patterns.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local Markdown file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local Markdown records under ~/memory/; no external services or network requests are required by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
