## Description:

Generates structured, source-traceable industry definition reports from an industry, product, or technology term.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youhaokun0514-sys](https://clawhub.ai/user/youhaokun0514-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use this skill to turn a seed industry, product, or technology term into a standardized Markdown definition report with classification, statistical scope, and cited sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present placeholder or weakly verified research as high-confidence sourced material.

Mitigation: Treat outputs as drafts and independently verify every cited source before using the report.

Risk: Seed terms may be sent through external search paths during research.

Mitigation: Avoid confidential seed terms unless the user has approved external searches.

Risk: The built-in quality score may be insufficient for regulated, medical, financial, or business-critical decisions.

Mitigation: Require domain expert review and do not rely on pass/fail scoring as the final acceptance criterion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youhaokun0514-sys/skills/industry-intro)
- [L1-L5层级分类规范](references/l1-l5-classification.md)
- [四维结构写作模板与示例](references/four-structure-template.md)
- [溯源标注规范与可信来源清单](references/source-tracing.md)
- [质量评估标准与评分细则](references/LLM-as-a-Judge.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance, Shell commands]

**Output Format:** [Markdown report with source references and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a standardized definition report, classification level, statistical scope, source list, and generation timestamp.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
