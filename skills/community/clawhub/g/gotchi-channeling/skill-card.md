## Description: <br>
Channel Aavegotchis on Base via Bankr. Checks cooldown, builds calldata, and submits channel txs safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Aavegotchi users and developers use this skill to check channeling cooldowns and submit configured Alchemica channeling transactions for Base mainnet parcels through Bankr. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real wallet transactions on Base mainnet through Bankr. <br>
Mitigation: Review each configured gotchi and parcel, test manually first, and use a dedicated Bankr API key where possible. <br>
Risk: The shipped config contains live-looking parcel and gotchi IDs. <br>
Mitigation: Replace config.json with your own verified targets before running channel.sh, channel-all.sh, or cron automation. <br>
Risk: Incorrect parcel or gotchi choices can spend cooldowns or route rewards unexpectedly. <br>
Mitigation: Verify parcel ownership, gotchi permission, Aaltar presence, and expected reward recipient before enabling recurring channeling. <br>
Risk: Documentation claims strong safety properties while the security scan flags overstated safety documentation. <br>
Mitigation: Treat the scripts as transaction automation, not a guarantee of safe outcomes, and review transaction details before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaigotchi/gotchi-channeling) <br>
- [Function search notes](references/FUNCTION_SEARCH.md) <br>
- [Function signature notes](references/FUNCTION_SIGNATURE.md) <br>
- [Aavegotchi REALM diamond repository](https://github.com/aavegotchi/aavegotchi-realm-diamond) <br>
- [Bankr transaction submit API](https://api.bankr.bot/agent/submit) <br>
- [Base mainnet RPC](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit real Base mainnet transactions through Bankr when run with a valid BANKR_API_KEY.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
