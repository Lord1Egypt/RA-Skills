## Description: <br>
Use when a DevOps or SRE team needs to write a blameless postmortem after a production incident. Guides timeline reconstruction, root cause analysis, and produces a complete postmortem document with prioritized action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident response teams use this skill to facilitate a blameless post-incident review and produce a shareable postmortem with timeline, impact, root cause, and action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident details may include credentials, customer PII, tokens, raw IP addresses, or confidential operational data. <br>
Mitigation: Prompt users to redact sensitive data before sharing logs or timelines, and omit secrets or customer identifiers from the generated postmortem. <br>
Risk: Regulatory, security, or legal implications may be mischaracterized if the postmortem is treated as authoritative advice. <br>
Mitigation: Flag potential obligations without making definitive legal claims, and recommend security or legal review for P0, security, compliance, or externally shared incidents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/incident-postmortem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational guidance and Markdown postmortem document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a draft postmortem with impact metrics, timeline, root cause, contributing factors, and prioritized action items.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
