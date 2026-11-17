## Description: <br>
Grain Crawler Free helps an agent search local Granola archives, retrieve note details, and check archive freshness with local-first JSON command output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search local Granola meeting-note archives, retrieve note details, and check archive freshness before answering questions about prior meetings or personal knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could cause unnecessary access to sensitive local meeting-note archives. <br>
Mitigation: Limit use to explicit Granola note search, note-detail retrieval, and freshness checks; avoid invoking it for generic report or visualization requests. <br>
Risk: The skill can run the grain-crawler CLI and read local Granola archive/cache content. <br>
Mitigation: Use it only when the user is comfortable granting local note access, and review CLI actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/grain-crawler-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses grain-crawler CLI commands to read local Granola archive/cache content and should report cache source and freshness when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
