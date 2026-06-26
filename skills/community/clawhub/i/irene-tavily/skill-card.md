## Description: <br>
Uses the Tavily API to run AI-enhanced web searches with configurable result limits, search depth, time filtering, optional images, and Chinese or English language hints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chyher](https://clawhub.ai/user/chyher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve web search results, summaries, URLs, and optional images from Tavily for current information gathering, research, and technical troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily and may include sensitive user-provided terms. <br>
Mitigation: Avoid confidential or regulated queries unless Tavily handling is acceptable for the deployment environment. <br>
Risk: The skill requires a Tavily API key that could be exposed if stored carelessly. <br>
Mitigation: Use a dedicated key, keep .env files private, and monitor quota usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chyher/irene-tavily) <br>
- [Publisher profile](https://clawhub.ai/user/chyher) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, shell commands, configuration guidance] <br>
**Output Format:** [Plain text search summaries or JSON search responses printed to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, and a TAVILY_API_KEY configured in the environment or a supported .env file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
