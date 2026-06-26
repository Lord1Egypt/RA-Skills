## Description: <br>
Use when the user asks for Pionex market data, including price, ticker, order book depth, recent trades, symbol info, and OHLCV klines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pibrandon](https://clawhub.ai/user/pibrandon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve public, read-only Pionex market data through the Pionex CLI before analysis or trading workflows. It is scoped to market lookup tasks and excludes account balance checks and order placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on installing and invoking the external global npm package @pionex/pionex-ai-kit. <br>
Mitigation: Install only if comfortable with that package and run it in an environment appropriate for global npm CLI execution. <br>


## Reference(s): <br>
- [Pionex API Docs](https://pionex-doc.gitbook.io/apidocs/) <br>
- [Pionex](https://www.pionex.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/pibrandon/pionex-market) <br>
- [Publisher Profile](https://clawhub.ai/user/pibrandon) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples and read-only CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public market-data retrieval guidance; the skill states no API credentials are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter metadata says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
