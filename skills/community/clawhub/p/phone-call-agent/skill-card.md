## Description: <br>
AI voice call agent that can make outbound calls, generate browser call links, accept inbound calls, and retrieve transcripts and summaries when calls end. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Littlesheepxy](https://clawhub.ai/user/Littlesheepxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a self-hosted voice calling stack for outbound follow-up calls, browser-based call links, inbound call handling, and post-call transcript review. It supports English and Chinese call workflows that require explicit operator setup and approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real outbound calls and public browser call links. <br>
Mitigation: Require explicit approval before each real call or shared link, and keep public links private and short-lived. <br>
Risk: Calls may produce transcripts, summaries, and webhook deliveries that contain sensitive conversation data. <br>
Mitigation: Tell participants they are speaking with an AI system and may be transcribed, protect the .env file, and only enable WEBHOOK_URL for an HTTPS endpoint under the operator's control. <br>
Risk: Running the self-hosted stack requires external services, API keys, Docker, and a SIP trunk for phone dialing. <br>
Mitigation: Review the external repository before running Docker and use low-privilege API keys for configured providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Littlesheepxy/phone-call-agent) <br>
- [Publisher profile](https://clawhub.ai/user/Littlesheepxy) <br>
- [GitHub repository from skill metadata](https://github.com/Littlesheepxy/phone-call-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce call links, call summaries, transcript retrieval guidance, and setup instructions for Docker, MCP, SIP, webhook, and provider configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
