## Description:

Prepare and publish a git release tag by inspecting the repo's release convention, bumping affected package versions, validating release builds, committing the release prep, pushing the branch, and pushing a new tag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femto](https://clawhub.ai/user/femto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to prepare version bumps, validate release builds, commit release preparation changes, and push annotated git tags that may trigger release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare remote release-triggering actions by pushing a branch and git tag.

Mitigation: Require the agent to show the target branch, commit SHA, tag name, changed files, affected packages, and likely workflows before explicitly approving any branch or tag push.

Risk: A tag push may trigger GitHub Actions or package publishing before the release is ready.

Mitigation: Run the builds required by the tag-triggered workflow and do not approve tag creation or tag push while required validation is failing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/femto/skills/new-tag)
- [Publisher Profile](https://clawhub.ai/user/femto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown summary with release details and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bumped packages, new versions, validation commands, commit SHA, pushed tag name, and residual release risk.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
