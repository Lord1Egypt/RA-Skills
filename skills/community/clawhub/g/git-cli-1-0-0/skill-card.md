## Description: <br>
Helper for using the Git CLI to inspect, stage, commit, branch, and synchronize code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for practical Git command-line guidance, including repository inspection, staging, committing, branching, stashing, syncing with remotes, and troubleshooting common Git states. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git write or sync commands can commit secrets, overwrite local work, or publish unintended changes. <br>
Mitigation: Check repository status, branch, staged files, diff, and remote before running write or sync commands. <br>
Risk: Destructive Git commands can permanently discard work or rewrite shared history. <br>
Mitigation: Prefer read-only inspection commands first and avoid destructive commands unless the user explicitly asks and understands the risk. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kenswj/git-cli-1-0-0) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kenswj) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
