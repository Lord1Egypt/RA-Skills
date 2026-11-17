## Description:

Provides market-entity statistics for an L1 mini-program home page, including active enterprise counts, monthly additions, and regional distribution data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinxin970620-prog](https://clawhub.ai/user/xinxin970620-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents use this skill to retrieve market-entity statistics such as active enterprise counts, year-to-date growth, regional and scale distributions, enterprise pyramid data, financing statistics, and deregistration trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls a documented external dfwycredit endpoint for market-entity statistics.

Mitigation: Install it only when that network call is intended and confirm the rcd-test endpoint is appropriate for the deployment environment.

Risk: The API requires an API key.

Mitigation: Provide the key through a secure secret mechanism and avoid placing real keys in prompts, examples, logs, or shared transcripts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xinxin970620-prog/skills/marketsub-statistics)
- [Unified invoke endpoint](https://rcd-test.dfwycredit.com/s1/skill/unified-invoke)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown guidance with a bash curl example and JSON request/response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the API result directly; requires an API key and one province, city, or district code.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
