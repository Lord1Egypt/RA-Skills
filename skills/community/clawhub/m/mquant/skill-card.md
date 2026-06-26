## Description: <br>
Matic MQuant strategy development assistant that generates Python strategy code for the Matic-MQuant platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chouchounii](https://clawhub.ai/user/chouchounii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Matic MQuant traders use this skill to generate runnable Python strategy code, logs, and deployment-oriented guidance for the Matic-MQuant platform. Generated strategies should be reviewed and tested in a simulation or test account before any live trading use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategies can guide live trading decisions and order placement. <br>
Mitigation: Review generated code, parameters, and risk controls, then test in a simulation or test account before live use. <br>
Risk: Version-retention behavior and generated workflows may delete local strategy files. <br>
Mitigation: Require explicit confirmation before file deletion and keep backups of strategy files and logs. <br>
Risk: CSV exports and logs may contain account or trading data. <br>
Mitigation: Protect generated files, avoid committing sensitive exports, and disable or restrict local data persistence when not needed. <br>
Risk: Bundled example strategies may not match the user's production risk controls. <br>
Mitigation: Treat examples as reference material and adapt them with user-specific validation before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chouchounii/mquant) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [API reference](artifact/reference/API_REFERENCE.md) <br>
- [Log format](artifact/reference/LOG_FORMAT.md) <br>
- [Trading rules](artifact/TRADING_RULES.md) <br>
- [Common errors](artifact/COMMON_ERRORS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python code blocks and optional saved .py and .log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code targets Matic-MQuant strategy files and includes logging and basic error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
