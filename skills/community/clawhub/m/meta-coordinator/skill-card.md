## Description: <br>
CS Coordinator agent turns customer support and operations input into structured triage records with conservative severity routing, owner suggestions, no-response follow-up guidance, and tracker or log-based case updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yonghyeokrhee](https://clawhub.ai/user/yonghyeokrhee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support, operations, and engineering teams use this skill to convert customer-reported incidents, billing or entitlement issues, permission problems, and loose CS notes into durable issue records, owner recommendations, next actions, and follow-up updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Case records may include customer identifiers, payment or order references, and billing-adjacent support details. <br>
Mitigation: Use approved issue trackers or controlled log locations, redact identifiers where possible, avoid full payment details and secrets, and apply organizational retention and access-control rules. <br>
Risk: Incorrect triage or premature resolution could misroute active customer-impacting incidents. <br>
Mitigation: Keep facts, guesses, and missing information separate; use conservative severity; and move cases to RESOLVED only after explicit recovery confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yonghyeokrhee/meta-coordinator) <br>
- [Korean demo script](references/demo-script-ko.md) <br>
- [Tracker workflow mapping](references/tracker-workflow.md) <br>
- [Log-only workflow](references/log-only-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with structured issue skeletons, triage sections, owner suggestions, status moves, and optional JSONL log shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance and record templates; it does not perform tracker writes or payment actions by itself.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
