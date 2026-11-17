## Description:

Generate random quotes from The Office (US), with offline text output and optional API-backed SVG or image quote cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to fetch Office-themed quotes for chat responses, social posts, icebreakers, or generated quote cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation is unpinned, so future installs may resolve package contents that differ from the reviewed release.

Mitigation: Pin the npm package version before deployment and review the resolved package contents.

Risk: API image mode renders remote SVG content in a local browser context.

Mitigation: Prefer offline text mode, or run API image conversion in an isolated environment with no secrets or sensitive local or network access.

Risk: Documented CLI usage may not match the included script's parsed options.

Mitigation: Confirm the installed CLI options and update the skill documentation before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/office-quotes)
- [Publisher profile](https://clawhub.ai/user/gumadeiras)
- [npm package: @gumadeiras/office-quotes](https://www.npmjs.com/package/@gumadeiras/office-quotes)
- [Office Quotes API](https://officeapi.akashrajpurohit.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Plain text or JSON; API image mode can create SVG, PNG, JPG, or WebP files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline mode avoids network calls; API image mode uses an external quote API and local browser rendering for non-SVG image formats.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
