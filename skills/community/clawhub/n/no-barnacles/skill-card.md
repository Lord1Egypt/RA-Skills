## Description:

Guides setup and repair of a long-running agent's private memory, working state, incident ledger, and prompt-injection practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnayotte](https://clawhub.ai/user/cnayotte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal-agent operators use this skill to establish or repair private workspace memory, session handoffs, incident logging, and prompt-injection response practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private memory and user notes may expose personal information if shared or published.

Mitigation: Keep USER.md, MEMORY.md, STATE.md, daily notes, and tool notes local and private; do not store secrets in them.

Risk: Replacing or deleting existing workspace files can discard personal-agent context.

Mitigation: Merge templates into existing files; archive BOOTSTRAP.md rather than deleting it without explicit confirmation.

Risk: Flagged phrases alone cannot reliably prevent prompt injection.

Mitigation: Treat the phrase list as an alarm, require human approval for external actions, and verify protective controls independently.

## Reference(s):

- [ClawHub release](https://clawhub.ai/cnayotte/skills/no-barnacles)
- [Project homepage (listed in release metadata; import provenance unavailable)](https://github.com/cnayotte/no-barnacles)
- [Memory architecture](artifact/docs/memory-architecture.md)
- [Safety layers](artifact/docs/safety-layers.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration guidance]

**Output Format:** [Markdown guidance and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggests edits to private memory, state, agent instructions, and incident logs; bundles no executable code.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
