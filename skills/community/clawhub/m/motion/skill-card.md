## Description: <br>
Motion API integration with managed OAuth for managing tasks, projects, workspaces, comments, recurring tasks, schedules, and related Motion data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and manage connected Motion workspaces through Maton-managed OAuth, including tasks, projects, comments, custom fields, schedules, and recurring tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive MATON_API_KEY and delegates Motion OAuth access through Maton. <br>
Mitigation: Install only if Maton is trusted, keep MATON_API_KEY private, and use the intended Motion connection when multiple accounts are linked. <br>
Risk: Create, update, and delete calls can change Motion tasks, projects, comments, custom fields, connections, and recurring tasks. <br>
Mitigation: Approve write or delete actions only after checking the exact target resource and intended effect. <br>


## Reference(s): <br>
- [Motion on ClawHub](https://clawhub.ai/byungkyu/motion) <br>
- [Maton](https://maton.ai) <br>
- [Motion API Documentation](https://docs.usemotion.com/) <br>
- [Motion API Reference](https://docs.usemotion.com/api-reference) <br>
- [Motion Cookbooks](https://docs.usemotion.com/cookbooks/getting-started) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoints and Python or JavaScript examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Motion OAuth connection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
