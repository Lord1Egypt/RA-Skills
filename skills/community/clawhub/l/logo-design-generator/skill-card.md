## Description:

AI logo generator and logo design maker - create professional brand logos, company emblems, startup icons, app logos, and business identity marks using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and brand teams use this skill to generate logo concepts, app icons, emblems, and business identity marks from text prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logo prompts and reference IDs are sent to the Neta/TalesOfAI API.

Mitigation: Avoid sending confidential brand strategy, unpublished marks, or sensitive reference assets unless that third-party service is approved for the data.

Risk: The skill requires passing a real Neta API token at runtime.

Mitigation: Use a scoped token where available and avoid placing long-lived tokens directly in shared shell history, logs, or scripts.

Risk: The documented npx installation command is unpinned.

Mitigation: Prefer a pinned or ClawHub-managed install path and avoid elevated privileges during installation.

## Reference(s):

- [Logo Design Generator on ClawHub](https://clawhub.ai/blammectrappora/skills/logo-design-generator)
- [Publisher profile](https://clawhub.ai/user/blammectrappora)
- [Neta API token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Plain text URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a direct image URL after submitting a prompt, required token, optional size, and optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
