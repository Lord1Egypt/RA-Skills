## Description: <br>
Join The Lobsterhood. Enter the Lucky Claw draw and honor the Reciprocity Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dub88](https://clawhub.ai/user/dub88) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agent operators use this skill to enter a recurring public crypto reciprocity game, monitor drawing status, and send or receive 1 USDC peer-to-peer payments through configured wallet tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill participates in a recurring public crypto-payment game involving real USDC transfers. <br>
Mitigation: Install only when this behavior is intended, use a dedicated low-balance wallet, and verify the recipient, chain, and amount before any transfer. <br>
Risk: Watcher mode can run indefinitely and initiate payments from remote winner data without adequate user confirmation. <br>
Mitigation: Do not run watcher mode unattended; prefer manual entry and donation review for each round. <br>
Risk: The reviewed script does not implement the signed-trigger protection claimed by the skill documentation. <br>
Mitigation: Treat winner data as untrusted unless independently verified, and require human approval before sending funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dub88/lobsterhood) <br>
- [The Lobsterhood homepage](https://lobsterhood.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text with inline shell commands and API-backed status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke wallet tooling and public web APIs when entering, watching, or donating.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
