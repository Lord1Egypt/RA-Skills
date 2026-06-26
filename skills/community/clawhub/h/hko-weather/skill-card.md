## Description: <br>
Fetches Hong Kong Observatory weather data, forecasts, and warning signals and formats reports for OpenClaw and Discord-oriented workflows. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[firenai3424](https://clawhub.ai/user/firenai3424) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to retrieve Hong Kong current weather, forecasts, and warning information and publish concise bilingual or Traditional Chinese weather updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing to the wrong skill directory or overwriting an existing skill could affect an OpenClaw workspace. <br>
Mitigation: Verify the install path before running the installer and review overwrite prompts before continuing. <br>
Risk: Discord or scheduled posting can send weather updates to an unintended channel if configured incorrectly. <br>
Mitigation: Enable Discord posting only for the intended channel and review channel IDs and posting intervals before use. <br>
Risk: HKO weather data has attribution, disclaimer, and non-commercial-use requirements described in the artifact documentation. <br>
Mitigation: Keep the HKO attribution and disclaimer in generated reports and obtain the required permission before commercial exploitation of HKO data. <br>
Risk: Public weather API responses may be delayed, unavailable, or time-sensitive. <br>
Mitigation: Use the documented timeout, retry, and 10-15 minute caching guidance, and include update times in displayed weather reports. <br>


## Reference(s): <br>
- [ClawHub HKO Weather listing](https://clawhub.ai/firenai3424/hko-weather) <br>
- [HKO Open Data Portal](https://www.hko.gov.hk/tc/abouthko/opendata_intro.htm) <br>
- [HKO Open Data API Documentation](https://www.hko.gov.hk/tc/weatherAPI/doc/files/HKO_Open_Data_API_Documentation.pdf) <br>
- [DATA.GOV.HK HKO Datasets](https://data.gov.hk/tc-datasets/provider/hk-hko) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown weather reports, command examples, configuration snippets, and JSON from the fetch script when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather reports may include Traditional Chinese or English text, Hong Kong time, Celsius temperatures, HKO attribution, and the HKO disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
