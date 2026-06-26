## Description: <br>
Connect ElevenLabs Agents to your OpenClaw via phone with Twilio. Includes caller ID auth, voice PIN security, call screening, memory injection, and cost tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cortexuvula](https://clawhub.ai/user/cortexuvula) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure a phone-accessible OpenClaw assistant through Twilio, ElevenLabs, and Anthropic Claude. It helps set up call routing, authentication, memory injection, transcript logging, and cost controls for voice interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A public phone bridge can expose call content, transcripts, local memory, and profile data to external services. <br>
Mitigation: Limit the contents of MEMORY.md and USER.md, use strong unique bridge tokens, restrict callers, and define retention and deletion rules for logs and transcripts. <br>
Risk: Outbound calling and public tunnel exposure can increase abuse and cost risk. <br>
Mitigation: Disable outbound calling unless required, keep caller whitelists and voice PIN checks enabled, and use rate limiting and cost tracking. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cortexuvula/phone-voice) <br>
- [Publisher Profile](https://clawhub.ai/user/cortexuvula) <br>
- [ElevenLabs Conversational AI](https://elevenlabs.io/conversational-ai) <br>
- [Twilio](https://www.twilio.com/) <br>
- [Cloudflare Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance for external voice, telephony, tunnel, and LLM services.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
