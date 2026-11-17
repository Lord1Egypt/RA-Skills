## Description:

Obsidian persistent memory system: AI-delivered session continuity, task tracking, decision records, and project context for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to receive AI-delivered Obsidian memory support after clawtip payment verification, including work logs, task tracking, decision records, session continuity, note organization, and periodic reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad filesystem and credential permissions while saving the user's question locally.

Mitigation: Review before installing, and do not include secrets, vault excerpts, API keys, or private project details in the question.

Risk: The payment-verification helpers are weak and may affect payment integrity.

Mitigation: Treat payment authorization as a local gate only and review clawtip payment status before relying on service access.

Risk: The optional sandbox payment command invokes npx.

Mitigation: Run the sandbox payment command only in a constrained environment if it is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinyu12166/skills/obsidian-memory-system-clawhub-reviewfix)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON_RESULT status lines from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and stores payment order data locally before service authorization.]

## Skill Version(s):

3.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
