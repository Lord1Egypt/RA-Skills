## Description: <br>
Command-line tool for Kakao Local API keyword and category place search, geocoding, and reverse geocoding with JSON output and API key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to perform Kakao Local API place searches, address-to-coordinate lookups, and coordinate-to-address lookups from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Kakao REST API key, so credentials or location queries could be exposed through shared logs or command output. <br>
Mitigation: Store KAKAO_REST_API_KEY in a secret manager or local environment variable, use quota-limited credentials, and redact API keys and sensitive query data from logs. <br>
Risk: Executable package code is not bundled in the skill artifact. <br>
Mitigation: Inspect and pin the referenced repository or package revision before installing or running the CLI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/kakao-local-cli) <br>
- [Project homepage](https://github.com/ChloePark85/kakao-local-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI examples and environment variable instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of a JSON-producing CLI and requires KAKAO_REST_API_KEY for authenticated Kakao Local API requests.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
