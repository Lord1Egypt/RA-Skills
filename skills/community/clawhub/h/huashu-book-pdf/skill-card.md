## Description: <br>
Guides an agent through researching a topic, planning a long-form manual, writing modular HTML fragments, and building a 100+ page book-style PDF with Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shixiangyu2](https://clawhub.ai/user/shixiangyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation teams, and agents use this skill to create complete PDF manuals, e-books, orange papers, and reference guides from an initial topic. It covers topic clarification, research organization, outline planning, parallel HTML-fragment writing, versioning, and PDF generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js and Playwright scripts that create, update, and render project files. <br>
Mitigation: Use a dedicated project directory, review generated HTML and shell commands before running them, and install Playwright only in an environment where local rendering is acceptable. <br>
Risk: Default cover and back-page templates include author, social, and branding text that may be unsuitable for client-facing or sensitive documents. <br>
Mitigation: Replace the default branding and social links before publishing or delivering generated manuals. <br>
Risk: The bundled design system references Google Fonts, which may be undesirable in restricted or confidential environments. <br>
Mitigation: Vendor fonts locally or remove external font loading when network access or third-party font requests are not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shixiangyu2/huashu-book-pdf) <br>
- [Publisher profile](https://clawhub.ai/user/shixiangyu2) <br>
- [Design system reference](references/design-system.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands, HTML fragments, JavaScript/CSS templates, and project file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated projects can produce merged HTML and A4 PDF files through local Node.js and Playwright scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
