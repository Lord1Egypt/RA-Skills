## Description: <br>
Manage projects, tasks, schedules, custom fields, and team collaboration in Motion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, teams, and developers use this skill to manage Motion workspaces, projects, tasks, comments, custom fields, statuses, schedules, and users through ClawLink-backed Motion API tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review verdict is suspicious because related ClawHub and Convex maintenance workflows can run nested review processes with broad local authority. <br>
Mitigation: Install only if the publisher is trusted; when using autoreview-style workflows, prefer --no-yolo or AUTOREVIEW_YOLO=0 unless unrestricted local authority is intentional. <br>
Risk: The skill can guide write and destructive Motion actions such as deleting tasks, deleting custom fields, or unassigning tasks. <br>
Mitigation: Preview write operations, confirm the target resource and intended effect with the user, and require explicit confirmation before high-impact actions. <br>
Risk: Motion access depends on a connected ClawLink account and the permissions of the authenticated Motion workspace. <br>
Mitigation: Verify the Motion connection and live tool catalog before use, and report permission or missing-connection errors directly instead of assuming capability availability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/motion-planning) <br>
- [Motion API Documentation](https://motion.app/developers) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs agents to verify the live Motion tool catalog, preview write actions, and require user confirmation for destructive operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
