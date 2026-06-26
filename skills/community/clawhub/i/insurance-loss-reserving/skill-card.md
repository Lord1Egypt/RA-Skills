## Description: <br>
Assists agents with actuarial loss reserving using chainladder-python, from historical claims triangles to IBNR reserve estimates and tail-factor fitting across reinsurance, catastrophe, and general-liability lines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Actuaries, insurance analytics developers, and reserving teams can use this skill to guide loss triangle preparation, development-factor analysis, reserving method selection, tail-factor review, and IBNR estimation workflows. Review is required before execution because the artifact also contains unrelated trading and order-workflow instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Purpose mismatch: the release is advertised for insurance reserving but includes trading, market-data, and order-workflow instructions. <br>
Mitigation: Review and correct or reclassify the artifact before deployment; restrict use to verified reserving guidance until the publisher removes or separates the trading workflow. <br>
Risk: Trading or purchase-related behavior could connect to broker, paid-provider, or market-data workflows. <br>
Mitigation: Test only in a sandbox, do not provide broker or paid-provider credentials, and require explicit manual approval before any order-related action. <br>
Risk: Actuarial estimates can be misleading when triangle structure, cumulative versus incremental data, latest diagonals, or tail assumptions are mishandled. <br>
Mitigation: Validate input data, temporal ordering, triangle representation, excluded diagonals, and tail-factor assumptions with qualified actuarial review before relying on outputs. <br>


## Reference(s): <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Human summary](artifact/human_summary.md) <br>
- [Anti-patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Component capability map](artifact/references/COMPONENTS.md) <br>
- [Semantic locks and preconditions](artifact/references/LOCKS.md) <br>
- [Cross-project wisdom](artifact/references/WISDOM.md) <br>
- [Seed reference](artifact/references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, provider, strategy, time range, or entity identifiers when following the trading-oriented artifact path; reserving workflows should require human validation of actuarial assumptions and source data.] <br>

## Skill Version(s): <br>
0.3.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
