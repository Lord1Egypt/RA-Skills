## Description:

酷家乐AI室内设计 guides an agent through Chinese-language interior design workflows for floorplan confirmation, style selection, automated layout, and rendering output using Kujiale capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, and real-estate teams use this skill to turn a known community floorplan or uploaded floorplan image into Kujiale layout previews, rendered room images, panorama links, and design highlights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded floorplan images and derived design data may be sent to Kujiale.

Mitigation: Use the skill only when the user is comfortable sharing those images and design data with Kujiale.

Risk: The skill requires an account token for Kujiale operations.

Mitigation: Keep the token in a dedicated project folder, remove it after use, and avoid committing token files.

Risk: Layout or rendering steps may consume account quota or credits.

Mitigation: Confirm quota-consuming layout and rendering actions with the user before execution.

Risk: The security evidence flags the invocation scope as overbroad.

Mitigation: Use the skill only for Kujiale interior-design tasks and review requested commands before allowing execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/kujiale-design-free)
- [Kujiale skills token page](https://www.kujiale.com/skills)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with rendered image links, panorama links, progress messages, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final output is expected in ./outputs/result.md with design highlights, rendered images ordered by room priority, panorama links, and a Kujiale design detail link.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
