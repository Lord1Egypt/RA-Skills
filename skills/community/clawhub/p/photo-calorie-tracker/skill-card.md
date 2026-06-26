## Description: <br>
Photo Calorie Tracker recognizes food photos, logs daily calorie intake, and generates date-range calorie reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobo23456](https://clawhub.ai/user/bobo23456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to identify meal photos, estimate calories, save local daily meal records, and summarize calorie intake over requested date ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal photos and calorie history are saved in the local OpenClaw workspace. <br>
Mitigation: Review or delete /root/.openclaw/workspace/temp_qqdata/ and /root/.openclaw/workspace/memory/ when local retention is not desired. <br>
Risk: Photo-based food recognition and calorie estimates can be inaccurate. <br>
Mitigation: Treat reports as tracking aids and review estimated meal items and calories before relying on them. <br>


## Reference(s): <br>
- [Photo Calorie Tracker on ClawHub](https://clawhub.ai/bobo23456/photo-calorie-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown-style calorie reports and local daily record files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenClaw workspace paths for temporary meal photos, daily records, and target calorie configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
