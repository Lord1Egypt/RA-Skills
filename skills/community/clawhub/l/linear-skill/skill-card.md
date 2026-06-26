## Description: <br>
Manage Linear projects, issues, and tasks via the bundled Node CLI and the official Linear API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaTriXy](https://clawhub.ai/user/MaTriXy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect and update Linear teams, projects, issues, labels, workflow states, comments, and user records through a local CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local CLI uses LINEAR_API_KEY and can act according to the token's Linear permissions. <br>
Mitigation: Use a dedicated least-privilege Linear token and avoid sharing it outside the local environment. <br>
Risk: Create or update commands can change Linear projects, issues, comments, labels, and workflow state. <br>
Mitigation: Read current state first, confirm issue and project IDs before mutations, prefer narrow updates, and summarize changed records after execution. <br>
Risk: Secrets or sensitive data could be exposed if placed in Linear issue descriptions or comments. <br>
Mitigation: Do not include secrets in Linear content and review generated descriptions or comments before submitting them. <br>
Risk: Runtime dependencies are installed locally with npm. <br>
Mitigation: Install from the included lockfile before use. <br>


## Reference(s): <br>
- [Linear API Reference](references/API.md) <br>
- [Project homepage](https://github.com/MaTriXy/linear-skill) <br>
- [Linear API key settings](https://linear.app/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read from or mutate Linear records through the bundled local CLI when LINEAR_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
