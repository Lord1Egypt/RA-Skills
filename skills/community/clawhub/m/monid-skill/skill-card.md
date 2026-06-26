## Description: <br>
Monid helps agents discover, inspect, and run online data endpoints for web data collection, including social media, product, content monitoring, and research data tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[monid](https://clawhub.ai/user/monid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find available data endpoints, inspect accepted parameters, execute data collection runs, and retrieve structured results from online sources. It is especially relevant for social media search and comparison workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to save or enable itself for future sessions. <br>
Mitigation: Allow persistent installation or enablement only after explicit user approval. <br>
Risk: The skill handles Monid API keys during setup. <br>
Mitigation: Use limited, revocable API keys and prefer running key configuration commands locally instead of pasting secrets into chat. <br>
Risk: Data endpoint runs may incur per-result costs or execute paid data collection. <br>
Mitigation: Inspect endpoint schemas first, start with small result limits, and confirm budget-sensitive runs before increasing scope. <br>
Risk: The setup flow installs or updates the Monid npm CLI. <br>
Mitigation: Verify the npm package and requested install command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/monid/monid-skill) <br>
- [Monid application](https://app.monid.ai) <br>
- [Monid API keys](https://app.monid.ai/access/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or file outputs from CLI runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce saved result files from completed Monid runs.] <br>

## Skill Version(s): <br>
0.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
