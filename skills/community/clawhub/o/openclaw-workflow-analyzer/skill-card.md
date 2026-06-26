## Description: <br>
Analyzes a user's workflow, breaks it into automatable subprocesses, rates OpenClaw implementation difficulty, confirms third-party data dependencies, and suggests a practical rollout path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and OpenClaw adopters use this skill to identify which parts of a workflow can be automated with OpenClaw, what dependencies must be confirmed, and which improvements to attempt first. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask about APIs, accounts, OAuth, or API keys while analyzing third-party data dependencies. <br>
Mitigation: Describe credential availability, access constraints, and approval status without sharing actual secrets during the analysis step. <br>
Risk: Workflow automation recommendations may be incomplete or incorrect if data access, network reachability, permissions, rate limits, or costs are unclear. <br>
Mitigation: Confirm each third-party dependency before treating an automation path or difficulty rating as actionable. <br>
Risk: The skill is advisory and does not implement or execute the proposed automation. <br>
Mitigation: Use its output as planning guidance, then perform implementation, credential handling, and execution in a separate trusted workflow. <br>


## Reference(s): <br>
- [OpenClaw capabilities matrix](references/openclaw-capabilities.md) <br>
- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/openclaw-workflow-analyzer) <br>
- [Project homepage](https://github.com/fangshan101-coder/openclaw-workflow-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown workflow analysis report with tables, difficulty ratings, dependency checks, rollout recommendations, and learning-path guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces advisory text only; it does not execute automation tasks or require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
