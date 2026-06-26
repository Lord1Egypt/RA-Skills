## Description: <br>
Search, compare, and analyze 330K+ open-source GitHub repos by growth rate, acceleration, and originality. Discover trending projects, find alternatives, check licenses, and get AI-powered analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alessandroflati](https://clawhub.ai/user/alessandroflati) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to research open-source repository momentum, compare technology choices, find alternatives, check dependency licenses, and request AI-assisted repository analysis through the Oosmetrics MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs the third-party @oosmetrics/mcp npm package. <br>
Mitigation: Install only when the publisher and package are trusted, and review the package source or lock the reviewed version before deployment. <br>
Risk: OOSMETRICS_API_KEY is a sensitive credential used to query the hosted Oosmetrics service. <br>
Mitigation: Store the key in a secret manager or scoped environment, avoid logging it, and rotate or delete it from the Oosmetrics profile if exposed. <br>
Risk: Repository metrics, license checks, and AI analysis may be incomplete or become outdated. <br>
Mitigation: Use the results as decision support and verify critical project, security, and licensing decisions against authoritative sources. <br>


## Reference(s): <br>
- [Oosmetrics Skill Page](https://clawhub.ai/alessandroflati/oosmetrics) <br>
- [Oosmetrics Publisher Profile](https://clawhub.ai/user/alessandroflati) <br>
- [Oosmetrics API Key Profile](https://oosmetrics.com/profile) <br>
- [Oosmetrics MCP Package Source](https://github.com/AlessandroFlati/GitHubMetrics/tree/main/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API Calls] <br>
**Output Format:** [Markdown or plain text responses with repository metrics, comparisons, recommendations, and analysis returned through MCP tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool availability depends on the user's Oosmetrics subscription tier; the skill requires npx and OOSMETRICS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
