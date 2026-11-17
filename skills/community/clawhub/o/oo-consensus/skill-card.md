## Description:

Consensus (consensus.app). Use this skill for ANY Consensus request — searching and reading data. Whenever a task involves Consensus, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and analysts use this skill to search Consensus for relevance-ranked academic papers, with publication, study, and quality filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded CLI code whose contents were unavailable for inspection.

Mitigation: Install a verified oo CLI release yourself and review setup before enabling the skill.

Risk: The effects of managed-skill synchronization may be broader than the setup description makes clear.

Mitigation: Review the CLI's managed-skill synchronization settings and approve the Consensus connection deliberately.

## Reference(s):

- [Consensus](https://consensus.app)
- [Consensus API documentation](https://docs.consensus.app/reference/v1_search)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [JSON search results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relevance-ranked academic paper results can be filtered by publication, study, and quality criteria.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
