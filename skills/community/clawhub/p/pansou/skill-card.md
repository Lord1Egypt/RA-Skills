## Description: <br>
PanSou 网盘搜索 helps agents search a user-configured PanSou service for cloud-drive resources across supported providers, with filters for drive type, plugin, Telegram channel, and result keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[212-mei](https://clawhub.ai/user/212-mei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search PanSou-indexed cloud-drive resources such as media, software, and study materials from a configured PanSou endpoint. It is useful when a user asks to find net-disk resources and wants filtered, clickable result links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/212-mei/pansou) <br>
- [CLI parameter reference](references/api-params.md) <br>
- [Supported cloud-drive types](references/cloud-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON search-result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and PANSOU_URL. Search terms and optional PANSOU_USER/PANSOU_PWD credentials are sent to the configured PanSou server; prefer HTTPS, the default POST search mode, and review the local token stored at ~/.config/pansou/token.json.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
