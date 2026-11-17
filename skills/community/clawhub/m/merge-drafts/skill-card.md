## Description:

Merges supplied drafts and review comments into one coherent document while preserving useful contributions, source attribution, and unresolved conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and other users merge multiple supplied drafts or integrate review comments into a coherent document without losing attribution or concealing unresolved factual conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions may change local agent skill directories.

Mitigation: Review the README commands before installing and run only those for agents in use.

Risk: The skill may read private documents through host connectors already authorized for the agent.

Mitigation: Provide only drafts and documents you are authorized to merge; do not broaden access or share documents publicly.

Risk: Conflicting or unavailable source material could lead to misleading merged claims.

Mitigation: Keep citations and unresolved claims visible, and label missing inputs rather than inventing a complete merge.

## Reference(s):

- [Merge Drafts on ClawHub](https://clawhub.ai/0xcjl/skills/merge-drafts)
- [Codex skills documentation](https://developers.openai.com/codex/skills/)
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills)
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)
- [OpenClaw skills documentation](https://docs.openclaw.ai/cli/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown or plain text by default; other formats only when supported and requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Merged document first, with brief source and decision notes and any unresolved conflicts; a separate file when saving is requested.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
