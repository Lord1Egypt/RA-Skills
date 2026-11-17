## Description:

GitHub Issue to auto-implement to PR to review to auto-merge pipeline; write an Issue with an [auto] tag and the pipeline handles task analysis, implementation, testing, PR creation, review, merge, progress comments, and early-exit optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shunsukehayashi](https://clawhub.ai/user/shunsukehayashi)

### License/Terms of Use:


## Use Case:

Developers and repository maintainers use this skill to turn tagged GitHub Issues into implementation branches, pull requests, automated reviews, and merges through an OpenClaw webhook workflow. It is intended for tightly governed repositories where issue-driven automation is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook content can trigger code changes, pushes, pull request creation, and merges.

Mitigation: Use trusted repository and actor allowlists, mandatory CI, and human approval before pushing or merging.

Risk: Automation runs with repository and GitHub credentials in response to external events.

Mitigation: Run in sandboxed disposable environments with scoped, short-lived GitHub credentials.

Risk: Templated webhook fields can become unsafe when interpolated into shell commands.

Mitigation: Use safe argument handling and avoid direct shell interpolation of untrusted webhook data.

## Reference(s):

- [Prompt Request Pipeline on ClawHub](https://clawhub.ai/shunsukehayashi/skills/prompt-request)
- [Publisher profile](https://clawhub.ai/user/shunsukehayashi)
- [sample-hook-config.json](examples/sample-hook-config.json)
- [messageTemplate.txt](templates/messageTemplate.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, GitHub comments, Git commands, GitHub CLI commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository automation instructions and templates for OpenClaw GitHub hook sessions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
