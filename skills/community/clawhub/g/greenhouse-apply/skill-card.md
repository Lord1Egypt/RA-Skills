## Description:

Submit job applications on Greenhouse (job-boards.greenhouse.io), including text fields, React Select dropdowns, phone country selection, resume upload, email verification code entry, and submit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildingbrien](https://clawhub.ai/user/buildingbrien)

### License/Terms of Use:

MIT-0

## Use Case:

Job applicants use this skill to automate Greenhouse application forms with their resume, contact details, and answers to custom questions. It is intended for agents operating a browser with user-provided application data and narrowly scoped email access for verification codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit job applications containing personal data without an explicit approval checkpoint.

Mitigation: Manually review every completed field and require user confirmation before the final submit action.

Risk: The skill requires access to a resume path, application answers, browser session, and email verification code.

Mitigation: Scope browser and email access to the target Greenhouse application and retrieve only the relevant verification code.

Risk: Repeated Greenhouse submissions or expired verification codes can disrupt the application flow.

Mitigation: Avoid repeated submissions, space retries, and request a fresh verification code when one expires.

## Reference(s):

- [Greenhouse Field Mapping Reference](references/field-mapping.md)
- [ClawHub Skill Page](https://clawhub.ai/buildingbrien/skills/greenhouse-apply)
- [Publisher Profile](https://clawhub.ai/user/buildingbrien)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown instructions with browser automation steps and JavaScript evaluation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser interaction, resume upload, and email verification-code retrieval; no files are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
