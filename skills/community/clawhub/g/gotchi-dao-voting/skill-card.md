## Description: <br>
Check active Aavegotchi DAO proposals and vote on Snapshot via Bankr EIP-712 signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External DAO participants and agent operators use this skill to inspect active Aavegotchi Snapshot proposals, preview vote payloads, and submit votes through Bankr signing when they have voting power. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cast real Aavegotchi DAO Snapshot votes. <br>
Mitigation: Run --dry-run first, then verify the proposal ID, choice, voting power, wallet, and Snapshot endpoints before allowing a live submission. <br>
Risk: The skill can reuse Bankr credentials from broad local sources. <br>
Mitigation: Supply BANKR_API_KEY explicitly for this workflow and use only the intended Bankr credential. <br>
Risk: The bundled wallet may not be the intended voting wallet. <br>
Mitigation: Replace the configured wallet with your own and confirm it has voting power on the target proposal before submitting a vote. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aaigotchi/gotchi-dao-voting) <br>
- [Aavegotchi Snapshot space](https://snapshot.org/#/aavegotchi.eth) <br>
- [Snapshot GraphQL API endpoint](https://hub.snapshot.org/graphql) <br>
- [Snapshot sequencer endpoint](https://seq.snapshot.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON payload previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live vote submission requires curl, jq, BANKR_API_KEY, and a configured wallet and Snapshot endpoints.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
