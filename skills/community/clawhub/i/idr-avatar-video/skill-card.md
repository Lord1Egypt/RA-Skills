## Description: <br>
Creates avatar videos using video templates or digital-human and voice selections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ihanxu2022](https://clawhub.ai/user/ihanxu2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to list available avatars, voices, and templates, then generate asynchronous avatar videos from text, uploaded audio, or templates through the IDR/neural-avatar service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends video scripts, selected audio files, account asset metadata, and the service token to a remote provider. <br>
Mitigation: Use only content appropriate for that provider, avoid confidential or regulated material, and treat IDR_USER_TOKEN as a secret. <br>
Risk: The security summary states that API traffic uses plain HTTP while carrying user content and an API token. <br>
Mitigation: Prefer a version that uses HTTPS before sensitive use, and run it only on trusted networks when HTTPS is unavailable. <br>
Risk: The security summary states that generated text files are left behind locally. <br>
Mitigation: Delete generated idr_text_*.txt files after runs or use a version that removes temporary text files automatically. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ihanxu2022/skills/idr-avatar-video) <br>
- [Publisher Profile](https://clawhub.ai/user/ihanxu2022) <br>
- [Neural Avatar](https://www.neural-avatar.com) <br>
- [IDR](https://idr.ai) <br>
- [Authentication](references/authentication.md) <br>
- [Avatars](references/avatars.md) <br>
- [Voices](references/voices.md) <br>
- [Templates](references/templates.md) <br>
- [Video Generation](references/video-generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IDR_USER_TOKEN and network access to the neural-avatar service; video-generation commands return task status text and video URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
