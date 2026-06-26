## Description: <br>
Novel Orchestrator routes and coordinates long-form web novel planning, drafting, review, revision, and agent setup across manager, planner, writer, and checker roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NaitOah](https://clawhub.ai/user/NaitOah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors and teams using OpenClaw use this skill to coordinate long-form web novel workflows, including chapter planning, drafting, review, revision loops, and multi-agent task routing. It also guides creation of writer, checker, planner, and manager agent workspaces when the user explicitly starts setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow makes persistent OpenClaw agent configuration changes, including agent directories, workspace files, openclaw.json updates, and agent-to-agent permissions. <br>
Mitigation: Review the workspace path, agent additions, openclaw.json changes, and agentToAgent allow list before confirming setup. <br>
Risk: Configured agents may use Moonshot or Xiaomi API keys from environment variables. <br>
Mitigation: Confirm which model provider is selected and which MOONSHOT_API_KEY or XIAOMI_API_KEY credentials are available before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NaitOah/novel-orchestrator) <br>
- [Agent setup workflow](references/agent-setup.md) <br>
- [Routing rules](references/routing.md) <br>
- [Workflow diagrams](references/workflow-diagrams.md) <br>
- [Chapter format](references/chapter-format.md) <br>
- [Quality standards](references/quality-standards.md) <br>
- [Review template](references/review-template.md) <br>
- [Moonshot API endpoint](https://api.moonshot.cn/v1) <br>
- [Xiaomi MiMo API endpoint](https://api.xiaomimimo.com/anthropic) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with configuration steps and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OpenClaw agent setup instructions, task routing decisions, review reports, revision guidance, and chapter workflow artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
