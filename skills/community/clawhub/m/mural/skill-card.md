## Description: <br>
Mural API integration with managed OAuth for collaborative whiteboard automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to browse Mural workspaces, rooms, murals, widgets, templates, and tags through ClawLink-managed OAuth. It can also create sticky notes on selected murals after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ClawLink OAuth access to a user's Mural account. <br>
Mitigation: Install only if ClawLink is trusted to broker Mural access, and review the requested Mural permissions during OAuth connection. <br>
Risk: Sticky-note creation modifies mural content. <br>
Mitigation: Confirm the target mural and sticky-note content carefully before approving write operations. <br>
Risk: Tool calls operate within the authenticated user's Mural permissions. <br>
Mitigation: Use a Mural account with appropriate access for the intended workspace, room, or mural. <br>


## Reference(s): <br>
- [Mural API Docs](https://developers.mural.co/public/docs) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Dashboard](https://claw-link.dev/dashboard?add=mural) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/mural) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke ClawLink tools that read Mural account content or create sticky notes according to the authenticated user's permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
