## Description: <br>
Lingqu Banner Config orchestrates Lingqu discovery-page banner reservations, material intake, schedule comparison, exception handling, tracking-sheet updates, and handoffs for backend promotion changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudmusiccio](https://clawhub.ai/user/cloudmusiccio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal operations employees and campaign PMs use this skill to coordinate Lingqu discovery-page banner campaign reservations, material collection, schedule reconciliation, cancellation and material-change handling, and handoff packets for backend promotion tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive shared campaign state changes and delegate backend promotion changes from chat-triggered inputs. <br>
Mitigation: Install only in a controlled internal workspace, restrict who may trigger schedule, cancellation, and material-change flows, and require explicit project confirmation before backend-changing actions. <br>
Risk: Incorrect material, schedule, or routing decisions could affect promotion records or approval state. <br>
Mitigation: Use the tracking sheet as the source of truth, require confirmation for ambiguous matches and configuration fields, delegate backend writes to the designated promotion skill, and perform post-action detail checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudmusiccio/skills/lingqu-banner-config) <br>
- [config-matrix.md](artifact/references/config-matrix.md) <br>
- [hard-rules.md](artifact/references/hard-rules.md) <br>
- [phase-one-reserve.md](artifact/references/phase-one-reserve.md) <br>
- [phase-two-material.md](artifact/references/phase-two-material.md) <br>
- [phase-three-config.md](artifact/references/phase-three-config.md) <br>
- [phase-three-exceptions.md](artifact/references/phase-three-exceptions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown workflow responses, handoff packets, and tracking-sheet field updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured handoff details for promotion-apply-skills; backend writes are delegated and require confirmation and post-action checks.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence; artifact metadata: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
