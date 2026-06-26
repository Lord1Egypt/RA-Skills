## Description: <br>
Gigma Design Canvas lets agents create, edit, preview, and export social media graphics, thumbnails, banners, cards, and batch designs through a hosted editable design canvas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and design teams use this skill to drive Gigma's cloud canvas from an agent, building or editing marketing graphics and exporting PNGs without manual design-tool steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP link contains an embedded authentication token that grants design access to Gigma projects. <br>
Mitigation: Treat the MCP link like a password, keep it out of public logs or repositories, and regenerate it if it may have been exposed. <br>
Risk: Design operations, provided image URLs, and PNG exports are processed by Gigma's hosted service. <br>
Mitigation: Avoid confidential designs or images unless Gigma's cloud processing and 7-day signed export URLs fit the user's requirements. <br>
Risk: The skill can create, edit, delete, and export project content within the connected Gigma account. <br>
Mitigation: Preview with screenshots before export, confirm element IDs before destructive edits, and clone template projects for batch work when preserving originals matters. <br>


## Reference(s): <br>
- [Gigma Documentation](https://gigma-doc.10xboost.org) <br>
- [Gigma Service](https://gigma.10xboost.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/gigma-design-canvas) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, text] <br>
**Output Format:** [Markdown guidance, MCP tool call arguments, and exported PNG links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated designs are managed in Gigma, and PNG export links are signed URLs valid for 7 days.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
