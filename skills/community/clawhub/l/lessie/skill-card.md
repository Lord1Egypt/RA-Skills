## Description: <br>
Search, qualify, and enrich people and companies by title, company, location, seniority, audience, contact details, company attributes, hiring activity, news, and background web research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkgeekjack](https://clawhub.ai/user/jkgeekjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, recruiters, sales teams, and business researchers use this skill to source people, enrich known contacts, qualify candidates, research companies, and collect web-backed business intelligence through Lessie CLI or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a remote people-search service that may return personal contact details. <br>
Mitigation: Use only for lawful, consent-appropriate recruiting, sales, or research workflows and verify compliance obligations before enriching or contacting people. <br>
Risk: The setup flow can install external npm tooling, open a browser login flow, and cache an OAuth token locally. <br>
Mitigation: Require explicit user approval before package installation, browser authorization, or changes to local MCP or skill configuration. <br>
Risk: Search queries may be logged by the remote service for service improvement and abuse prevention. <br>
Mitigation: Avoid submitting sensitive, confidential, or unnecessary personal data in search prompts or enrichment requests. <br>
Risk: Remote web search and fetch tools can retrieve arbitrary URLs and summarize web content that may be stale or misleading. <br>
Mitigation: Cross-check important claims against reliable sources and disclose uncertainty when enrichment or web results conflict. <br>


## Reference(s): <br>
- [CLI Tool Calling Reference](references/cli-reference.md) <br>
- [Workflow Patterns](references/workflow-patterns.md) <br>
- [Domain Resolution](references/domain-resolution.md) <br>
- [Lessie Website](https://lessie.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/jkgeekjack/lessie) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and JSON tool output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lessie CLI output is JSON on stdout with status messages on stderr; people and organization enrichment calls are capped at 10 records per call.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
