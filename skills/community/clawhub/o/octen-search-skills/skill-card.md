## Description: <br>
Real-time web search for AI agents powered by Octen, with date filtering and structured results for current research, news monitoring, and other up-to-date information tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jac9935](https://clawhub.ai/user/Jac9935) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add live Octen web search to OpenClaw agents, including result-count controls and optional publish-date filtering. It is suited for research, news monitoring, and workflows that need current web results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries to Octen, which may disclose sensitive user-provided terms. <br>
Mitigation: Do not search for secrets, private customer data, or confidential internal material unless sharing that content with Octen is acceptable. <br>
Risk: The skill requires an OCTEN_API_KEY for API access. <br>
Mitigation: Use a scoped or revocable API key where possible and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Octen Homepage](https://octen.ai) <br>
- [Octen Search API Endpoint](https://api.octen.ai/search) <br>
- [ClawHub Skill Page](https://clawhub.ai/Jac9935/octen-search-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted search results printed to standard output, with setup guidance and shell command examples in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an OCTEN_API_KEY environment variable; search result count is bounded from 1 to 20.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
