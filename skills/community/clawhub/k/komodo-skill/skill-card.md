## Description: <br>
Interact with Komodo Core API using this project. Use when the user wants to list, manage, deploy, or execute operations against Komodo resources (servers, stacks, deployments, builds, repos, procedures, variables, alerts, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onekill0503](https://clawhub.ai/user/onekill0503) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect and manage Komodo resources through the Komodo Core API. It supports listing resources, creating and updating configurations, deploying stacks, controlling stacks and deployments, running builds, procedures, and actions, and fetching logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or destroy Komodo infrastructure using the configured API credentials. <br>
Mitigation: Use least-privilege Komodo credentials scoped to the intended resources and require explicit human confirmation before stop, restart, deploy, run, update, or destroy operations. <br>
Risk: Production API keys could expose high-impact infrastructure controls to agent-driven commands. <br>
Mitigation: Avoid production credentials unless necessary, rotate keys regularly, and prefer a dedicated key for this skill. <br>
Risk: The artifact does not include built-in confirmation safeguards for destructive or state-changing operations. <br>
Mitigation: Review generated commands and requested JSON configuration before execution, especially for deploy, destroy, update, and control scripts. <br>


## Reference(s): <br>
- [Komodo](https://komo.do) <br>
- [ClawHub skill page](https://clawhub.ai/onekill0503/komodo-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Komodo update IDs, status, success flags, durations, operators, and logs for execution workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
