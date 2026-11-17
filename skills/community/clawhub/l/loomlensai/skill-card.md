## Description:

Estimate the cost of any AI prompt across 19+ models before you run it. Works with OpenAI, Anthropic, Google, DeepSeek, xAI, MiniMax, and local models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avale-slai](https://clawhub.ai/user/avale-slai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI practitioners use Loomlensai to estimate prompt costs before running prompts across multiple AI models, compare model costs, and optimize production pipeline budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer makes a persistent PATH change in ~/.zshrc.

Mitigation: Review install.sh before installation and run it only if the persistent shell configuration change is acceptable.

Risk: The installer sends an install analytics ping.

Mitigation: Run install.sh only if install telemetry to Signalloom is acceptable for the deployment environment.

Risk: The declared loomlens executable is required but not supplied in the artifact evidence.

Mitigation: Verify that a legitimate loomlens executable is installed from a trusted source before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avale-slai/skills/loomlensai)
- [Publisher profile](https://clawhub.ai/user/avale-slai)
- [Signalloom signup](https://signalloomai.com/signup)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text cost estimates with model-by-model cost bands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include input, output, and cached token estimates; low, mid, and high cost bands; cheapest model recommendation; and savings comparison.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact package.json says 1.0.1 and install.sh says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
