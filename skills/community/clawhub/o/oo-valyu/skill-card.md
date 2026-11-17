## Description:

Valyu (valyu.ai). Use this skill for ANY Valyu request — searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Valyu through an OOMOL-connected account use this skill to search web, academic, financial, and proprietary data. It guides agents to inspect the live action schema before submitting a search request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes a remote installer whose behavior has not been verified. Searches also pass through the connected OOMOL account, and server-side credential protections remain unverified.

Mitigation: Review setup behavior, install a reviewed and pinned oo CLI yourself, and require approval before running installers or changing agent skills. Review the connected account's permissions and billing.

## Reference(s):

- [Valyu](https://valyu.ai)
- [Valyu API quickstart](https://docs.valyu.ai/quickstart)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured Valyu search results in JSON, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on Valyu's available data sources and the connected account.]

## Skill Version(s):

1.0.6 (source: skill metadata, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
