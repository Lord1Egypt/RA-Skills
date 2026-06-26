## Description: <br>
Manage Hong Kong IPO user preferences and watchlists, including risk profile, default output, budget, financing preference, and tracked symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackstoic](https://clawhub.ai/user/hackstoic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to maintain personalized Hong Kong IPO profile settings and watchlists for later batch decisions. It is most useful when a workflow needs persistent risk preferences, budget settings, output preferences, financing preferences, or tracked IPO symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle includes broader HK IPO research, scoring, review, import/export, and persistence features beyond profile and watchlist management. <br>
Mitigation: Review the packaged CLI before installation and invoke only the commands needed for the intended workflow. <br>
Risk: Some packaged features can fetch third-party market data and store profile, watchlist, review, or scoring history under ~/.hkipo-next. <br>
Mitigation: Confirm data-source expectations before networked use and inspect or clear local state when handling sensitive preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hackstoic/hkipo-profile-watchlist-manager) <br>
- [hkipo-next README](runtime/hkipo-next/README.md) <br>
- [AiPO API reference](runtime/hkipo-next/references/aipo-api.md) <br>
- [HK IPO analysis guide](runtime/hkipo-next/references/analysis-guide.md) <br>
- [HK IPO API guide](runtime/hkipo-next/references/api-guide.md) <br>
- [HK IPO mechanism reference](runtime/hkipo-next/references/ipo-mechanism.md) <br>
- [Risk preferences reference](runtime/hkipo-next/references/risk-preferences.md) <br>
- [AiPO data source](https://aipo.myiqdii.com) <br>
- [AASTOCKS IPO market page](https://www.aastocks.com/tc/stocks/market/ipo/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with shell commands; CLI results may be JSON, text, or markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profile and watchlist commands store local state under ~/.hkipo-next.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, release metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
