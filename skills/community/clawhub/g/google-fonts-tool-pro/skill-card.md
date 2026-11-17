## Description:

谷歌字体工具专业版 helps developers and teams plan Google Fonts self-hosting, font subsetting, typography system governance, performance budgets, and font license audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and web platform teams use this skill to create self-hosted Google Fonts workflows, subset multilingual font assets, define typography tokens, manage LCP-focused font budgets, and audit font licensing before commercial deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's trigger language includes unrelated security, encryption, and generic automation tasks outside the Google Fonts workflow.

Mitigation: Use the skill only for Google Fonts self-hosting, subsetting, typography performance, and font licensing tasks; reject unrelated security or encryption requests.

Risk: The skill may propose shell commands and file-write actions for downloading, subsetting, and hosting font files.

Mitigation: Review commands, paths, and external URLs before execution, and run them in a controlled workspace.

Risk: Incorrect font license interpretation could affect commercial redistribution or modified font use.

Mitigation: Confirm each font's license and required notices from authoritative font sources before commercial release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/google-fonts-tool-pro)
- [google-webfonts-helper API example](https://gwfh.mranftl.com/api/fonts/inter?download=zip&subsets=latin&variants=regular,600)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash, CSS, HTML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose shell commands and file-write steps for font hosting, subsetting, performance budget, and license audit workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
