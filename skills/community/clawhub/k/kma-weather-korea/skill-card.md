## Description: <br>
KMA short-term forecast API - ultra-short-term observation/forecast, short-term forecast <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to fetch Korean weather observations, short-term forecasts, and air-quality context from data.go.kr-backed services, then format the results as concise weather briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a data.go.kr API key for Korean weather and air-quality requests. <br>
Mitigation: Store the API key with restrictive file permissions and avoid exposing it in logs, prompts, or shared outputs. <br>
Risk: The morning briefing script reads an API key from a hard-coded /home/scott path. <br>
Mitigation: Review or edit the script to use the operator's own config path before running scheduled briefings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sw326/kma-weather-korea) <br>
- [data.go.kr](https://www.data.go.kr) <br>
- [KMA short-term forecast open API](https://www.data.go.kr/data/15084084/openapi.do) <br>
- [KMA VilageFcstInfoService endpoint](https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0) <br>
- [AirKorea measurement endpoint](https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty) <br>
- [playbook.md](playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses KMA grid coordinates and may include weather, precipitation, wind, humidity, and PM2.5 or PM10 air-quality values.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
