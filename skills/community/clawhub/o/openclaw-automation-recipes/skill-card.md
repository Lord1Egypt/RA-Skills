## Description: <br>
OpenClaw automation recipe pack with 10 practical automation scenarios for productivity users and automation beginners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and automation builders use this skill as a recipe pack for scheduled news summaries, email replies, issue monitoring, price alerts, meeting reminders, content publishing, backups, social monitoring, and task planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipes for email replies and public content publishing could send outbound messages without enough review. <br>
Mitigation: Use draft mode or explicit human approval before enabling email replies or public posts. <br>
Risk: The backup recipe targets local OpenClaw data and an S3 bucket, which could expose sensitive data if access controls are weak. <br>
Mitigation: Limit backup sources, use least-privilege bucket permissions, enable encryption, and define retention before deployment. <br>
Risk: Persistent scheduled automations may continue running after they are no longer appropriate. <br>
Mitigation: Periodically audit ~/.openclaw/automations/ and disable tasks that are stale or no longer approved. <br>
Risk: Social monitoring recipes may store brand mentions or sentiment data without clear retention rules. <br>
Mitigation: Define data minimization, storage, and retention rules before saving social monitoring results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/openclaw-automation-recipes) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yang1002378395-cmyk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes editable automation recipes; users must customize endpoints, schedules, destinations, and access controls before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter and skill.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
