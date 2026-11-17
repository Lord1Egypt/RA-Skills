## Description:

牛股王独家研发的A股机游共振选股模型，基于机构资金与游资动向双重筛选，精准定位同时被机构和游资关注的股票，这类股票兼具基本面支撑和短线活跃度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoxx779-cmd](https://clawhub.ai/user/maomaoxx779-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External investors and market analysts use this skill to query A-share stock pools selected by a Niuguwang institutional and speculative-capital convergence model, compare the three supported strategies, and review current or historical stock-screening results. It is informational and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a credential-like API token in a sample request.

Mitigation: Remove or rotate the token-like value before deployment, and avoid copying it into logs, scripts, or shared prompts.

Risk: The artifact requires every response to include a fixed Niuguwang-branded app-download footer.

Mitigation: Review the footer requirement before installation and change the skill text if promotional content is not acceptable for the deployment context.

Risk: The skill returns stock-screening information that could be mistaken for investment advice.

Mitigation: Preserve the artifact's AI disclaimer and require users to treat outputs as informational rather than as trading instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maomaoxx779-cmd/skills/institutional-speculative-capital-convergence)
- [Niuguwang factor settings API](https://apicore.niuguwang.com/selstock/factor/getsetting?packType=2000&version=5.0.16.0)
- [Niuguwang stock pool API](https://apicore.niuguwang.com/selstock/factor/getstocks?packType=2000&version=5.0.16.0&codes=sys:corevent10,sys:amount610)
- [Niuguwang historical stock pool API](https://apicore.niuguwang.com/selstock/FactorPool/GetStock?packType=2000&version=5.0.16.0&date=2026-04-14)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional curl command examples and stock-screening summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Every generated answer is required by the artifact to include a Niuguwang data-source footer and an AI investment-advice disclaimer.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
