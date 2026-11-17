## Description:

AnySearch (anysearch.com). Use this skill for ANY AnySearch request — searching and reading data. Whenever a task involves AnySearch, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search AnySearch's routed data sources, discover specialized search domains, and extract cleaned page content through their connected AnySearch account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installer and resulting binaries were not verified and setup may execute unverified software.

Mitigation: Review the CLI release and installer independently, and install the CLI separately before enabling automatic use.

Risk: Automatic skill synchronization can introduce persistent agent changes without clear user control.

Mitigation: Verify the release and review or disable automatic skill synchronization before enabling it.

Risk: Search inputs pass through OOMOL and AnySearch, and usage may incur charges.

Mitigation: Avoid sending sensitive search inputs and check applicable provider billing before use.

## Reference(s):

- [AnySearch homepage](https://anysearch.com/home)
- [AnySearch API documentation](https://www.anysearch.com/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [AnySearch ClawHub release](https://clawhub.ai/oomol/skills/oo-anysearch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Structured data]

**Output Format:** [Markdown content or structured search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results and extracted page content are returned for use in the agent's response.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
