## Description:

Cross-platform local printer CLI - Manage and print to local printers (Windows/macOS/Linux) via the printer-ai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nullying](https://clawhub.ai/user/nullying)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list local printers, check printer status, print local files, inspect printer capabilities, and manage print jobs through the printer-ai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata points to an unpinned executable package.

Mitigation: Prefer a pinned commit or versioned release before installing printer-ai.

Risk: The skill can print files and cancel print jobs, which can cause physical output or job disruption.

Mitigation: Require confirmation of the file, printer, print options, and job ID before printing or canceling jobs.

Risk: Printed documents may expose sensitive content on shared or unattended printers.

Mitigation: Avoid sending sensitive documents to shared or unattended printers.

## Reference(s):

- [Printer Ai ClawHub skill page](https://clawhub.ai/nullying/skills/printer-ai-skills)
- [printer-ai install package metadata](https://github.com/NullYing/printer-ai-skills.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON option examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is intended for local printer operations and printer-ai CLI usage.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
