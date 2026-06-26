## Description: <br>
Integrates Solana escrow contracts so agents can register PayLock profiles, create escrow payment contracts, submit delivery evidence, verify deliveries, release payments, and check trust scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add PayLock escrow payment flows to agent services, including profile registration, contract creation, delivery submission, payer verification, payment release, and trust-score lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PayLock POST requests can submit wallet or profile data and trigger crypto escrow actions. <br>
Mitigation: Require human confirmation of recipient, amount, contract ID, and wallet address before sending any POST request. <br>
Risk: Milestones and delivery URLs may expose sensitive business details. <br>
Mitigation: Keep private or sensitive details out of milestone text and delivery links unless the user has approved sharing them with PayLock. <br>
Risk: Real escrow payments depend on PayLock fee, privacy, verification, and release controls. <br>
Mitigation: Independently verify PayLock's operational controls and fee model before relying on the skill for meaningful payments. <br>


## Reference(s): <br>
- [PayLock service](https://paylock.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/paylock-solana) <br>
- [Publisher profile](https://clawhub.ai/user/1477009639zw-blip) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown with HTTP, JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration guidance and example requests; live POST requests can trigger external escrow actions.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
