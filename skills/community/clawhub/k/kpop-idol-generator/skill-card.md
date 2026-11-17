## Description:

Generate k-pop idol style portraits and kpop photocard aesthetic images from text prompts via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate K-pop idol style portrait or photocard images from plain text prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing a real Neta API token literally on the command line may expose it through shell history, logs, or local process inspection.

Mitigation: Prefer safer token handling such as environment variables or a secrets manager when available, and rotate any token that may have been exposed.

Risk: Prompts and reference image UUIDs are sent to the Neta/TalesOfAI service.

Mitigation: Avoid submitting sensitive personal, proprietary, regulated, or confidential content as prompts or reference identifiers.

Risk: The documented unpinned npx install command may fetch changing installer behavior.

Mitigation: Use a pinned and reviewed installer or package version where possible before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/kpop-idol-generator)
- [Neta API token and service page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Direct image URL printed to stdout, with progress messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supported image sizes are portrait, landscape, square, and tall.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
