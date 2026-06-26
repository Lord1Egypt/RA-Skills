## Description: <br>
Converts user-provided images into validated, decision-ready action drafts for events, meal macros, places, products, receipts, documents, and civic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use Look to turn photos of real-world objects, documents, receipts, signs, meals, places, and flyers into one to three action drafts for review and confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes potentially sensitive images and writes journals and extracted entity signals. <br>
Mitigation: Install only where this data handling is acceptable, review retention settings, and confirm sensitive actions before execution. <br>
Risk: The skill registers a daily self-update job that can replace its own code without explicit per-update approval or integrity checks. <br>
Mitigation: Disable or remove the cron update and use manual, reviewed updates pinned to trusted releases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/indigokarasu/ocas-look) <br>
- [Command reference](references/command_reference.md) <br>
- [Decision policy](references/decision_policy.md) <br>
- [Domain playbooks](references/domain_playbooks.md) <br>
- [Schemas](references/schemas.md) <br>
- [Storage and config](references/storage_and_config.md) <br>
- [Journal](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like action drafts, decision records, journals, and execution receipts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft-first outputs and requires explicit confirmation before high-risk execution.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
