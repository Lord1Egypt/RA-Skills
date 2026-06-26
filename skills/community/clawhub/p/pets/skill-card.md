## Description: <br>
Track and care for your pets with profiles, routines, behavior logging, training progress, and creative projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill as a local pet journal for profiles, routines, training progress, behavior logs, reports, and creative pet projects. It helps organize pet care information and surface patterns while keeping medical diagnosis and breed-selection advice out of scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet profiles, care notes, photos, sitter instructions, or lost-pet materials may include sensitive contact, address, medical, or travel details. <br>
Mitigation: Store only necessary information in ~/pets/, avoid sensitive details where possible, and review generated shareable materials before distributing them. <br>
Risk: Recurring reminder setup may create cron jobs that persist after the original care need changes. <br>
Mitigation: Require explicit user confirmation before creating reminders and tell the user what was scheduled and how to remove it. <br>
Risk: Behavior and health logs could be mistaken for professional veterinary diagnosis or treatment advice. <br>
Mitigation: Keep responses limited to logging, pattern spotting, and care organization, and direct symptoms, diagnoses, treatments, sudden behavior changes, or serious concerns to a veterinarian or certified behavior professional. <br>


## Reference(s): <br>
- [Pets Skill Page](https://clawhub.ai/ivangdavila/pets) <br>
- [Behavior Tracking Patterns](artifact/behavior.md) <br>
- [Report Generation](artifact/reports.md) <br>
- [Routines and Reminders](artifact/routines.md) <br>
- [Training Methods by Species](artifact/training.md) <br>
- [Creative Projects](artifact/creative.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown summaries and reports, JSONL pet log entries, and plain-text care guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to local files under ~/pets/ and may propose reminder schedules for user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
