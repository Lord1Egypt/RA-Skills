## Description: <br>
Track lease expirations and manage the 90-day renewal process. Use when checking upcoming lease expirations, planning rent increases, drafting renewal offers, or managing the renewal negotiation timeline. Reads property and tenant data to proactively flag leases expiring within 90 days and guides through the Homestruk renewal SOP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdamsJB](https://clawhub.ai/user/AdamsJB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External self-managing landlords and property managers use this skill to find leases expiring within 90 days, plan renewal decisions, draft tenant renewal offers, and manage follow-up through the renewal timeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create renewal drafts or propose updates to rent-roll and property records. <br>
Mitigation: Keep routine expiration checks read-only and require explicit approval before saving drafts, updating rent-roll.json or properties.json, sending notices, changing rent, or scheduling recurring runs. <br>
Risk: The skill depends on local tenant, property, and rent-roll files that may contain sensitive property-management data. <br>
Mitigation: Install and run it only when the agent is expected to access those local files, and review generated renewal decisions or notices before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdamsJB/homestruk-lease-renewal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with renewal dashboards, renewal offer drafts, timeline guidance, and file update recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local property, tenant, and rent-roll records and may propose draft files or updates for explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
