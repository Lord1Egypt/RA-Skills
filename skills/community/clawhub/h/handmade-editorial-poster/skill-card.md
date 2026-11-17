## Description:

Create one high-end handmade editorial poster per supplied photo using a paper-textured, minimal illustrated-cover aesthetic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative agents use this skill to turn each supplied photo into a separate handmade editorial poster while preserving the source subject, pose, and relationship. When image generation is unavailable, the skill produces mapped prompts instead of claiming to create images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos may be sent to the configured image-generation provider.

Mitigation: Use only providers whose privacy and retention settings are acceptable for the photos being processed, and avoid sensitive photos unless those settings are appropriate.

Risk: A text-only host may be unable to create poster images directly.

Mitigation: Return one ready-to-paste prompt per source photo and clearly identify the missing image-generation capability.

Risk: Generated output may drift from the one-photo-to-one-poster contract or include unwanted text.

Mitigation: Apply the skill's quality gate before returning results, retry with named corrections when practical, and report any remaining deviation.

## Reference(s):

- [Prompt library](references/prompt-library.md)
- [Platform adapters](references/platform-adapters.md)
- [ClawHub skill page](https://clawhub.ai/0xcjl/skills/handmade-editorial-poster)
- [Publisher profile](https://clawhub.ai/user/0xcjl)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance or ready-to-paste image-generation prompts; image-capable hosts may return generated poster files separately.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One independent output is produced per source photo; portrait sources use 9:16, landscape sources use 16:9, and collages are excluded.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
