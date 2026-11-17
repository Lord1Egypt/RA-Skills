## Description:

Provides eight prompt-injection drill cases and expected safe responses for manual pre-launch testing of an agent's system prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and red-team testers use the drill cases and expected responses to manually check an agent's resistance to prompt injection before launch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive system prompts may be exposed during local testing.

Mitigation: Use sanitized or non-production prompts when possible and limit access to test inputs and outputs.

Risk: An unintended --out path may write a drill file to the wrong location.

Mitigation: Review the destination path before running the CLI.

Risk: Fixed examples do not establish that an agent is secure against all injection attempts.

Mitigation: Manually compare actual responses against the expected behaviors and supplement with broader testing.

## Reference(s):

- [LGD theory (background link in README)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown drill checklist; optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight fixed attack cases with expected behaviors; optional local output file. Results require manual comparison with the target agent's responses.]

## Skill Version(s):

1.0.6 (source: server-resolved ClawHub release; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
