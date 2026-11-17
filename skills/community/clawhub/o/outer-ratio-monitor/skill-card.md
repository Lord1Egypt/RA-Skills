## Description:

Monitors selected A-share stocks by fetching public Tencent market data, reporting an outer/inner volume signal, and storing local history for trend review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoranyt](https://clawhub.ai/user/guoranyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can run the skill to inspect selected A-share stocks, view terminal status and history output, and experiment with outer/inner volume monitoring. Outputs are technical indicators only and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial signals and alerts may be materially unreliable, including a core ratio calculation that conflicts with the documentation.

Mitigation: Do not use the output as a trading trigger; fix and validate the calculation and alert behavior before relying on results.

Risk: Advertised automatic alerts and webhook delivery are not present in the shipped code.

Mitigation: Treat the shipped behavior as terminal output and local history unless alert delivery is implemented and tested.

Risk: The skill fetches public Tencent market data and stores local stock-monitoring history.

Mitigation: Review network access and local storage paths before installation, and run in a constrained environment when appropriate.

## Reference(s):

- [Outer Ratio Guide](references/outer_ratio_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/guoranyt/skills/outer-ratio-monitor)
- [Tencent Market Data Endpoint](https://qt.gtimg.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is terminal text with local JSON history and snapshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public market data and may write local history under the user's OpenClaw memory directory.]

## Skill Version(s):

2.4.0 (source: server release, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
