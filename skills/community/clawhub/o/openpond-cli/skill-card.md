## Description: <br>
Use the OpenPond CLI to create repos, watch deployments, and run tools without the web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glucrypto](https://clawhub.ai/user/glucrypto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the OpenPond CLI for repository creation, deployment monitoring, tool execution, account-level app commands, and OpenTool passthrough workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed through prompts, shell history, or insecure environment handling. <br>
Mitigation: Prefer interactive login or secure environment injection for OPENPOND_API_KEY, and avoid placing real keys in prompts or command history. <br>
Risk: Repository, tool, and agent-creation commands can affect OpenPond account resources. <br>
Mitigation: Verify the openpond-code package source and review repository, tool, deployment, and agent-creation commands before running them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI setup, authentication options, repository workflows, deployment watching, tool commands, account commands, and cache/environment configuration notes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
