## Description: <br>
Add phone calling to your agent through OpenCawl. Use this skill to place calls, check outcomes, end active calls, and review voicemails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ammbo](https://clawhub.ai/user/ammbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use OpenCawl to place authorized outbound phone calls, track call status, end active calls, and review recent calls or voicemails through the OpenCawl API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real phone calls and may contact people without proper authorization or consent. <br>
Mitigation: Use it only for authorized recipients and require explicit confirmation before each outbound call. <br>
Risk: Calls may collect personal data and return recordings, transcripts, summaries, or extracted contact details. <br>
Mitigation: Keep call goals minimal, avoid sensitive personal or confidential information, and follow applicable recording, consent, and privacy rules. <br>
Risk: The OpenCawl API key is a sensitive credential. <br>
Mitigation: Store OPENCAWL_API_KEY securely, restrict access to it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [OpenCawl Skill Page](https://clawhub.ai/ammbo/opencawl) <br>
- [OpenCawl Homepage](https://opencawl.com) <br>
- [API Reference](artifact/api.md) <br>
- [Inbound Automation Reference](artifact/inbound.md) <br>
- [Persona Reference](artifact/personas.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Guidance] <br>
**Output Format:** [JSON API requests and responses with text summaries, transcripts, call status, voicemail details, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCAWL_API_KEY and uses asynchronous call flows that return a call_id for later status checks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
