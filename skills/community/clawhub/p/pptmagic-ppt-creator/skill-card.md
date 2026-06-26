## Description: <br>
Use Banana Slides / pptmagic-compatible project APIs to create, continue, and export presentation decks from an idea, outline, or page-by-page description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin808](https://clawhub.ai/user/kevin808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, continue, regenerate, and export presentation decks through a Banana Slides / PPTMagic-compatible service from a topic, outline, or page-by-page description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation prompts, outlines, slide descriptions, and uploaded template images are sent to the fixed external PPTMagic endpoint. <br>
Mitigation: Avoid confidential, regulated, or sensitive material unless the user trusts the service operator and its data handling; redact, summarize, or generalize sensitive source material before sending it. <br>
Risk: An optional PPTMAGIC_ACCESS_CODE may be used for controlled access. <br>
Mitigation: Treat the access code as a credential and send it only through the documented X-Access-Code header when the operator explicitly provides it. <br>
Risk: Partial generation or export failures can leave a project incomplete. <br>
Mitigation: Inspect the current project state before retrying, retry only failed image pages where possible, and confirm expected pages and generated assets before export. <br>


## Reference(s): <br>
- [API Workflow](references/api-workflow.md) <br>
- [Curl Examples](references/curl-examples.md) <br>
- [PPTMagic Public Endpoint](https://openclaw-nopass.pptmagic.tech/) <br>
- [ClawHub Skill Page](https://clawhub.ai/kevin808/pptmagic-ppt-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown status updates with project IDs, completion state, page counts, and export or download URLs; curl examples when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include failure stage and next-step guidance when a generation, polling, or export step fails.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
