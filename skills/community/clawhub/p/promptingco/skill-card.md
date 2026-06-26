## Description: <br>
Interact with The Prompting Company platform to monitor brand visibility across AI engines, manage tracked prompts, review and publish content drafts, and retrieve SOV and AI traffic analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardtanoto](https://clawhub.ai/user/edwardtanoto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with The Prompting Company workspaces use this skill to monitor brand visibility across AI engines, manage tracked prompts, and review or publish content drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required TPC session token may let an agent act in the user's The Prompting Company workspace. <br>
Mitigation: Install only when the publisher is trusted, prefer a scoped API token if TPC offers one, and require explicit confirmation before approving, deleting, publishing, or batch-changing content. <br>
Risk: Multi-step workflows pass the live session token into general-purpose subagent prompts. <br>
Mitigation: Limit token exposure to the active session, avoid storing the token in durable notes or logs, and confirm the request is using the expected TPC domain before execution. <br>


## Reference(s): <br>
- [The Prompting Company API Quick Reference](artifact/references/api-guide.md) <br>
- [The Prompting Company Application](https://app.promptingco.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardtanoto/promptingco) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline curl examples and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TPC_SESSION_TOKEN for authenticated requests to the user's The Prompting Company workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
