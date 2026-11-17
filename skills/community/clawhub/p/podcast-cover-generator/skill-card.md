## Description:

Generate professional podcast cover art and show artwork from plain text prompts for major podcast platforms using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, podcast teams, and agents use this skill to turn podcast artwork prompts into generated cover-image URLs. It supports optional size presets and style inheritance from a reference image UUID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, optional reference image IDs, and the image-service token to api.talesofai.com.

Mitigation: Use only prompts and references appropriate for that third-party service, and install only if this data sharing is acceptable.

Risk: The token is supplied on the command line, where it may appear in shell history, logs, or process telemetry.

Mitigation: Prefer expanding a shell variable, avoid placing real tokens in CI logs or shared shell commands, and rotate any token that may have been exposed.

Risk: Evidence.security marks the release suspicious because of token exposure and disclosure or supply-chain weaknesses.

Mitigation: Prefer a pinned release or ClawHub-managed install, review the source before execution, and follow the security guidance from the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/podcast-cover-generator)
- [Neta access page](https://www.neta.art/open/)
- [Neta image API host](https://api.talesofai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text URL printed to stdout, with progress and errors printed to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one image URL per successful run; requires a Neta API token and a text prompt.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
