## Description:

Channel Aavegotchis on Base via Bankr by checking cooldowns, building calldata, and submitting channel transactions safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT

## Use Case:

External Aavegotchi and REALM parcel users use this skill to check channeling cooldowns and submit Bankr wallet transactions for configured gotchi and parcel pairs on Base. It supports manual single-channel use and batch channeling for configured entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended Bankr wallet transactions can be submitted, especially when batch mode or cron automation is used.

Mitigation: Use an explicit BANKR_API_KEY, test with a single pair first, add confirmation or dry-run safeguards before cron automation, and monitor submitted transaction hashes.

Risk: Incorrect parcel or gotchi configuration can cause value to accrue to an unintended parcel owner or waste a gotchi cooldown.

Mitigation: Verify every parcel and gotchi pair yourself before adding it to config.json, and only configure parcels you own or have explicit permission to use.

Risk: Under-scoped transaction settings could submit to the wrong chain or contract if configuration is changed unexpectedly.

Mitigation: Keep chainId and realmDiamond pinned to the intended Base REALM deployment and review configuration changes before running channeling scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaigotchi/skills/gotchi-channeling)
- [Function Signature Reference](references/FUNCTION_SIGNATURE.md)
- [Function Search Reference](references/FUNCTION_SEARCH.md)
- [Aavegotchi Contracts](https://wiki.aavegotchi.com/en/contracts)
- [Aavegotchi REALM Diamond Source](https://github.com/aavegotchi/aavegotchi-realm-diamond)
- [Foundry Install](https://getfoundry.sh/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [CLI text output with transaction hashes, cooldown status strings, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cast, jq, curl, and BANKR_API_KEY; submits transactions through Bankr when channeling is ready.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
