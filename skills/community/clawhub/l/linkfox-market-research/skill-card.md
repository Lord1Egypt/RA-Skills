## Description:

Generates a single-page Amazon US market research report from a category name and node ID, covering market overview, launch timing, pricing, reviews, brands, sellers, top competitors, and overall assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators, e-commerce analysts, and agents use this skill to generate Amazon category research from a category name and node ID. It automates LinkFox Agent tasks and merges returned HTML analyses into one report for market sizing, pricing, review, brand, seller, competitor, and opportunity assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include untrusted active web content when opened in a browser.

Mitigation: Review generated HTML before opening it in a privileged browser profile, and prefer a restricted browser context until report URL validation, HTML sanitization, remote script controls, and user-text escaping are added.

Risk: Prompts and report generation may expose sensitive business plans, secrets, or regulated data to the external LinkFox Agent API.

Mitigation: Avoid entering secrets, regulated data, or sensitive business plans, and use only inputs approved for the external service.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jiafar/skills/linkfox-market-research)
- [LinkFox Agent API key setup](https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Shell command workflow that produces a single-page HTML market research report plus terminal status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY, Python 3, network access to LinkFox Agent API, and a category name plus Amazon category node ID.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
