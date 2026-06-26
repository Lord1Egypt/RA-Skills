## Description: <br>
Mainland China A-share stock and sector analysis tool (中国A股个股与板块分析) for stock snapshots, finance indicators, price levels, sector lookup, strategy, researcher, bayesian monitor, and preview deep research flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jickchen34](https://clawhub.ai/user/jickchen34) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer mainland China A-share stock and sector questions, inspect finance and price context, produce preview research reports, manage subscribed instruments or buckets, and query strategy, researcher, and bayesian monitor data. It is intended for non-sensitive public market queries and authenticated Kungfu/Tianshan workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change authenticated account data through bucket, subscription, and related Tianshan API workflows. <br>
Mitigation: Install only when the publisher and Tianshan API are trusted, and review requested write actions before approving them. <br>
Risk: The skill stores an OpenKey locally for configuration workflows. <br>
Mitigation: Use a scoped credential, avoid sharing sensitive account data, and rotate the key if the local environment may be exposed. <br>
Risk: Optional research search can send research queries to a configurable external endpoint. <br>
Mitigation: Enable optional search only for a controlled or trusted provider and keep its credential separate from KUNGFU_OPENKEY. <br>
Risk: The security scan verdict is suspicious because update behavior may ask the agent to run shell commands. <br>
Mitigation: Approve update commands manually and inspect the command target before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jickchen34/kungfu-finance) <br>
- [Kungfu skills homepage](https://github.com/kungfu-trader/kungfu-skills) <br>
- [README](README.md) <br>
- [Data Products Schema](references/schemas/data_products.md) <br>
- [Research Flows](references/research-flows/README.md) <br>
- [Bucket Flow Contract](references/schemas/bucket_flow.md) <br>
- [Strategy Flow Contract](references/schemas/strategy_flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, structured JSON responses, SVG/PNG chart file paths, and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require KUNGFU_OPENKEY for authenticated Tianshan API workflows; optional Inkscape support converts chart SVG to PNG.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
