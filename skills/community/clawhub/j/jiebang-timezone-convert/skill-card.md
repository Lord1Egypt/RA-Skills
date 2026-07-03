## Description: <br>
捷帮时区转换 helps agents query current times and convert times across global time zones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebang-tools](https://clawhub.ai/user/jiebang-tools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query world-clock times, convert times between IANA time zones, compare offsets, and plan meetings across time zones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timezone inputs are sent to an external service for processing. <br>
Mitigation: Use only with timezone and meeting-time inputs that are appropriate to share with jiebang.site, and avoid including sensitive context in requests. <br>
Risk: The skill requires an admin-style API key for the external service. <br>
Mitigation: Provide credentials only in controlled runtimes, rotate them if exposed, and prefer a future version with a narrowly scoped API token. <br>
Risk: The security scan verdict is suspicious because the external domain and data handling are not fully disclosed in the skill documentation. <br>
Mitigation: Review the service dependency and disclosure before deployment, or prefer an implementation based on local timezone libraries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiebang-tools/jiebang-timezone-convert) <br>
- [Jiebang API site](https://www.jiebang.site) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON results with converted time or timezone information, plus concise natural-language guidance when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the external jiebang.site API for timezone conversion and timezone lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
