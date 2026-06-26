## Description: <br>
微信公众号文章订阅 — 每天 9 点，盯梢竞对、同类、关注账号，一份你订阅的公众号文章推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track subscribed WeChat public accounts, fetch article metadata, and generate terminal or HTML daily reports for competitor monitoring, industry tracking, and content follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key, and persistent configuration or scheduler files may expose that key if file permissions are weak. <br>
Mitigation: Prefer REDFOX_API_KEY from the environment or a securely permissioned config file, and rotate the API key if the config or scheduler file may have been exposed. <br>
Risk: The optional daily scheduler changes local OS scheduling and can continue running after setup. <br>
Mitigation: Enable --subscribe only when daily automation is intended, use --unsubscribe to remove it, and inspect LaunchAgent or crontab entries during review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/gzh-subscribe) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, HTML, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, terminal tables, JSON configuration files, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RedFox API key via REDFOX_API_KEY, --api-key, or ~/.qoder/apis/redfox.json; can create a daily 09:00 scheduler when --subscribe is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
