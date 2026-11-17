## Description:

Identifies prolific patent inventors in a technology area and organizes public patent evidence into a talent shortlist for recruiting, expert search, or partnerships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External hiring teams, recruiters, and partnership leads use this skill to identify inventors active in a technology area, review their public patent activity and organizations, and prepare a shortlist for recruiting, expert search, or collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and filters may disclose confidential project details to PatentMax.

Mitigation: Use public terminology and omit confidential project details.

Risk: API keys may be exposed if pasted into chat or stored insecurely.

Mitigation: Prefer the limited trial or a securely supplied restricted key; do not paste production credentials into chat.

Risk: Retrying a timed-out paid patent download may incur charges.

Mitigation: Set a spending limit and check provider billing before retrying.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ip930/skills/patent-talent-finder)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Search workflow](artifact/references/search-workflow.md)
- [Query syntax](artifact/references/query-syntax.md)
- [API reference](artifact/references/api-reference.md)
- [Search pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV]

**Output Format:** [Markdown summary and UTF-8 CSV talent shortlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranked by patent count; based only on publicly disclosed patent information; excludes contact details.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
