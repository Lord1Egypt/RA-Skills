## Description: <br>
Note Process Engine Free helps personal researchers and knowledge workers summarize JSON-based research notes, extract keywords, search full text, and list research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, personal researchers, and knowledge workers use this skill to inspect local research-note JSON databases, produce lightweight summaries, identify frequent terms, locate matching notes, and review topic-level statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a suspicious verdict because read-only claims conflict with documented create, modify, import, export, and save actions. <br>
Mitigation: Review intended file access and command behavior before installing, and limit the agent to note databases and directories you are comfortable exposing. <br>
Risk: The skill uses command execution for local note-processing workflows. <br>
Mitigation: Inspect commands before execution and run them in a constrained workspace with non-sensitive test data until the publisher clarifies the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/note-process-engine-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with command examples and structured analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include status, result data, logs, summaries, keyword counts, search matches, and topic statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
