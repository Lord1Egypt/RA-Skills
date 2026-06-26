## Description: <br>
Local A-share analysis with Markdown/JSON reports, optional Feishu notifications, and optional iFinD enhancement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etherstrings](https://clawhub.ai/user/etherstrings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run local JusticePlutus A-share stock analysis for one or more six-digit stock codes, producing structured Markdown and JSON reports. Optional modes add notifications, dry-run data checks, and iFinD financial enhancement when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper runs local JusticePlutus code and may use LLM, market-data, iFinD, and notification credentials. <br>
Mitigation: Install only when the local code is trusted and provide only the credentials needed for the selected run mode. <br>
Risk: Notification mode can send report contents to configured external channels such as Feishu or Telegram. <br>
Mitigation: Enable --notify only after confirming the destination channel is appropriate for the report contents. <br>


## Reference(s): <br>
- [JusticePlutus Skill Overview](artifact/references/overview.md) <br>
- [ClawHub skill page](https://clawhub.ai/etherstrings/justice-plutus) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON report files with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes per-stock reports, summary reports, and run metadata under reports/YYYY-MM-DD/.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
