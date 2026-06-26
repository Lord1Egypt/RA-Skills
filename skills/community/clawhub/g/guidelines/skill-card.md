## Description: <br>
Generates FTdesign-compliant HTML preview pages for list, form, and detail interfaces from natural-language page descriptions. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[Nero1510](https://clawhub.ai/user/Nero1510) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill to turn page requirements into FTdesign-style HTML previews for management lists, data-entry forms, and detail views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-influenced HTML can be written and previewed, which may expose users to unsafe or misleading generated content. <br>
Mitigation: Use explicit requests only, review generated HTML before previewing it, and avoid auto-previewing output created from untrusted prompts. <br>
Risk: Weak filename and overwrite controls can lead to unexpected file placement or replacement. <br>
Mitigation: Check destination filenames before generation and add path validation plus overwrite prompts before broader deployment. <br>
Risk: Generated pages may load external CDN resources. <br>
Mitigation: Provide an option to disable external CDN loading or pin approved local assets for restricted environments. <br>
Risk: HTML escaping is not clearly enforced for all user-supplied content. <br>
Mitigation: Escape inserted text by default and review generated markup before sharing or opening it in privileged contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Nero1510/guidelines) <br>
- [FTdesign Component API](artifact/references/components-api.md) <br>
- [FTdesign Design System](artifact/references/design-system.md) <br>
- [FTdesign Examples](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, Python, and JSON snippets; generated output is HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages may reference external icon or font CDNs and can be opened in a browser or IDE preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
