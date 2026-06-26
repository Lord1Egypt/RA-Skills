## Description: <br>
LSP Novel Writer helps agents collect fiction requirements, draft Chinese web-novel outlines, confirm them with the user, and generate chapter-by-chapter Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and agent users use this skill to plan Chinese web novels, refine outlines, and generate chapter drafts after approving the outline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local novel chapter files in ./novels/ within the current workspace. <br>
Mitigation: Use it in a workspace where generated files are acceptable and review the save location before sharing or publishing outputs. <br>
Risk: Generated outlines or chapters may need editorial review before publication. <br>
Mitigation: Review the outline before confirming chapter generation and check completed chapters before publishing or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/156554395/lsp-novel-writer) <br>
- [Writing Guide](references/writing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown outlines, progress text, and chapter files saved under ./novels/] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one Markdown file per chapter after user outline confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
