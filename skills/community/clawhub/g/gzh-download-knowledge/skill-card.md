## Description:

Exports the user's own WeChat official-account article history from the logged-in publisher backend into a local Markdown knowledge base, using webclaw3 to reuse the active browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content maintainers use this skill to archive articles from their own WeChat official account into local Markdown files for backup, search, or knowledge-base workflows. It is intended for the account currently logged into the WeChat public-account backend, not for collecting other publishers' content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the browser's currently logged-in WeChat public-account session, so it may export from the wrong account if the browser is logged into a different backend.

Mitigation: Confirm the browser is logged into the intended mp.weixin.qq.com account before running the skill.

Risk: Exported article text, titles, links, dates, and account names are saved locally and may be sensitive in some workflows.

Mitigation: Choose a dedicated output directory, protect that directory according to the content sensitivity, and review exported files before sharing them.

Risk: The skill depends on a local webclaw3 browser relay and an active WeChat backend session; missing relay setup or expired login state will cause failed or partial exports.

Mitigation: Run the webclaw3 doctor check first and refresh the WeChat backend login before starting a batch export.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fatmind/skills/gzh-download-knowledge)
- [Publisher profile](https://clawhub.ai/user/fatmind)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, files, configuration, shell commands, guidance]

**Output Format:** [Local Markdown article files with frontmatter, index JSON, status JSON, a Markdown run summary, and one stdout JSON status line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes articles under outputDir/articles, writes index.json for the export set, and writes res.json plus data.md for pipeline output.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
