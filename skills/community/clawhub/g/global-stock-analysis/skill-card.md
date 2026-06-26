## Description: <br>
Global stock analysis for US, China, and EU markets, including technical, fundamental, macro, forex, crypto, and options workflows powered by Alpha Vantage market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luohy15](https://clawhub.ai/user/luohy15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to run terminal-based market research workflows for equities, fundamentals, technical indicators, macro conditions, forex, crypto, and US options chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an ALPHAVANTAGE_API_KEY, which is a sensitive credential. <br>
Mitigation: Provide the key through an environment variable, a local .env file, or the CLI's explicit key flag; avoid committing it to source control or sharing it in prompts and logs. <br>
Risk: Market data and generated analysis may be delayed, incomplete, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Check source timestamps and compare important conclusions against authoritative market data and qualified financial review before acting. <br>
Risk: The authoritative security evidence reports clean scan inputs but notes that artifact text was not available for a full independent review and VirusTotal was pending rather than conclusive. <br>
Mitigation: Install only when the listing and files match expected behavior, review commands before running them, and deploy in an environment appropriate for external CLI and network access. <br>


## Reference(s): <br>
- [Global Stock Analysis listing](https://clawhub.ai/luohy15/global-stock-analysis) <br>
- [Alpha Vantage](https://www.alphavantage.co) <br>
- [Fundamental Analysis](references/fundamentals.md) <br>
- [Technical Analysis](references/technicals.md) <br>
- [Macro & Market Overview](references/macro.md) <br>
- [Sector / Multi-Stock Comparison](references/comparison.md) <br>
- [Forex & Crypto](references/forex-crypto.md) <br>
- [Options Chain](references/options.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires marketdata-cli and an ALPHAVANTAGE_API_KEY for live data workflows.] <br>

## Skill Version(s): <br>
0.0.13 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
