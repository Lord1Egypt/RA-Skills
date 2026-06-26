## Description: <br>
Create public Gougoubi prediction proposals from minimal input with deterministic enrichment, group creation, approval handling, and transaction submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to publish a new Gougoubi public prediction market from a market name and deadline, with generated rules, tags, group creation, approval handling, and proposal submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet approval and transaction submission from minimal user input. <br>
Mitigation: Require a full user preview and explicit confirmation of generated rules, tags, language, stake amount, approval spender, chain, and transaction parameters before approval or submission. <br>
Risk: The skill publishes public crypto prediction markets, where generated content may be incorrect, misleading, or moderation-sensitive. <br>
Mitigation: Review the generated market details and require confirmation when moderation risk is detected before creating the group or proposal. <br>
Risk: The artifact references a local helper script for creation flows that is not included in the release package. <br>
Mitigation: Inspect and dry-run any referenced local script separately before allowing an agent to execute it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-create-prediction) <br>
- [Gougoubi public prediction creation page](https://gougoubi.ai/premarket/proposals/create/public) <br>


## Skill Output: <br>
**Output Type(s):** [Structured JSON, Guidance] <br>
**Output Format:** [JSON success or failure object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes transaction hash, proposal address when available, normalized input, stage-specific errors, retryability, and warnings.] <br>

## Skill Version(s): <br>
1.0.3 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
