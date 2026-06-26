## Description: <br>
Intelligent model routing for sub-agent task delegation that chooses models based on task complexity, cost, and capability requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicocabrerac](https://clawhub.ai/user/nicocabrerac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to classify tasks, choose cost-appropriate models for sub-agent and cron execution, validate model assignments, and maintain model availability data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can persistently change standing agent instructions by adding router policy to AGENTS.md. <br>
Mitigation: Review the AGENTS.md block before applying it and back up AGENTS.md and config.json before installation. <br>
Risk: Live model discovery can use configured provider credentials and may create paid API calls. <br>
Mitigation: Run discovery with --no-live unless live provider probing and any associated cost are acceptable. <br>
Risk: The hourly model discovery cron can perform ongoing model probing. <br>
Mitigation: Enable the cron only when continuous model availability checks are desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nicocabrerac/intelligent-router-openclaw) <br>
- [Package README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown guidance, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit model recommendations, task tiers, validation results, cost estimates, health checks, and configuration update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
