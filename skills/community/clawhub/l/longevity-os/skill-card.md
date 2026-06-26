## Description: <br>
Meta-skill for the Longevity OS bundle that routes natural language health conversations to the right capability, including nutrition logging, health profile updates, pattern discovery, experiments, news, and daily coaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madeyexz](https://clawhub.ai/user/madeyexz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, understand, and route natural language personal health requests across a local-first health companion bundle. It helps direct meal logging, Apple Health profile updates, health and longevity news, self-experimentation, and daily coaching workflows to the appropriate sub-skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to install external code and update OpenClaw skill loading paths. <br>
Mitigation: Review the linked repository, sub-skill definitions, and scripts/install_bundle.py before installation; pin a trusted commit and confirm changes to ~/.openclaw/openclaw.json. <br>
Risk: The bundle can store sensitive personal health, nutrition, Apple Health, experiment, and coaching data locally. <br>
Mitigation: Review where longevityOS-data is created and maintained, protect the directory according to local privacy requirements, and back it up before uninstalling or deleting the bundle. <br>
Risk: Optional cron templates can send proactive health, news, and coaching messages. <br>
Mitigation: Enable cron jobs only intentionally after reviewing the templates and replacing placeholder Telegram chat identifiers. <br>


## Reference(s): <br>
- [Longevity OS ClawHub Listing](https://clawhub.ai/madeyexz/longevity-os) <br>
- [madeyexz Publisher Profile](https://clawhub.ai/user/madeyexz) <br>
- [Longevity OS Repository README](https://github.com/compound-life-ai/longClaw/blob/main/README.md) <br>
- [Longevity OS Skills Directory](https://github.com/compound-life-ai/longClaw/tree/main/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown responses with inline shell commands, configuration steps, and repository links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes user intent to sub-skills and may summarize installation, verification, cron setup, uninstall, and health-bundle workflows.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
