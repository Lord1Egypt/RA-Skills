## Description: <br>
Curates weekly music album picks with search, scoring, deduplication, Notion writing, and push delivery to configured messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romanticmysterylh](https://clawhub.ai/user/romanticmysterylh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a weekly music recommendation workflow that finds recent albums, verifies scores, avoids duplicate recommendations, writes records to Notion, and sends the resulting picks to a configured delivery channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Notion integration key and can write music records to the configured Notion database. <br>
Mitigation: Use a dedicated Notion integration shared only with the intended page or database, keep the configuration file private, and avoid passing the key on the command line. <br>
Risk: Scheduled runs can send recommendations to the configured messaging channel or recipient. <br>
Mitigation: Double-check delivery channel and target values before enabling cron or other unattended execution. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Configuration Template](references/config-template.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/romanticmysterylh/music-weekly) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and Python helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration and history files, write music records to the configured Notion database, and send recommendation messages to the configured delivery target when the included scripts are run.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
