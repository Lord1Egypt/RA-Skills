## Description: <br>
Comprehensive research grounded in web data with explicit citations for multi-source synthesis, comparisons, current events, market analysis, and detailed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthew77](https://clawhub.ai/user/matthew77) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run Tavily-backed web research, synthesize cited answers, compare topics, analyze markets, and optionally save research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to Tavily and may contain sensitive information. <br>
Mitigation: Do not include secrets, private customer data, or sensitive internal material unless Tavily's handling is acceptable for the use case. <br>
Risk: The skill requires a Tavily API key. <br>
Mitigation: Keep TAVILY_API_KEY protected and avoid exposing it in configuration, logs, reports, or shared files. <br>
Risk: Optional report output writes to a user-provided file path. <br>
Mitigation: Choose output filenames carefully and review generated reports before sharing or relying on them. <br>


## Reference(s): <br>
- [Tavily Research on ClawHub](https://clawhub.ai/matthew77/liang-tavily-research) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown research report by default, or raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an AI-generated answer, source titles and URLs, relevance scores when available, response time metadata, and optional file output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
