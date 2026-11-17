## Description:

Find alumni connections from LinkedIn data using a school ID and person ID to support alumni network research, talent sourcing, and B2B contact enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sales teams, B2B lead-generation specialists, and agents acting for them use this skill to query alumni ties between a person and an educational institution, then page through returned alumni records for sourcing or relationship research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reads an UpKuaJing API key from a home-directory environment file, and the security evidence warns against exposing that file.

Mitigation: Use a scoped secret mechanism for UPKUAJING_API_KEY, do not print the local environment file, and rotate the key if it is exposed.

Risk: The skill uses paid UpKuaJing API calls and can initiate account top-up flows.

Mitigation: Confirm each paid query or top-up action explicitly before execution, and check current pricing through the documented pricing flow.

Risk: The skill sends LinkedIn-related person and school identifiers, and optional error-report context, to a third-party service.

Mitigation: Share only the identifiers and diagnostic context needed for the request, and confirm error reporting before sending troubleshooting data.

## Reference(s):

- [LinkedIn Person Alumni List API](references/linkedin-person-alumni-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-person-alumni)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing developer platform](https://developer.upkuajing.com/)
- [UpKuaJing API pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an UPKUAJING_API_KEY; alumni queries are paid API calls and may use cursor-based pagination.]

## Skill Version(s):

1.0.5 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
