## Description: <br>
Guides agents using the NorthData German commercial-register and financials API to look up companies, owners, representatives, financials, publications, person records, and credit usage through the NorthData CLI or MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p-meier](https://clawhub.ai/user/p-meier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to choose safe NorthData CLI or MCP workflows for company research, ownership and representative lookup, financial review, publications, person lookup, and paid power search while controlling credit spend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NorthData searches and lookups may consume paid API credits. <br>
Mitigation: Use free suggest, reference, and billing checks first; dry-run billed requests where parameters are uncertain; keep limits narrow; and only approve higher limits when credit spend is intentional. <br>
Risk: The skill requires a separate NorthData API key for CLI or MCP use. <br>
Mitigation: Configure the API key outside the skill and avoid exposing credentials in prompts, logs, or shared outputs. <br>


## Reference(s): <br>
- [NorthData API documentation](https://github.com/northdata/api) <br>
- [ClawHub NorthData skill page](https://clawhub.ai/p-meier/northdata) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline CLI commands and MCP tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include dry-run steps, cost-control checks, and API-key configuration reminders.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
