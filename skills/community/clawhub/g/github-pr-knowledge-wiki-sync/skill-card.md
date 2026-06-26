## Description: <br>
GitHub PR documentation automation that fetches PR details, analyzes code changes, generates technical Markdown, and can sync the result to Feishu Wiki or WeCom Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to convert a GitHub pull request into a structured change document and publish or save it for team knowledge bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read full GitHub PR diffs, which may include sensitive implementation details. <br>
Mitigation: Use the Markdown target for sensitive PRs and review generated content before any external sync. <br>
Risk: Generated content can be published to Feishu or WeCom without a clearly documented confirmation or redaction step. <br>
Mitigation: Confirm the destination knowledge base is appropriate for the repository and require human review before publishing. <br>
Risk: GitHub and wiki credentials may grant broader access than the workflow needs. <br>
Mitigation: Use credentials with only the minimum repository and knowledge-base permissions required for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/github-pr-knowledge-wiki-sync) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown technical documentation with optional Feishu Wiki, WeCom Docs, or local Markdown destinations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR metadata, change summaries, changed-file tables, key code-change notes, risk notes, and destination links or file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, workflow.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
