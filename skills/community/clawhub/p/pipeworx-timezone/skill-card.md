## Description: <br>
Provides current time for IANA timezones or IP addresses, lists IANA timezone strings, and converts datetimes between timezones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer timezone questions, list valid IANA timezone identifiers, resolve current time from IP geolocation, and convert meeting times between timezones through the Pipeworx timezone MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timezone queries and optional IP-based lookup are sent to the disclosed Pipeworx MCP endpoint. <br>
Mitigation: Use the skill only where sending timezone queries to gateway.pipeworx.io is acceptable, and avoid IP-based lookup for sensitive users or environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-timezone) <br>
- [Pipeworx timezone MCP endpoint](https://gateway.pipeworx.io/timezone/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an external Pipeworx MCP endpoint; IP-based lookup can involve processing an IP address.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
