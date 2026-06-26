## Description: <br>
Nexus AI helps agents publish Nexus recruiting, business opportunity, funding, and event posts, retrieve Nexus usage reports, and answer Nexus-backed questions about people, resources, and opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songsh66](https://clawhub.ai/user/songsh66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub users and their agents use this skill to route Nexus recruiting and business-opportunity workflows to Nexus services, including posting resources, looking up account reports by phone number, and asking Nexus-backed RAG questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger language may route recruiting or business-opportunity requests to Nexus before the user explicitly asks for that service. <br>
Mitigation: Confirm the user's intent to use Nexus before invoking the skill, especially for posting resources or retrieving account reports. <br>
Risk: Phone numbers, post content, recruiting details, business opportunities, and report lookup requests may be sent to remote Nexus or RAG services. <br>
Mitigation: Collect and send only the minimum information needed for the requested action, and avoid sensitive business or personal details unless necessary. <br>
Risk: Posting actions can create Nexus resources from user-provided title and content. <br>
Mitigation: Review the phone number, title, content, and automatically selected label with the user before executing a posting command. <br>
Risk: Usage report lookup by phone number may expose account-related report content. <br>
Mitigation: Use report lookup only for the user's intended account and handle returned report text as potentially sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/songsh66/nexus-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, guidance] <br>
**Output Format:** [Plain text command output with occasional JSON response snippets, Nexus links, and local QR image path references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include remote service responses for posting, report lookup, or RAG search actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
