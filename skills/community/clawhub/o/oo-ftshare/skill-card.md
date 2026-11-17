## Description:

FTShare (ftai.chat). Use this skill for ANY FTShare request — searching and reading data. Whenever a task involves FTShare, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search and read FTShare company snapshots and A-share financial statements, earnings reports, and forecasts through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback executes unverified remote code and may introduce broader agent changes without clear user control.

Mitigation: Review the CLI installation before allowing setup; use a verified, fixed release and disable managed-skill synchronization if only FTShare access is needed.

Risk: Requests may incur charges through OOMOL.

Mitigation: Check applicable OOMOL billing and request costs before using the connected service.

## Reference(s):

- [FTShare homepage](https://ftai.chat/ftshare)
- [FTShare API documentation](https://market.ft.tech/gateway/doc/p/g6ba7f1z)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [FTShare financial data as JSON, with natural-language summaries or answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only company and financial information; requires an FTShare connection.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
