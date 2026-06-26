## Description: <br>
Free basic version that drafts a structured GitHub issue response and triage checklist. Reserves premium upgrade hooks for multilingual replies and fix-draft generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingogx](https://clawhub.ai/user/wingogx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to draft an initial GitHub issue reply, suggest a basic issue label, and produce a short triage checklist from an issue title and body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft replies or triage labels may be incorrect, incomplete, or unsuitable for posting as-is. <br>
Mitigation: Review and edit generated replies, labels, and checklist items before posting them to GitHub. <br>
Risk: The skill exposes an external SkillPay upgrade link and includes user_id in payment URLs. <br>
Mitigation: Use the payment flow only when the publisher is trusted, and avoid sensitive or stable personal identifiers as user_id. <br>


## Reference(s): <br>
- [SkillPay API Contract](references/skillpay-api-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON containing a draft reply, suggested label, triage checklist, issue context preview, and upgrade information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free tier returns a basic reply and checklist; premium features are advertised as reserved upgrade hooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
