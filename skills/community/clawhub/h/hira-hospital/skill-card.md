## Description: <br>
Searches Health Insurance Review and Assessment Service hospital information and detail APIs for Korean medical institutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search Korean medical institutions by name, region, type, or department and retrieve details such as address, phone number, departments, hours, transport, equipment, and staffing. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: A crafted hospital-name search can execute local Python code in hospital_search.sh. <br>
Mitigation: Do not install this version until hospital_search.sh passes the hospital name to Python as an argument or environment variable instead of embedding it in source code. <br>
Risk: The skill depends on a data.go.kr API key stored on disk. <br>
Mitigation: Store the key with restrictive permissions. <br>
Risk: Detail lookups or optional enrichment can act on the wrong institution if the hospital is not confirmed. <br>
Mitigation: Require a confirmed hospital before detail lookups or optional web-search and notification enrichment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sw326/hira-hospital) <br>
- [data.go.kr public data portal](https://www.data.go.kr) <br>
- [HIRA hospital information OpenAPI](https://www.data.go.kr/data/15001698/openapi.do) <br>
- [HIRA hospital information API base](https://apis.data.go.kr/B551182/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown summaries and JSON responses from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a data.go.kr API key at ~/.config/data-go-kr/api_key; detail lookup requires a confirmed institution code.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
