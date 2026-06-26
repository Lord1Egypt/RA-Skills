## Description: <br>
Agentic AI video editor: send a prompt, the autonomous editor plans, uses internal tools, exports, and returns the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brajendrak00068](https://clawhub.ai/user/brajendrak00068) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, editors, and developers use this skill to ask an agent for natural-language video edits, captioning, privacy redaction, brand/project/asset workflows, and MP4 or ZIP exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send API keys and user media or project data to Levea's cloud service. <br>
Mitigation: Install only when that cloud processing is acceptable, keep API keys secret, and avoid sending sensitive media without authorization. <br>
Risk: Mutating edits may automatically render outputs and create artifact URLs. <br>
Mitigation: Use requirePlanApproval for important, sensitive, or destructive workflows and review generated outputs before publishing or sharing. <br>
Risk: Beta editing outputs can be incorrect or incomplete. <br>
Mitigation: Preview final media, check captions and redactions, and rerun or repair edits before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/brajendrak00068/levea-ai-video-editor) <br>
- [Levea MCP server package](https://www.npmjs.com/package/levea-mcp-server) <br>
- [ClawHub plugin listing](https://clawhub.ai/plugins/openclaw-ai-video-editor) <br>
- [Levea Studio for API keys](https://studio.livecore.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return video URLs, ZIP URLs, job IDs, scene state, and status messages from the Levea cloud service.] <br>

## Skill Version(s): <br>
1.0.23 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
