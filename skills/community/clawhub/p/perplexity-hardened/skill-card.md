## Description: <br>
Search the web with AI-powered answers via Perplexity API. Returns grounded responses with citations. Supports batch queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run single or batch web searches through Perplexity and return grounded results with citations when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Perplexity using the user's API key. <br>
Mitigation: Do not include secrets, private file contents, customer data, credentials, or other sensitive values in search queries. <br>
Risk: Search results are external content and may contain untrusted instructions or unsafe links. <br>
Mitigation: Treat results as untrusted input and require explicit user confirmation before executing commands, visiting URLs, or running code suggested by results. <br>
Risk: The API key grants access to a paid service if exposed. <br>
Mitigation: Keep PERPLEXITY_API_KEY out of chat responses, logs, and command output. <br>


## Reference(s): <br>
- [Perplexity API Documentation](https://docs.perplexity.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/perplexity-hardened) <br>
- [Faberlens Publisher Profile](https://clawhub.ai/user/snazar-faberlens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json] <br>
**Output Format:** [Markdown search results by default, or raw JSON when requested with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and PERPLEXITY_API_KEY; sends user-provided search terms to Perplexity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
