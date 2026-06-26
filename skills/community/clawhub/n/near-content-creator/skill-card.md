## Description: <br>
Generate NEAR-focused content (threads, market updates, ecosystem news, tutorials). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mastrophot](https://clawhub.ai/user/mastrophot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, ecosystem teams, and developers use this skill to draft NEAR educational threads, daily market updates, curated news digests, and practical tutorials for review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market updates and news digests depend on third-party public data sources that may be unavailable, incomplete, stale, or unsuitable for publication without review. <br>
Mitigation: Review generated market and news content before publishing or relying on it, and check the included data-quality or source details. <br>
Risk: Generated market commentary could be mistaken for financial advice. <br>
Mitigation: Keep the informational disclaimer in published market updates and have a qualified reviewer approve externally shared content. <br>
Risk: Installing from an unexpected package source could introduce unreviewed code or dependency changes. <br>
Mitigation: Install from the expected source and use the provided lockfile when building or testing the skill. <br>


## Reference(s): <br>
- [NEAR Content Creator repository](https://github.com/mastrophot/near-content-creator) <br>
- [NEAR Blog](https://near.org/blog) <br>
- [NEAR Foundation](https://near.foundation) <br>
- [nearcore releases](https://github.com/near/nearcore/releases) <br>
- [near-api-js releases](https://github.com/near/near-api-js/releases) <br>
- [CoinGecko NEAR market data endpoint](https://api.coingecko.com/api/v3/simple/price?ids=near&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Plain text, string arrays, structured news items, and Markdown tutorials with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Thread output is normalized to eight posts, news is deduplicated and ranked, and market updates include a data-quality line.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
