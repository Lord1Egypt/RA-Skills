## Description: <br>
Equip, unequip, and inspect Aavegotchi wearables on Base via Bankr submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to inspect and modify Aavegotchi wearable loadouts on Base mainnet through Bankr-backed transaction submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Equip and unequip commands can change on-chain Aavegotchi wearable state through Bankr-backed transactions. <br>
Mitigation: Review the gotchi ID, slot names, wearable IDs, and unequip-all intent before submitting a transaction. <br>
Risk: The skill requires access to a Bankr API key. <br>
Mitigation: Install only when comfortable allowing the skill to use BANKR_API_KEY for transaction submission, and keep the key scoped and stored according to local credential practices. <br>


## Reference(s): <br>
- [Gotchi Equip on ClawHub](https://clawhub.ai/aaigotchi/gotchi-equip) <br>
- [Gotchi Equip publisher profile](https://clawhub.ai/user/aaigotchi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Shell commands and JSON transaction submission responses with concise terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, jq, curl, and BANKR_API_KEY; equip and unequip operations can submit on-chain wearable state changes.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
