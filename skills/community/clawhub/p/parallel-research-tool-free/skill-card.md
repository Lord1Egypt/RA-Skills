## Description: <br>
并行研究助手免费版 helps an agent run interactive topic research, organize findings in persistent Markdown research folders, and optionally export the research document to PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, students, and independent founders use this skill to research a topic through interactive agent sessions, preserve findings in structured Markdown, track open questions and resources, and export a report when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research notes are saved locally under ~/.research-workspace and may expose sensitive topics on shared or managed machines. <br>
Mitigation: Avoid sensitive research topics on shared systems, and manually review or delete generated files after use. <br>
Risk: The optional callback_url parameter can send completion data to an external destination. <br>
Mitigation: Use callback_url only with fully trusted destinations, or omit it when no callback is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/parallel-research-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research documents, optional PDF exports, configuration snippets, and status-style JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local research folders under ~/.research-workspace/research; PDF export depends on optional local tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
