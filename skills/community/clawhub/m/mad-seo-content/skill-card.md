## Description: <br>
Autonomously plans, drafts, audits, and optimizes SEO content with omnichannel research, GEO targeting, internal linking, schema, analytics integration, and WordPress publishing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mazgalesc](https://clawhub.ai/user/mazgalesc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, SEO, and growth teams use this skill to build SEO strategy, draft and audit articles, generate schema, plan editorial calendars, repurpose content, analyze visibility, and create WordPress drafts. It is intended for workflows where the user can review generated content, credentials, dependencies, and publishing actions before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores WordPress application credentials in a local shared M.A.D. SEO folder. <br>
Mitigation: Use a dedicated low-privilege WordPress account, restrict access to the shared workspace, and revoke or rotate the application password after use. <br>
Risk: Broad triggers could activate the skill outside a clearly SEO-specific request. <br>
Mitigation: Invoke it only for intended SEO and WordPress workflows, and review the planned action before allowing credential use, file writes, or publishing steps. <br>
Risk: Network operations and WordPress integrations depend on external skills or plugins. <br>
Mitigation: Review the dependent skills and any recommended WordPress plugin before connecting a production site. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mazgalesc/mad-seo-content) <br>
- [Engine Strategy](artifact/references/engine_strategy.md) <br>
- [Writer Quality](artifact/references/writer_quality.md) <br>
- [Content Structure Templates](artifact/references/content-structure-templates.md) <br>
- [Title Formulas](artifact/references/title-formulas.md) <br>
- [Schema Architect Logic](artifact/references/schema-architect-logic.md) <br>
- [Author EEAT Benchmarks](artifact/references/author-eeat-benchmarks.md) <br>
- [GEO Sync Logic](artifact/references/geo-sync-logic.md) <br>
- [Roadmap Strategy](artifact/references/roadmap-strategy.md) <br>
- [Local Compliance Benchmarks](artifact/references/local-compliance-benchmarks.md) <br>
- [Funnel Strategy](artifact/references/funnel-strategy.md) <br>
- [Database Schema](artifact/references/db-schema.md) <br>
- [Humanizer Configuration](artifact/references/humanizer_config.json) <br>
- [Rank Math API Manager](https://github.com/Devora-AS/rank-math-api-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text guidance with optional HTML, JSON-LD, SQL, API payloads, and local file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WordPress draft instructions, editorial plans, audit reports, schema snippets, and local workspace artifacts under the configured M.A.D. SEO folder.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
