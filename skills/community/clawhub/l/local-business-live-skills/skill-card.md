## Description:

AI operations assistant for local-life business owners that diagnoses storefront readiness, drafts short-video scripts, prepares livestream selling flows, writes preshow talking points, reviews performance data, and answers tactical livestream questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1027399464-tech](https://clawhub.ai/user/1027399464-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External local-life merchants and solo operators use this skill to collect store information, generate a diagnostic report, plan short-video and livestream acquisition work, and turn livestream or video data into next actions. It is aimed at small restaurants, beauty, hospitality, parent-child, and retail storefronts rather than large chains or pure delivery-only businesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic flows may prompt users to share screenshots or business details through WeChat or Notion feedback paths.

Mitigation: Share only information intended for the publisher, remove sensitive customer or business data, and review contact prompts before using the skill with real merchants.

Risk: Hosted and CDN diagnostic pages are mutable unless the exact deployed content is pinned and audited.

Mitigation: Prefer the packaged artifact or a pinned, reviewed deployment before sending diagnostic links to merchants.

Risk: Marketing scripts and examples may conflict with platform, privacy, advertising, or consumer-protection rules.

Mitigation: Review generated scripts and offers against current platform policies and applicable laws before publication.

Risk: Generated diagnosis and livestream recommendations may be incomplete or misleading if merchant inputs are vague or inaccurate.

Mitigation: Validate recommendations against actual store data, keep assumptions visible in the report, and treat outputs as advisory rather than guaranteed results.

## Reference(s):

- [Skill Source](artifact/SKILL.md)
- [Standard Store Diagnosis Questions](artifact/references/diagnosis-questions.md)
- [Deep Diagnosis Follow-Up Questions](artifact/references/deep-diagnosis-questions.md)
- [Standalone HTML Diagnosis Tool](artifact/references/standalone-html-tool.md)
- [HTML Diagnosis Tool Workflow](artifact/references/html-diagnosis-tool-workflow.md)
- [Entity Copywriter Compliance Audit](artifact/references/entity-copywriter-compliance-audit.md)
- [Tongcheng Livestream Pattern](artifact/references/tongcheng-live-pattern.md)
- [Live Script Template](artifact/templates/live-script-template.md)
- [Hosted Diagnostic Page](https://1027399464-tech.github.io/local-business-live-skills/)
- [CDN Diagnostic Page](https://cdn.jsdelivr.net/gh/1027399464-tech/local-business-live-skills@main/diagnosis-tool.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, structured diagnostic reports, short-video scripts, livestream talk tracks, review templates, and standalone HTML templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Chinese-language business advice, checklists, scoring summaries, platform compliance self-checks, and user-facing contact or feedback prompts.]

## Skill Version(s):

2.4.3 (source: server release evidence and target metadata; artifact frontmatter reports 2.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
