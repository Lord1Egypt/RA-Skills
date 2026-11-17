## Description:

HIRA hospital information search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Korean hospitals, clinics, and pharmacies through HIRA/data.go.kr APIs and retrieve hospital details such as departments, hours, transport, address, and phone information.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: Crafted hospital search inputs can execute local Python code with the user's permissions.

Mitigation: Patch the unsafe python3 -c argument handling before installing or running the skill, and review all shell scripts before use.

Risk: Queries and the service key are sent to data.go.kr.

Mitigation: Store the API key with restrictive file permissions and use the skill only when sending search terms to data.go.kr is acceptable.

Risk: The server security verdict is suspicious.

Mitigation: Use only if the publisher is trusted and the unsafe input handling has been fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sw326/skills/hira-hospital)
- [data.go.kr](https://www.data.go.kr)
- [HIRA Hospital Info OpenAPI](https://www.data.go.kr/data/15001698/openapi.do)
- [HIRA API base URL](https://apis.data.go.kr/B551182/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown summaries with JSON data from shell-backed API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a data.go.kr API key stored at ~/.config/data-go-kr/api_key.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
