## Description:

Provides nine paste-ready inline-HTML layout templates and a swappable theme-color model for Chinese public-service and government-affairs WeChat official-account articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuaron895-cpu](https://clawhub.ai/user/wuaron895-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Editors, communications teams, and agent users use this skill to classify a government-service WeChat article, apply the matching article template, adjust the theme color, fill placeholders, and produce HTML that can be pasted into the WeChat official-account editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Templates include placeholders for account names, locations, hotlines, agency names, dates, legal details, links, QR codes, and article-specific content.

Mitigation: Replace and review every placeholder against approved source copy before publishing, and mark missing facts as needing editor completion instead of inventing them.

Risk: The auxiliary icon script can write generated output if run without reviewing its paths.

Mitigation: Use the script only when its output path has been reviewed, or rely on the static templates and theme-color workflow.

Risk: The security scan is clean, but generated HTML can still carry incorrect policy or public-service guidance if the input copy is wrong.

Mitigation: Review generated HTML for policy accuracy, legal names, dates, phone numbers, and links before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuaron895-cpu/skills/gov-service-wechat-layout)
- [README_EN.md](README_EN.md)
- [README.md](README.md)
- [Color slot model](references/color-slot-model.md)
- [Component library](references/component-library.md)
- [Layout SOP](references/layout-sop.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Paste-ready inline HTML with concise Markdown guidance and optional bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses de-identified account and article placeholders that must be replaced before publication.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
