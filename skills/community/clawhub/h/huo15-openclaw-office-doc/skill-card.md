## Description: <br>
Huo15 Openclaw Office Doc helps agents generate Chinese enterprise documents as Word or PDF files across contracts, reports, plans, technical documents, and related business formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business or technical teams use this skill to draft, format, and convert enterprise documents such as contracts, project reports, API documentation, deployment guides, resumes, press releases, and risk assessments. It supports Word generation, native PDF generation, Word-to-PDF conversion, and reusable Markdown templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document generation may attempt Odoo access using existing OpenClaw credentials when company information is missing. <br>
Mitigation: Run document commands with explicit --company-name and --logo-path values or use --no-odoo when external Odoo access is not intended. <br>
Risk: The skill can persist local company information and related memory files. <br>
Mitigation: Review ~/.huo15/company-info.json and generated memory files before and after use, especially on shared machines. <br>
Risk: generate-config.sh can write OpenClaw workspace, persona, and memory files outside ordinary document generation. <br>
Mitigation: Avoid running generate-config.sh unless the intended task is OpenClaw workspace configuration. <br>
Risk: A deployment template includes an admin/admin test credential. <br>
Mitigation: Replace or remove the test credential before using the template in any real deployment documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-office-doc) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown source and generated DOCX or PDF files, with CLI-oriented command output where scripts are used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Document commands can use local company information, logo assets, templates, and optional conversion backends.] <br>

## Skill Version(s): <br>
7.9.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
