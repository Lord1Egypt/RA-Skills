## Description:

Discover and classify a live website's legal/compliance pages, including privacy policies, HIPAA/Part 2 notices, terms of use, informed consents, and similar documents, by triangulating sitemap.xml, robots.txt, footer and navigation links, and common compliance path guesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance operators, and legal operations teams use this skill to inventory a live website's legal and compliance pages before routing them for separate review. It records page classification, controlling entity, discoverability, and mismatch observations without assessing compliance sufficiency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live URL discovery can be influenced by the target website and may lead the agent to fetch unintended internal or third-party locations.

Mitigation: Run the skill in a network-restricted environment, keep discovered URLs and redirects on the approved domain, block private and loopback addresses, and ask before contacting any other origin.

Risk: Default manifest filenames may overwrite existing files in the working directory.

Mitigation: Choose an explicit output directory or filename before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dangsllc/skills/legal-page-discovery)
- [Rote Compliance Skills](https://github.com/Rote-Compliance/rote-compliance-skills)
- [Dang's Solutions](https://dangssolutions.com)
- [Rote Compliance](https://rotecompliance.com)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text, Shell commands, Guidance]

**Output Format:** [Markdown manifest and JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes legal-page-manifest.md and legal-page-manifest.json to the current working directory or an operator-specified output path.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
