## Description:

Finds Jike users who show vibecoding practice, entrepreneurial activity, or independent product-building work, then records verified candidates in a deduplicated local talent pool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinc913](https://clawhub.ai/user/robinc913)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, founders, and talent scouts use this skill to browse Jike, identify young vibecoding and independent-product talent, verify candidates from posts and profiles, and maintain a deduplicated candidate list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a logged-in browser profile for Jike can expose account context to the agent during browsing.

Mitigation: Use a dedicated or low-risk browser profile and authenticate only with the account intended for talent discovery.

Risk: The local talent-pool file stores candidate profile data and evidence links, which creates privacy and retention considerations.

Mitigation: Keep only necessary candidate fields, review the file periodically, and delete it when the stored records are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robinc913/skills/hunter-qg)
- [Jike web app](https://web.okjike.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown summary with local JSON talent-pool updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the number of new candidates, total pool size, and each new candidate's Jike ID and post link.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
