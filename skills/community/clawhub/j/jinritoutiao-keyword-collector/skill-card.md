## Description:

Automatically accesses the Jinri Toutiao homepage via browser automation, inputs keywords into the search bar, and collects related keyword suggestions from the auto-suggest dropdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External content, SEO, and market research users use this skill to collect Jinri Toutiao search suggestions for keyword research, trend discovery, content ideation, competitor analysis, and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates a browser session against Toutiao and may use an existing browser profile.

Mitigation: Use a non-sensitive browser session where possible and verify that the activity matches the site's terms and account expectations.

Risk: Excessive automated requests may create account, availability, or site-compliance risk.

Mitigation: Throttle collection, avoid high-frequency batches, and add waiting intervals between keyword searches.

Risk: Jinri Toutiao page structure can change, which may cause missing or incorrect suggestion extraction.

Mitigation: Use fresh browser snapshots during each run and verify the returned keyword suggestions before relying on them.

## Reference(s):

- [Browser Automation Best Practices](references/browser-automation-best-practices.md)
- [Jinri Toutiao Page Structure Description](references/toutiao-structure.md)
- [Jinri Toutiao](https://www.toutiao.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown numbered list of keyword suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include one or more keyword blocks when batch collection is requested.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
