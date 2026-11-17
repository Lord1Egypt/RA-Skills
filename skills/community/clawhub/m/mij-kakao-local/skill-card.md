## Description:

PowerShell skill for calling Kakao Local API to normalize addresses and search places with keyword, location, radius, and category filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muninjun](https://clawhub.ai/user/muninjun)

### License/Terms of Use:

MIT License

## Use Case:

Developers and agents use this skill to normalize Korean addresses and search Kakao Local places from PowerShell workflows. It is suited for address lookup, place discovery, and location-filtered search tasks that can send queries to Kakao's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, addresses, keywords, and optional coordinates may be sent to Kakao Local API.

Mitigation: Use the skill only when sending that location data to Kakao is acceptable for the workflow and users involved.

Risk: A plaintext data/config.json API key file can be created, and the promised gitignore protection is not present in the packaged artifact.

Mitigation: Prefer the KAKAO_REST_API_KEY environment variable and avoid creating data/config.json inside a source-controlled directory.

Risk: Cache and favorites examples can store local location history.

Mitigation: Do not copy those examples unless local history storage is intended and the files can be protected or deleted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/muninjun/skills/mij-kakao-local)
- [Kakao Developers](https://developers.kakao.com/)
- [Embedded PowerShell Script](references/kakao_local.ps1.md)
- [Config Template](references/config.json.template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell examples and JSON response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for invoking a PowerShell wrapper around Kakao Local API calls; runtime responses are JSON objects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
