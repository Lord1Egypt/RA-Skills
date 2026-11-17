## Description:

Track OpenClaw AI token usage and cost per model on Linux by parsing session JSONL files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hablabechir](https://clawhub.ai/user/hablabechir)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect local OpenClaw session logs and summarize token usage, model activity, cache usage, and estimated cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session logs, which may contain sensitive conversation records.

Mitigation: Use the default sessions directory or a narrowly chosen --sessions-dir, and avoid pointing the skill at unrelated private JSONL files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON summaries with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local JSONL session logs and reports per-model turns, input tokens, output tokens, cache tokens, and cost.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
