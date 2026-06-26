## Description: <br>
Professional PDF document generator for reports, invoices, certificates, portfolios, and other publication-ready PDFs with images, tables, charts, tables of contents, headers, footers, and cross-platform fonts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to plan and generate print-quality PDF reports, invoices, certificates, resumes, portfolios, contracts, and academic documents using local Python PDF libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may select PDF output when a user asks for a generic report. <br>
Mitigation: Confirm the user wants a PDF deliverable before choosing PDF-specific generation steps. <br>
Risk: The skill depends on manually installed Python PDF libraries. <br>
Mitigation: Install dependencies only from trusted package sources, preferably in an isolated virtual environment, and review generated code before execution. <br>
Risk: Marketplace capability tags include crypto and purchase labels that do not match the reviewed skill behavior. <br>
Mitigation: Treat those tags as labeling noise unless future evidence shows payment, purchase, wallet, or crypto behavior. <br>


## Reference(s): <br>
- [PDF Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tobewin/pdf-studio) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown with PDF-generation guidance, dependency commands, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local PDF files when the agent follows the generated implementation steps with user-approved Python libraries.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
