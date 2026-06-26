## Description: <br>
Repair the OpenClaw Control UI Skills modal when clicking a skill row does nothing and DevTools shows a showModal InvalidStateError because the dialog is not yet in the document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danrudy33](https://clawhub.ai/user/danrudy33) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to repair an OpenClaw dashboard UI timing issue that prevents skill detail modals from opening. It guides a manual patch to the active OpenClaw Control UI bundle and confirms the modal behavior after reload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch targets a built OpenClaw dashboard asset whose filename may differ between installations or releases. <br>
Mitigation: Confirm the active skills bundle filename in the installed OpenClaw Control UI before editing. <br>
Risk: Manual edits to the installed bundle can be overwritten or superseded by future OpenClaw updates. <br>
Mitigation: Back up the bundle before editing and re-check whether the issue remains after each OpenClaw update. <br>
Risk: Editing the wrong JavaScript bundle could fail to fix the modal or alter unrelated dashboard behavior. <br>
Mitigation: Search for the exact showModal call pattern and verify the skill detail modal opens after a hard reload. <br>


## Reference(s): <br>
- [OpenClaw Dashboard Skill Modal Patch on ClawHub](https://clawhub.ai/danrudy33/openclaw-dashboard-skill-modal-patch) <br>
- [danrudy33 publisher profile](https://clawhub.ai/user/danrudy33) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell, text, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual repair guidance for a local OpenClaw dashboard bundle; no generated files or automated scripts are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
