## Description:

Find museums, art galleries, and exhibitions in any city, with ticket links and visiting tips, and support related travel booking tasks through Fliggy-powered flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and planning agents use this skill to find museums, galleries, exhibitions, and related travel options for a city using live flyai CLI results. It formats recommendations as user-facing Markdown with booking links and visiting tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global third-party npm CLI and run shell commands for travel searches.

Mitigation: Install and run it only in an isolated workspace or container, and manually approve any package installation.

Risk: The skill can show third-party booking links and requires travel results to include booking URLs.

Mitigation: Review booking links before use and avoid treating prices, availability, or terms as final until confirmed on the provider site.

Risk: The skill may keep local plaintext execution logs that include raw user requests.

Mitigation: Avoid entering sensitive travel, identity, payment, or itinerary details unless logging is removed or disabled.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, tips, and inline shell commands when setup or recovery is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data and may keep local plaintext execution logs when filesystem writes are available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
