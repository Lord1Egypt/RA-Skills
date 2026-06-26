## Description: <br>
Triggers on Apple Watch pool-swim workout screenshots or swim-related image messages, extracts distance, pace, heart-rate, and stroke data, stores records locally, and summarizes trends and training suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zygzzp](https://clawhub.ai/user/zygzzp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert Apple Watch pool-swim screenshots into structured swim-training records, local workout history, and short trend reports for personal training review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles health-related fitness data and includes bundled workout records. <br>
Mitigation: Clear bundled sample data before use and review where local swim history is stored. <br>
Risk: Same-day workout records can be overwritten when screenshots are reprocessed. <br>
Mitigation: Require explicit user confirmation before saving or replacing an existing date's record. <br>
Risk: The skill trigger is broad for swim-related messages with images. <br>
Mitigation: Confirm the image is an Apple Watch pool-swim workout screenshot before extracting or storing data. <br>


## Reference(s): <br>
- [Swimming Training Data Schema](references/data_schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zygzzp/iwatch-swim-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report with JSON data passed to local Python scripts and JSON workout records saved on disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores per-date swim records under swim_data/YYYY/MM and can overwrite same-day records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
