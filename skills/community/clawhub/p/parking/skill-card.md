## Description: <br>
Find, verify, and reserve parking worldwide with provider selection, live-signal triage, and local memory for favorite places and cities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find nearby parking, pre-book airport or event parking, compare local parking providers, and research parking APIs or market coverage. It helps an agent separate discovery, payment, and reservation workflows before recommending or handing off to a provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local parking memory may store recurring locations, vehicle constraints, favorite facilities, or provider preferences. <br>
Mitigation: Ask before creating persistent memory, offer one-off mode, and store reusable parking knowledge rather than raw payment details, credentials, or full booking receipts. <br>
Risk: Provider handoffs can send destination, timing, route context, plate number, or vehicle details to parking services. <br>
Mitigation: Require user approval before live booking, plate entry, or payment flows, and confirm the provider, destination, time window, price, cancellation terms, and data being sent. <br>
Risk: Static listings or payment apps can be mistaken for guaranteed reservations or live occupancy. <br>
Mitigation: Label each recommendation as discovery, payment, reservation, or occupancy evidence, and claim guaranteed inventory only when the provider exposes confirmed reservation status. <br>


## Reference(s): <br>
- [Parking Radar on ClawHub](https://clawhub.ai/ivangdavila/parking) <br>
- [Parking Radar Homepage](https://clawic.com/skills/parking) <br>
- [Setup - Parking Radar](artifact/setup.md) <br>
- [Execution Playbook - Parking Radar](artifact/execution-playbook.md) <br>
- [Provider Registry - Parking Radar](artifact/provider-registry.md) <br>
- [API Notes - Parking Radar](artifact/api-notes.md) <br>
- [Source Ledger - Parking Radar](artifact/source-ledger.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with provider comparisons, verification notes, setup instructions, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce provider handoff guidance and local memory update suggestions after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
