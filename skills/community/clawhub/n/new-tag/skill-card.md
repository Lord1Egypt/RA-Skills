## Description: <br>
Prepare and publish a git release tag by inspecting the repo's release convention, bumping affected package versions, validating release builds, committing the release prep, pushing the branch, and pushing a new tag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femto](https://clawhub.ai/user/femto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to prepare version bumps, run release validations, commit release prep, and push annotated git tags that may trigger publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real repository changes and trigger release automation. <br>
Mitigation: Before allowing it to push, confirm the repository, branch, version, changed files, remote, tag name, and expected CI/CD or package-publishing effects. <br>
Risk: Incorrect release preparation can include unrelated changes, use the wrong tag pattern, or publish from an unvalidated build. <br>
Mitigation: Review the release plan, stage only release files, run the builds required by the tag-triggered workflow, and do not create or push the tag while required builds are failing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/femto/new-tag) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with shell commands and release metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports bumped packages and versions, validation commands, commit SHA, pushed tag name, and residual release risk.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
