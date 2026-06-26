## Description: <br>
Generates professional PPT presentations with 课件帮 (Kejian365), including outline confirmation, theme selection, AI content creation, layout generation, and delivery of a preview link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[good0007](https://clawhub.ai/user/good0007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to turn a topic and presentation requirements into a slide deck for business reports, product pitches, academic presentations, or training materials through Kejian365. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kejian365 authentication tokens may be exposed through chat, parameter files, or persisted task state. <br>
Mitigation: Use a dedicated revocable token, prefer environment-variable injection, avoid pasting secrets into chat, and remove token persistence from task state before installation. <br>
Risk: Presentation topics, outlines, requirements, and supporting material are sent to the external Kejian365 service. <br>
Mitigation: Confirm the content is appropriate to share with Kejian365 before running the skill, especially for confidential business, academic, or training material. <br>
Risk: Task creation can trigger billing on the external service. <br>
Mitigation: Review the generated outline and selected template before creating the task, and use a stable work directory to prevent duplicate submissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/good0007/kejian365-aippt) <br>
- [Kejian365 platform](https://kejian365.com) <br>
- [Kejian365 Open API portal](https://kejian365.com/oapi-portal) <br>
- [AIPPT Skill API Reference](api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with generated outline text, progress updates, shell command guidance, and a final preview link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and polls a remote PPT-generation task; final output is an online preview link rather than a local presentation file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
