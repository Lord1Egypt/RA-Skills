## Description: <br>
Tool-agnostic project collaboration for AI assistants that lets agents create and manage shared project context, log activity, check peer agents before project work, and summarize cross-peer contributions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dp-pcs](https://clawhub.ai/user/dp-pcs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project collaborators use this skill to keep project context, activity, decisions, blockers, and peer-agent knowledge available across their own tools and workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project context can persist sensitive project details in local OGP state. <br>
Mitigation: Avoid logging secrets, credentials, or exact private paths, and periodically review stored project context. <br>
Risk: Approved peer agents may receive project context more broadly than a user expects. <br>
Mitigation: Review approved peers and projects before enabling proactive sharing, and prefer summary or escalate response policies for sensitive work. <br>


## Reference(s): <br>
- [OGP documentation](https://github.com/dp-pcs/ogp) <br>
- [ClawHub listing](https://clawhub.ai/dp-pcs/ogp-project) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and response templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ogp CLI and configured local OGP state before the workflow can operate.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
