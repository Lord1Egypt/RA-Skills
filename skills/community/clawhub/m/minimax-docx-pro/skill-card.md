## Description: <br>
Enterprise-grade Word document generation. Creates validated .docx files with professional formatting, visual hierarchy, and cross-application compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to create polished Word documents from scratch or apply updates to user-provided DOCX/DOC templates while preserving structure and validating the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically download and run a .NET installer and modify the user's home-directory .NET installation. <br>
Mitigation: Install .NET 9 manually first, review setup/build/audit commands before running them, and do not permit removal of ~/.dotnet unless that directory is disposable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luaqnyin/minimax-docx-pro) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Create workflow](artifact/guides/create-workflow.md) <br>
- [Template apply workflow](artifact/guides/template-apply-workflow.md) <br>
- [DOC input normalization protocol](artifact/guides/doc-input-normalization.md) <br>
- [C# OpenXML coding guide](artifact/guides/development.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance, Text] <br>
**Output Format:** [DOCX files with text previews, validation reports, Markdown guidance, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and .NET 9.0 SDK for core workflows; LibreOffice, Pandoc, matplotlib, Playwright, and Pillow are optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
