## Description: <br>
Create, manage, and validate SOUL.md personality files for multi-agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuderu-hub](https://clawhub.ai/user/xuderu-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and multi-agent operators use this skill to create, audit, and maintain SOUL.md personality files, reusable persona templates, and collaboration protocols for OpenClaw-style agent teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional web editor can expose and overwrite local agent personality files through an unauthenticated local server. <br>
Mitigation: Prefer the Python CLI scripts for routine work; if the server is used, run it only when needed, bind it to localhost, restrict CORS, and add authentication before broader use. <br>
Risk: The web editor documentation describes persistent Windows auto-start behavior for the local server. <br>
Mitigation: Remove the SOULServer Windows Run entry when the editor is not needed and verify that no hidden launcher remains enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/xuderu-hub/jarvis-soul-system) <br>
- [SOUL.md Template](references/soul-template.md) <br>
- [Personality Library](references/personality-library.md) <br>
- [Multi-Agent Collaboration Protocol](references/collaboration-protocol.md) <br>
- [SOUL Editor README](scripts/SOUL-EDITOR-README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated SOUL.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, list, validate, or edit persistent SOUL.md files in local agent directories.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
