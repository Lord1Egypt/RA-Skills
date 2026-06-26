## Description: <br>
Korea Weather helps agents retrieve current conditions, short and mid-term forecasts, and weather warnings from the Korea Meteorological Administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steamb23](https://clawhub.ai/user/steamb23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to query South Korea weather by coordinates or region, including 5 km grid forecasts, mid-term outlooks, and weather warnings. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a KMA/data.go.kr service key. <br>
Mitigation: Use a dedicated API key, avoid sharing configurations that contain it, and rotate or revoke the key if exposure is suspected. <br>
Risk: Weather query parameters are sent to KMA/data.go.kr APIs. <br>
Mitigation: Limit queries to necessary location and forecast parameters and avoid including unrelated sensitive context. <br>
Risk: Weather results can be unavailable or stale around KMA release schedules or service timeouts. <br>
Mitigation: Retry after the documented KMA release windows and present source timing or freshness when using results in decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steamb23/kma-weather) <br>
- [KMA short-term forecast API](https://www.data.go.kr/data/15084084/openapi.do) <br>
- [KMA weather warnings API](https://www.data.go.kr/data/15000415/openapi.do) <br>
- [KMA mid-term forecast API](https://www.data.go.kr/data/15059468/openapi.do) <br>
- [Short-term forecast reference](references/api-forecast.md) <br>
- [Weather warnings reference](references/api-warnings.md) <br>
- [Mid-term forecast reference](references/api-midterm.md) <br>
- [KMA category codes reference](references/category-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text weather summaries and optional JSON API responses, with Markdown usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and KMA_SERVICE_KEY; sends Korean weather query parameters to KMA/data.go.kr APIs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
