## Description: <br>
Use the Imans CLI from OpenClaw agents to query Imans workspace, catalog, and sales order data as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imans-ai](https://clawhub.ai/user/imans-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to query Imans workspace, catalog, product variant, sales order, order item, and classification data through the Imans CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve business-sensitive product, order, and customer-related data from an Imans workspace. <br>
Mitigation: Confirm broad exports before running them, use the narrowest query or profile that answers the request, and summarize results instead of dumping raw JSON into chat. <br>
Risk: Raw API tokens or login secrets could be exposed through chat or shell history if handled directly. <br>
Mitigation: Avoid printing or requesting raw tokens; use token environment variables or standard input for automation. <br>


## Reference(s): <br>
- [Imans CLI GitHub repository](https://github.com/imans-ai/imans-cli) <br>
- [Imans CLI latest release](https://github.com/imans-ai/imans-cli/releases/latest) <br>
- [Imans install script](https://imans.ai/install) <br>
- [ClawHub skill page](https://clawhub.ai/imans-ai/imans-claw) <br>
- [Publisher profile](https://clawhub.ai/user/imans-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to request JSON output from the Imans CLI and summarize results instead of exposing raw business data unnecessarily.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
