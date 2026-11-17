## Description:

Processes user-supplied Instagram Reel or Post links for download, Chinese translation, Bilibili reposting, and post-upload verification without feed scraping, automatic filtering, deduplication, or author blacklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arvinyin1](https://clawhub.ai/user/arvinyin1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert user-supplied Instagram Reel or Post links into Bilibili uploads, including media preparation, Chinese title and description generation, category and tag selection, upload, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may use a user's Bilibili browser session to upload under that account.

Mitigation: Use an isolated browser profile and dedicated Bilibili account, protect credentials.json, avoid logging cookies, and rotate the session if exposed.

Risk: The artifact references setup and upload scripts that are not present in the release evidence and therefore cannot be audited from these files.

Mitigation: Audit or obtain the missing scripts before installation or execution, and run the skill only in an environment where those scripts are trusted.

Risk: Reposting third-party Instagram content to Bilibili can create authorization, copyright, or platform-policy issues.

Mitigation: Only repost content the user is authorized to share, preserve attribution, and stop when verification or platform review indicates rejection.

Risk: Bilibili upload APIs can report initial success before the video is actually available.

Mitigation: Wait before verification, run the documented upload verification step, and treat repeated pending or failure states as requiring review rather than immediate success.

## Reference(s):

- [Server-resolved GitHub import source](https://github.com/ArvinYin1/ig-link-bili-skill)
- [ClawHub skill page](https://clawhub.ai/arvinyin1/skills/ig-link-bili-skill)
- [Diagnosis methodology](artifact/references/diagnosis-methodology.md)
- [Known pitfalls](artifact/references/pitfalls.md)
- [Upload verification](artifact/references/upload-verification.md)
- [Configuration example](artifact/config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a Bilibili video URL after upload verification; may also return troubleshooting guidance when upload or verification fails.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
