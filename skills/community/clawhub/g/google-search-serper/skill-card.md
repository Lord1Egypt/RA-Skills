## Description:

Google Search (Serper.dev) lets agents query Serper.dev for Google web, news, image, video, places, shopping, scholar, patent, and autocomplete results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minilozio](https://clawhub.ai/user/minilozio)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to give an OpenClaw-style agent access to current Google search results through Serper.dev, including specialized verticals such as news, images, places, scholar, patents, and shopping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and result requests are sent to Serper.dev.

Mitigation: Avoid submitting confidential, regulated, or user-sensitive queries unless that external disclosure is approved.

Risk: The local skill process requires access to SERPER_API_KEY.

Mitigation: Store the key in the runtime environment only, scope and rotate it where possible, and avoid logging command environments.

Risk: The documented runtime path executes an unpinned third-party package through npx.

Mitigation: Prefer a pinned or vendored tsx dependency, a lockfile, or compiled JavaScript before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minilozio/skills/google-search-serper)
- [Serper.dev](https://serper.dev)
- [Serper.dev API Reference](references/serper-api.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Formatted terminal text or raw JSON, with Markdown usage guidance and bash commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPER_API_KEY; shopping queries use 2 Serper credits while other searches use 1 credit.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
