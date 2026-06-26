## Description: <br>
Create, update, and manage Glance dashboard widgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acfranzen](https://clawhub.ai/user/acfranzen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Glance to create, arrange, refresh, and query local dashboard widgets for API data, metrics, schedules, and other tracked information. The skill helps agents generate widget definitions, manage dashboard instances, store required credentials, and populate widget caches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can establish ongoing widget refresh jobs that may invoke local commands or CLI tools. <br>
Mitigation: Enable scheduled refresh only for widgets whose fetch.instructions have been reviewed, and disable or remove jobs that are no longer needed. <br>
Risk: Widgets may depend on stored API keys or credentials for external services. <br>
Mitigation: Use least-privilege, revocable credentials and avoid broad personal tokens when a scoped token will work. <br>
Risk: A local dashboard may expose sensitive API, calendar, email, or code activity data if reachable from the network. <br>
Mitigation: Keep Glance bound to localhost unless external access is intentional, and require strong bearer-token authentication for non-local access. <br>
Risk: Imported widget instructions can ask the agent to collect data or execute steps beyond the user's intent. <br>
Mitigation: Review imported widget definitions and fetch.instructions before adding them to a dashboard or enabling cron-based refresh. <br>


## Reference(s): <br>
- [Glance ClawHub listing](https://clawhub.ai/acfranzen/glance) <br>
- [Glance homepage](https://github.com/acfranzen/glance) <br>
- [Widget SDK Documentation](artifact/widget-sdk.md) <br>
- [Dashboard Management API](artifact/dashboard-api.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON, JSX/TSX, HTTP, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update dashboard widget definitions, cache payloads, credential setup steps, and scheduled refresh instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
