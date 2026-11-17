## Description:

Plasmic (plasmic.app). Use this skill for ANY Plasmic request — searching and reading data. Whenever a task involves Plasmic, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use the skill to count and list Plasmic CMS items through an OOMOL-connected account, with query filters, draft mode, and locale options where supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time CLI setup can execute downloaded code and may introduce persistent agent changes without a clear approval step; remote installer behavior is unverified.

Mitigation: Review and approve CLI installation separately, use an inspected and verified release, and consider OO_SKILLS_SYNC_DISABLED to prevent automatic skill synchronization.

Risk: The connected Plasmic account may grant broader access than the read-only count and list actions require.

Mitigation: Connect only the Plasmic account and permissions needed for the requested reads.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Plasmic CMS API reference](https://docs.plasmic.app/learn/plasmic-cms-api-reference/)
- [Plasmic](https://www.plasmic.app)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Plasmic CMS query results in JSON, with command guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only item counts and lists; results depend on the connected Plasmic account and query inputs.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
