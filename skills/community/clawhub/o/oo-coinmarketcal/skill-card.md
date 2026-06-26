## Description: <br>
CoinMarketCal. Use this skill for ANY CoinMarketCal request -- searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and read CoinMarketCal coin, category, confirmed event, filtered event, and ranked event data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad trigger wording for CoinMarketCal-related requests. <br>
Mitigation: Use it only for explicit CoinMarketCal lookup requests and review proposed actions before execution. <br>
Risk: The first-time setup guidance includes a one-line pipe-to-shell installer. <br>
Mitigation: Review OOMOL's installer or use documented manual installation steps before installing the oo CLI. <br>
Risk: The skill requires an OOMOL-connected CoinMarketCal credential. <br>
Mitigation: Connect CoinMarketCal only in the intended OOMOL account and do not expose raw credentials to the agent. <br>


## Reference(s): <br>
- [CoinMarketCal skill page](https://clawhub.ai/oomol/oo-coinmarketcal) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [CoinMarketCal connection setup](https://console.oomol.com/app-connections?provider=coinmarketcal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON from the oo CLI when actions are executed with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version and SKILL.md frontmatter metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
