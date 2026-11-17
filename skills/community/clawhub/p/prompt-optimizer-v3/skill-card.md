## Description:

Optimizes vague user requests into structured, executable AI prompts with task, format, audience, style, and constraint handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntaffffff](https://clawhub.ai/user/ntaffffff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prompt authors use this skill to turn short or ambiguous requests into clearer prompts for coding, writing, analysis, translation, research, and other AI tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom configuration can alter prompt patterns and enhancements in ways that change generated instructions.

Mitigation: Review custom config files before enabling them.

Risk: Batch input and output options read from and write to user-specified paths.

Mitigation: Use trusted paths and review file targets before running batch processing.

Risk: Optimized prompts may still be incorrect, overly broad, or unsuitable for the target task.

Mitigation: Review optimized prompts before sending them to an AI system for important work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntaffffff/skills/prompt-optimizer-v3)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, YAML, guidance]

**Output Format:** [Plain text, Markdown, JSON, or YAML depending on CLI options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process one prompt or batch prompts from a file and can write results to a user-specified output path.]

## Skill Version(s):

3.2.0 (source: server release metadata, artifact _meta.json, config_data.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
