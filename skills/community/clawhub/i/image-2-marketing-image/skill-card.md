## Description:

Helps brand and ecommerce teams use AI Hive GPT Image 2 to create traceable campaign image masters, channel derivatives, and localized assets while preserving approved product and brand facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, retail, event, and CRM teams use this skill to plan and generate campaign image assets with explicit parent-child lineage, channel recomposition, and market localization boundaries. It is intended for workflows where approved product, brand, legal, and copy facts must remain separate from model-generated imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-selected campaign or product images to AI Hive and downloads generated results from returned HTTPS URLs.

Mitigation: Use --preview before live runs, upload only approved non-confidential assets, and run live generation only when AI Hive and returned storage domains are trusted.

Risk: The workflow requires an AI Hive API key, and the security evidence says credential-handling boundaries are under-specified.

Mitigation: Prefer a restricted key, avoid entering real keys directly in shell commands, and review the local credential file before installing or running the skill.

Risk: Generated imagery can contain unapproved text, legal claims, prices, dates, or product facts if reviewers treat model output as final copy.

Mitigation: Keep copy, pricing, legal, QR, and claim areas blank for approved post-production layout, and require human review of product and campaign facts before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/image-2-marketing-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands; CLI preview emits text prompts and live runs download PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live generation uses one image per task item, supports optional routing and image parameters, and can write downloaded results to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
