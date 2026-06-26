## Description: <br>
Misskey API integration for posting notes and uploading media to Misskey/Fediverse instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasuganosora](https://clawhub.ai/user/kasuganosora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure Misskey API access, post notes, upload media, check the authenticated account, and delete notes on Misskey/Fediverse instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a user's Misskey account, including posting, uploading, reading account information, and deleting notes. <br>
Mitigation: Use a least-privilege Misskey token for the intended actions, keep it in environment variables, and avoid broad account tokens. <br>
Risk: The authoritative security evidence flags unsafe command execution and note deletion without enough scoping or safeguards. <br>
Mitigation: Review the scripts before enabling them, test with a non-critical account first, require explicit confirmation for delete actions, and prefer a patched version that removes eval. <br>


## Reference(s): <br>
- [ClawHub Misskey skill page](https://clawhub.ai/kasuganosora/misskey) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell command examples and text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MISSKEY_HOST and MISSKEY_TOKEN; actions may create notes, upload files, read account metadata, or delete notes through the configured Misskey instance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json; SKILL.md metadata says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
