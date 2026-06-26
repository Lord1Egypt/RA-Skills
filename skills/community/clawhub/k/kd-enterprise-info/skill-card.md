## Description: <br>
Researches a company from public web sources and optional Tavily search, then generates a structured responsive HTML business information report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kindeex](https://clawhub.ai/user/kindeex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, presales, partner review, and competitive research teams use this skill to gather public company facts, business context, financial signals, digital-system clues, and industry context into an HTML report. It is intended for public-information research and should be reviewed before business decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When Tavily is configured, company names and research queries may be sent to an external search provider. <br>
Mitigation: Use a dedicated limited Tavily key, configure it only where needed, and avoid placing credentials in broad home-directory .env files. <br>
Risk: Generated reports may include external content that has not been fully escaped. <br>
Mitigation: Treat generated HTML reports as unsafe for untrusted inputs until report fields and error messages are confirmed to be HTML-escaped. <br>
Risk: Company research based on public web results can be incomplete or misleading. <br>
Mitigation: Review key facts against authoritative sources before using the report for sales, partner review, or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kindeex/kd-enterprise-info) <br>
- [Tavily search provider](https://tavily.com/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, configuration, guidance] <br>
**Output Format:** [Responsive HTML report with structured company research sections and missing-data placeholders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a company name as input; Tavily API configuration is optional for enhanced search coverage.] <br>

## Skill Version(s): <br>
5.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
