## Description: <br>
AI Agent定时任务管理工具，通过自然语言创建、查询、完成、删除定时任务，查看执行日志，并使用预设模板创建常用任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebang-tools](https://clawhub.ai/user/jiebang-tools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to manage scheduled reminders and cron-like task workflows through the Jiebang external task service. It supports creating, listing, completing, deleting, and reviewing scheduled tasks and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task names, schedules, tags, execution status, and log messages are sent to the external jiebang.site task service. <br>
Mitigation: Do not include sensitive task content unless sharing it with the service is acceptable. <br>
Risk: Create, completion, failure, and delete commands can change remote task state. <br>
Mitigation: Confirm the intended task and action before allowing the agent to run state-changing commands. <br>
Risk: The API key is stored in a local .jiebang_api_key file after registration. <br>
Mitigation: Remove or rotate the key when the skill is no longer used, and avoid exposing the file in shared workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiebang-tools/jiebang-cron-task) <br>
- [Jiebang task service](https://www.jiebang.site) <br>
- [Jiebang cron task API](https://www.jiebang.site/api/cron-task) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the skill's commands return JSON objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command results include status and data/result fields, or an error field on failure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
