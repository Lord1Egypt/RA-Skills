## Description:

Computer use for GUI automation tasks via VLA models. Use when the user describes a task in natural language that requires visual screen interaction and no API or CLI exists for the target app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoluohei](https://clawhub.ai/user/xiaoluohei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use Mano Cua A to automate visible desktop GUI tasks from natural language when target apps do not provide API or CLI access. It supports local on-device inference for private work and cloud mode for more complex screen reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install external native desktop-control components without pinned versions or hashes in the reviewed artifact.

Mitigation: Install only from trusted publisher channels and prefer pinned releases with hashes or signatures before running the binary, SDK installer, or model installer.

Risk: The tool can observe and act on the visible foreground desktop during a user-initiated task.

Mitigation: Avoid sensitive accounts unless the session can be monitored, use step limits, and stop the task immediately if behavior diverges from the requested scope.

Risk: Cloud mode sends primary-display screenshots for inference during active sessions.

Mitigation: Use local mode for privacy-sensitive work and close or hide unrelated sensitive content before starting a task.

## Reference(s):

- [Mano Cua A on ClawHub](https://clawhub.ai/xiaoluohei/skills/mano-cua-a)
- [Mininglamp-AI mano-skill source](https://github.com/Mininglamp-AI/mano-skill)
- [mano-skill GitHub releases](https://github.com/Mininglamp-AI/mano-skill/releases)
- [Mano-P model](https://huggingface.co/Mininglamp-2718/Mano-P)
- [task_model.py audit reference](https://github.com/Mininglamp-AI/mano-skill/blob/main/visual/model/task_model.py)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation commands, run examples, local and cloud mode notes, and operational safety constraints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
