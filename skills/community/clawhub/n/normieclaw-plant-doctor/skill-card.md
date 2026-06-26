## Description: <br>
Plant Doctor helps a vision-capable agent identify plants, diagnose plant health issues, provide personalized care advice, maintain watering schedules, flag toxicity concerns, and explain propagation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and plant owners use Plant Doctor with a vision-capable agent to identify plants, diagnose common plant health issues, receive care cards and toxicity alerts, and maintain local watering schedules. The skill also provides optional guidance for a dashboard companion kit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can maintain persistent plant records in plants/ and memory entries. <br>
Mitigation: Install it only when persistent plant tracking is intended, and review or delete plants/ and related memory entries when tracking is no longer wanted. <br>
Risk: The optional dashboard can move plant schedules and photos into cloud-backed storage. <br>
Mitigation: Enable authentication and row-level security, keep Supabase credentials in environment variables, and use private storage for photos. <br>
Risk: Plant photos may include private home details or sensitive background information. <br>
Mitigation: Avoid uploading private home photos unless storage is locked down, and review images for sensitive background content before use. <br>
Risk: Vision-based plant identification and diagnosis can be uncertain, especially with blurry or incomplete photos. <br>
Mitigation: Ask for clearer photos when needed and use local nursery or specialist advice for plants that may be beyond saving or require specialized treatment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-plant-doctor) <br>
- [README](artifact/README.md) <br>
- [Security Guidance](artifact/SECURITY.md) <br>
- [Dashboard Companion Kit](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional JSON plant records, markdown care schedules, setup shell commands, and dashboard configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local plants/collection.json and plants/care-schedule.md; optional dashboard guidance describes Supabase-backed tables, widgets, authentication, and storage controls.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
