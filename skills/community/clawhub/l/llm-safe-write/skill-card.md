## Description: <br>
Guides agents to write large or CJK-containing files with an incremental skeleton-and-edit workflow instead of direct Write. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkdonk](https://clawhub.ai/user/thinkdonk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to create or modify large files, files with CJK or special characters, and files affected by Write truncation errors through smaller incremental edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated edits can introduce incorrect file content or leave temporary append markers if the agent is interrupted. <br>
Mitigation: Review generated edits, spot-check the resulting file, and remove any temporary marker lines before relying on the output. <br>
Risk: The workflow includes examples with API-key placeholders and may be used around files containing sensitive configuration. <br>
Mitigation: Keep real secrets out of committed files and review credential-bearing edits before deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/thinkdonk/llm-safe-write) <br>
- [Server-resolved source repository](https://github.com/ThinkDonk/llm-safe-write) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, command examples, and editing workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Self-contained workflow with no declared runtime dependencies; users should review generated edits and cleanup markers after interrupted append operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
