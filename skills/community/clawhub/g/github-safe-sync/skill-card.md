## Description: <br>
Inspect, trigger, and clean up GitHub mirror repositories that use a safe-sync GitHub Actions workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grey0758](https://clawhub.ai/user/grey0758) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect GitHub mirror repositories, trigger safe-sync workflows, audit recent workflow runs, and clean up false-positive sync artifacts after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change GitHub repository state when dispatching workflows, closing issues, or deleting backup branches. <br>
Mitigation: Run status before write actions, review the repository state, and re-run status after each write operation. <br>
Risk: A broad GitHub token could allow unintended access beyond the target mirrors. <br>
Mitigation: Use a fine-grained GitHub token limited to the target repositories and keep it only in the GITHUB_TOKEN environment variable. <br>
Risk: Closing force-push alert issues can hide real upstream history problems. <br>
Mitigation: Close force-push alert issues only after confirming the alerts are false positives. <br>
Risk: Deleting backup branches can remove recovery points that may still be needed. <br>
Mitigation: Delete backup branches only after confirming the mirror workflow is healthy; use dry-run mode to preview deletions when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/grey0758/github-safe-sync) <br>
- [GitHub REST API](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GITHUB_TOKEN from the environment and repository identifiers in owner/repo form.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
