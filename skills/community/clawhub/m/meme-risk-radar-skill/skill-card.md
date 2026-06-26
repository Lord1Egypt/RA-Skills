## Description: <br>
Bilingual meme token risk radar for Binance Web3 data that scans newly launched or fast-rising meme tokens from Meme Rush, enriches them with token audit and token info, produces normalized risk reports in Chinese or English, and supports SkillPay billing hooks for paid scan and audit calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2663629531](https://clawhub.ai/user/2663629531) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External traders, researchers, alpha communities, and content operators use this skill to turn Binance Web3 meme token discovery data into bilingual, risk-ranked shortlists for further research. The skill is a read-only risk-filtering workflow and does not execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan and audit commands can contact Binance Web3 and SkillPay, including paid SkillPay calls. <br>
Mitigation: Use noop billing for testing, confirm required SkillPay environment variables before paid use, and run only in an environment where Binance Web3 and SkillPay network access is acceptable. <br>
Risk: Billing URL and API-key environment variables can affect paid calls. <br>
Mitigation: Set billing URL and API-key variables only in trusted environments and avoid hard-coding secrets. <br>
Risk: Risk scores are point-in-time screening signals and may be misleading if treated as investment advice. <br>
Mitigation: Use the output for risk triage and further research only; do not treat LOW risk as safe or as a trading recommendation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/2663629531/meme-risk-radar-skill) <br>
- [ClawHub Listing Copy](artifact/references/clawhub_listing.md) <br>
- [Binance Web3](https://web3.binance.com) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-style structured risk reports with bilingual Chinese or English text and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes token risk scores, risk levels, visible risk signals, metrics, audit enrichment, links, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, CHANGELOG.md, VERSION.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
