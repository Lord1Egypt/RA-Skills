## Description:

Look up Placekey identifiers and geocode information for one or multiple locations through the connected Placekey service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using the connected Placekey service can resolve addresses to geocodes or Placekey identifiers, look up a single location, and run bulk lookups for up to 100 locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup executes an unverified remote CLI installer, and the deployed connector implementation was not verified.

Mitigation: Review the CLI dependency before automatic setup and prefer a verified, version-pinned installation.

Risk: Startup skill synchronization can make broader changes to agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 if those additional changes are unwanted.

Risk: Addresses sent through the service are processed by OOMOL and Placekey.

Mitigation: Submit only addresses you intend both services to process.

## Reference(s):

- [Placekey API Documentation](https://docs.placekey.io/)
- [Placekey Homepage](https://www.placekey.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Placekey ClawHub Release](https://clawhub.ai/oomol/skills/oo-placekey)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON service responses with concise guidance and Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bulk lookups support up to 100 locations per request.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
