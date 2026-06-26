## Description: <br>
Investment Framework Skill provides an investment-analysis toolkit for value analysis, moat evaluation, intrinsic-value calculation, asset allocation, decision checks, trend forecasting, risk assessment, and market sentiment review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors and agents use this skill bundle to structure educational investment analysis, compare companies, test decision logic, evaluate risks, and produce portfolio or allocation guidance. It is not a substitute for professional financial advice or independent due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes account-affecting publishing automation and live-looking embedded credentials. <br>
Mitigation: Remove and rotate embedded tokens before installation, and delete or isolate ClawHub publishing and cron tooling unless it is explicitly needed. <br>
Risk: The bundle requests broad execution, network, crypto, and purchase-related capabilities for an investment-analysis workflow. <br>
Mitigation: Narrow permissions to the specific skills being used, review scripts before execution, and deny purchasing or account-impacting actions unless separately approved. <br>
Risk: Investment outputs may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as educational analysis only, retain the investment-risk disclaimer, and require independent review before acting on any recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/investment-framework-skill) <br>
- [Publisher profile](https://clawhub.ai/user/lj22503) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/USAGE.md) <br>
- [Application guide](artifact/docs/APPLICATION_GUIDE.md) <br>
- [Theory](artifact/docs/THEORY.md) <br>
- [Output schema](artifact/OUTPUT_SCHEMA.md) <br>
- [Value analyzer theory](artifact/value-analyzer/references/theory.md) <br>
- [Moat theory](artifact/moat-evaluator/references/moat-theory.md) <br>
- [Portfolio theory](artifact/portfolio-designer/references/theory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, checklists, scorecards, allocation plans, and optional script or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include the skill's investment-risk disclaimer and remain educational rather than personalized financial advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
