## Description: <br>
Generates realistic fake data for testing and development, including users, names, emails, addresses, phone numbers, UUIDs, dates, lorem ipsum, companies, URLs, IPs, and custom records in JSON, CSV, SQL, or line-delimited formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and agent operators use this skill to generate local mock records for tests, UI prototypes, fixtures, SQL seed data, and load-test inputs without calling an external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script can overwrite a user-specified output file path. <br>
Mitigation: Run without elevated privileges and choose the --output path deliberately, preferably in a test workspace. <br>
Risk: Generated records are realistic-looking mock data and may be mistaken for real personal or business data. <br>
Mitigation: Label generated datasets as synthetic and avoid using them where real customer records are required. <br>


## Reference(s): <br>
- [Jrv Mock Data on ClawHub](https://clawhub.ai/Johnnywang2001/jrv-mock-data) <br>
- [Johnnywang2001 publisher profile](https://clawhub.ai/user/Johnnywang2001) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated data may be JSON, CSV, SQL INSERT statements, line-delimited text, or files written by the script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports count, data type, output format, SQL table name, custom fields, random seed, lorem word count, and output file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
