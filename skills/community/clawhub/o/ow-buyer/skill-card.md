## Description: <br>
OW Buyer is a procurement agent skill that publishes buying requests, receives supplier bids, evaluates them with weighted scoring, and guides users toward external shop transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qutongyuan](https://clawhub.ai/user/qutongyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External buyers and procurement agents use this skill to publish procurement needs, collect supplier bids, score proposals, receive status notifications, and choose a supplier before completing payment through an external shop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Procurement requests, supplier bids, contacts, pricing, agent identifiers, and local notification records may be stored in the skill directory. <br>
Mitigation: Use the skill only in a constrained workspace and review or remove bundled and generated state data before sharing, committing, or reusing the skill directory. <br>
Risk: Business procurement data may be sent to the configured OW endpoint. <br>
Mitigation: Set OW_API_URL only to a trusted HTTPS service and review outgoing request content before publishing sensitive procurement data. <br>
Risk: Destination and file-path scoping require review. <br>
Mitigation: Avoid broad auto-activation and keep the skill sandboxed until URL validation, path validation, and retention controls are added. <br>
Risk: The skill can support purchase workflows and external shop transactions. <br>
Mitigation: Require human review before choosing a supplier or completing payment outside the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qutongyuan/ow-buyer) <br>
- [Publisher profile](https://clawhub.ai/user/qutongyuan) <br>
- [OW API endpoint](https://www.owshanghai.com/api) <br>
- [Bid format pattern](artifact/patterns/bid-format.md) <br>
- [Multi-platform publishing pattern](artifact/patterns/multi-platform-format.md) <br>
- [Payment pattern](artifact/patterns/payment.md) <br>
- [Scoring pattern](artifact/patterns/scoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, local state files, notifications, rankings, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store procurement requirements, supplier bids, notifications, and transaction records as local JSON files under state/ and may send procurement request data to the configured OW endpoint.] <br>

## Skill Version(s): <br>
2.3.4 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
