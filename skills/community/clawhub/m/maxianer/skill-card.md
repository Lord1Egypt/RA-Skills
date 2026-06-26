## Description: <br>
中华术数推演系统（八字/紫微/六爻/梅花/奇门/称骨/铁板/解梦）。当用户提到算命/算八字/排八字/看命盘/紫微斗数/六爻/占卜/梅花易数/奇门遁甲/称骨/铁板神数/解梦/算一卦/帮我算算/看看运势/什么命/命理时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xgimiapoll-code](https://clawhub.ai/user/xgimiapoll-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect birth, event, or dream inputs, call deterministic Chinese divination engines, and produce natural-language interpretations from the returned data. It supports fate analysis, Liuyao, Meihua, Qimen, dream interpretation, engine discovery, and HTML report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive personal inputs such as birth details, birthplace, gender, name, dreams, and questions are sent to an external service. <br>
Mitigation: Use the skill only when users consent to sharing that data with the configured service, and avoid collecting identifying information unless it is necessary. <br>
Risk: The configured default API endpoint uses unencrypted HTTP transport. <br>
Mitigation: Prefer an HTTPS-only service endpoint before production use, especially when sending personal or sensitive inputs. <br>
Risk: The helper script includes a shared default bearer token. <br>
Mitigation: Configure a publisher-managed credential through MAXIANER_API_KEY and remove reliance on embedded shared credentials. <br>
Risk: Privacy, retention, and API credential handling are not explained in the evidence. <br>
Mitigation: Confirm the publisher's privacy, retention, and credential handling practices before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xgimiapoll-code/maxianer) <br>
- [Publisher profile](https://clawhub.ai/user/xgimiapoll-code) <br>
- [Server-resolved provenance](unavailable) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and natural-language interpretations; script calls return JSON or HTML depending on the endpoint.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Node.js helper script to call an external API; fate, event, dream, engines, and report endpoints are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
