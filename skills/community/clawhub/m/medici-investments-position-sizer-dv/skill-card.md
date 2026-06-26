## Description: <br>
Calculate risk-based position sizes for long stock trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate long-stock position sizes from account size, entry price, stop-loss or ATR values, risk percentage, and Kelly inputs. It supports risk-management review before a trade, not trade entry or exit recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local report files may contain portfolio size and planned trade details. <br>
Mitigation: Run the skill in a folder where saved reports are acceptable, avoid synced or shared directories for sensitive trades, and do not provide brokerage credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/medici-investments-position-sizer-dv) <br>
- [Position Sizing Methodologies](artifact/references/sizing_methodologies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Natural-language summary with CLI commands; local JSON and Markdown report files when the bundled script runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped report files in the selected output directory; reports may contain portfolio size and planned trade details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
