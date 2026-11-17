## Description:

Helps agents summarize and compare public Meituan merchant, product, deal, price, rating, and promotion information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting analysts use this skill to gather concise summaries and comparisons from public Meituan merchant, product, and offer pages. It is intended for lightweight internal insight, not ordering, login-only data access, bulk scraping, reverse engineering, or bypassing platform controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be misused for login-only data, ordering, scraping at scale, or attempts to bypass platform controls.

Mitigation: Use it only for explicit tasks involving public Meituan pages, keep request frequency low, and exclude ordering, authenticated data, reverse engineering, and control-bypass workflows.

Risk: Prices, delivery details, promotions, and availability can vary by time and region.

Mitigation: Confirm location-sensitive results and label summaries with the relevant region and collection time before using them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/meituan-ai)
- [Meituan homepage](https://www.meituan.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown summaries, comparison notes, and extraction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Location- and time-sensitive findings should include the relevant region and collection time.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
