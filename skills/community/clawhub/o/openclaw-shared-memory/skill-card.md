## Description: <br>
Searches, inspects, and updates shared OpenClaw memory on the current machine for local servers, services, paths, workflow notes, and preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kamiender](https://clawhub.ai/user/kamiender) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to check remembered local infrastructure details, runbook notes, workspace conventions, and user preferences before acting, and to persist approved durable or day-specific notes back into OpenClaw memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read shared local memory that may contain sensitive local servers, internal services, file paths, runbooks, or preferences. <br>
Mitigation: Install only when shared OpenClaw memory access is intended, avoid storing secrets, and ask the agent to show memory results before relying on them. <br>
Risk: The skill can append new information into long-term or daily memory, which can persist incorrect or sensitive facts. <br>
Mitigation: Require dry-run output and explicit approval before any append, and review the exact destination path and text before writing. <br>
Risk: Security evidence notes weak write containment for daily memory notes and recommends narrowing implicit invocation. <br>
Mitigation: Prefer a fixed version that validates daily note dates and configure agents to invoke the skill only for requests that intentionally need OpenClaw memory. <br>


## Reference(s): <br>
- [OpenClaw Memory on ClawHub](https://clawhub.ai/kamiender/openclaw-shared-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON from the bundled CLI, usually summarized by the agent as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search returns path, source, score, and snippet; append returns the destination path; doctor reports detected OpenClaw paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
