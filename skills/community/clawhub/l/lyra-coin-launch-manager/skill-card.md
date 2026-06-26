## Description: <br>
Coin launch memory and verification workflow for Clawnch (4claw/Moltx/Moltbook) that helps agents record canonical receipts, update local launch state, and save monitoring links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and launch operators use this skill to manage Clawnch token launches by requiring canonical Clawnch receipts, normalizing launch records, verifying indexing signals, and bookmarking monitoring links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill assists public token-launch operations and could trigger or support an unintended launch if used without a final approval gate. <br>
Mitigation: Require explicit final approval before any !clawnch post, and inspect the target wallet, symbol, metadata, and trigger surface before posting. <br>
Risk: Monitoring and bookmark workflows can persist local state or bookmarks beyond the immediate launch task. <br>
Mitigation: Enable cron and bookmark steps only deliberately, scope output paths before execution, and review generated receipt, verification, and bookmark files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DeepSeekOracle/lyra-coin-launch-manager) <br>
- [Cron Template - STARCORE family monitor](references/cron_template_starcore_family.md) <br>
- [Clawnch Launches API](https://clawn.ch/api/launches) <br>
- [Clanker](https://clanker.world/) <br>
- [Base Blockscout](https://base.blockscout.com/) <br>
- [Dexscreener Search API](https://api.dexscreener.com/latest/dex/search/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON receipt files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local receipt summaries, verification reports, bookmark entries, and monitoring logs when the bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
