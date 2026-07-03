## Description: <br>
Downloads user-provided Instagram Reel or Post links, drafts Chinese Bilibili title and description metadata, uploads them to Bilibili, and verifies the resulting video link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arvinyin1](https://clawhub.ai/user/arvinyin1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when a user explicitly provides one or more Instagram Reel or Post links and asks to repost them to Bilibili. It guides media download, metadata drafting, Bilibili upload, and post-upload verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to read local browser session cookies and store Bilibili credentials locally. <br>
Mitigation: Use only a Bilibili account acceptable for posting, keep credentials.json out of version control and logs, restrict file permissions, and delete or rotate credentials when finished. <br>
Risk: The artifact references upload and cookie setup scripts that were not included for review. <br>
Mitigation: Review the installed scripts before execution and do not run cookie setup or upload commands until the local implementation has been inspected. <br>
Risk: The skill reposts user-supplied Instagram content to Bilibili, which can create rights or platform-policy issues. <br>
Mitigation: Only repost content when the user has confirmed permission or a legitimate basis for reposting, and stop when Bilibili verification indicates rejection or removal. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/ArvinYin1/ig-link-bili-skill) <br>
- [ClawHub skill page](https://clawhub.ai/arvinyin1/ig-link-bili-skill) <br>
- [Publisher profile](https://clawhub.ai/user/arvinyin1) <br>
- [Diagnosis methodology](references/diagnosis-methodology.md) <br>
- [Known pitfalls](references/pitfalls.md) <br>
- [Upload verification](references/upload-verification.md) <br>
- [Configuration example](config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration values, and final Bilibili video URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include upload status details such as bvid or aid when the referenced upload scripts return them.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
