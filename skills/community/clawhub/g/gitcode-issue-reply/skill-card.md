## Description:

Generate reply drafts for a single GitCode issue with similar-issue references for maintainer review before posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to prepare a reviewed Markdown reply for one GitCode issue, with similar-issue references, issue context, optional image analysis, and DeepWiki background when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Issue content is automatically sent to DeepWiki when that integration is enabled.

Mitigation: Review repository sensitivity before use and disable DeepWiki where possible for private or sensitive repositories.

Risk: Issue-linked images may be fetched from arbitrary URLs and processed locally.

Mitigation: Avoid automatic processing of untrusted image links and inspect image sources before using their contents in a reply.

Risk: Repository and issue data can be retained locally through output files, cache files, and the BM25 knowledge base.

Mitigation: Disable cache or persistence where possible and clean generated output or temp data after handling sensitive issues.

Risk: Posting comments requires a GitCode token and can affect live issue discussions.

Mitigation: Use a narrowly scoped token and confirm the exact comment body before sending any post.

## Reference(s):

- [GitCode API documentation](https://docs.gitcode.com/docs/apis/)
- [GitCode personal access token settings](https://gitcode.com/setting/token-classic)
- [Draft reply prompt template](references/prompts/draft_reply.txt)
- [ClawHub skill page](https://clawhub.ai/autoxj/skills/gitcode-issue-reply)
- [ClawHub publisher profile](https://clawhub.ai/user/autoxj)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reply draft with similar-issue links, status notes, warnings, and command guidance; preparation scripts also emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITCODE_TOKEN. The generated issue reply is shown for maintainer review before posting; preparation output may include similar issues, DeepWiki status, image references, and security warnings.]

## Skill Version(s):

1.2.0 (source: release metadata and SKILL.md history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
