## Description: <br>
Helps agents create Word documents and .docx templates that follow Huo15 formatting, header, footer, typography, naming, and Markdown-to-Word conversion rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents preparing Huo15 business documents use this skill to generate Word files such as contracts, quotes, meeting notes, formal notices, reports, and project documents with consistent company formatting. It also provides Python patterns for document layout, Chinese font handling, page headers and footers, logo insertion, and file naming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local Odoo/OpenClaw credential files and contact configured company systems. <br>
Mitigation: Use only with trusted Huo15/Odoo environments, require user approval before remote access, and prefer platform-managed scoped credentials. <br>
Risk: The included Odoo access pattern disables TLS hostname and certificate verification. <br>
Mitigation: Keep TLS verification enabled in production and verify the configured Odoo endpoint before sending credentials. <br>
Risk: The skill can cache downloaded logo assets under the user's home directory without clear control in the source text. <br>
Mitigation: Document the cache location, ask before downloading assets, and allow users to inspect or remove cached files. <br>
Risk: Broad trigger wording can cause the skill to activate for many document-generation tasks. <br>
Mitigation: Narrow activation to intentional Huo15 Word-document workflows or ask the user to confirm before applying company-specific formatting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-doc-template) <br>
- [Publisher profile](https://clawhub.ai/user/jobzhao15) <br>
- [Huo15 logo endpoint](https://huihuoyun.huo15.com/web/image/website/1/logo) <br>
- [Fallback Huo15 logo asset](https://tools.huo15.com/uploads/images/system/logo-colours.png) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with embedded Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create or save .docx files when the provided Python patterns are executed.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
