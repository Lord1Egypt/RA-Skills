## Description: <br>
Converts Word, Excel, PowerPoint, PDF, and Markdown documents into Markdown and saves them to an Obsidian-style knowledge base, with optional image upload links or Base64 fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunshinegw](https://clawhub.ai/user/sunshinegw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to import local documents into a Markdown knowledge base, preserving tables and optionally extracting images for hosted links or embedded fallback content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted documents are saved into the configured knowledge-base folder. <br>
Mitigation: Configure the knowledge-base path deliberately and test imports with non-sensitive files before processing confidential material. <br>
Risk: Extracted images may be uploaded to a configured image host. <br>
Mitigation: Use a trusted or local image host and avoid importing confidential documents unless those images are intended to be stored there. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunshinegw/knowledge-importer) <br>
- [Publisher profile](https://clawhub.ai/user/sunshinegw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save converted documents into the configured knowledge-base folder and can upload extracted images to a configured image host.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
