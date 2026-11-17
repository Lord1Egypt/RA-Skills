## Description:

Search and read Printify shop, order, and product data through a connected Printify account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and their assistants use the skill to inspect Printify shops, products, and orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote code and introduce broader persistent changes.

Mitigation: Review CLI installation separately before allowing automatic setup; prefer a pinned, verified release and restrict Printify permissions to the access needed.

Risk: The exact local effects of remote installers could not be inspected.

Mitigation: Review installer behavior before running it. The available evidence does not establish malicious intent.

## Reference(s):

- [Printify](https://printify.com/)
- [Printify API documentation](https://developers.printify.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-printify)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON data and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected read action and its inputs.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
