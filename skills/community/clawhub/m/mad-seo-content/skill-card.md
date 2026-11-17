## Description:

M.A.D. SEO CONTENT helps agents plan, draft, audit, optimize, repurpose, analyze, and publish SEO content with omnichannel research, GEO targeting, schema generation, analytics integration, and WordPress draft creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mazgalesc](https://clawhub.ai/user/mazgalesc)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, SEO operators, and content teams use this skill to run WordPress-oriented SEO workflows, including research, content planning, drafting, quality audits, structured data generation, internal linking, analytics review, repurposing, and draft publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask users to store reusable WordPress publishing credentials in local shared project state.

Mitigation: Use a dedicated low-privilege WordPress account, prefer HTTPS-only sites, avoid administrator credentials, and rotate or revoke the application password after use.

Risk: The skill can create WordPress drafts and therefore has authority to stage content in a live publishing system.

Mitigation: Review generated content, SEO metadata, categories, media, and preview URLs before publication or promotion.

Risk: The workflow relies on network-capable dependencies for analytics, browsing, scraping, and plugin-mediated SEO metadata updates.

Mitigation: Install only trusted dependencies, review external dependency behavior before production use, and validate the Rank Math API Manager plugin before connecting production sites.

## Reference(s):

- [Skill overview](SKILL.md)
- [Engine strategy](references/engine_strategy.md)
- [Writer quality standards](references/writer_quality.md)
- [Content structure templates](references/content-structure-templates.md)
- [Title formulas](references/title-formulas.md)
- [Schema architect logic](references/schema-architect-logic.md)
- [Author EEAT benchmarks](references/author-eeat-benchmarks.md)
- [GEO sync logic](references/geo-sync-logic.md)
- [Roadmap strategy](references/roadmap-strategy.md)
- [Local compliance benchmarks](references/local-compliance-benchmarks.md)
- [Funnel strategy](references/funnel-strategy.md)
- [Database schema](references/db-schema.md)
- [Humanizer configuration](references/humanizer_config.json)
- [Rank Math API Manager](https://github.com/Devora-AS/rank-math-api-manager)
- [ClawHub skill page](https://clawhub.ai/mazgalesc/skills/mad-seo-content)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, HTML-ready content, JSON-LD snippets, configuration records, audit summaries, strategy plans, and publication instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare local shared-state files, SQLite content-calendar records, structured SEO payloads, and WordPress draft publication details for agent-mediated review and execution.]

## Skill Version(s):

1.2.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
