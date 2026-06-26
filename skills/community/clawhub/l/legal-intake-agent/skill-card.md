## Description: <br>
Ultra-high-ticket intake agent for Law Firms. Qualifies leads, performs preliminary conflict-of-interest checks, and books consultations. Hardened with ThumbGate to prevent illegal legal advice or unauthorized practice of law (UPL). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Law-firm staff and intake teams use this skill to screen potential clients, perform preliminary conflict checks, qualify leads, and book consultations while applying guardrails against unauthorized legal advice and outcome promises. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive legal intake, adverse-party, and conflict-list data may be routed through third-party tools without enough privacy, access-control, or retention guidance. <br>
Mitigation: Use only approved vendors, restrict Google Sheet sharing, minimize synced fields, configure least-privilege service accounts, define retention and audit logging, and obtain legal and compliance review before deployment. <br>
Risk: The agent may be used in legal intake workflows where unauthorized legal advice, outcome promises, missed conflicts, or expired limitation periods could create professional risk. <br>
Mitigation: Keep ThumbGate rules enabled for UPL prevention, outcome liability blocking, conflict routing, statute-of-limitations checks, jurisdiction checks, and human review by qualified legal staff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/legal-intake-agent) <br>
- [Publisher profile](https://clawhub.ai/user/igorganapolsky) <br>
- [Setup guide](artifact/setup-guide.md) <br>
- [ThumbGate prevention rules](artifact/thumbgate-rules.md) <br>
- [Make.com](https://make.com) <br>
- [ElevenLabs](https://elevenlabs.io/affiliates) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with setup steps, rules, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external CRM, voice, automation, and spreadsheet tools selected by the deploying law firm.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
