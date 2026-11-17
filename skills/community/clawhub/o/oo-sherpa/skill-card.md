## Description:

Search and read personalized Sherpa travel requirements for an itinerary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to retrieve personalized entry restrictions, visa requirements, and document guidance for an itinerary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute downloaded installer code whose behavior is unverified.

Mitigation: Prefer an already reviewed CLI installation and require approval before running downloaded installers.

Risk: Automatic bundled-skill synchronization may introduce broader agent changes than Sherpa access requires.

Mitigation: Disable automatic bundled-skill synchronization when only Sherpa access is needed.

Risk: Trip lookups may involve personal travel details.

Mitigation: Share only the travel details necessary for the itinerary lookup.

## Reference(s):

- [Sherpa requirements API documentation](https://docs.joinsherpa.io/requirements-api/quickstart.html)
- [Sherpa](https://www.joinsherpa.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Sherpa on ClawHub](https://clawhub.ai/oomol/skills/oo-sherpa)

## Skill Output:

**Output Type(s):** [Text, Markdown, Travel guidance]

**Output Format:** [Concise Markdown summaries or detailed travel requirement information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized to the itinerary provided]

## Skill Version(s):

1.0.5 (source: evidence.json release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
