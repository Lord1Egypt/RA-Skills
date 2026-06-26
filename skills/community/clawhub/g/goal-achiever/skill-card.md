## Description: <br>
Guides an agent through a goal-driven content publishing workflow that reads task and prompt files, decomposes work, develops or reuses automation scripts, writes results, and scores progress toward a target platform goal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LDZ2010326](https://clawhub.ai/user/LDZ2010326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a repeatable agent workflow for planning, executing, logging, and reviewing platform-specific content publishing goals. It is intended for controlled workspaces where the user has permission to operate the target platform account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and run scripts, use logged-in browser sessions, and modify external-platform content. <br>
Mitigation: Use only in a controlled workspace after confirming the operator has permission for the target platform and account. <br>
Risk: The skill can post, edit, schedule jobs, and change prompt registries without enough user control. <br>
Mitigation: Require clear user approval before any post, edit, scheduled job, or prompt-registry change. <br>
Risk: Workflow logs or generated files could expose sensitive account or prompt data. <br>
Mitigation: Exclude secrets, cookies, tokens, private prompts, and account data from logs and generated artifacts. <br>


## Reference(s): <br>
- [Goal Achiever release page](https://clawhub.ai/LDZ2010326/goal-achiever) <br>
- [Core goal configuration](references/core_goal.json) <br>
- [Cron design reference](references/cron-design-reference.md) <br>
- [External publishing design reference](references/external-publishing-design-reference.md) <br>
- [Logging reference](references/logging.md) <br>
- [Technical decision reference](references/technical-decision-reference.md) <br>
- [Goal prompt](references/prompts/goal_prompt.md) <br>
- [Retrospective prompt](references/prompts/retro_prompt.md) <br>
- [Prompt registry](references/prompts/prompt_registry.md) <br>
- [Prompt authoring guide](references/prompts/prompt_authoring_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON task files, scripts, shell commands, and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create run logs, task records, retrospective records, prompt files, script registry entries, scheduled-job configuration, and platform publishing outputs when permitted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
