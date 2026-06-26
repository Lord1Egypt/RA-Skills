## Description: <br>
Queries current and forecast weather for cities in China using Moji Weather as the primary source and MSN Weather as a fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather, temperature, rain, and short-range forecast questions for cities in China using domestic weather sources. <br>

### Deployment Geography for Use: <br>
Global; weather coverage is intended for cities in China. <br>

## Known Risks and Mitigations: <br>
Risk: Weather answers can become stale or incorrect if the live source is unavailable, delayed, or parsed incorrectly. <br>
Mitigation: Query the source at response time, include the data source and query time, and avoid answering with unverified weather information. <br>
Risk: The skill depends on browser access to third-party weather pages, so site layout changes or access failures can affect results. <br>
Mitigation: Use the documented fallback from Moji Weather to MSN Weather and clearly state the source used. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/moji-weather) <br>
- [Publisher profile](https://clawhub.ai/user/paudyyin) <br>
- [Moji Weather](https://tianqi.moji.com/) <br>
- [MSN Weather China](https://www.msn.cn/zh-cn/weather/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown weather summary with source attribution and optional screenshot guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current conditions, daily high and low temperatures, wind, AQI, and a 3-5 day forecast when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
