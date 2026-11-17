## Description:

Scores leads from 0-100 by analyzing a domain's website, DNS, sitemap, and social presence with customizable JSON scoring profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Sales, partnerships, and growth teams use this skill through an agent to qualify domains, prioritize outreach lists, and evaluate potential partners with configurable signal weights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches websites and DNS records and may make unsafe network requests.

Mitigation: Run it in an isolated environment, use it only for domains you are authorized to assess, and avoid internal or private-network hosts.

Risk: The scanner disables normal HTTPS verification.

Mitigation: Restore normal TLS verification before using the skill at scale.

Risk: The skill can extract public contact details and write results to a user-specified destination.

Mitigation: Review output destinations before execution and keep generated lead data in approved storage locations.

Risk: The skill depends on dnspython.

Mitigation: Pin the dnspython dependency before installation or production-style use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyduckler/skills/lead-scorer-free)
- [Publisher profile](https://clawhub.ai/user/psyduckler)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON lead-scoring results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write JSON results to a specified output file and can process CSV batches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
