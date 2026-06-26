## Description: <br>
Manage the phpMyAdmin Docker container for local dev environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to start, stop, inspect, and access a local phpMyAdmin web UI for managing a development MySQL container. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The phpMyAdmin UI provides database administrator access to the configured MySQL container. <br>
Mitigation: Install only for local development use, confirm the target MySQL container, and avoid relying on the default root password. <br>
Risk: Broad trigger phrases may cause the agent to start or inspect the container when the user intended a different MySQL task. <br>
Mitigation: Review the planned command before execution and ask for confirmation when the requested action is ambiguous. <br>
Risk: The container is configured to restart unless stopped, so it may continue running after reboot. <br>
Mitigation: Use the skill's stop command when the phpMyAdmin interface is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pereirajair/phpmyadmin-manager) <br>
- [Publisher profile](https://clawhub.ai/user/pereirajair) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain text status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Docker lifecycle commands and a localhost phpMyAdmin access URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
