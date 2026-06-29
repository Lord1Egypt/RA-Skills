## Description: <br>
Openclaw helps an agent discover, compare, and contact services or agents through the MeshKore mesh, including travel, events, shopping, local services, and professional agentic work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capitaharlock](https://clawhub.ai/user/capitaharlock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route service-discovery requests to MeshKore, then present ranked providers with pricing, availability, and contact or booking endpoints. It is intended for discovery and handoff rather than processing payments directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad service-discovery prompts may send user query text to an external routing service. <br>
Mitigation: Avoid including private, account, financial, or confidential details unless the user intends to share them with the selected provider. <br>
Risk: Returned booking or payment links are completed with third-party providers outside MeshKore. <br>
Mitigation: Present links as provider handoffs and ask for confirmation before any paid agent contact or payment challenge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/capitaharlock/meshkore) <br>
- [MeshKore homepage](https://meshkore.com) <br>
- [MeshKore agent oracle documentation](https://hub.meshkore.com/platform/docs/agent/oracle) <br>
- [MeshKore public Oracle API](https://meshkore-oracle.rjj.workers.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional JSON-backed CLI results and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results usually include ranked providers, pricing, availability, reputation signals, and contact or booking endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
