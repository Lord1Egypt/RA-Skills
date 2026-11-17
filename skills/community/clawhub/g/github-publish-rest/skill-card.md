## Description:

Publishes a local folder to a GitHub repository as one commit using the Git Data REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to publish an approved local folder to a GitHub repository when their available GitHub connector cannot write or local Git credentials are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing unintended files could expose private information.

Mitigation: Use a checked staging folder containing only approved files, reject symlinks, and inspect the upload list; .gitignore is not enforced.

Risk: A publishing credential could be exposed or have broader access than needed.

Mitigation: Use a token limited to the target repository, keep it in memory, and avoid temporary-token recovery examples.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/catsmansion/skills/github-publish-rest)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Python script and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a publish script, file verification guidance, and operational troubleshooting notes.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
