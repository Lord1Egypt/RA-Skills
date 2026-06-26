## Description: <br>
PowerShell skill for calling Kakao Local API to normalize addresses and search places with keyword, location, radius, and category filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MunInJun](https://clawhub.ai/user/MunInJun) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and agents use this skill on Windows to normalize Korean addresses and search Kakao places through a PowerShell interface. It returns structured JSON that can feed place recommendations, favorites, caches, and downstream location workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kakao API keys can be exposed if stored in committed config files or passed through visible command channels. <br>
Mitigation: Prefer the KAKAO_REST_API_KEY environment variable, do not pass keys as skill parameters, and do not commit data/config.json. <br>
Risk: Address, coordinate, place-search, favorites, and cache data can reveal private location history. <br>
Mitigation: Treat generated places.json and cache.json files as private, restrict access to them, and delete them when no longer needed. <br>
Risk: Address, keyword, and optional coordinate queries are sent to Kakao's Local API. <br>
Mitigation: Use the skill only when sending those queries to Kakao is acceptable for the user and deployment context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MunInJun/mij-kakao-local) <br>
- [Kakao Developers](https://developers.kakao.com/) <br>
- [Packaged PowerShell script source](references/kakao_local.ps1.md) <br>
- [Packaged config template](references/config.json.template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with PowerShell and JSON examples; runtime script output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, PowerShell 5.0 or later, curl.exe, and a Kakao Developers REST API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
