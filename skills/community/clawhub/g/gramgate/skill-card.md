## Description: <br>
GramGate helps agents and automation access a real Telegram account over REST or MCP for reading history, searching chats, joining groups, clicking inline buttons, and sending messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zakirovdmr](https://clawhub.ai/user/zakirovdmr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support or CRM automation teams use GramGate to give agents structured Telegram user-account read/write access for channel monitoring, research collection, Telegram bot flow testing, and Telegram workflow operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can exercise broad read and write access through a real Telegram user account. <br>
Mitigation: Use a dedicated Telegram account, restrict which agents can connect, and require human approval for sending, deleting, joining, forwarding, reacting, voting, or clicking inline buttons. <br>
Risk: Exposing the gateway beyond localhost can allow remote access to Telegram account capabilities. <br>
Mitigation: Keep the service bound to localhost unless network exposure is required, and add bearer-token authentication before exposing it. <br>


## Reference(s): <br>
- [GramGate GitHub repository](https://github.com/zakirovdmr/gramgate) <br>
- [GramGate ClawHub listing](https://clawhub.ai/zakirovdmr/gramgate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a running GramGate service; REST and MCP endpoints are local by default.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
