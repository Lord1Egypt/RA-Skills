## Description: <br>
Build an atomic Polymarket combo (parlay) by selecting 2+ binary market legs, getting live combined odds over RFQ, and optionally placing the whole combo as one signed Polymarket order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to construct and review multi-leg Polymarket combo trades, browse eligible legs, create the combo configuration, dry-run the plan, and place a live order only when intentionally requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live use involves wallet credentials and real-money Polymarket orders. <br>
Mitigation: Run dry-run first, verify every leg and stake, and use --live only for trades the user explicitly intends to place. <br>
Risk: A combo loses the entire stake if any single leg loses. <br>
Mitigation: Confirm each leg's exact resolution condition and the total-loss exposure before live placement. <br>
Risk: The skill depends on a Simmer API key and, for live trading, a local Polymarket wallet private key. <br>
Mitigation: Install only when comfortable providing those credentials, keep the wallet key local, and consider pinning or reviewing dependencies before using meaningful funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-combo-builder) <br>
- [DISCLAIMER.md](artifact/DISCLAIMER.md) <br>
- [combo_config.example.json](artifact/combo_config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and command output from dry-run, leg browsing, activation, or live placement.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live placement requires an explicit --live flag, a Simmer API key, and wallet configuration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
