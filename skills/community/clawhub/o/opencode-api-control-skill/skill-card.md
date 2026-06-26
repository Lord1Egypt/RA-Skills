## Description: <br>
A skill for controlling OpenCode CLI through its local web server API, including session management, prompt submission, provider selection, monitoring, and diff summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[malek262](https://clawhub.ai/user/malek262) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to orchestrate coding tasks through a local OpenCode server, manage project sessions, choose connected model providers, monitor progress, and summarize resulting changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct OpenCode to change files in configured project directories. <br>
Mitigation: Use it only for intended projects, review the selected project path and provider before task execution, and inspect diff summaries before relying on generated changes. <br>
Risk: An OpenCode server exposed beyond localhost can allow unintended access to project automation and project data. <br>
Mitigation: Keep BASE_URL pointed at 127.0.0.1 when possible, avoid binding the server to shared networks without authentication, and verify network exposure before use. <br>
Risk: Saved state, event logs, prompts, project paths, and diffs may contain sensitive project information. <br>
Mitigation: Treat skill state and logs as sensitive local data, limit access to the skill directory, and clear stale state when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/malek262/opencode-api-control-skill) <br>
- [README](artifact/README.md) <br>
- [API Quick Reference](artifact/Reference/API_QUICK_REFERENCE.md) <br>
- [State Management](artifact/Reference/STATE_MANAGEMENT.md) <br>
- [Events Guide](artifact/Reference/EVENTS_GUIDE.md) <br>
- [Providers Reference](artifact/Reference/PROVIDERS_REFERENCE.md) <br>
- [Complete Examples](artifact/Reference/COMPLETE_EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenCode API responses and saved session state when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
