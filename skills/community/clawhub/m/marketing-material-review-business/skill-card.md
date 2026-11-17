## Description:

Reviews marketing layouts and images for advertising compliance, highlights risk locations, and provides suggested revisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mabihuan](https://clawhub.ai/user/mabihuan)

### License/Terms of Use:

MIT-0

## Use Case:

External business, brand, and legal reviewers use this skill to assess Chinese marketing materials for advertising, food-labeling, promotion, livestreaming, and related compliance risks. It returns risk findings, annotated image outputs, and concrete revision guidance for review workflows.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Reviewed images and OCR credentials may be sent to Baidu OCR through broad environment configuration.

Mitigation: Use a clean, explicit OCR configuration, avoid relying on CWD or global OpenClaw dotenv files, and install only when this data flow is acceptable.

Risk: The launcher can automatically create a virtual environment and install dependencies.

Mitigation: Preinstall pinned dependencies from a trusted package source and run the skill in a constrained environment.

Risk: A custom OCR endpoint could redirect OCR traffic if BAIDU_OCR_ENDPOINT is set unexpectedly.

Mitigation: Do not set BAIDU_OCR_ENDPOINT unless the endpoint is allowlisted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mabihuan/skills/marketing-material-review-business)
- [Baidu AI OCR](https://ai.baidu.com)
- [advertising-law.md](references/advertising-law.md)
- [barcode-compliance-rules.md](references/barcode-compliance-rules.md)
- [common-cases.md](references/common-cases.md)
- [compliance-rules.md](references/compliance-rules.md)
- [consumer-protection-law.md](references/consumer-protection-law.md)
- [food-category-standards.md](references/food-category-standards.md)
- [forbidden-words.md](references/forbidden-words.md)
- [gb-19301-2010-raw-milk.md](references/gb-19301-2010-raw-milk.md)
- [gb-19645-pasteurized-milk.md](references/gb-19645-pasteurized-milk.md)
- [gb-24154-2015-sports-nutrition.md](references/gb-24154-2015-sports-nutrition.md)
- [gb-25190-2010-sterilized-milk.md](references/gb-25190-2010-sterilized-milk.md)
- [gb-28050-2025-nutrition-labeling.md](references/gb-28050-2025-nutrition-labeling.md)
- [gb-7718-2025-food-labeling.md](references/gb-7718-2025-food-labeling.md)
- [gbt-32950-2016-fresh-agricultural-labels.md](references/gbt-32950-2016-fresh-agricultural-labels.md)
- [live-streaming-regulations.md](references/live-streaming-regulations.md)
- [map-usage-rules.md](references/map-usage-rules.md)
- [national-language-law.md](references/national-language-law.md)
- [promotion-regulations.md](references/promotion-regulations.md)
- [risk-rules.json](references/risk-rules.json)
- [sc-food-production-license.md](references/sc-food-production-license.md)
- [zhejiang-language-implementation.md](references/zhejiang-language-implementation.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, image files, shell commands, configuration, guidance]

**Output Format:** [Markdown review reports, JSON risk payloads, annotated PNG images, and shell/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use Baidu OCR when configured, reuse cached OCR JSON, or render externally supplied risks with bounding boxes.]

## Skill Version(s):

1.1.10 (source: server release evidence and SKILL.md version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
