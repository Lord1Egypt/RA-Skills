## Description: <br>
A CLI tool that executes Python source code to manage todos via Linear's API, including task creation with natural language dates, priorities, and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avegancafe](https://clawhub.ai/user/avegancafe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, employees, and agents use this skill to create, list, complete, snooze, and review Linear-based todos from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes bundled Python source code and uses a Linear API key that can create and update issues. <br>
Mitigation: Review the source before use and prefer a dedicated, revocable Linear API token with the minimum needed scope. <br>
Risk: Running setup can store the Linear API key in plaintext JSON at ~/.config/linear-todos/config.json. <br>
Mitigation: Prefer LINEAR_API_KEY as an environment variable when possible; if setup is used, rely on the user-only config permissions and revoke the token if no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/avegancafe/linear-todos) <br>
- [Linear API Settings](https://linear.app/settings/api) <br>
- [Linear GraphQL API Endpoint](https://api.linear.app/graphql) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>
- [Skill Documentation](SKILL.md) <br>
- [Security Information](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, optional JSON for list results, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Linear API key; setup can optionally persist configuration at ~/.config/linear-todos/config.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
