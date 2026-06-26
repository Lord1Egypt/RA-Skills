## Description: <br>
Converts a Claude Code session into a blog post, case study, or Reddit post. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, developer advocates, and technical writers use this skill after a coding session to turn git history, file changes, test evidence, metrics, and conversation context into public-facing engineering posts, case studies, social threads, or Reddit posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may surface session details, repository context, private prompts, internal URLs, customer data, proprietary code details, or configuration values in public-facing prose. <br>
Mitigation: Review the generated post before publishing or committing it, remove sensitive details, and verify claims against the cited session and repository evidence. <br>


## Reference(s): <br>
- [Night Market scribe source](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Session Extraction Checklist](artifact/modules/session-extraction.md) <br>
- [Narrative Structure](artifact/modules/narrative-structure.md) <br>
- [Reddit Post Format](artifact/modules/reddit-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown draft plus a concise status report with format, word count, claim count, and recording notes when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the generated post to docs/posts/ or another requested path and may propose verification commands for evidence gathering.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
