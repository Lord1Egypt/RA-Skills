## Description: <br>
Analyzes competitor SEO and GEO strategies, including ranking keywords, content approaches, backlink profiles, and AI citation patterns, to identify opportunities to outperform competitors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, SEO, and growth teams use this skill to compare competitors' search visibility, content, backlinks, technical SEO, and AI citation patterns, then turn gaps into prioritized actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive credentials can be exposed if SKILLBOSS_API_KEY is pasted into prompts or stored in plain text. <br>
Mitigation: Keep the API key in the agent environment or a secret manager, and avoid including it in chat transcripts, reports, or generated files. <br>
Risk: Competitor domains, owned-site URLs, and research queries may be sent to connected SEO providers. <br>
Mitigation: Confirm that the requested analysis can be shared with the configured provider, and label whether metrics are provider-collected, user-provided, or estimated. <br>
Risk: Broad trigger phrases could activate the skill when the user did not intend a competitor-analysis workflow. <br>
Mitigation: Use the skill only for explicit SEO or competitor-analysis requests, and confirm scope before collecting or sending data. <br>
Risk: Recommendations can be misleading if they are based on assumptions rather than observed competitor data. <br>
Mitigation: Require each recommendation to cite specific rankings, content examples, backlink evidence, technical findings, or clearly marked estimates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-competitor-analysis) <br>
- [Analysis Templates](references/analysis-templates.md) <br>
- [Battlecard Template](references/battlecard-template.md) <br>
- [Positioning Frameworks](references/positioning-frameworks.md) <br>
- [Example Report](references/example-report.md) <br>
- [SEO and GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, comparison tables, battlecards, and prioritized action plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require competitor URLs, site metrics, industry context, and SKILLBOSS_API_KEY for connected SEO data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
