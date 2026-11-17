## Description:

Analyze the opportunity landscape of a given industry across demand scenarios, customer pain points, policy opportunities, and likely future developments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to generate the opportunity section of an industry analysis workflow, including market scenarios, customer pain points, policy opportunities, and forward-looking trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform web searches and generate policy or market claims from sparse sources.

Mitigation: Review generated claims for source quality and mark unsupported conclusions explicitly before using the report.

Risk: The skill creates or modifies local files under output/{industry-slug}, including session.json.

Mitigation: Run it in the intended workspace and review generated report and session-state changes before committing or reusing them.

## Reference(s):

- [Industry Opportunity 4-Dimension Framework](references/opportunity-dimensions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report plus local session state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/{industry-slug}/04-opportunity.md and updates output/{industry-slug}/session.json.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
