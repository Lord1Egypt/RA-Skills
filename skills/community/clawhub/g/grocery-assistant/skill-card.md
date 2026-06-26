## Description: <br>
Persistent pantry-backed grocery checklist for OpenClaw, intended for normal conversational use with Telegram shopping-list UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serdarsalim](https://clawhub.ai/user/serdarsalim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to maintain a pantry-backed grocery list, update needed and have states from conversational requests, and optionally render a Telegram shopping checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send stored grocery-list contents through a configured Telegram bot. <br>
Mitigation: Use a dedicated grocery-only Telegram bot and restrict allowed senders before enabling Telegram integration. <br>
Risk: Broad script allowlisting may grant more execution access than the skill needs. <br>
Mitigation: Allowlist only the specific grocery wrapper and reviewed scripts needed for the deployment. <br>
Risk: The bundled session-pruning script can alter grocery agent session files. <br>
Mitigation: Review or remove the session-pruning script if session archival and reset behavior is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/serdarsalim/grocery-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/serdarsalim) <br>
- [README](artifact/README.md) <br>
- [Setup Guide](artifact/SETUP.md) <br>
- [Agent Notes](artifact/AGENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and conversational text with inline shell commands and local configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update local JSON grocery state and render Telegram checklist interactions when configured.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
