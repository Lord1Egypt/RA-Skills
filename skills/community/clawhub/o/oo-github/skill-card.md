## Description: <br>
Operates GitHub through an OOMOL-connected account for reading, creating, updating, and deleting repository, branch, commit, file, issue, pull request, release, workflow, event, and search data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate GitHub repositories, branches, commits, files, issues, pull requests, releases, workflows, events, and searches through an OOMOL-connected GitHub account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive actions can modify, overwrite, or remove GitHub data. <br>
Mitigation: Confirm the exact repository, branch, file, issue, pull request, label, release, workflow, and payload before approving write or destructive actions. <br>
Risk: A connected GitHub account can expose private repositories or organization resources according to its granted scopes. <br>
Mitigation: Install only when OOMOL and the connected GitHub account or organizations are trusted, and use appropriately scoped connections. <br>
Risk: Workflow reruns, pull request merges, releases, and commit statuses can affect CI/CD or release processes. <br>
Mitigation: Review the target repository, branch, workflow, release, and intended operational effect before approving those actions. <br>


## Reference(s): <br>
- [ClawHub GitHub skill page](https://clawhub.ai/oomol/skills/oo-github) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [GitHub homepage](https://github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected GitHub account and appropriate scopes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
