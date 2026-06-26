## Description: <br>
Complete Kimai time-tracking API integration for managing timesheets, customers, projects, activities, teams, invoices, exports, and system status through the Kimai REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x7466](https://clawhub.ai/user/0x7466) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operations teams, and Kimai administrators use this skill to automate time tracking, reporting, exports, and related account management tasks against a configured Kimai 2.x server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Kimai API token can read or change time-tracking and business records on the configured server. <br>
Mitigation: Use a least-privilege Kimai token and verify KIMAI_BASE_URL points to the intended trusted Kimai instance before running commands. <br>
Risk: Delete and --force operations can remove timesheets or cascade through customers, projects, activities, and teams. <br>
Mitigation: Require explicit confirmation before destructive operations and review affected records before confirming. <br>
Risk: Timesheet exports and API output can contain sensitive personal or business data. <br>
Mitigation: Store exports only in the configured workspace, restrict file permissions, and redact personal data before sharing logs or exported records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x7466/kimai-time-tracking) <br>
- [Kimai REST API Docs](https://www.kimai.org/documentation/rest-api.html) <br>
- [Kimai API Pagination Guide](https://www.kimai.org/documentation/api-pagination.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI output in JSON, table, or CSV formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Kimai API responses, exported time-tracking records, and validation or API error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
