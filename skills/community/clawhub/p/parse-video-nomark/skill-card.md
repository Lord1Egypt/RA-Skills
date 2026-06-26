## Description: <br>
Parses shared video links from 20+ short-video and social platforms and returns watermark-free media results. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[mackjosn](https://clawhub.ai/user/mackjosn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to parse shared video links, remove watermarks, and optionally run a local HTTP interface for supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use downloads and runs an unverified native executable from a mutable Gitee repository. <br>
Mitigation: Install only if the publisher and referenced repository are trusted, and run first use in a constrained environment when possible. <br>
Risk: The HTTP service workflow may expose the parser service if it binds beyond localhost or is reachable from untrusted networks. <br>
Mitigation: Avoid starting the service unless the binding is verified as local-only, and do not expose the service to untrusted networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mackjosn/parse-video-nomark) <br>
- [Publisher profile](https://clawhub.ai/user/mackjosn) <br>
- [Gitee source repository](https://gitee.com/qiushuihanjing/parse-video-nomark) <br>
- [Gitee binary download directory](https://gitee.com/qiushuihanjing/parse-video-nomark/raw/master/dist/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text output from the parse-video executable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [First use may download a platform-specific native executable and the serve workflow can start a local HTTP service.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
