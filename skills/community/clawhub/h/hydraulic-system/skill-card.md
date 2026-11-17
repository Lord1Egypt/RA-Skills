## Description:

Generates CAD drawings for hydraulic and pneumatic systems through a guided Chinese workflow that collects parameters, calls the JixieTools API, and tracks production-sheet status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide creation of hydraulic and pneumatic CAD drawing production sheets on JixieTools, including product selection, parameter collection, calculation review, incremental edits, and status polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell commands may be assembled from user-entered or API-provided values, creating command-injection exposure.

Mitigation: Use a structured HTTP client or safely serialized request payloads instead of shell templates, and review generated commands before execution.

Risk: Engineering inputs and production-sheet identifiers are sent to jixietools.com.

Mitigation: Avoid entering confidential engineering data unless the user accepts sending that data to the external service.

Risk: Polling the production-sheet status too frequently can create unnecessary service load.

Mitigation: Keep the documented 5-second polling interval and stop polling once the production sheet reaches a final status.

## Reference(s):

- [Hydraulic System ClawHub Skill Page](https://clawhub.ai/liv09370/skills/hydraulic-system)
- [JixieTools API Base URL](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls]

**Output Format:** [Chinese Markdown with tables, inline shell commands, JSON examples, and status links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains filename and guest_code state across calculation, production-sheet creation, and polling steps.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
