## Description:

Give your agent a virtual board of 8 specialized reasoning frameworks (strategy, risk, market, operations, ethics, forecasting, execution, AI-engineering) that independently evaluate a decision and synthesize a go/hold/kill verdict with confidence and concrete findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roberthill0475-lang](https://clawhub.ai/user/roberthill0475-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run structured decision reviews for ventures, campaigns, content, and business choices. It returns council-by-council findings plus a synthesized go, hold, kill, or iterate recommendation with confidence and cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted prompts, campaign briefs, venture ideas, and context are sent to OpenRouter and possible downstream model providers.

Mitigation: Use only with an approved external-model data-handling path, and do not submit secrets, customer records, regulated data, or confidential strategy.

Risk: The artifact can write local prompt, application, and cost logs.

Mitigation: Review log contents and retention behavior before use, and disable or restrict logging when sensitive business context may be present.

Risk: The setup text suggests installing dependencies with a system pip override.

Mitigation: Install in a virtual environment with pinned dependencies and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roberthill0475-lang/skills/multi-council-decision-engine)
- [Publisher profile](https://clawhub.ai/user/roberthill0475-lang)
- [OpenRouter model catalog](https://openrouter.ai/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python-returned dictionaries and dataclass objects containing JSON-like council results, synthesized verdict text, flags, confidence, and cost fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and OPENROUTER_API_KEY; sends prompts to OpenRouter-backed models and may write local prompt, application, and cost logs.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
