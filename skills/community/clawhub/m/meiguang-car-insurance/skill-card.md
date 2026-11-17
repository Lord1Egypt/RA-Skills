## Description:

Extracts key data from Meiguang car insurance PDF policies across supported Chinese insurers and outputs the results as an Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cc19960203cc](https://clawhub.ai/user/cc19960203cc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users handling authorized vehicle-insurance policy PDFs use this skill to extract policy, insured-person, vehicle, premium, and coverage-start fields into a spreadsheet for review or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Insurance PDFs can contain sensitive personal, vehicle, and policy data that is exported into an unprotected spreadsheet.

Mitigation: Process only authorized PDFs, write the workbook to a protected location, restrict access to the output, and delete generated files when they are no longer needed.

Risk: Source PDFs are untrusted inputs and may trigger parser or dependency issues during extraction.

Mitigation: Run the extraction in a least-privileged environment with current PDF-processing dependencies and keep source files isolated from unrelated data.

Risk: The optimize_*.py helper scripts rewrite run_extract.py when executed.

Mitigation: Do not run optimization scripts unless code rewriting is intentional; keep a backup or version-controlled copy before using them.

Risk: Known PDF text-extraction limitations may leave some fields empty or inaccurate for specific insurers or document encodings.

Mitigation: Review the generated spreadsheet against source PDFs before relying on extracted values for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cc19960203cc/skills/meiguang-car-insurance)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with Python command examples; the extraction script writes an .xlsx workbook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default input and output paths are configured in scripts/run_extract.py and should be changed before use.]

## Skill Version(s):

5.7.5 (source: server evidence and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
