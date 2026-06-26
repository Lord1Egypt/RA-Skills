## Description: <br>
Plant Doctor helps agents identify plants, diagnose plant health issues, provide care advice, manage watering schedules, and flag pet or child toxicity risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify houseplants from photos, diagnose visible plant problems, generate care cards, calculate watering schedules, and track a local plant collection. It is also useful for plant placement recommendations that account for light conditions, user experience level, and pet or child safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist plant names, room or location details, care history, and related notes in a local plants/ folder. <br>
Mitigation: Install only in a private workspace, restrict permissions on the plants/ directory, and avoid enabling memory unless persistent plant data is desired. <br>
Risk: Plant photos can include home interiors, documents, people, or other sensitive background information. <br>
Mitigation: Review photos before sharing them with the agent and crop or retake images that include sensitive background details. <br>
Risk: The optional dashboard can move plant data, photos, schedules, and health history into remote storage. <br>
Mitigation: Use private storage, authentication, row-level security, and environment variables for credentials before deploying the dashboard. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nollio/plant-doctor) <br>
- [Publisher Profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security Guidance](artifact/SECURITY.md) <br>
- [Plant Care Templates](artifact/config/care-templates.md) <br>
- [Dashboard Companion Kit](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses, JSON plant records, and Markdown care schedules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local files under plants/ for collection records and care schedules; optional dashboard materials describe database and UI configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
