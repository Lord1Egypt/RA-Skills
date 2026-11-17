## Description:

Screens product images or Amazon ASINs for intellectual property risk across design patents, utility and invention patents, text trademarks, graphic trademarks, copyright, and policy compliance, then produces a structured HTML report with deeper patent details when relevant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, compliance reviewers, and agent workflows use this skill to screen Amazon listings or product images for patent, trademark, copyright, and product-policy risk before publishing or review. It can append legal status, claims, patent family, citation, bibliography, abstract, image, PDF, and specification details for patents that need deeper analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, ASINs, patent queries, generated prompts, and feedback text may be sent to LinkFox services.

Mitigation: Use the skill only when those inputs are approved for external service processing, and avoid uploading private files or images unless public accessibility is acceptable.

Risk: Credentials and account data can be used with configurable LinkFox network endpoints.

Mitigation: Treat LINKFOX_AGENT_API_KEY as a secret and run with only trusted LINKFOX_* gateway URLs that you control.

Risk: Full lookup results may be stored locally during report generation.

Mitigation: Run in a clean, non-shared workspace and remove local outputs when the review is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-ip-patent-copyright-search)
- [LinkFox Skills](https://skill.linkfox.com/)
- [Root Skill Definition](artifact/SKILL.md)
- [IP Full Detection Workflow](artifact/skills/ip-full-detection/references/workflow.md)
- [IP Full Detection Output Schema](artifact/skills/ip-full-detection/references/output-schema.md)
- [IP Full Detection Data Fields](artifact/skills/ip-full-detection/references/data-fields.md)
- [Report Layout Components](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [Ruiguan Design Patent API](artifact/skills/linkfox-ruiguan-detection-patent-design/references/api.md)
- [Ruiguan Copyright API](artifact/skills/linkfox-ruiguan-copyright-detection/references/api.md)
- [Ruiguan Text Trademark API](artifact/skills/linkfox-ruiguan-text-trademark-detection/references/api.md)
- [Ruiguan Graphic Trademark API](artifact/skills/linkfox-ruiguan-trademark-graphic-detection/references/api.md)
- [Zhihuiya Patent Image Search API](artifact/skills/linkfox-zhihuiya-patent-image-search/references/api.md)
- [Zhihuiya Legal Status API](artifact/skills/linkfox-zhihuiya-legal-status/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, structured summaries, JSON examples, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LinkFox API credentials for service-backed lookups and may store full lookup results locally.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
