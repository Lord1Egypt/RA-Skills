## Description: <br>
Dispatch coding tasks to Warp Oz cloud agents and chain them into multi-agent pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[in-liberty420](https://clawhub.ai/user/in-liberty420) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to start, monitor, schedule, and chain Warp Oz cloud coding agents from chat-driven workflows. It supports single-agent runs, multi-turn sessions, and staged pipelines such as architecture, implementation, testing, and security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Warp Oz cloud agents and schedules using the user's Warp account credentials. <br>
Mitigation: Install it only for intended Warp Oz automation, use a dedicated or least-privileged API key where possible, and review active schedules regularly. <br>
Risk: Prompts, generated artifacts, or remote agent output may include sensitive repository or account context. <br>
Mitigation: Avoid placing secrets in prompts and review generated PRs, artifacts, and session outputs before using or merging them. <br>
Risk: Incorrect environment IDs, cron schedules, or multi-agent retry loops can trigger unintended cloud work. <br>
Mitigation: Verify environment IDs, schedule definitions, and pipeline retry settings before running commands. <br>


## Reference(s): <br>
- [Warp Oz Skill Listing](https://clawhub.ai/in-liberty420/oz) <br>
- [Oz Agent REST API Reference](references/api.md) <br>
- [Agent Role Definitions](references/agent-roles.md) <br>
- [Warp Oz API Base URL](https://app.warp.dev/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, python3, and a Warp API key; can optionally read the API key from 1Password using OP_WARP_REFERENCE.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
