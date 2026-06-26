## Description: <br>
Searches NoahAI medical conference and presentation databases for conferences, session abstracts, posters, oral presentations, and conference-presented drug or trial data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombert](https://clawhub.ai/user/bombert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query medical conference metadata and presentation abstracts by conference, drug, disease, target, author, institution, or date range. It helps retrieve public conference-presented medical and clinical-trial information from NoahAI endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical conference search terms and query payloads are sent to NoahAI and may appear in execution logs. <br>
Mitigation: Avoid confidential research topics in shared or hosted agent environments unless the user is comfortable with NoahAI processing and logging those queries. <br>
Risk: The skill requires a sensitive NOAH_API_TOKEN for API access. <br>
Mitigation: Provide the token only through environment variables or local secret management, and do not place it inline in commands, chats, or packaged files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bombert/medical-conference) <br>
- [NoahAI](https://noah.bio) <br>
- [NoahAI API base](https://www.noah.bio/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests Python package, network access to NoahAI HTTPS endpoints, and NOAH_API_TOKEN in the environment.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
