## Description: <br>
Hunter Search v1.0 helps agents use the QAX Hunter OpenAPI to create batch asset export tasks, poll task progress, and download export results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biglizi775](https://clawhub.ai/user/biglizi775) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security operators use this skill to run authorized QAX Hunter asset-mapping exports from an API key, with non-interactive command output suitable for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Hunter API key. <br>
Mitigation: Use a limited API key through an environment variable, avoid pasting keys into chat or files, and do not commit real credentials. <br>
Risk: The security summary notes that downloaded files may use a server-provided filename without path safety checks. <br>
Mitigation: Specify a safe output filename or review and patch filename sanitization before running the download path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/biglizi775/hunterserach) <br>
- [QAX Hunter batch search endpoint](https://hunter.qianxin.com/openApi/search/batch) <br>
- [QAX Hunter download endpoint](https://hunter.qianxin.com/openApi/search/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the CLI can emit one-line JSON and downloaded CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Hunter API key, preferably supplied through HUNTER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
