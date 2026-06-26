## Description: <br>
Business Writing helps agents draft business research reports, business insights, consulting analyses, company research reports, competitive analyses, user research, and market analyses with cited supporting evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, consultants, researchers, and other external users use this skill to produce Markdown business writing with sourced claims, tables, and Mermaid diagrams when the underlying data supports them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requires sensitive credentials and can invoke authenticated service behavior when used. <br>
Mitigation: Install only where the SkillBoss API workflow is intended, keep SKILLBOSS_API_KEY scoped and rotated, and review requested actions before use. <br>
Risk: Business reports can become misleading if citations, table data, or diagrams are unsupported. <br>
Mitigation: Require citations for factual claims and verify source relevance and data accuracy before relying on generated analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-business-writing) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with clickable numbered citations, optional tables, and optional Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's question language by default and requires real sources for citations, tables, and graphs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
