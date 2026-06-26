## Description: <br>
When a message uses the @deviceid-agentid-ip plus instruction format, this skill forwards the instruction to the specified IP gateway agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxx328](https://clawhub.ai/user/lxx328) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route an instruction from one gateway chat context to a named agent on another gateway. It is intended for controlled cross-gateway agent messaging where the destination gateway, agent ID, and instruction are supplied in the mention text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat text can trigger outbound requests to specified IP gateway agents without clear trust controls. <br>
Mitigation: Install only where gateway destinations are controlled, authenticated, and restricted by a trusted allowlist before forwarding instructions. <br>
Risk: Remote responses may appear indistinguishable from local gateway replies. <br>
Mitigation: Keep visible provenance or routing context for remote responses so users can tell which gateway and agent produced the content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxx328/mention-to-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Remote agent response text extracted from an OpenAI-compatible chat completion response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns only choices[0].message.content from the remote gateway response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
