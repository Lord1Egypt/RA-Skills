## Description: <br>
Call GET /api/xiaohongshu-pgy/api/pgy/kol/data/core_data/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Core Metrics through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing operations teams use this skill to retrieve Xiaohongshu Creator Marketplace creator core metrics for a supplied KOL user ID. It supports benchmarking, creator vetting, and campaign planning through the JustOneAPI endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is a sensitive credential and may appear in command lines, request URLs, logs, screenshots, shell history, or process monitoring. <br>
Mitigation: Keep JUST_ONE_API_TOKEN private, avoid exposing full commands or request URLs, and rotate the token if it may have been disclosed. <br>
Risk: The skill calls a third-party metrics endpoint and depends on JustOneAPI availability, permissions, and response behavior. <br>
Mitigation: Install only when the publisher and endpoint are trusted, provide only the needed userId and filters, and review backend error payloads before using results in campaign decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-api-pgy-kol-data-core-data) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI authentication guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_pgy_kol_data_core_data&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_pgy_kol_data_core_data&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with inline shell command examples and raw JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and a JUST_ONE_API_TOKEN credential; the endpoint requires userId and accepts optional business, noteType, dateType, and advertiseSwitch filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
