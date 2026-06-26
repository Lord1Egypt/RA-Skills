## Description: <br>
Participant MoltBot for allocation proposal, validation, and submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wiimdy](https://clawhub.ai/user/wiimdy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure and operate an OpenFunderse participant bot that proposes, validates, and optionally submits AllocationClaimV1 records for fund epochs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests participant wallet-key authority and can submit blockchain or vault actions. <br>
Mitigation: Use a dedicated low-balance participant wallet, never reuse treasury or admin keys, and keep explicit-submit required. <br>
Risk: Auto-submit and relayer settings can enable unintended network transmission of financial actions. <br>
Mitigation: Leave auto-submit disabled unless intentional, restrict trusted relayer hosts, and avoid HTTP relayers outside local testing. <br>
Risk: Install and bot initialization can mutate global OpenClaw runtime configuration and restart the gateway. <br>
Mitigation: Review the npm package before running it, back up OpenClaw configuration first, and use no-sync or no-restart options when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wiimdy/openfunderse-strategy) <br>
- [Publisher profile](https://clawhub.ai/user/wiimdy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment settings, Telegram command examples, and JSON task contracts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces AllocationClaimV1-oriented guidance and submission instructions; network submission is gated by explicit submit and auto-submit settings.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
