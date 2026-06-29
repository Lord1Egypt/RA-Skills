## Description: <br>
SuperSaaS lets agents read SuperSaaS scheduling data through the OOMOL oo CLI using a connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SuperSaaS users use this skill to let an agent inspect schedules, appointments, slots, recent booking changes, resources, services, groups, SuperForms, and available fields from a connected SuperSaaS account. It is intended for read-only scheduling and discovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Read operations can expose appointment, schedule, and account data from the connected SuperSaaS account. <br>
Mitigation: Use the skill only when SuperSaaS access is intended, and review requested actions, payloads, and returned data before sharing results. <br>
Risk: Future connector actions tagged as write or destructive could change or remove SuperSaaS data. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before running any write action, and require explicit approval for destructive actions. <br>
Risk: Setup, connection, or billing fallback commands can initiate account or payment-related flows. <br>
Mitigation: Run setup, login, connection, or billing steps only after a connector command fails for the matching reason. <br>


## Reference(s): <br>
- [ClawHub SuperSaaS listing](https://clawhub.ai/oomol/oo-super-saas) <br>
- [SuperSaaS homepage](https://www.supersaas.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands, JSON payloads, and JSON connector results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only connector actions; fetch the live action schema before constructing payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
