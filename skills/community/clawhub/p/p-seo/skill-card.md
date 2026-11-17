## Description:

Builds programmatic SEO systems at scale by guiding agents to generate schema-valid JSON content, niche taxonomies, and React renderer plans for resource, comparison, tool, checklist, guide, and template pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichoss](https://clawhub.ai/user/chichoss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and SEO operators use this skill to design scalable programmatic SEO systems that separate generated JSON content from React presentation components. It is most useful when planning niche taxonomies, strict content schemas, page generation workflows, and renderer patterns for large content sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes brand-specific instructions to load Tolstoy workspace files, which could expose private business context if used in the wrong workspace.

Mitigation: Confirm the target workspace and user authorization before loading local Tolstoy context files, and avoid copying sensitive source material into generated public content.

Risk: The skill includes live Webflow CMS publishing steps that could create or publish items if credentials are available.

Mitigation: Require explicit user approval before any CMS API action, prefer draft or preview creation first, and verify collection fields before publishing.

Risk: Large-scale programmatic SEO generation can produce inaccurate, duplicative, or low-value pages if niche context and schema validation are weak.

Mitigation: Validate generated JSON against strict schemas, review sample pages for niche specificity and factual accuracy, and scale only after quality checks pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichoss/skills/p-seo)
- [Publisher profile](https://clawhub.ai/user/chichoss)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with JSON schema examples, TypeScript interfaces, React renderer patterns, checklists, and CMS publishing steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include brand-specific context loading and Webflow publishing guidance; use explicit approval and draft or preview workflows before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
