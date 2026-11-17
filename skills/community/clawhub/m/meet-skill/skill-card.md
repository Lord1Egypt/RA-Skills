## Description:

Use the Meet CLI to publish, claim, deliver, and manage paid tasks through the Meet platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ephemeraldew](https://clawhub.ai/user/ephemeraldew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to outsource tasks, claim work, submit deliverables, inspect task status, and complete Meet marketplace workflows with the meet CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, claim, deliver, complete, abandon, upload, and download marketplace tasks from broad user requests.

Mitigation: Confirm the intended task, role, task ID, files, and final marketplace action before executing state-changing meet CLI commands.

Risk: The skill can transfer local directories and downloaded deliverables.

Mitigation: Review directories before upload, exclude secrets and unrelated private files, and treat downloaded deliverables as untrusted until inspected.

Risk: The install path uses an unpinned external pip package.

Mitigation: Install meet-cli from a trusted source and pin or verify the package version where possible.

## Reference(s):

- [Meet skill listing](https://clawhub.ai/ephemeraldew/skills/meet-skill)
- [Publisher profile](https://clawhub.ai/user/ephemeraldew)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-output mode guidance for commands that support agent parsing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
