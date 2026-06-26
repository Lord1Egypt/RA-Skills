## Description: <br>
股票仓位管理与风控专家。不负责选股，专注仓位管理和头寸调度。提供移动跟踪止盈、阶梯式止盈、核心 - 卫星策略、动态再平衡等经典模型。适用于大幅浮盈、深度套牢、震荡洗盘等各种持仓场景，给出冷酷理性的买卖和调仓建议。使用场景：用户已有持仓，需要止盈/止损建议、仓位调整、风险控制、心理疏导时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgetao730](https://clawhub.ai/user/georgetao730) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with existing stock positions use this skill to reason through position sizing, stop-loss and take-profit planning, rebalancing, and trading psychology. It produces structured risk-management guidance for scenarios such as large unrealized gains, drawdowns, high single-stock concentration, and range-bound positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce stock-position recommendations that may be mistaken for licensed financial advice. <br>
Mitigation: Treat outputs as informational risk-management support, verify prices and assumptions independently, and make investment decisions under the user's own responsibility. <br>
Risk: Optional market-data dependencies such as AKShare or pandas may change the runtime environment or data source behavior. <br>
Mitigation: Install optional dependencies only when needed, review package sources and versions, and verify any fetched market data before relying on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/georgetao730/position-risk-manager) <br>
- [Risk Management Rules](references/risk-rules.md) <br>
- [Trading Psychology](references/trading-psychology.md) <br>
- [Trailing Stop Guide](references/trailing-stop-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with optional shell commands for the local position calculator] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language position risk assessment, action plan, price-level suggestions, and trading psychology notes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
