## Description: <br>
AI-powered video editing via the Mosaic API for creating agents, running video workflows, managing social accounts, publishing content, uploading assets, and handling credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyle1373](https://clawhub.ai/user/kyle1373) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketing teams, and developers use this skill to operate Mosaic video-editing workflows through an agent. It helps upload media, configure editing nodes, run and resume jobs, connect social accounts, publish edited videos, and manage credits or plan upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and use a Mosaic API key. <br>
Mitigation: Install only when the agent is trusted with the Mosaic API key and require explicit approval before storing or reusing the key. <br>
Risk: The skill can upload sensitive media and use callback URLs. <br>
Mitigation: Confirm media sensitivity and callback destinations before upload or run execution. <br>
Risk: The skill can connect, disconnect, publish, update, or delete social content. <br>
Mitigation: Require explicit user approval before changing social account connections or publishing, updating, or deleting posts. <br>
Risk: The skill can upgrade plans and configure auto top-ups. <br>
Mitigation: Require explicit approval before plan upgrades, checkout flows, billing changes, or enabling auto top-ups. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kyle1373/mosaic-video-editor) <br>
- [Publisher Profile](https://clawhub.ai/user/kyle1373) <br>
- [Mosaic Homepage](https://edit.mosaic.so) <br>
- [Mosaic API Key Setup](https://edit.mosaic.so/automations?tab=api) <br>
- [Mosaic API Reference](https://docs.mosaic.so/api/introduction) <br>
- [Mosaic API Endpoint Map](references/docs-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOSAIC_API_KEY for Mosaic API access.] <br>

## Skill Version(s): <br>
1.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
