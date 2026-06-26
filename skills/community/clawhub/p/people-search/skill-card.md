## Description: <br>
Search, qualify, and enrich people and companies for recruiting, business development, contact lookup, company research, and web research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lessieai](https://clawhub.ai/user/lessieai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, sales teams, founders, and researchers use this skill to find and qualify people or companies, enrich known contacts, source candidates or leads, and gather business intelligence using Lessie CLI or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Lessie tooling with npm or npx and may run code from an external package source. <br>
Mitigation: Review or install the Lessie packages yourself, pin trusted versions where possible, and run the tooling only in an environment where npm-installed code is acceptable. <br>
Risk: Lessie authorization stores a persistent OAuth token locally at ~/.lessie/oauth.json. <br>
Mitigation: Authorize only accounts you trust for this workflow, protect the local token file, and remove ~/.lessie/oauth.json when you no longer want agent access. <br>
Risk: Most Lessie actions consume credits and some workflows can spend credits repeatedly. <br>
Mitigation: Keep confirmation prompts enabled for paid actions, require an estimated credit cost before each call, and review credit usage after tool calls. <br>
Risk: People enrichment may return personal contact details such as email, phone, and social profile information. <br>
Mitigation: Use enrichment only for lawful and appropriate purposes, minimize personal-email and phone lookups, and follow applicable privacy and outreach rules. <br>
Risk: Search queries are sent to Lessie and logged for service improvement and abuse prevention. <br>
Mitigation: Avoid submitting confidential or unnecessary personal data in queries, and review Lessie's privacy policy and terms before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lessieai/people-search) <br>
- [Lessie pricing](https://lessie.ai/pricing) <br>
- [Lessie privacy policy](https://lessie.ai/privacy) <br>
- [Lessie terms of service](https://lessie.ai/terms-of-service) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Workflow patterns](references/workflow-patterns.md) <br>
- [Domain resolution](references/domain-resolution.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and summarized JSON results from Lessie tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Lessie search IDs, company or person records, contact details, credit-cost summaries, and setup or MCP configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release; artifact metadata version: 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
