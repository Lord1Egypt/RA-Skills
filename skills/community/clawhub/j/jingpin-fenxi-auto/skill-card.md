## Description:

Automates competitor research from public keywords or websites, gathering product, pricing, review, and SEO information into structured JSON or Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, marketers, product managers, and market analysts use this skill to collect public competitor information from keywords or URLs and produce structured comparison reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the host environment.

Mitigation: Use it only with public competitor domains or non-sensitive keywords, and avoid internal URLs, staging hosts, localhost, private-network addresses, or confidential research terms.

Risk: The skill can write reports to arbitrary paths.

Mitigation: Write reports only to a dedicated export folder that is acceptable to overwrite.

Risk: Network access may expose sensitive targets or broaden execution impact.

Mitigation: Review before installing and run in a network-restricted environment when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jingpin-fenxi-auto)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)
- [Skill homepage](https://miaoda.feishu.cn/app/app_4jpczkukw8tkd/)

## Skill Output:

**Output Type(s):** [text, markdown, json, files]

**Output Format:** [Markdown or JSON competitor analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reports to a user-specified output path when export is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
