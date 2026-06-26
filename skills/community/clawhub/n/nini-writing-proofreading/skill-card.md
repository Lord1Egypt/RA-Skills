## Description: <br>
Use when a user wants to review, polish, or proofread Chinese articles through a structured editorial workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Writers and editors use this skill to review Chinese Markdown articles for structure, reader context, language quality, source support, personal style consistency, and optional Markdown formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional file edits and Markdown formatting can change user-authored articles. <br>
Mitigation: Confirm the exact file and review the diff before accepting automatic formatting or applying edits. <br>
Risk: Optional external setup for markdown linting may add dependencies or configuration. <br>
Mitigation: Assess the markdown-lint setup separately before installing or enabling it. <br>


## Reference(s): <br>
- [Chinese style guide](references/chinese-style.md) <br>
- [Personal style guide](references/personal-style.md) <br>
- [Source verification guide](references/source-verification.md) <br>
- [Structure review guide](references/structure-review.md) <br>
- [ClawHub skill page](https://clawhub.ai/niracler/nini-writing-proofreading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review notes, suggested edits, source-checking guidance, and optional markdownlint-cli2 commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill asks for confirmation before applying substantive edits and reviews one or two Markdown sections at a time.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
