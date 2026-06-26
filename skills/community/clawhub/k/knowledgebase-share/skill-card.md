## Description: <br>
Operate a multi-agent shared knowledge layer backed by one GitHub repository. Use when setting up shared/private knowledge folders, enforcing branch+PR workflow, syncing branches, resolving merge conflicts, and standardizing how agents write/promote knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and operate a shared GitHub-backed knowledgebase for multi-agent work. It supports private agent notes, reviewed promotion into shared knowledge, branch synchronization, and conflict-handling practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync helper can push changes directly to the configured repository branch, including main by default. <br>
Mitigation: Use a dedicated repository and an agent branch, enable branch protection and pull request review, and run status mode or --no-push until changes have been reviewed. <br>
Risk: Knowledgebase repositories can accidentally collect sensitive notes or secrets. <br>
Mitigation: Keep secrets out of repository content and review local changes before committing or pushing. <br>


## Reference(s): <br>
- [Knowledgebase Share release page](https://clawhub.ai/reed1898/knowledgebase-share) <br>
- [Publisher profile](https://clawhub.ai/user/reed1898) <br>
- [KB configuration template](references/kb-config.json) <br>
- [Ops Playbook](references/ops-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper shell scripts for initializing and syncing a configured Git-backed knowledgebase.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
