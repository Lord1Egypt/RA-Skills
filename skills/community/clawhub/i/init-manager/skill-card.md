## Description: <br>
Manage tasks in Init Manager -- pick up ready tasks, update status, comment, and close out. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomislavpet](https://clawhub.ai/user/tomislavpet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent coordinate assigned Init Manager tasks, read task context, update statuses, add comments, and hand off blocked work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote Init Manager AI Guide settings may give external project configuration too much influence over agent behavior. <br>
Mitigation: Install only for trusted Init Manager instances and trusted guide editors; treat fetched guides as project guidance subject to higher-priority system, developer, and workspace rules. <br>
Risk: The skill can write task status, assignment, and comment changes to an external Init Manager service. <br>
Mitigation: Use a least-privilege API token, pin the base URL to an approved Init Manager domain, and review or confirm write actions before posting them. <br>
Risk: Task comments or updates could accidentally disclose secrets or sensitive implementation details. <br>
Mitigation: Avoid sending secrets in task comments or updates and summarize work without exposing credentials or private data. <br>


## Reference(s): <br>
- [Init Manager](https://manager.init.hr) <br>
- [ClawHub Init Manager Skill Page](https://clawhub.ai/tomislavpet/init-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with endpoint tables, JSON payload examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Init Manager base URL, bearer API key, and user ID supplied by the operating environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact/version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
