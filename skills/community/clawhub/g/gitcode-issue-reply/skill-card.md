## Description: <br>
Generates maintainer-reviewed GitCode issue reply drafts with similar issue references when a user provides a single GitCode issue and asks to reply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to draft GitCode issue responses, review similar issue references, and publish comments only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a GitCode token to read issue data and post comments. <br>
Mitigation: Use a least-privilege token and review label actions and final reply text before publication. <br>
Risk: Issue text may be sent to DeepWiki and issue images may be downloaded for analysis. <br>
Mitigation: Avoid private or sensitive issues unless DeepWiki sharing and local caching are acceptable. <br>
Risk: Issue data may be retained locally during the reply workflow. <br>
Mitigation: Review generated local outputs and remove cached issue artifacts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/autoxj/gitcode-issue-reply) <br>
- [GitCode API documentation](https://docs.gitcode.com/docs/apis/) <br>
- [Draft reply prompt template](artifact/references/prompts/draft_reply.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown draft reply with issue-reference links, status notes, and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintainer review and explicit confirmation are required before posting the final reply.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact history, released 2026-03-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
