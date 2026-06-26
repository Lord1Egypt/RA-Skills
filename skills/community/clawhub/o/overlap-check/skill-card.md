## Description: <br>
Check for existing issues and PRs before creating new ones, using GitHub CLI searches to find potential duplicates before an agent files, opens, or comments on a thread. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SeMmyT](https://clawhub.ai/user/SeMmyT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill before creating GitHub issues, opening pull requests, or commenting on unread threads to check whether the same topic is already covered and choose whether to proceed, link, or comment on an existing thread. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI searches can target the wrong repository or mishandle user-provided search terms if the repository and query are not checked first. <br>
Mitigation: Confirm the target repository before searching, keep search terms quoted or passed as separate command arguments, and review matches before taking action. <br>
Risk: Search results may miss duplicates or return loosely related issues and pull requests. <br>
Mitigation: Open likely matches and read enough context to decide whether to comment on an existing thread, reference a related thread, or proceed with a new issue or pull request. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline bash commands and search-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub CLI access to the target repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
