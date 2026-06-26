## Description: <br>
Collects AI news, validates stage1 JSON, publishes KeplerJAI bulletins, and generates a final summary for an agent workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renjicode](https://clawhub.ai/user/renjicode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing KeplerJAI bulletin workflows use this skill to collect AI-news candidates, validate structured JSON, publish seven bulletins through the KeplerJAI API, and produce a final review message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create live KeplerJAI website posts using account credentials without a clear confirmation gate. <br>
Mitigation: Install only for controlled KeplerJAI accounts, prefer a scoped API token, review payloads before live posting, and enable cron only when recurring autonomous publication is intended. <br>
Risk: The workflow requires sensitive credentials for KeplerJAI publication. <br>
Mitigation: Provide credentials through environment variables, avoid storing tokens in skill files, and prefer scoped API tokens over cookies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/renjicode/keplerjai-bulletin-publish) <br>
- [Publisher profile](https://clawhub.ai/user/renjicode) <br>
- [README](artifact/README.md) <br>
- [Cron setup](artifact/CRON_SETUP.md) <br>
- [NewsNow AI feed](https://www.newsnow.co.uk/h/Science/AI?type=ln) <br>
- [KeplerJAI bulletin API](https://www.keplerjai.com/api/content/bulletin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text summaries, JSON files, and markdown or shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes workspace artifacts such as stage1-output.txt, stage1-output.normalized.json, publish-result.json, final-message.txt, and pipeline.log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
