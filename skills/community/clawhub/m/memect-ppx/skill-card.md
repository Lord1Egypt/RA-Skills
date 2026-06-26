## Description: <br>
Parse PDFs and images into Markdown/JSON using the memect-ppx (`ppx`) CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihanghang](https://clawhub.ai/user/lihanghang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to OCR scanned PDFs or images, extract tables, convert documents into Markdown or JSON, and inspect the generated parsing output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs and images may contain sensitive content, and parsed text, JSON, pages, or extracted images may persist in the output directory. <br>
Mitigation: Parse only files the user chooses, write results to a private output directory, and review retained outputs before sharing or archiving them. <br>
Risk: LLM or persistent backend settings can expose document contents to configured services. <br>
Mitigation: Use backend modes only with services trusted for the document contents, and prefer the default local pipeline when privacy is the priority. <br>
Risk: Debug or development modes may retain extra intermediate data while troubleshooting. <br>
Mitigation: Avoid debug/dev modes during normal parsing and clean up intermediate files after troubleshooting. <br>


## Reference(s): <br>
- [Memect PPX homepage](https://github.com/memect/memect-ppx) <br>
- [CLI Options](references/cli-options.md) <br>
- [Backend Config](references/backend-config.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and paths to generated Markdown/JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports OCR mode, table mode, backend choice, and output directory when they materially affect accuracy.] <br>

## Skill Version(s): <br>
0.2.6 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
