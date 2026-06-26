## Description: <br>
LBS Market Analyzer helps agents perform AMAP-based geospatial market intelligence, competitor distribution analysis, site-selection evaluation, Golden Path flow analysis, and market-gap identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raphaelxiao](https://clawhub.ai/user/raphaelxiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, site-selection teams, and agents use this skill to fetch AMAP point-of-interest data and turn it into concise market-pressure, site-fit, traffic-flow, and market-gap findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser automator can operate inside an AMAP account, create app/key resources, accept an agreement, persist session state, and append an API key to .env. <br>
Mitigation: Prefer manual AMAP key creation and provide the key through a managed secret process; run the automator only when that account-side behavior is intended. <br>
Risk: The session directory, .env file, and logs may expose AMAP credentials or login state. <br>
Mitigation: Protect or delete ./amap_session, .env, and logs after use, and keep them out of source control. <br>
Risk: AMAP API errors, quota limits, or incomplete point-of-interest data can lead to weak market recommendations. <br>
Mitigation: Check AMAP status codes and quota responses, then review generated market findings before making site-selection decisions. <br>


## Reference(s): <br>
- [AMAP API Reference](references/amap-api-guide.md) <br>
- [Analysis Logic](references/analysis-logic.md) <br>
- [AMAP Console](https://console.amap.com/dev/key/app) <br>
- [AMAP REST API](https://restapi.amap.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, and JSON API-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run browser automation and AMAP API calls when invoked with user-provided credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
