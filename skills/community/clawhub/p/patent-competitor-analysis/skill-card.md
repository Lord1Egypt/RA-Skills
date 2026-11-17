## Description:

Analyzes a company's patent landscape and competitors in a specified technology area, producing a traceable report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External business and IP teams use this skill to compare a named company's patent activity with competitors in a defined technology area and prepare a report for review. The report supports research and planning, not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional background materials may contain sensitive information and be submitted to PatentMax.

Mitigation: Use public or redacted materials unless you explicitly approve sending them to PatentMax.

Risk: API keys could be exposed through insecure redirects or insufficiently protected persistent storage.

Mitigation: Keep keys out of chat, use a restricted key, and require secure persistent storage and protection against authenticated cross-origin or insecure redirects.

Risk: Report generation can incur charges and take a long time.

Mitigation: Confirm charges before submission and set an overall waiting limit.

## Reference(s):

- [Patent Competitor Analysis skill release](https://clawhub.ai/ip930/skills/patent-competitor-analysis)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [PatentMax API service](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Analysis, Files, Text]

**Output Format:** [Patent competitor analysis report in Word (.docx), with textual progress and status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous report generation; results cite patent publication numbers, and coverage and quality may vary.]

## Skill Version(s):

1.1.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
