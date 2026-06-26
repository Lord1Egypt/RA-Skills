## Description: <br>
Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, and advanced repository queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrherojack](https://clawhub.ai/user/mrherojack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate GitHub through the GitHub CLI, including inspecting pull request checks, workflow runs, issues, and structured API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may use the active GitHub CLI account and scopes when executing suggested commands. <br>
Mitigation: Confirm the active `gh` account and token scopes before use. <br>
Risk: Commands can target the wrong repository when run outside the intended git directory. <br>
Mitigation: Prefer explicit `--repo owner/repo` targets or direct GitHub URLs. <br>
Risk: Some GitHub CLI actions can modify issues, pull requests, workflow runs, or repository data. <br>
Mitigation: Review commands that change repository state before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use structured JSON output from the GitHub CLI when commands include `--json` or `--jq`.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
