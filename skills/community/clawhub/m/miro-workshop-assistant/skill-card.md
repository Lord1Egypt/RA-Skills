## Description: <br>
Turns workshop whiteboard photos or raw notes into an editable Miro diagram with frames, stickies, connectors, idempotent updates, rollback, undo, and local Miro API push commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SimoneFerrario](https://clawhub.ai/user/SimoneFerrario) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Workshop facilitators, product teams, architects, and developers use this skill to convert workshop photos or notes into structured Miro boards with real frames, grouped sticky notes, and connectors. It can push the generated board content through the Miro API and undo or replace a prior run using the same session key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete live Miro board content when apply or undo commands are run. <br>
Mitigation: Require explicit confirmation before apply or undo and test on a non-critical board before using it with production workshop content. <br>
Risk: A reused sessionKey can replace or delete items from a previous run. <br>
Mitigation: Use clear, unique session keys per workshop and review _out/.state.json before first use or before reusing a workspace. <br>
Risk: The Miro access token can grant board write access. <br>
Mitigation: Use a least-privileged Miro token limited to the intended board and keep MIRO_ACCESS_TOKEN in environment variables only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SimoneFerrario/miro-workshop-assistant) <br>
- [README.txt](artifact/README.txt) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [miro-push.mjs](artifact/miro-push.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Miro-ready JSON files and local Node.js commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates frame, sticky, connector, sessionKey, runId, and warning data; apply and undo commands can modify live Miro board content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
