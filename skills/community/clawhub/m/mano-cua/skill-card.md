## Description:

Computer use for GUI automation tasks via VLA models when the user describes a natural-language task that requires visual screen interaction and no API or CLI exists for the target app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanningwang](https://clawhub.ai/user/hanningwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to delegate bounded desktop GUI tasks to a computer-use agent when an application or website does not expose a suitable API or CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install a native binary through an unpinned distribution path.

Mitigation: Review the publisher and release before installation, and verify checksums or package provenance where available.

Risk: Cloud mode may transmit primary-display screenshots and can use local shell actions.

Mitigation: Use local mode for private tasks when supported, and disable cloud-mode shell execution with `mano-cua config --set disable-bash true` when shell actions are not required.

Risk: Desktop automation requires GUI permissions and can affect visible applications within the requested task scope.

Mitigation: Grant only the permissions needed for the task, keep the status panel visible, set bounded step limits, and stop the session before switching to unrelated work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanningwang/skills/mano-cua)
- [mano-cua source homepage](https://github.com/Mininglamp-AI/mano-skill)
- [mano-cua releases](https://github.com/Mininglamp-AI/mano-skill/releases)
- [Mano-P model](https://huggingface.co/Mininglamp-2718/Mano-P)
- [Network-call module reference](https://github.com/Mininglamp-AI/mano-skill/blob/main/visual/model/task_model.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands for installing, running, configuring, and stopping desktop automation sessions.]

## Skill Version(s):

1.1.0 (source: release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
