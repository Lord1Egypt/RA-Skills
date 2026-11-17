## Description:

Knowledge Importer converts Word, Excel, PowerPoint, PDF, and Markdown documents into Markdown files for an Obsidian knowledge base, with optional image extraction and image-host links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinegw](https://clawhub.ai/user/sunshinegw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base users use this skill to import supported office, PDF, and Markdown documents into an Obsidian vault as Markdown, preserving tables and optionally converting embedded images to external image-host links or Base64 data URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted documents may be saved into the configured Obsidian knowledge-base path.

Mitigation: Use a dedicated or reviewed vault path and verify output location before importing sensitive documents.

Risk: Extracted document images may be uploaded to a configured image host, including hosts using plain HTTP.

Mitigation: Use a trusted HTTPS image host and avoid confidential documents unless uploads are disabled or made local-only.

Risk: Extracted images may remain in temporary asset folders after conversion.

Mitigation: Clean temporary asset folders after use and run the importer in an isolated environment when processing untrusted files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunshinegw/skills/knowledge-importer)
- [ClawHub Publisher Profile](https://clawhub.ai/user/sunshinegw)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files with command-line and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes converted files to a configured knowledge-base path and may upload extracted images to a configured image host.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
