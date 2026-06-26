## Description: <br>
Read Lanhu UI designs, inspect slices, and download Web, iOS, and Android assets using the lh-design CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuwenxindeai](https://clawhub.ai/user/xuwenxindeai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design implementation agents use this skill to turn Lanhu design URLs into slice metadata and platform-specific asset downloads for web, iOS, and Android work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lanhu and DDS cookie values can grant access to private design resources if exposed. <br>
Mitigation: Treat LANHU_COOKIE and DDS_COOKIE like passwords; do not paste them into chat, commit them, or allow tools to print them in logs. <br>
Risk: Authenticated downloads can retrieve design assets the user did not intend to share or process. <br>
Mitigation: Use this skill only for Lanhu designs the user intends the agent to access and download. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of slices.json and platform-specific asset directories through lh-design.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
