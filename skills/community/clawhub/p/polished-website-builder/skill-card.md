## Description:

Builds an editable, responsive local website with researched copy from a product or service description, retaining sources and revisions in JishuDB without deploying the site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and developers use this skill to turn product or service descriptions into editable local landing pages and showcase sites with sourced copy and revision records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads and runs native JishuDB installers and changes the agent host's connection configuration.

Mitigation: Review the setup plan and installer source, authorize installation and configuration changes explicitly, and confirm the connector works afterward.

Risk: Website source material and revisions are stored in JishuDB.

Mitigation: Choose the storage destination and approve which materials may be retained before transferring them.

Risk: The Windows setup helper uses PowerShell despite contrary wording in its installation contract.

Mitigation: Review the Windows setup flow and its PowerShell use before approving execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bowen-aijishu/skills/polished-website-builder)
- [Skill homepage listed in release metadata](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/polished-website-builder)
- [Bundled JishuDB setup quickstart](references/jishudb-setup/references/setup-quickstart.md)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Guidance]

**Output Format:** [Editable local HTML/CSS with optional JavaScript and assets, plus Markdown site guidance, copy, sources, and revision notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responsive static site; JishuDB retains product sources and revisions; deployment and production backend are out of scope.]

## Skill Version(s):

0.1.17 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
