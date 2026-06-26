## Description: <br>
Multi-stage backtest validation framework that uses smoke, stress, medium, and full validation windows before committing to expensive full-period backtests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and strategy authors use this skill to plan staged backtest validation, record each stage outcome, and decide the next validation step before running longer or more expensive tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest backtest-poller commands, while actual submission and early-stop behavior are handled by a separate skill. <br>
Mitigation: Review any generated backtest-poller command before running it and review the backtest-poller skill independently before relying on submissions or early-stop behavior. <br>
Risk: Validation decisions depend on complete and accurate local records of each stage result. <br>
Mitigation: Record every stage outcome, including failures, and check status or next-stage output before advancing a strategy. <br>


## Reference(s): <br>
- [Progressive Validator on ClawHub](https://clawhub.ai/tltby12341/progressive-validator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Terminal text with suggested shell commands and local JSON result records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and no external Python packages; actual backtest submission depends on the separate backtest-poller skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
