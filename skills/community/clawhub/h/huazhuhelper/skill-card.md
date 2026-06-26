## Description: <br>
Helps agents query Huazhu hotel lists through Huazhu OpenAPI using OAuth2 credentials supplied by the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjinliang1991](https://clawhub.ai/user/wangjinliang1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators with Huazhu OpenAPI access use this skill to generate Python-oriented guidance for obtaining OAuth2 tokens and querying Huazhu hotel list data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default examples can send OAuth bearer tokens to a plain HTTP business endpoint. <br>
Mitigation: Use test credentials for the default test configuration and avoid sending production tokens to the plain HTTP endpoint. <br>
Risk: The example code prints part of an access token and requires sensitive OAuth credentials. <br>
Mitigation: Do not paste long-lived secrets into chat or source files, and remove token printing before using the code in shared terminals, CI, or production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjinliang1991/huazhuhelper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth credential handling steps, Huazhu API endpoint selection, and hotel list parsing examples.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
