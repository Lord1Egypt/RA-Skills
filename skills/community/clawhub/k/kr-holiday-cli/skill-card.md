## Description: <br>
Korean Holiday CLI helps agents answer Korean public holiday questions, calculate business days, convert between Korean lunar and solar dates, and render monthly calendar output without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill for Korean scheduling workflows such as payroll, delivery SLAs, billing cycles, appointment reminders, marketing sends, and date conversion tasks that must account for Korean public holidays and lunar calendar dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Holiday or business-day results can drift when dependency rules change or when ad-hoc government holiday announcements are not yet reflected upstream. <br>
Mitigation: Use a virtual environment, pin or review dependencies for reproducible installs, and update the holidays package deliberately when current statutory rules are needed. <br>
Risk: Server metadata includes crypto, purchase, and sensitive-credential capability tags that do not match the scanned code behavior. <br>
Mitigation: Treat those tags as a labeling issue and confirm or correct capability metadata before using it for policy decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/kr-holiday-cli) <br>
- [README](README.md) <br>
- [Skill usage guide](SKILL.md) <br>
- [holidays package](https://pypi.org/project/holidays/) <br>
- [korean-lunar-calendar package](https://pypi.org/project/korean-lunar-calendar/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, text] <br>
**Output Format:** [Markdown guidance with shell commands; the CLI emits compact UTF-8 JSON by default and optional text calendar output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required. Runtime depends on the holidays and korean-lunar-calendar Python packages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
