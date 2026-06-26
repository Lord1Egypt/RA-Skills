## Description: <br>
Industry Research Analyst 行业研究分析师 helps an agent produce structured, investment-oriented industry research reports covering market sizing, value chain analysis, competitive landscape, growth drivers, risk assessment, and investment thesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YBridge](https://clawhub.ai/user/YBridge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investment analysts, strategy teams, founders, and business operators use this skill to request industry deep dives, sector comparisons, competitive maps, trend updates, and investment theses in a structured research-report format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Industry research and investment conclusions may be incorrect, stale, or unsuitable for a user's financial decisions. <br>
Mitigation: Independently verify financial data, market estimates, and investment conclusions before relying on the output. <br>
Risk: The optional helper script sends ticker symbols to Yahoo Finance for public market data. <br>
Mitigation: Avoid sending sensitive or non-public ticker lists, and review outbound data-sharing requirements before using the script. <br>


## Reference(s): <br>
- [Research Framework](references/research-framework.md) <br>
- [Output Examples](references/output-examples.md) <br>
- [Yahoo Finance Chart API endpoint used by optional helper script](https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1y&interval=1d) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research reports with tables; optional helper-script output can include Markdown comparison tables and JSON details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English guidance; emphasizes dated source attribution, cross-checking key data, and explicit uncertainty labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
