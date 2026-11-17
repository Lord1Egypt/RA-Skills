## Description:

Analyzes a supplied Git repository or web URL, classifies the content type, and routes it to security review, queueing, project evaluation, or skill installation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to triage user-provided URLs, identify whether they point to skills, papers, function projects, direct files, or webpages, and dispatch follow-up handling such as queueing, evaluation, security scanning, or installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact user-provided URLs and clone remote repositories.

Mitigation: Use it only with trusted repositories and links.

Risk: The skill can write to OpenClaw memory and install or replace local skills.

Mitigation: Add explicit confirmation and path validation before install or memory-write actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woai36d/skills/git-repo-analyzer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files, guidance]

**Output Format:** [Markdown instructions with JSON command output and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append queued URL records to OpenClaw memory and install or replace local skills after security review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
