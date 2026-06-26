## Description: <br>
Gigma AI Design Canvas lets agents create, edit, preview, and export cloud canvas designs such as social graphics, thumbnails, banners, cards, and batch variations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to direct an agent to build editable Gigma canvas designs, manage project variations, preview results, and export PNG assets. It is suited for social graphics, thumbnails, banners, cards, and batch design workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation can allow an agent to create, modify, or delete cloud canvas content without enough user confirmation. <br>
Mitigation: Confirm the active project before edits, duplicate or back up important designs before destructive actions, and preview with screenshots before export. <br>
Risk: Exported assets are shared through signed URLs, which may expose confidential branding, unreleased assets, or sensitive text if used carelessly. <br>
Mitigation: Avoid exporting confidential material unless signed URL sharing is acceptable, and review each export request before producing a link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/gigma-design) <br>
- [Gigma documentation](https://gigma-doc.10xboost.org) <br>
- [Gigma service](https://gigma.10xboost.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance with MCP configuration examples, tool call examples, previews, and exported PNG URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, modify, delete, preview, and export canvas projects in the Gigma cloud service; exported PNG links are signed URLs valid for 7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
