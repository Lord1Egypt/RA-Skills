## Description: <br>
Provides asynchronous reflection and local memory continuity workflows for extracting structured memories, generating follow-up questions, and surfacing them in later sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Riley-Coyote](https://clawhub.ai/user/Riley-Coyote) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add local cross-session memory reflection: it can inspect a supplied session transcript, maintain identity and question files, report memory status, and surface unresolved follow-up questions when a user returns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and resurfaces local cross-session memory notes, which can be privacy-sensitive if transcripts or memories contain sensitive information. <br>
Mitigation: Run reflection only on transcripts intended for retention, review the memory directory periodically, and enable heartbeat automation only when automatic post-session reflection is acceptable. <br>


## Reference(s): <br>
- [Continuity Framework](references/framework.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Riley-Coyote/memory-continuity) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown and plain text CLI output, with optional JSON reflection logs and Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local memory, identity, question, and reflection files under the configured continuity memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
