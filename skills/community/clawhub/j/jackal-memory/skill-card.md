## Description: <br>
Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Regan-Milne](https://clawhub.ai/user/Regan-Milne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Jackal Memory to persist, restore, and provision agent memory across sessions and machines through a Python client or HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memory is sent to the Jackal Memory service and may contain sensitive content. <br>
Mitigation: Only store content appropriate for that service, and avoid saving passwords, private keys, credentials, or sensitive personal data. <br>
Risk: The skill requires a JACKAL_MEMORY_API_KEY for authenticated save, load, and provision requests. <br>
Mitigation: Keep JACKAL_MEMORY_API_KEY out of chats, logs, and shared artifacts. <br>
Risk: The security guidance notes a load-key URL encoding issue. <br>
Mitigation: Prefer simple key names until the load-key URL encoding issue is fixed. <br>


## Reference(s): <br>
- [Jackal Memory service](https://web-production-5cce7.up.railway.app) <br>
- [ClawHub skill page](https://clawhub.ai/Regan-Milne/jackal-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JACKAL_MEMORY_API_KEY; save and provision commands send user-provided content to the Jackal Memory service.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
