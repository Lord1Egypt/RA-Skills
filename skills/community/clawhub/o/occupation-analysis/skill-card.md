## Description:

Occupation Analysis helps agents generate vocational education occupation analysis reports using a work-process-systematized method for secondary vocational, higher vocational, and vocational undergraduate programs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

External users and education or curriculum developers use the skill to map a vocational major to occupations, analyze work tasks and competencies, convert them into learning areas and scenarios, and produce a seven-part report.

### Deployment Geography for Use:

Global, with source data centered on China's vocational education and occupation standards.

## Known Risks and Mitigations:

Risk: The security evidence reports an unusually broad dependency set.

Mitigation: Install in an isolated virtual environment and review or prune requirements.txt before installation.

Risk: The security evidence reports that PDF fetching can accept arbitrary URLs without clear safety limits.

Mitigation: Restrict PDF fetching to known official domains and review downloaded content before using it in reports.

Risk: The skill references sudo-based system package installation for Pandoc.

Mitigation: Avoid sudo unless the package source and environment are explicitly trusted; prefer controlled base images or managed package installation.

Risk: The security guidance warns against storing real API keys in project .env files.

Mitigation: Use protected secret storage and keep .env files excluded from sharing and release packaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/occupation-analysis)
- [Work process method](references/work_process_method.md)
- [Workflow details](references/workflow_details.md)
- [Report template](references/report_template.md)
- [Precheck guide](references/precheck_guide.md)
- [Troubleshooting](references/troubleshooting.md)
- [MOE teaching standards index](assets/moe_pdfs_final.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report, Word document, JSON intermediate data, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured seven-part occupation analysis report and may use local data assets and validation scripts before final document conversion.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
