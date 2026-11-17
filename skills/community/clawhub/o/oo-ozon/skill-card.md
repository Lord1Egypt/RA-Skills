## Description:

Ozon (ozon.ru). Use this skill for ANY Ozon request — searching and reading data. Whenever a task involves Ozon, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and operators use this skill to retrieve product, pricing, stock, posting, and seller-account information through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded code without clear user approval or integrity checks, and the remote installer payloads were unavailable for inspection.

Mitigation: Review and approve CLI installation separately before allowing setup to run, and check its bundled-skill installation behavior.

Risk: The connected Ozon account provides access to seller data.

Mitigation: Limit the connected account to the read permissions needed for the task.

## Reference(s):

- [Ozon Seller API documentation](https://docs.ozon.ru/api/seller/zh/)
- [Ozon](https://www.ozon.ru)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON data and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves Ozon seller information through the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
