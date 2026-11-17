## Description:

Detects and rewrites AI-generated Chinese text using weighted scoring, sentence-level analysis, configurable phrase replacement, sentence restructuring, and seven writing style transforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xspeter](https://clawhub.ai/user/0xspeter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and evaluators use this skill to detect Chinese AI-writing signals, rewrite text into more natural Chinese, apply specific Chinese writing styles, and compare detector scores before and after editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can disguise AI-generated Chinese text and measure reduced detector scores.

Mitigation: Use it only for legitimate editing or authorized detector research, and do not use it to evade disclosure, academic integrity rules, platform moderation, or authenticity checks.

Risk: The workflow processes user-provided local text files and can write rewritten outputs.

Mitigation: Review input and output file paths before execution, and avoid processing sensitive or unauthorized text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xspeter/skills/humanize-chinese-2-0-0)
- [Publisher profile](https://clawhub.ai/user/0xspeter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plain text rewrites, optional JSON detection results, and file outputs from CLI scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python scripts can emit score-only text, verbose analysis, JSON detection reports, rewritten text, styled text, and before/after comparisons.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json and _meta.json identify the packaged tool as 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
