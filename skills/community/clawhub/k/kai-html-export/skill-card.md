## Description: <br>
Exports HTML files to PPTX or PNG, or publishes HTML to a public share URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to convert HTML presentations or reports into PowerPoint or PNG outputs, or to share HTML through public hosting when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local HTML files and copied assets can be uploaded to public hosting. <br>
Mitigation: Review files for secrets or private data before sharing and prefer manual or isolated deployments for sensitive content. <br>
Risk: Publishing flows can use Cloudflare or Vercel credentials and may affect hosting protection settings. <br>
Mitigation: Use a dedicated account or project where possible and verify protection settings before and after deployment. <br>
Risk: Untrusted HTML is processed by a headless browser and export scripts. <br>
Mitigation: Avoid untrusted HTML or run exports in an isolated environment with minimal local file and credential access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/kai-html-export) <br>
- [README](artifact/README.md) <br>
- [PPTX Export Strategy](artifact/PPTX_EXPORT_STRATEGY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated PPTX, PNG, or public URL outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can operate on local HTML files or folders and may use optional Cloudflare or Vercel publishing flows.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
