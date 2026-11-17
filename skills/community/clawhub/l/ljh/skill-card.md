## Description:

Routes content-commerce product-launch work across pre-task tool selection, post-task next-step navigation, and a guided walkthrough of the launch chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and product-launch teams use this skill to route product, content, creator, ad, and unit-economics questions to the appropriate LJH toolkit workflow. It also guides users through the full launch sequence when they want a step-by-step product-launch walkthrough.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The onboarding flow includes off-platform WeChat contact promotion.

Mitigation: Review the onboarding text before deployment and remove or disclose the off-platform contact prompt if it is not appropriate for the workspace.

Risk: The guided workflow may write local onboarding state and product-launch dossier files containing business notes.

Mitigation: Tell users about the archive behavior before guided walkthroughs, honor opt-outs, and inspect or delete local LJH dossier files when retention is not wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh)
- [ClawHub publisher profile](https://clawhub.ai/user/handsomeng)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance, with optional local Markdown dossier entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create onboarding state and product-launch dossier files when the user has not opted out.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
