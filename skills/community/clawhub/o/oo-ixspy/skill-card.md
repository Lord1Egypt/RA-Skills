## Description:

Use IXSPY to search AliExpress products, stores, categories, rankings, and market metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use IXSPY to investigate AliExpress products, stores, categories, rankings, and sales trends through a connected IXSPY account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote installers whose full behavior was unavailable for review, and startup skill synchronization may change other agent skills.

Mitigation: Review the CLI setup, install a verified fixed release, and set OO_SKILLS_SYNC_DISABLED=1 for invocations where you want to avoid startup skill synchronization.

Risk: IXSPY requests use the connected OOMOL account and may consume credits.

Mitigation: Check the connected account's access and credit usage before running requests.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [IXSPY](https://ixspy.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [JSON data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and lookup results; detail lookups support up to 10 products or stores, and trend data covers up to 90 days.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
