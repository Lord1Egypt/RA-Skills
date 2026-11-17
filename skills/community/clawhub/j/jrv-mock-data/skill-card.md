## Description:

Generate realistic fake/mock data for testing and development, including names, emails, addresses, phone numbers, UUIDs, dates, lorem ipsum, companies, and output as JSON, CSV, or SQL INSERT statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and test automation authors use this skill to generate local mock datasets for API testing, UI prototyping, fixture creation, SQL seeding, and load-test preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL uses caller-supplied table names and selected field names.

Mitigation: Use trusted table and field names, inspect generated SQL, and run it only in development or test databases.

Risk: The --output option writes to the path provided by the caller and may overwrite an existing file.

Mitigation: Choose a non-sensitive destination path and check whether the target file already exists before writing.

Risk: The description mentions credit card support, but the provided artifact does not implement a credit card generator.

Mitigation: Verify required data types before relying on the generated fixtures, especially for payment or compliance test cases.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; generated data can be JSON, CSV, SQL INSERT statements, or line-separated text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports count, output format, field selection, SQL table name, random seed, lorem word count, and optional file output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
