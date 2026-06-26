## Description: <br>
Use when organizing Microsoft Edge bookmarks or favorites when persistence matters, when folder priorities like AI/investing/social are important, or when previous bookmark edits were reverted after restart or sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenoexia](https://clawhub.ai/user/xenoexia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to organize a local Microsoft Edge profile's bookmarks into explicit folders while preserving persistence across browser reloads, restarts, and sync reconciliation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bookmark reorganization changes may persist locally or sync to other Edge devices. <br>
Mitigation: Confirm the exact Edge profile and scope, capture a backup or export, record a dry-run move plan, and verify results after reload, restart, and sync reconciliation. <br>
Risk: Unapproved browser restart, profile takeover, or live bookmark mutation could disrupt the user's current session. <br>
Mitigation: Require explicit user consent before intrusive browser actions and downgrade to manual instructions if a local, authorized control path has not been proven. <br>
Risk: Raw bookmark-file edits can be reverted or produce a structure that does not match the visible Edge bookmark tree. <br>
Mitigation: Prefer the live browser bookmark model and stop if the live tree, counts, or structural diff do not match the intended plan. <br>


## Reference(s): <br>
- [Edge Bookmarks Organization Workflow](references/edge-bookmarks-workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/xenoexia/organizing-edge-bookmarks) <br>
- [Publisher profile](https://clawhub.ai/user/xenoexia) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists and command suggestions when a local control path is proven.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans, safeguards, rollback steps, and verification instructions; it does not require external API tokens or cloud credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
