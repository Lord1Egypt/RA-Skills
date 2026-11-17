## Description:

Enables agents to search and read Keenable data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search Keenable's web index and fetch pages as Markdown for reading. Use requires an installed and authenticated oo CLI with Keenable connected to the intended OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run remote installer code, and automatic skill synchronization may make broader changes to installed agent skills.

Mitigation: Review setup behavior, install a verified oo CLI version, and decide whether to disable synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Requests through OOMOL may consume credits.

Mitigation: Connect the intended Keenable account and consider expected credit use before running requests.

## Reference(s):

- [Keenable](https://keenable.ai)
- [Keenable API documentation](https://docs.keenable.ai/api-reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Text or Markdown search results and fetched page content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and fetch results depend on the connected Keenable account and requested filters.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
