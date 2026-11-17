## Description:

Track OpenRouter API spending, including credit balance, per-model cost breakdown, and spending projections from OpenClaw session logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcajigasm](https://clawhub.ai/user/lcajigasm)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to monitor OpenRouter credits, usage costs, per-model spending, and credit runway from local OpenClaw session logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may delete an existing ~/.openclaw/workspace/skills/openrouter-usage directory or symlink when linking the skill.

Mitigation: Back up that path before installation, decline the automatic linking prompt, or create the symlink manually after reviewing the target.

Risk: The tool reads local OpenClaw session logs and may read an OpenRouter API key from the OpenClaw auth store or OPENROUTER_API_KEY.

Mitigation: Run it only in an environment where the user intends to expose those local logs and credentials to this command, and review file permissions for the OpenClaw auth store.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenRouter API](https://openrouter.ai/api/v1)
- [ClawHub skill page](https://clawhub.ai/lcajigasm/skills/openrouter-usage-info)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON command output, with Markdown usage guidance in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include credit balance, per-model usage totals, date-filtered cost summaries, agent filters, and spending projections.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
